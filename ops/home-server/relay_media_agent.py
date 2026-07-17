#!/usr/bin/env python3
"""Media-aware wrapper for the proven Kind Robots ArtJob relay.

Kind Robots-targeted jobs that carry both:

- targetRepo: silasfelinus/kind_robots
- imagePath: public/images/<path>

are written to the exact equivalent path under KR_MEDIA_IMAGES_DIR before the
ArtJob is marked successful. If the filesystem write or manifest update fails,
the job is reported FAILED and remains retryable instead of silently completing
with a missing public file.

All other jobs use relay_agent.py unchanged, except that Comfy prompt submission
uses a longer timeout and can recover a prompt id from /queue when Comfy accepted
the prompt but its HTTP response arrived too late.
"""

import base64
import io
import json
import os
import time
from pathlib import Path, PurePosixPath

import relay_agent as relay

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
MEDIA_ROOT_VALUE = (
    os.environ.get("KR_MEDIA_IMAGES_DIR", "").strip()
    or os.environ.get("KR_LOCAL_IMAGES_DIR", "").strip()
)
IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg"}
GENERATED_IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv"}
COMFY_PROMPT_TIMEOUT = float(os.environ.get("COMFY_PROMPT_TIMEOUT", "180"))
COMFY_RECOVERY_SECONDS = float(os.environ.get("COMFY_RECOVERY_SECONDS", "45"))
ORIGINAL_PROCESS = relay.process


def job_payload(job):
    payload = job.get("payload") or {}
    if isinstance(payload, str):
        payload = json.loads(payload)
    if not isinstance(payload, dict):
        raise ValueError("ArtJob payload must be an object")
    return payload


def direct_media_relative(job):
    payload = job_payload(job)
    target_repo = str(payload.get("targetRepo") or "").strip()
    image_path = str(payload.get("imagePath") or "").strip().replace("\\", "/")

    if target_repo != KIND_ROBOTS_REPO or not image_path:
        return None

    logical = PurePosixPath(image_path)
    parts = logical.parts
    if len(parts) < 3 or parts[:2] != ("public", "images"):
        raise ValueError(
            "Kind Robots media job imagePath must begin with public/images/"
        )

    relative_parts = parts[2:]
    if any(part in ("", ".", "..") for part in relative_parts):
        raise ValueError(f"Unsafe media imagePath: {image_path}")

    return Path(*relative_parts)


def media_root():
    if not MEDIA_ROOT_VALUE:
        raise RuntimeError(
            "KR_MEDIA_IMAGES_DIR is required for direct Kind Robots media jobs"
        )
    root = Path(MEDIA_ROOT_VALUE).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def encode_image_for_suffix(raw, suffix):
    suffix = suffix.lower()
    if suffix not in GENERATED_IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported generated image target extension: {suffix}")

    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError(
            "Pillow is required for exact-path image conversion; "
            "install it with: py -3.12 -m pip install Pillow"
        ) from error

    with Image.open(io.BytesIO(raw)) as image:
        output = io.BytesIO()
        if suffix == ".webp":
            image.save(output, format="WEBP", quality=90, method=6)
        elif suffix == ".png":
            image.save(output, format="PNG")
        elif suffix in (".jpg", ".jpeg"):
            image.convert("RGB").save(output, format="JPEG", quality=92)
        elif suffix == ".gif":
            image.save(output, format="GIF")
        return output.getvalue()


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(
        f".{path.name}.tmp-{os.getpid()}-{time.time_ns()}"
    )
    temporary.write_bytes(data)
    os.replace(temporary, path)


def atomic_write_json(path, value):
    encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    atomic_write(path, encoded)


def refresh_manifests(root, destination):
    folder = destination.parent
    if folder == root:
        return

    folder_relative = folder.relative_to(root).as_posix()
    filenames = sorted(
        item.name
        for item in folder.iterdir()
        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS
    )
    atomic_write_json(folder / "gallery.json", filenames)

    index_path = root / "collections.json"
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise RuntimeError(f"Cannot safely read {index_path}: {error}") from error
        if not isinstance(index, dict):
            raise RuntimeError(f"Cannot safely update non-object {index_path}")
    else:
        index = {}

    # Folder collections use the leaf directory name as their slug. The exact
    # folder path is retained as the value, matching collections.json today.
    index[folder.name] = folder_relative
    atomic_write_json(index_path, index)


def write_direct_media(job, media):
    relative = direct_media_relative(job)
    if relative is None:
        return None

    root = media_root()
    destination = (root / relative).resolve()
    if destination != root and root not in destination.parents:
        raise ValueError(f"Media destination escaped root: {destination}")

    suffix = destination.suffix.lower()
    raw = base64.b64decode(media["data_b64"])
    if media.get("is_video"):
        if suffix not in VIDEO_EXTENSIONS:
            raise ValueError(
                f"Video result cannot be written to target extension {suffix or '(none)'}"
            )
        encoded = raw
    else:
        if not suffix:
            raise ValueError("Generated image target must include a file extension")
        encoded = encode_image_for_suffix(raw, suffix)

    atomic_write(destination, encoded)
    refresh_manifests(root, destination)
    relay.log(f"direct media: {destination}")
    return destination


