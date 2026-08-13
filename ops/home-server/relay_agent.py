#!/usr/bin/env python3
"""Pull-based ArtJob relay for the Kind Robots queue.

Runs on the home server beside ComfyUI/A1111:

  1. claim a runnable ArtJob from kind_robots
  2. render it on the local engine
  3. upload the bytes through /api/art/save-generated
  4. complete the ArtJob with exact Comfy request and output provenance

The upload creates a staging ArtImage. Normal jobs keep that id. An OVERWRITE
retry is finalized by kind_robots into its stable target ArtImage id; completion
returns that canonical id and this relay uses it for local-copy naming and logs.
That distinction matters because the temporary staging ArtImage is deleted by the
server's overwrite transaction.
"""

import base64
import hashlib
import io
import json
import os
import signal
import socket
import subprocess
import threading
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

KR_BASE_URL = os.environ.get(
    "KR_BASE_URL", "https://kindrobots.org"
).rstrip("/")
KR_RELAY_TOKEN = os.environ.get("KR_RELAY_TOKEN", "").strip()
KR_RELAY_USER_ID = int(os.environ.get("KR_RELAY_USER_ID", "0") or 0)
KR_LOCAL_IMAGES_DIR = os.environ.get("KR_LOCAL_IMAGES_DIR", "").strip()
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
SD_URL = os.environ.get("SD_URL", "http://127.0.0.1:7860").rstrip("/")
POLL_SECONDS = float(os.environ.get("POLL_SECONDS", "10"))
GEN_TIMEOUT = float(os.environ.get("GEN_TIMEOUT", "600"))
AGENT_ID = os.environ.get("AGENT_ID", socket.gethostname())
HEARTBEAT_SECONDS = float(os.environ.get("HEARTBEAT_SECONDS", "60"))
RELAY_VERSION = os.environ.get(
    "KR_RELAY_VERSION", "conductor-relay-completion-proof-v1"
).strip()

