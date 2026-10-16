"""Coat Dance VACE adapter run *inside* the existing KR Relay process.

One poll loop, one KR_RELAY_TOKEN, one ComfyUI, one ArtJob claim slot.
The relay only advertises VACE capability after checking the real model,
nodes, FFmpeg, and ComfyUI input path. No second daemon to activate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

import coat_dance_vace_worker as vace
import relay_agent as relay

CAPABILITY_TTL = 180.0
WORK_ROOT = Path(os.environ.get("KR_VACE_WORK_ROOT") or Path(tempfile.gettempdir()) / "kindrobots-vace")
INPUT_ROOT = Path(os.environ.get("KR_VACE_INPUT_DIR") or "D:/comfy/comfy-fast/input")
_UUID = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$", re.I)
_last_check = 0.0
_last_ok = False
_last_reason = ""


def capable():
    """Safe claim gate. An unprepared Comfy host never burns the pilot attempt."""
    global _last_check, _last_ok, _last_reason
    now = time.monotonic()
    if _last_check > 0 and now - _last_check < CAPABILITY_TTL:
        return _last_ok
    _last_check = now
    try:
        for command in ("ffmpeg", "ffprobe"):
            if not shutil.which(command):
                raise RuntimeError(f"{command} not available on KR Relay PATH")
        if not INPUT_ROOT.is_dir():
            raise RuntimeError(f"ComfyUI input folder missing: {INPUT_ROOT}")
        vace.check_comfy(relay.COMFY_URL)
        _last_ok = True
        _last_reason = ""
    except (RuntimeError, OSError, ValueError, urllib.error.URLError, TimeoutError) as error:
        _last_ok = False
        _last_reason = str(error)[:400]
        relay.log(f"VACE capability pending: {_last_reason}")
    return _last_ok


def _path(restyle_id, endpoint):
    return f"{relay.KR_BASE_URL}/api/video-restyle/{restyle_id}/pilot/{endpoint}"


def _report(restyle_id, art_id, kind, completed, **additional):
    body = {
        "artJobId": art_id,
        "agentId": relay.AGENT_ID,
        "kind": kind,
        "completedSegments": completed,
        **additional,
    }
    status, reply = relay.http_json(
        "POST", _path(restyle_id, "report"), body,
        bearer=relay.KR_RELAY_TOKEN, timeout=120,
    )
    if status != 200 or not reply or not reply.get("success"):
        raise RuntimeError(f"VACE report rejected HTTP {status}: {reply and reply.get('message')}")
    return reply


def _source(restyle_id, art_id, destination):
    params = urllib.parse.urlencode({"artJobId": art_id})
    request = urllib.request.Request(
        _path(restyle_id, "source") + "?" + params,
        headers={
            "Authorization": f"Bearer {relay.KR_RELAY_TOKEN}",
            "X-Relay-Agent": relay.AGENT_ID,
        },
    )
    scratch = destination.with_name(destination.name + ".download")
    length = 0
    try:
        with urllib.request.urlopen(request, timeout=180) as response, scratch.open("wb") as out:
            while True:
                packet = response.read(1024 * 1024)
                if not packet:
                    break
                length += len(packet)
                if length > 128 * 1024 * 1024:
                    raise RuntimeError("Source exceeds the video-restyle 128 MiB limit")
                out.write(packet)
        if not length:
            raise RuntimeError("KR returned empty motion source")
        os.replace(scratch, destination)
    finally:
        scratch.unlink(missing_ok=True)


def _submit_video(restyle_id, art_id, completed, file_path):
    raw = file_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    boundary = "krvace" + uuid.uuid4().hex
    fields = {
        "artJobId": str(art_id), "agentId": relay.AGENT_ID,
        "kind": "complete", "completedSegments": str(completed),
        "sha256": digest,
    }
    parts = []
    for key, value in fields.items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode("utf-8")
        )
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"pilot.mp4\"\r\nContent-Type: video/mp4\r\n\r\n".encode("utf-8")
    )
    parts.extend([raw, f"\r\n--{boundary}--\r\n".encode()])
    data = b"".join(parts)
    request = urllib.request.Request(
        _path(restyle_id, "report"),
        data=data,
        headers={
            "Authorization": f"Bearer {relay.KR_RELAY_TOKEN}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=240) as response:
        result = json.loads(response.read().decode("utf-8"))
    if not result.get("success") or result.get("data", {}).get("status") != "REVIEW":
        raise RuntimeError("KR did not confirm private pilot upload")


def process(job):
    """Called by relay_media_agent.process_with_media after the normal ArtJob claim."""
    payload = job.get("payload") or {}
    if isinstance(payload, str):
        payload = json.loads(payload)
    video = payload.get("videoRestyle") or {}
    restyle_id = str(video.get("id") or "")
    if not _UUID.fullmatch(restyle_id) or video.get("phase") != "pilot":
        raise ValueError("Malformed Coat Dance pilot payload")
    art_id = int(job["id"])
    user_id = int(job["userId"])
    if not capable():
        raise RuntimeError(f"VACE capability became unavailable: {_last_reason}")
    job_dir = WORK_ROOT / str(user_id) / restyle_id
    job_dir.mkdir(parents=True, exist_ok=True)
    source = job_dir / "source.mp4"
    _source(restyle_id, art_id, source)
    prior = job_dir / "job.json"
    metadata = {
        "id": restyle_id, "userId": user_id, "sourceFile": "source.mp4",
        "status": "PILOT_QUEUED", "sourceBytes": source.stat().st_size,
        "quality": video.get("quality") if video.get("quality") in ("720p", "1080p") else "1080p",
        "renderRecipe": {"stylePrompt": payload.get("promptString") or "Hand-painted Japanese cel animation"},
        "pilot": {
            "startSec": float(video.get("startSec")),
            "durationSec": float(video.get("durationSec")),
            "completedSegments": 0,
            "totalSegments": int(video.get("totalSegments") or 0),
        },
    }
    prior.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    complete_count = 0
    _report(restyle_id, art_id, "progress", 0)
    original_update = vace.update
    args = argparse.Namespace(
        private_root=WORK_ROOT, comfy_input=INPUT_ROOT,
        comfy_url=relay.COMFY_URL, timeout_seconds=10800, dry_run=False,
    )

    def traced_update(job_path, local_job, **fields):
        nonlocal complete_count
        original_update(job_path, local_job, **fields)
        info = fields.get("pilot") or local_job.get("pilot") or {}
        new_count = int(info.get("completedSegments") or 0)
        if new_count > complete_count and new_count <= metadata["pilot"]["totalSegments"]:
            _report(restyle_id, art_id, "progress", new_count)
            complete_count = new_count

    vace.update = traced_update
    try:
        vace.render(prior, args)
        final = json.loads(prior.read_text(encoding="utf-8"))
        if final.get("status") != "REVIEW":
            raise RuntimeError(f"VACE did not render a pilot: {final.get('stage')}")
        result = job_dir / "pilot.mp4"
        if not result.is_file():
            raise RuntimeError("VACE result MP4 not found")
        _submit_video(restyle_id, art_id, metadata["pilot"]["totalSegments"], result)
        relay.log(f"job {art_id}: VACE pilot finished and registered for private review")
    except Exception as error:
        try:
            _report(restyle_id, art_id, "failed", complete_count, error=str(error)[:1800])
            relay.log(f"job {art_id}: VACE failed; reported to ArtJob: {error}")
        except Exception as report_error:
            # Fall through to the parent relay's existing normal failed-job handling.
            raise RuntimeError(f"VACE error {error}; server error report also failed: {report_error}") from error
    finally:
        vace.update = original_update