def queued_prompt_id_for_client(client_id):
    """Find a prompt accepted by Comfy when POST /prompt timed out client-side."""
    try:
        status, queue = relay.http_json(
            "GET", f"{relay.COMFY_URL}/queue", timeout=15
        )
    except Exception:  # noqa: BLE001 - recovery probes are best-effort
        return None
    if status != 200 or not isinstance(queue, dict):
        return None

    for key in ("queue_running", "queue_pending"):
        entries = queue.get(key) or []
        for entry in entries:
            if not isinstance(entry, (list, tuple)) or len(entry) < 4:
                continue
            prompt_id = entry[1]
            extra_data = entry[3]
            if (
                isinstance(prompt_id, str)
                and isinstance(extra_data, dict)
                and extra_data.get("client_id") == client_id
            ):
                return prompt_id
    return None


def run_comfy_with_recovery(payload):
    workflow = payload.get("workflow")
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError('COMFY payload needs a "workflow" object (API format)')

    relay.upload_comfy_input_images(payload)
    want_video = str(payload.get("media") or "").strip().lower() == "video"
    client_id = str(
        payload.get("_relayClientId")
        or f"{relay.AGENT_ID}-prompt-{time.time_ns()}"
    )

    prompt_id = None
    submit_error = None
    try:
        status, response = relay.http_json(
            "POST",
            f"{relay.COMFY_URL}/prompt",
            {"prompt": workflow, "client_id": client_id},
            timeout=COMFY_PROMPT_TIMEOUT,
        )
        if status != 200 or not response or not response.get("prompt_id"):
            raise RuntimeError(
                f"ComfyUI /prompt returned HTTP {status} at {relay.COMFY_URL}: "
                f"{response and response.get('node_errors')}"
            )
        prompt_id = response["prompt_id"]
    except Exception as error:  # noqa: BLE001 - accepted prompt may be recoverable
        submit_error = error
        relay.log(
            f"ComfyUI /prompt response failed after {COMFY_PROMPT_TIMEOUT}s; "
            f"checking queue for client {client_id}"
        )
        deadline = time.time() + COMFY_RECOVERY_SECONDS
        while time.time() < deadline and not prompt_id:
            prompt_id = queued_prompt_id_for_client(client_id)
            if not prompt_id:
                time.sleep(2)

    if not prompt_id:
        raise RuntimeError(
            f"ComfyUI POST /prompt failed at {relay.COMFY_URL} ({submit_error}). "
            f"No accepted prompt for client {client_id} appeared within "
            f"{COMFY_RECOVERY_SECONDS}s."
        ) from submit_error

    if submit_error:
        relay.log(f"recovered accepted Comfy prompt {prompt_id} for {client_id}")

    deadline = time.time() + relay.GEN_TIMEOUT
    while time.time() < deadline:
        time.sleep(2)
        status, history = relay.http_json(
            "GET", f"{relay.COMFY_URL}/history/{prompt_id}"
        )
        if status != 200 or not history:
            continue
        entry = history.get(prompt_id)
        if not entry:
            continue
        result = relay.extract_comfy_output(entry.get("outputs") or {}, want_video)
        if result:
            return result
        comfy_status = (entry.get("status") or {}).get("status_str")
        if comfy_status == "error":
            raise RuntimeError("ComfyUI reported a workflow error")

    kind = "video" if want_video else "image"
    raise RuntimeError(
        f"ComfyUI {kind} job timed out after {relay.GEN_TIMEOUT}s"
    )


def process_with_media(job):
    relative = direct_media_relative(job)
    if relative is None:
        return ORIGINAL_PROCESS(job)

    job_id = job["id"]
    engine = (job.get("engine") or "A1111").upper()
    payload = job_payload(job)
    payload["_relayClientId"] = f"{relay.AGENT_ID}-artjob-{job_id}"
    relay.log(f"job {job_id}: {engine} direct media -> {relative.as_posix()}")

    if engine == "COMFY":
        media = relay.run_comfy(payload)
    else:
        media = {
            "data_b64": relay.run_a1111(payload),
            "file_type": "png",
            "is_video": False,
        }

    staged_art_image_id = relay.upload_result(job, media)
    if not staged_art_image_id:
        raise RuntimeError("upload returned no ArtImage id")

    destination = write_direct_media(job, media)

    completed_job = relay.complete_job(
        job_id, True, art_image_id=staged_art_image_id
    )
    final_art_image_id = completed_job.get("artImageId") or staged_art_image_id

    if final_art_image_id != staged_art_image_id:
        relay.log(
            f"job {job_id}: staged ArtImage {staged_art_image_id} finalized "
            f"as canonical ArtImage {final_art_image_id}"
        )

    kind = "video" if media.get("is_video") else "image"
    relay.log(
        f"job {job_id}: DONE ({kind} ArtImage {final_art_image_id}; "
        f"media {destination})"
    )


relay.run_comfy = run_comfy_with_recovery
relay.process = process_with_media


if __name__ == "__main__":
    relay.main()
