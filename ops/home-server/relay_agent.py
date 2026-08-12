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
import socket
import sys
import time
import urllib.error
import urllib.request

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
RELAY_COMMIT = os.environ.get("KR_RELAY_COMMIT", "").strip()

# .webp covers animated-clip jobs saved via ComfyUI's native SaveAnimatedWEBP
# node (kind_robots' video generator defaults to it: smaller/better quality
# than gif, no custom node needed). Without it here, find_output_file()'s
# is_video_filename() check rejects the SaveAnimatedWEBP output for a
# want_video=True job and the relay reports "no output found" even though
# ComfyUI succeeded.
VIDEO_EXTENSIONS = (".mp4", ".webm", ".mov", ".mkv", ".gif", ".webp")


def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[relay {timestamp}] {message}", flush=True)


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

_OBJECT_INFO_TTL = 120.0
_object_info_cache = {"at": 0.0, "data": None}


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
    now = time.time()
    if (
        not force
        and _object_info_cache["data"] is not None
        and now - _object_info_cache["at"] < _OBJECT_INFO_TTL
    ):
        return _object_info_cache["data"]

    try:
        status, info = http_json("GET", f"{COMFY_URL}/object_info", timeout=30)
    except Exception as error:  # noqa: BLE001 - resolution is best-effort
        log(f"⚠️ could not fetch ComfyUI object_info for name resolution: {error}")
        return _object_info_cache["data"]

    if status != 200 or not isinstance(info, dict):
        log(f"⚠️ ComfyUI /object_info returned HTTP {status}; skipping name resolution")
        return _object_info_cache["data"]

    _object_info_cache["at"] = now
    _object_info_cache["data"] = info
    return info


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
        log(f"🔧 {class_type}.{input_name}: {old!r} -> {new!r}")

    _last_resolution.update(state="ran", remaps=len(remaps))
    return unresolved


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
        details = "; ".join(
            f"{class_type}.{input_name}={value!r}"
            for class_type, input_name, value in unresolved
        )
        raise RuntimeError(
            f"ComfyUI has no matching file for: {details}. Not in the live model "
            f"list at {COMFY_URL} (missing, misnamed, or an ambiguous basename). "
            "Failing fast instead of submitting a prompt ComfyUI would reject."
        )

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
            f"[asset-name resolution: {_last_resolution['state']}, "
            f"{_last_resolution['remaps']} remap(s)]"
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
                process(job)
                continue
        except KeyboardInterrupt:
            raise
        except Exception as error:  # noqa: BLE001 - relay must survive failures
            log(f"error: {error}")
            if job:
                try:
                    complete_job(job["id"], False, error=error)
                except Exception as report_error:  # noqa: BLE001
                    log(f"could not report failure: {report_error}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
