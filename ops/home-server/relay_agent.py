#!/usr/bin/env python3
"""Pull-based ArtJob relay for the Kind Robots queue.

Runs on the home server beside ComfyUI/A1111:

  1. claim a runnable ArtJob from kind_robots
  2. render it on the local engine
  3. upload the bytes through /api/art/save-generated
  4. complete the ArtJob

The upload creates a staging ArtImage. Normal jobs keep that id. An OVERWRITE
retry is finalized by kind_robots into its stable target ArtImage id; completion
returns that canonical id and this relay uses it for local-copy naming and logs.
That distinction matters because the temporary staging ArtImage is deleted by the
server's overwrite transaction.
"""

import base64
import io
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request

KR_BASE_URL = os.environ.get(
    "KR_BASE_URL", "https://kind-robots.vercel.app"
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

VIDEO_EXTENSIONS = (".mp4", ".webm", ".mov", ".mkv", ".gif")


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
        {"agentId": AGENT_ID, "supportsInputImages": True},
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
        return base64.b64encode(response.read()).decode()


def extract_comfy_output(outputs, want_video):
    file_meta = find_output_file(outputs, want_video)
    if not file_meta:
        return None
    extension = file_extension(file_meta["filename"])
    return {
        "data_b64": download_comfy_file(file_meta),
        "file_type": extension or ("mp4" if want_video else "png"),
        "is_video": bool(want_video),
    }


def run_comfy(payload):
    workflow = payload.get("workflow")
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError('COMFY payload needs a "workflow" object (API format)')

    upload_comfy_input_images(payload)
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
        raise RuntimeError(
            f"ComfyUI /prompt returned HTTP {status} at {COMFY_URL}: "
            f"{response and response.get('node_errors')}"
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
        result = extract_comfy_output(entry.get("outputs") or {}, want_video)
        if result:
            return result
        comfy_status = (entry.get("status") or {}).get("status_str")
        if comfy_status == "error":
            raise RuntimeError("ComfyUI reported a workflow error")

    kind = "video" if want_video else "image"
    raise RuntimeError(f"ComfyUI {kind} job timed out after {GEN_TIMEOUT}s")


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
        from PIL import Image  # optional dependency

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


def complete_job(job_id, success, art_image_id=None, error=None):
    body = {"success": success}
    if art_image_id:
        body["artImageId"] = art_image_id
    if error:
        body["error"] = str(error)[:4000]
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


def process(job):
    job_id = job["id"]
    engine = (job.get("engine") or "A1111").upper()
    payload = job.get("payload") or {}
    if isinstance(payload, str):
        payload = json.loads(payload)
    log(f"job {job_id}: {engine} attempt {job.get('attempts')}")

    if engine == "COMFY":
        media = run_comfy(payload)
    else:
        media = {
            "data_b64": run_a1111(payload),
            "file_type": "png",
            "is_video": False,
        }

    staged_art_image_id = upload_result(job, media)
    if not staged_art_image_id:
        raise RuntimeError("upload returned no ArtImage id")

    completed_job = complete_job(
        job_id, True, art_image_id=staged_art_image_id
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

    log(f"agent {AGENT_ID} polling {KR_BASE_URL} every {POLL_SECONDS}s")
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