def detect_relay_build():
    """Identify the code actually running, without needing anyone to set an env var.

    "Is this a live problem or a stale one, and is the box even running the
    fix?" has cost this project real time repeatedly. On 2026-08-13 a LoRA
    resolver that had been merged, tested, and pulled was diagnosed as a stale
    deployment, because nothing in the relay's logs or its heartbeat said which
    build was running -- the actual cause was a second submission path that
    never called it. KR_RELAY_COMMIT existed for exactly this and was empty,
    because it required a human to export it on every start.

    So derive it: git first (the relay runs from a conductor checkout), then
    this file's mtime, which still answers "older or newer than the fix?" on a
    box with no git. Returns a dict; never raises, never blocks startup.
    """
    here = Path(__file__).resolve().parent

    def git(*args):
        return subprocess.run(
            ["git", *args],
            cwd=here,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()

    try:
        commit = git("rev-parse", "--short", "HEAD")
        committed_at = git("log", "-1", "--format=%cI")
        dirty = bool(git("status", "--porcelain", "--", "."))
        return {
            "commit": commit + ("-dirty" if dirty else ""),
            "committed_at": committed_at,
            "source": "git",
        }
    except (OSError, ValueError, subprocess.SubprocessError):
        pass

    try:
        mtime = datetime.fromtimestamp(
            Path(__file__).resolve().stat().st_mtime, timezone.utc
        ).astimezone()
        return {
            "commit": "",
            "committed_at": mtime.isoformat(timespec="seconds"),
            "source": "mtime",
        }
    except OSError:
        return {"commit": "", "committed_at": "", "source": "unknown"}


RELAY_BUILD = detect_relay_build()
# An explicit env var still wins; it just is no longer the only way to get one.
RELAY_COMMIT = os.environ.get("KR_RELAY_COMMIT", "").strip() or RELAY_BUILD["commit"]

# .webp covers animated-clip jobs saved via ComfyUI's native SaveAnimatedWEBP
# node (kind_robots' video generator defaults to it: smaller/better quality
# than gif, no custom node needed). Without it here, find_output_file()'s
# is_video_filename() check rejects the SaveAnimatedWEBP output for a
# want_video=True job and the relay reports "no output found" even though
# ComfyUI succeeded.
VIDEO_EXTENSIONS = (".mp4", ".webm", ".mov", ".mkv", ".gif", ".webp")

# Named rather than inlined so the one place that has to survive a cp1252
# stdout is obvious. emit() guarantees it cannot raise; see _use_utf8_stdout.
WARN = "\N{WARNING SIGN}"
WRENCH = "\N{WRENCH}"


def _use_utf8_stdout():
    """Stop the console codepage from deciding what the relay may say.

    On Windows, Python picks stdout's encoding from the locale codepage
    (cp1252 here) whenever stdout is not a terminal -- which is exactly the
    case under pm2, where stdout is a pipe into a log file. Every non-cp1252
    character in a log message then raises UnicodeEncodeError from print().

    That is not cosmetic. `log("\N{HAMMER AND WRENCH} ...")` in
    align_workflow_asset_names and the two `\N{WARNING SIGN}` lines in
    fetch_comfy_object_info are all un-encodable in cp1252, and a raise from
    inside align_workflow_asset_names propagates out of run_comfy and FAILS
    THE JOB. ArtJobs 8276/8278 died exactly this way on 2026-08-13 -- the
    resolver had matched the LoRA and was logging the remap it was about to
    apply when print() killed the render. Worse, the warning that exists to
    report an unreachable /object_info would itself crash before reporting it.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            # Python < 3.7, an already-detached stream, or a stream that
            # refuses reconfiguration. emit()'s fallback still covers us.
            pass


_use_utf8_stdout()


def emit(line):
    """print() that can never take a job down with it.

    _use_utf8_stdout() should make this unreachable, but a log call is not
    worth a failed render under any circumstance, so the encoding is degraded
    rather than raised. backslashreplace keeps the line readable and reversible
    (a dropped remap line is a lost diagnosis) instead of silently emitting
    nothing.
    """
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "ascii"
        print(
            line.encode(encoding, "backslashreplace").decode(encoding, "replace"),
            flush=True,
        )
    except OSError:
        # A closed or broken stdout must not end the relay either.
        pass


def human_time(moment):
    """`Aug 13 3:47PM` -- the scannable half of the timestamp.

    Built by hand rather than with strftime because the no-pad directives that
    would express it are platform-specific: %-I/%-d are glibc, Windows wants
    %#I/%#d, and this relay runs on Windows. %b is portable, the rest is
    arithmetic.
    """
    hour = (moment.hour % 12) or 12
    meridiem = "AM" if moment.hour < 12 else "PM"
    return (
        f"{moment:%b} {moment.day} "
        f"{hour}:{moment.minute:02d}:{moment.second:02d}{meridiem}"
    )


def log(message):
    # One readable local time, seconds included. The ISO stamp that used to
    # lead every line was dropped as noise (Silas, 2026-08-13) -- what it bought
    # was an explicit UTC offset for correlating against ArtJob
    # createdAt/updatedAt, and in practice the box's own local time reads fine
    # for that. Seconds stay because job timings are compared at that
    # granularity (a claim and its submit are seconds apart).
    emit(f"{human_time(datetime.now().astimezone())} relay {message}")


def log_build_identity():
    """Log which build is running, at startup, before anything can go wrong.

    Pairs with log_media_roots(): state that is invisible until it causes a
    confusing failure hours later belongs in the log at boot.
    """
    build = RELAY_BUILD
    commit = RELAY_COMMIT or "unknown"
    when = build["committed_at"] or "unknown"
    if build["source"] == "git":
        log(f"build {commit} committed {when} (git)")
    elif build["source"] == "mtime":
        log(f"build {commit or 'unknown'} relay_agent.py modified {when} (no git)")
    else:
        log("build unknown (no git, no readable mtime)")


def http_json(method, url, body=None, bearer=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    if bearer:
        request.add_header("Authorization", f"Bearer {bearer}")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read().decode() or "null")
    except urllib.error.HTTPError as error:
        try:
            payload = json.loads(error.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return error.code, payload


def check_engine(base_url, health_path):
    started = time.time()
    try:
        request = urllib.request.Request(f"{base_url}{health_path}", method="GET")
        with urllib.request.urlopen(request, timeout=10) as response:
            ok = 200 <= response.status < 300
            response.read(1)
    except Exception:  # noqa: BLE001 - any failure means down
        return False, None
    return ok, int((time.time() - started) * 1000)


def post_heartbeat(engine, ok, latency_ms):
    try:
        http_json(
            "POST",
            f"{KR_BASE_URL}/api/server/heartbeat",
            {"engine": engine, "ok": ok, "latencyMs": latency_ms},
            bearer=KR_RELAY_TOKEN,
            timeout=15,
        )
    except Exception as error:  # noqa: BLE001 - never crash on heartbeat
        log(f"heartbeat({engine}) failed to post: {error}")


def send_heartbeats():
    comfy_ok, comfy_ms = check_engine(COMFY_URL, "/system_stats")
    post_heartbeat("COMFY", comfy_ok, comfy_ms)
    sd_ok, sd_ms = check_engine(SD_URL, "/sdapi/v1/progress")
    post_heartbeat("A1111", sd_ok, sd_ms)


def claim_job():
    status, response = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/queue/claim",
        {
            "agentId": AGENT_ID,
            "agentVersion": RELAY_VERSION,
            "supportsInputImages": True,
            "supportsCompletionProof": True,
        },
        bearer=KR_RELAY_TOKEN,
    )
    if status == 404:
        detail = ""
        if isinstance(response, dict):
            detail = str(response.get("message") or response.get("error") or "")[:200]
        log(f"claim got 404 - body: {detail or '(non-JSON body)'} - waiting")
        return None
    if status != 200 or not response or not response.get("success"):
        log(f"claim failed: HTTP {status} {response and response.get('message')}")
        return None
    return (response.get("data") or {}).get("job")


def run_a1111(payload):
    body = {
        "prompt": payload.get("prompt") or payload.get("promptString") or "",
        "negative_prompt": payload.get("negative_prompt")
        or payload.get("negativePrompt")
        or "",
        "steps": payload.get("steps", 20),
        "cfg_scale": payload.get("cfg_scale", payload.get("cfg", 7)),
        "seed": payload.get("seed", -1),
        "width": payload.get("width", 512),
        "height": payload.get("height", 512),
        "sampler_name": payload.get("sampler_name")
        or payload.get("sampler")
        or "Euler a",
    }
    if not body["prompt"]:
        raise ValueError("A1111 payload has no prompt/promptString")
    status, response = http_json(
        "POST", f"{SD_URL}/sdapi/v1/txt2img", body, timeout=GEN_TIMEOUT
    )
    if status != 200 or not response or not response.get("images"):
        raise RuntimeError(f"A1111 returned HTTP {status}, no images")
    return response["images"][0]


def decode_image_entry(entry):
    name = (entry or {}).get("name")
    data = (entry or {}).get("imageData") or ""
    if not name or not data:
        raise ValueError('each images entry needs "name" and "imageData"')
    if data.lstrip().lower().startswith("data:") and "," in data:
        data = data.split(",", 1)[1]
    return name, base64.b64decode(data)


def build_image_upload_request(name, raw, boundary):
    extension = os.path.splitext(name)[1].lstrip(".").lower() or "png"
    mime = "image/jpeg" if extension in ("jpg", "jpeg") else f"image/{extension}"
    parts = [
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'
            f"Content-Type: {mime}\r\n\r\n"
        ).encode(),
        raw,
        (
            f"\r\n--{boundary}\r\n"
            'Content-Disposition: form-data; name="type"\r\n\r\ninput\r\n'
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n'
            f"--{boundary}--\r\n"
        ).encode(),
    ]
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def upload_comfy_input_images(payload):
    images = payload.get("images") or []
    if not isinstance(images, list):
        raise ValueError('COMFY payload "images" must be a list')
    for entry in images:
        name, raw = decode_image_entry(entry)
        boundary = "krrelay" + base64.b16encode(os.urandom(12)).decode().lower()
        body, content_type = build_image_upload_request(name, raw, boundary)
        request = urllib.request.Request(
            f"{COMFY_URL}/upload/image", data=body, method="POST"
        )
        request.add_header("Content-Type", content_type)
        with urllib.request.urlopen(request, timeout=120) as response:
            uploaded = json.loads(response.read().decode() or "null")
        if not uploaded or not uploaded.get("name"):
            raise RuntimeError(f"ComfyUI input upload failed for {name}")
        log(f"uploaded input image {uploaded['name']}")


def is_video_filename(filename):
    return bool(filename) and filename.lower().endswith(VIDEO_EXTENSIONS)


def file_extension(filename):
    return os.path.splitext(filename or "")[1].lstrip(".").lower()


def find_output_file(value, want_video):
    if not value:
        return None
    if isinstance(value, list):
        for item in value:
            found = find_output_file(item, want_video)
            if found:
                return found
        return None
    if isinstance(value, dict):
        filename = value.get("filename")
        if isinstance(filename, str) and filename:
            if is_video_filename(filename) == bool(want_video):
                return {
                    "filename": filename,
                    "subfolder": value.get("subfolder", "") or "",
                    "type": value.get("type", "output") or "output",
                }
        for child in value.values():
            found = find_output_file(child, want_video)
            if found:
                return found
    return None


def download_comfy_file(file_meta):
    from urllib.parse import urlencode

    query = urlencode(
        {
            "filename": file_meta["filename"],
            "subfolder": file_meta.get("subfolder", ""),
            "type": file_meta.get("type", "output"),
        }
    )
    request = urllib.request.Request(f"{COMFY_URL}/view?{query}")
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def extract_comfy_output(outputs, want_video, prompt_id=None):
    file_meta = find_output_file(outputs, want_video)
    if not file_meta:
        return None
    raw = download_comfy_file(file_meta)
    extension = file_extension(file_meta["filename"])
    return {
        "data_b64": base64.b64encode(raw).decode(),
        "file_type": extension or ("mp4" if want_video else "png"),
        "is_video": bool(want_video),
        "comfy": {
            "prompt_id": prompt_id,
            "output": file_meta,
            "image_hash": hashlib.sha256(raw).hexdigest(),
        },
    }


def describe_comfy_error(entry):
    """Pull the node/exception detail out of a ComfyUI history entry's
    status.messages, when ComfyUI's error status includes one, instead of
    letting the generic status_str == 'error' fire blind."""
    messages = (entry.get("status") or {}).get("messages") or []
    for message in messages:
        if not isinstance(message, (list, tuple)) or len(message) != 2:
            continue
        message_type, detail = message
        if message_type != "execution_error" or not isinstance(detail, dict):
            continue
        exception_message = detail.get("exception_message") or detail.get("exception_type")
        if not exception_message:
            continue
        node_id = detail.get("node_id")
        node_type = detail.get("node_type")
        where = f"node {node_id} ({node_type})" if node_id else "workflow"
        return f"{where}: {exception_message}"
    return None


# --- model/LoRA name resolution against ComfyUI's live filename lists ---------
#
# A workflow baked upstream (kind_robots) carries checkpoint/LoRA/unet/vae/clip
# names as literal strings. ComfyUI validates each against its object_info combo
# list and rejects the whole prompt with HTTP 400 `value_not_in_list` if the
# string does not match a list entry EXACTLY -- and the list entries drift from
# what a job stored: slash direction (`Flux\SFW\x` vs `Flux/SFW/x`), case
# (`FLUX/` vs `Flux/`), and folder prefix all vary across ComfyUI versions and
# installs. This burned nine real queue jobs even though every file was present
# on disk. We resolve each name against the live list here -- ignoring case and
# slash direction, with a unique-basename fallback -- and substitute the exact
# current entry before POSTing. Mirrors scripts/compare_comfy_lora_paths.py so
# the two agree on what "the same LoRA" means. A value ComfyUI already accepts
# is left untouched, so correct jobs are unaffected.

# 15 minutes, not 2. A render takes ~7.5 minutes, so a 120s TTL expired during
# every single job -- guaranteeing that the next job's refetch raced a ComfyUI
# that was busy sampling, and a multi-MB /object_info over a 30s timeout loses
# that race essentially every time. That is what produced
# "could not fetch ComfyUI object_info ... timed out" on 2026-08-13, which
# silently downgraded align_workflow_asset_names to a no-op and submitted
# unresolved LoRA names straight to ComfyUI.
#
# A long TTL is safe because staleness is already handled where it matters:
# align_workflow_asset_names refetches with force=True the moment a name fails
# to resolve against the cached copy, so a model added since the last fetch is
# picked up on demand rather than by expiry. The TTL only bounds how long a
# REMOVED entry lingers, which costs one failed resolve at worst.
_OBJECT_INFO_TTL = float(os.environ.get("COMFY_OBJECT_INFO_TTL", "900"))

# ComfyUI serves /object_info from the same process that runs the sampler, so
# while a render is in flight it can be slow rather than unavailable. Wait
# longer, and retry once, before giving up and submitting unresolved.
_OBJECT_INFO_TIMEOUT = float(os.environ.get("COMFY_OBJECT_INFO_TIMEOUT", "90"))
_OBJECT_INFO_ATTEMPTS = int(os.environ.get("COMFY_OBJECT_INFO_ATTEMPTS", "2"))
_object_info_cache = {"at": 0.0, "data": None}
# One fetch at a time. Without this the startup warm-up and the first job both
# pull a multi-MB response from a ComfyUI that is already the bottleneck; the
# waiter re-checks the cache after acquiring and usually returns immediately.
_object_info_lock = threading.Lock()


def _normalize_asset_name(value):
    return value.strip().replace("\\", "/").strip("/").casefold()


def _asset_basename(value):
    return _normalize_asset_name(value).rsplit("/", 1)[-1]


def _combo_candidates(definition):
    """Return the list of string choices for an object_info input definition,
    or None when the input is not a resolvable filename/enum combo (e.g.
    INT/FLOAT/STRING, or an upload-backed input). Combo inputs are shaped
    `[[<choices>], {opts}]`."""
    if not (isinstance(definition, list) and definition and isinstance(definition[0], list)):
        return None
    choices = definition[0]
    if not choices or not all(isinstance(item, str) for item in choices):
        return None
    opts = definition[1] if len(definition) > 1 and isinstance(definition[1], dict) else {}
    # Upload-backed combos (LoadImage `image`/`mask`, video loaders) are
    # populated from Comfy's input dir. The relay uploads those files separately
    # (upload_comfy_input_images), and a cached/stale object_info won't list a
    # just-uploaded name -- so never remap or fail-fast on them.
    if any("upload" in str(key).lower() for key in opts):
        return None
    return choices


def _resolve_against_candidates(value, candidates):
    """Best current-list entry for `value`, or None. Exact match wins (caller
    skips those); then normalized-exact (case/slash-insensitive); then a unique
    basename match. Ambiguous basenames are left for a human, not guessed."""
    by_norm = {}
    for candidate in candidates:
        by_norm.setdefault(_normalize_asset_name(candidate), candidate)
    match = by_norm.get(_normalize_asset_name(value))
    if match is not None:
        return match

    by_base = {}
    for candidate in candidates:
        by_base.setdefault(_asset_basename(candidate), []).append(candidate)
    base_matches = by_base.get(_asset_basename(value), [])
    if len(base_matches) == 1:
        return base_matches[0]
    return None


def resolve_workflow_asset_names(workflow, object_info):
    """Rewrite filename-combo inputs in `workflow` in place to match the live
    `object_info` lists. Returns (remaps, unresolved): remaps is a list of
    (class_type, input_name, old, new); unresolved is (class_type, input_name,
    value) for names with no confident match. Values ComfyUI already lists are
    left as-is."""
    remaps = []
    unresolved = []
    if not isinstance(object_info, dict):
        return remaps, unresolved

    for node in workflow.values():
        if not isinstance(node, dict):
            continue
        class_type = node.get("class_type")
        inputs = node.get("inputs")
        if not class_type or not isinstance(inputs, dict):
            continue
        spec = object_info.get(class_type)
        if not isinstance(spec, dict):
            continue
        node_inputs = spec.get("input")
        if not isinstance(node_inputs, dict):
            continue
        required = node_inputs.get("required") if isinstance(node_inputs.get("required"), dict) else {}
        optional = node_inputs.get("optional") if isinstance(node_inputs.get("optional"), dict) else {}

        for input_name, value in list(inputs.items()):
            if not isinstance(value, str):
                continue
            definition = required.get(input_name, optional.get(input_name))
            candidates = _combo_candidates(definition)
            if not candidates or value in candidates:
                continue
            match = _resolve_against_candidates(value, candidates)
            if match is None:
                unresolved.append((class_type, input_name, value))
            elif match != value:
                inputs[input_name] = match
                remaps.append((class_type, input_name, value, match))

    return remaps, unresolved


def fetch_comfy_object_info(force=False):
    """Fetch ComfyUI's /object_info (node schemas + filename lists), cached for
    a short TTL to avoid refetching the multi-MB blob on every job. Returns the
    dict, or None when the fetch fails (resolution is then skipped, never fatal)."""
    def _fresh(at_time):
        return (
            _object_info_cache["data"] is not None
            and at_time - _object_info_cache["at"] < _OBJECT_INFO_TTL
        )

    now = time.time()
    if not force and _fresh(now):
        return _object_info_cache["data"]

    with _object_info_lock:
        # Someone may have fetched it while we waited for the lock.
        now = time.time()
        if _fresh(now):
            return _object_info_cache["data"]
        return _fetch_object_info_locked(now)


def _fetch_object_info_locked(now):
    last_error = None
    for attempt in range(1, max(1, _OBJECT_INFO_ATTEMPTS) + 1):
        try:
            status, info = http_json(
                "GET", f"{COMFY_URL}/object_info", timeout=_OBJECT_INFO_TIMEOUT
            )
        except Exception as error:  # noqa: BLE001 - resolution is best-effort
            last_error = error
            if attempt < _OBJECT_INFO_ATTEMPTS:
                time.sleep(2)
                continue
            break

        if status != 200 or not isinstance(info, dict):
            last_error = f"HTTP {status}"
            if attempt < _OBJECT_INFO_ATTEMPTS:
                time.sleep(2)
                continue
            break

        _object_info_cache["at"] = now
        _object_info_cache["data"] = info
        return info

    # Serving a stale copy beats skipping resolution: the model list barely
    # changes, and a name that is missing from it still force-refetches below.
    stale = _object_info_cache["data"]
    log(
        f"{WARN} could not fetch ComfyUI object_info after "
        f"{_OBJECT_INFO_ATTEMPTS} attempt(s): {last_error}"
        + (
            " - using the last known copy"
            if stale is not None
            else " - name resolution skipped for this job"
        )
    )
    return stale


# What the last call to align_workflow_asset_names actually did. Read only by
# run_comfy, to stamp the outcome onto a submission failure.
#
# "Returns [] when object_info can't be fetched" and "returns [] because every
# name resolved" are the same value, and the difference is the whole diagnosis.
# ArtJob 7905 failed three times on `ckpt_name:
# 'SDXL/dreamshaperXL_v21TurboDPMSDE.safetensors' not in (list of length 58)` —
# a file that is on disk, and a name this resolver would have fixed by slash or
# basename. From the queue it was impossible to tell whether the relay was
# running a build without the resolver or running it with /object_info
# unreachable, and the only place that distinction existed was a `⚠️` line in
# the relay's stdout on a machine nobody was watching. Now it rides along with
# the error.
_last_resolution = {"state": "not-run", "remaps": 0}


def align_workflow_asset_names(workflow):
    """Resolve every checkpoint/LoRA/unet/vae/clip name in `workflow` against
    the live ComfyUI lists before submission, rewriting each to the exact
    current list entry. Refetches object_info once if a name is unresolved
    against the cached copy (a model may have just been added). Logs each
    remap; returns the still-unresolved names as (class_type, input_name,
    value) tuples so the caller can fail fast. Returns [] when object_info
    can't be fetched (resolution skipped, submit as-is)."""
    object_info = fetch_comfy_object_info()
    if object_info is None:
        _last_resolution.update(state="skipped-no-object-info", remaps=0)
        return []

    remaps, unresolved = resolve_workflow_asset_names(workflow, object_info)
    if unresolved:
        fresh = fetch_comfy_object_info(force=True)
        if fresh is not None and fresh is not object_info:
            remaps, unresolved = resolve_workflow_asset_names(workflow, fresh)

    for class_type, input_name, old, new in remaps:
        log(f"{WRENCH} {class_type}.{input_name}: {old!r} -> {new!r}")

    _last_resolution.update(state="ran", remaps=len(remaps))
    return unresolved


def last_resolution_note():
    """The resolver-state suffix stamped onto a ComfyUI rejection.

    Defined once and shared by every submission path, so a caller that
    reimplements submission cannot quietly drop the diagnosis half of the
    error while keeping the rest.
    """
    return (
        f"[asset-name resolution: {_last_resolution['state']}, "
        f"{_last_resolution['remaps']} remap(s)]"
    )


def unresolved_asset_error(unresolved):
    """The fail-fast raised when a name cannot match ComfyUI's live list.

    Shared for the same reason as `last_resolution_note`: both submission
    paths must refuse an unresolvable name identically. `relay_media_agent`'s
    `run_comfy_with_recovery` reimplemented submission and, until 2026-08-13,
    called neither this nor `align_workflow_asset_names` — so every job going
    through the media wrapper (i.e. every job `kr-relay` actually runs)
    bypassed the resolver entirely and POSTed the unresolved name straight to
    ComfyUI. See the module docstring in relay_media_agent.py.
    """
    details = "; ".join(
        f"{class_type}.{input_name}={value!r}"
        for class_type, input_name, value in unresolved
    )
    return RuntimeError(
        f"ComfyUI has no matching file for: {details}. Not in the live model "
        f"list at {COMFY_URL} (missing, misnamed, or an ambiguous basename). "
        "Failing fast instead of submitting a prompt ComfyUI would reject."
    )


# The job this process claimed and has not finished. Read by the shutdown
# handler so a restart hands the job back instead of abandoning it.
_in_flight_job_id = None


def release_in_flight_claim(reason):
    """Hand a claimed-but-unfinished job back to the queue.

    Without this, every relay restart strands whatever was rendering: the row
    stays RUNNING with a stale claimedAt, and nothing reaps it, because the
    claim endpoint only FAILs a stale RUNNING job once attempts >= MAX_ATTEMPTS.
    Below that it is merely re-claimable after STALE_CLAIM_MINUTES -- correct,
    but it means the dashboard counts abandoned work as "running" for as long as
    it takes the queue to come back around. On 2026-08-13 six restarts in one
    afternoon left three RUNNING rows against one real render.

    resetAttempts is false on purpose. The attempt was already counted when the
    job was claimed, and a job that crashes the relay on every start would loop
    forever if each abandonment gave it a fresh budget; leaving the count intact
    means it eventually reaches MAX_ATTEMPTS and stops. A human requeue still
    resets, which is the right asymmetry.
    """
    job_id = _in_flight_job_id
    if not job_id:
        return
    log(f"{reason}: releasing claim on job {job_id}")
    try:
        status, _ = http_json(
            "POST",
            f"{KR_BASE_URL}/api/art/queue/{job_id}/requeue",
            {"resetAttempts": False},
            bearer=KR_RELAY_TOKEN,
            timeout=5,
        )
        if status == 200:
            log(f"job {job_id} returned to the queue")
        else:
            log(f"{WARN} could not release job {job_id}: HTTP {status}")
    except Exception as error:  # noqa: BLE001 - shutdown must not raise
        log(f"{WARN} could not release job {job_id}: {error}")


def install_shutdown_handler():
    """Release the in-flight claim on SIGTERM/SIGINT.

    pm2 sends SIGTERM on restart, stop and delete. Python's default SIGTERM
    disposition kills the process outright -- no exception, no finally, so the
    existing KeyboardInterrupt catch never sees it and the claim leaks.
    """

    def _handle(signum, _frame):
        release_in_flight_claim(f"signal {signum}")
        sys.exit(0)

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            signal.signal(sig, _handle)
        except (ValueError, OSError, AttributeError):
            # Not the main thread, or a platform without this signal.
            pass


def warm_object_info_async():
    """Warm the object_info cache WITHOUT blocking startup.

    The first version of this called fetch_comfy_object_info(force=True)
    inline, which was wrong: the fetch is allowed to take up to
    _OBJECT_INFO_TIMEOUT x _OBJECT_INFO_ATTEMPTS plus backoff, so on a box
    whose ComfyUI was mid-render the relay sat in main() for ~3 minutes before
    it could claim its first job -- silently, since neither the warm-up line
    nor the "polling" line had been reached yet. Observed 2026-08-13: a restart
    logged the build banner and then nothing.

    Warming is an optimisation, never a precondition. Every consumer of the
    cache already fetches on demand and degrades to submit-as-is, so this runs
    on a daemon thread and the poll loop starts immediately.
    """

    def _warm():
        try:
            if fetch_comfy_object_info(force=True) is not None:
                log("object_info cached for asset-name resolution")
            else:
                log("object_info not cached yet; will fetch on the first job")
        except Exception as error:  # noqa: BLE001 - warming must never escape
            log(f"{WARN} object_info warm-up failed: {error}")

    thread = threading.Thread(target=_warm, name="object-info-warm", daemon=True)
    thread.start()
    return thread


def run_comfy(payload):
    workflow = payload.get("workflow")
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError('COMFY payload needs a "workflow" object (API format)')

    upload_comfy_input_images(payload)

    # Fail fast on model names ComfyUI's live list can't match, rather than
    # POSTing a prompt it will reject with a 400 and then waiting out the
    # accept/generation timeout (× the queue's retry budget). ComfyUI validates
    # these combo inputs itself, so an unresolved name here is a guaranteed
    # rejection -- surface it immediately with the exact node/input/value.
    unresolved = align_workflow_asset_names(workflow)
    if unresolved:
        raise unresolved_asset_error(unresolved)

    want_video = str(payload.get("media") or "").strip().lower() == "video"

    try:
        status, response = http_json(
            "POST",
            f"{COMFY_URL}/prompt",
            {"prompt": workflow, "client_id": AGENT_ID},
        )
    except Exception as error:  # noqa: BLE001 - add actionable context
        raise RuntimeError(
            f"ComfyUI POST /prompt failed at {COMFY_URL} ({error}). "
            "Is ComfyUI running and responsive on that port? "
            f"Try opening {COMFY_URL}/system_stats."
        ) from error

    if status != 200 or not response or not response.get("prompt_id"):
        # Stamp the resolver's state onto the rejection. A `value_not_in_list`
        # here with "asset-name resolution ran" means the catalog and ComfyUI
        # genuinely disagree beyond slash/case/basename; the same rejection with
        # "skipped" means the relay never got to look, and the fix is the box,
        # not the name.
        raise RuntimeError(
            f"ComfyUI /prompt returned HTTP {status} at {COMFY_URL}: "
            f"{response and response.get('node_errors')} "
            f"{last_resolution_note()}"
        )

    prompt_id = response["prompt_id"]
    deadline = time.time() + GEN_TIMEOUT
    while time.time() < deadline:
        time.sleep(2)
        status, history = http_json("GET", f"{COMFY_URL}/history/{prompt_id}")
        if status != 200 or not history:
            continue
        entry = history.get(prompt_id)
        if not entry:
            continue
        result = extract_comfy_output(
            entry.get("outputs") or {}, want_video, prompt_id=prompt_id
        )
        if result:
            return result
        comfy_status = (entry.get("status") or {}).get("status_str")
        if comfy_status == "error":
            detail = describe_comfy_error(entry)
            message = "ComfyUI reported a workflow error"
            raise RuntimeError(f"{message}: {detail}" if detail else message)

    kind = "video" if want_video else "image"
    raise RuntimeError(f"ComfyUI {kind} job timed out after {GEN_TIMEOUT}s")


def completion_provenance(payload, media):
    request_provenance = payload.get("provenance") or {}
    comfy = media.get("comfy") or {}
    required = {
        "promptId": comfy.get("prompt_id"),
        "promptHash": request_provenance.get("promptHash"),
        "workflowHash": request_provenance.get("workflowHash"),
        "workflowPromptHash": request_provenance.get("workflowPromptHash"),
        "imageHash": comfy.get("image_hash"),
        "output": comfy.get("output"),
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise RuntimeError(
            "cannot complete strict COMFY ArtJob; missing provenance: "
            + ", ".join(missing)
        )
    return {
        "relayVersion": RELAY_VERSION,
        "relayCommit": RELAY_COMMIT or None,
        **required,
    }


def upload_result(job, media):
    payload = job.get("payload") or {}
    body = {
        "imageBase64": media["data_b64"],
        "promptString": payload.get("promptString")
        or payload.get("prompt")
        or f"art job {job['id']}",
        "negativePrompt": payload.get("negativePrompt")
        or payload.get("negative_prompt"),
        "steps": payload.get("steps"),
        "seed": payload.get("seed"),
        "fileType": media.get("file_type"),
        "designer": f"relay:{AGENT_ID}",
        "userId": KR_RELAY_USER_ID,
    }
    status, response = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/save-generated",
        body,
        bearer=KR_RELAY_TOKEN,
        timeout=180,
    )
    if status != 201 or not response or not response.get("success"):
        raise RuntimeError(
            f"save-generated failed: HTTP {status} "
            f"{response and response.get('message')}"
        )
    return (response.get("data") or {}).get("id")


def encode_webp(raw):
    try:
        from PIL import Image

        with Image.open(io.BytesIO(raw)) as image:
            buffer = io.BytesIO()
            image.save(buffer, format="WEBP", quality=90, method=6)
            return buffer.getvalue(), "webp"
    except Exception as error:  # noqa: BLE001 - Pillow missing or bad bytes
        log(f"webp encode skipped ({error}); keeping png")
        return raw, "png"


def write_local_copy(job, art_image_id, media):
    if not KR_LOCAL_IMAGES_DIR:
        return
    try:
        payload = job.get("payload") or {}
        collection = str(payload.get("collection") or "sdxl").strip().lower()
        if not collection.replace("-", "").replace("_", "").isalnum():
            collection = "sdxl"
        base = KR_LOCAL_IMAGES_DIR.replace("\\", "/").rstrip("/")
        folder = f"{base}/{collection}"
        os.makedirs(folder, exist_ok=True)
        raw = base64.b64decode(media["data_b64"])
        if media.get("is_video"):
            data, extension = raw, media.get("file_type") or "mp4"
        else:
            data, extension = encode_webp(raw)
        file_path = f"{folder}/{collection}-{art_image_id}.{extension}"
        with open(file_path, "wb") as output:
            output.write(data)
        log(f"local copy: {file_path}")
    except Exception as error:  # noqa: BLE001 - DB result remains authoritative
        log(f"local copy failed (job still DONE): {error}")


def complete_job(job_id, success, art_image_id=None, error=None, provenance=None):
    body = {"success": success}
    if art_image_id:
        body["artImageId"] = art_image_id
    if error:
        body["error"] = str(error)[:4000]
    if provenance:
        body["provenance"] = provenance
    status, response = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/queue/{job_id}/complete",
        body,
        bearer=KR_RELAY_TOKEN,
    )
    if status != 200 or not response or not response.get("success"):
        raise RuntimeError(
            f"complete({job_id}) failed: HTTP {status} "
            f"{response and response.get('message')}"
        )
    return (response.get("data") or {}).get("job") or {}


def resolve_job_engine(job):
    """Use Comfy for unlabeled jobs while preserving explicit A1111 support."""
    engine = str(job.get("engine") or "COMFY").strip().upper()
    if engine not in ("COMFY", "A1111"):
        raise ValueError(
            f"unsupported ArtJob engine {engine!r}; expected COMFY or A1111"
        )
    return engine


def process(job):
    job_id = job["id"]
    engine = resolve_job_engine(job)
    payload = job.get("payload") or {}
    if isinstance(payload, str):
        payload = json.loads(payload)
    log(f"job {job_id}: {engine} attempt {job.get('attempts')}")

    if engine == "COMFY":
        media = run_comfy(payload)
        provenance = completion_provenance(payload, media)
    else:  # explicit A1111 jobs remain supported for Kind Robots users
        media = {
            "data_b64": run_a1111(payload),
            "file_type": "png",
            "is_video": False,
        }
        provenance = None

    staged_art_image_id = upload_result(job, media)
    if not staged_art_image_id:
        raise RuntimeError("upload returned no ArtImage id")

    completed_job = complete_job(
        job_id,
        True,
        art_image_id=staged_art_image_id,
        provenance=provenance,
    )
    final_art_image_id = completed_job.get("artImageId") or staged_art_image_id

    if final_art_image_id != staged_art_image_id:
        log(
            f"job {job_id}: staged ArtImage {staged_art_image_id} finalized "
            f"as canonical ArtImage {final_art_image_id}"
        )

    write_local_copy(job, final_art_image_id, media)
    kind = "video" if media.get("is_video") else "image"
    log(f"job {job_id}: DONE ({kind} ArtImage {final_art_image_id})")


def main():
    if not KR_RELAY_TOKEN or not KR_RELAY_USER_ID:
        log("KR_RELAY_TOKEN and KR_RELAY_USER_ID are required - exiting")
        sys.exit(1)

    log_build_identity()
    install_shutdown_handler()
    warm_object_info_async()
    log(
        f"agent {AGENT_ID} ({RELAY_VERSION}) polling {KR_BASE_URL} "
        f"every {POLL_SECONDS}s"
    )
    last_heartbeat = 0.0
    while True:
        job = None
        try:
            if (
                HEARTBEAT_SECONDS > 0
                and time.time() - last_heartbeat >= HEARTBEAT_SECONDS
            ):
                send_heartbeats()
                last_heartbeat = time.time()

            job = claim_job()
            if job:
                global _in_flight_job_id
                _in_flight_job_id = job["id"]
                try:
                    process(job)
                finally:
                    _in_flight_job_id = None
                continue
        except KeyboardInterrupt:
            raise
        except Exception as error:  # noqa: BLE001 - relay must survive failures
            log(f"error: {error}")
            _in_flight_job_id = None
            if job:
                try:
                    complete_job(job["id"], False, error=error)
                except Exception as report_error:  # noqa: BLE001
                    log(f"could not report failure: {report_error}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
