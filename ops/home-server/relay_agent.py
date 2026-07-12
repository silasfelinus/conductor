#!/usr/bin/env python3
"""
relay_agent.py — pull-based art job relay for the kind_robots ArtJob queue.

Runs ON the home server (pm2-managed, alongside comfyui/sd-webui). Loop:

  1. POST {KR}/api/art/queue/claim          -> claim the next runnable job
  2. drive the local engine                 -> ComfyUI (:8188) or A1111 (:7860)
  3. POST {KR}/api/art/save-generated       -> upload result, get ArtImage id
  4. POST {KR}/api/art/queue/{id}/complete  -> mark DONE (or report failure)

Pull model: only outbound HTTPS to kind_robots — nothing dials into the home
network, no tailscale required on the data path, jobs wait out downtime.
All policy (auth, routing, retries, priorities) lives in kind_robots; this
script is deliberately dumb. Stdlib only — no pip installs needed.

Requires kind_robots' ArtJob queue endpoints (art-generator-connect/t-010).

Environment:
  KR_RELAY_TOKEN     required — admin user apiKey (or beta admin token)
  KR_RELAY_USER_ID   required — the user id matching that token (save-generated
                     verifies the two agree)
  KR_BASE_URL        default https://kindrobots.org
  COMFY_URL          default http://127.0.0.1:8188
  SD_URL             default http://127.0.0.1:7860
  POLL_SECONDS       default 10 (idle wait between claim attempts)
  HEARTBEAT_SECONDS  default 60 (how often to report ComfyUI/SD up-down to
                     kind_robots' /api/server/heartbeat; 0 disables)
  GEN_TIMEOUT        default 600 (max seconds per generation)
  AGENT_ID           default hostname (shows up as ArtJob.claimedBy)
  KR_LOCAL_IMAGES_DIR  optional — local kind_robots checkout's public/images
                     folder (e.g. D:/code/kind_robots/public/images). When set,
                     each finished image is ALSO written there as
                     {collection}/{collection}-{artImageId}.webp so the file
                     lands in a folder collection (payload.collection picks
                     the folder, default "sdxl" — the model family, not the
                     "comfy" frontend). Commit/push to publish. Engines emit
                     PNG; the copy is re-encoded to WebP when Pillow is
                     installed (pip install Pillow), else it falls back to .png.

A1111 job payload: either raw txt2img keys (prompt, negative_prompt,
cfg_scale, sampler_name, ...) or KR-style keys (promptString, negativePrompt,
cfg, sampler) — both accepted, KR-style is translated.
COMFY job payload: {"workflow": <full ComfyUI API-format graph>} plus
optional "promptString" for the ArtImage record, and optional
"images": [{"name", "imageData"}] — input images (base64 or data URL)
uploaded to ComfyUI's input folder before the workflow runs, so LoadImage
nodes can reference them (image-to-image, e.g. Flux Kontext / Hair Studio).
An optional "save" block ({isPublic, isMature, designer}) is applied by
kind_robots' complete endpoint, not by this agent.
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

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_RELAY_TOKEN = os.environ.get("KR_RELAY_TOKEN", "").strip()
KR_RELAY_USER_ID = int(os.environ.get("KR_RELAY_USER_ID", "0") or 0)
KR_LOCAL_IMAGES_DIR = os.environ.get("KR_LOCAL_IMAGES_DIR", "").strip()
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
SD_URL = os.environ.get("SD_URL", "http://127.0.0.1:7860").rstrip("/")
POLL_SECONDS = float(os.environ.get("POLL_SECONDS", "10"))
GEN_TIMEOUT = float(os.environ.get("GEN_TIMEOUT", "600"))
AGENT_ID = os.environ.get("AGENT_ID", socket.gethostname())
# How often to report ComfyUI/SD up-down to kind_robots' /api/server/heartbeat
# (feeds the ArtJob dashboard uptime chart). 0 disables heartbeats.
HEARTBEAT_SECONDS = float(os.environ.get("HEARTBEAT_SECONDS", "60"))


def log(msg):
    # Local timestamp so `pm2 logs` shows at a glance whether a line is recent.
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[relay {ts}] {msg}", flush=True)


def http_json(method, url, body=None, bearer=None, timeout=60):
    """JSON request/response via stdlib. Returns (status, parsed_json_or_None)."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if bearer:
        req.add_header("Authorization", f"Bearer {bearer}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return e.code, payload
    # URLError / timeout propagate to the caller's handler


def check_engine(base_url, health_path):
    """Ping a local engine's health endpoint. Returns (ok, latency_ms)."""
    url = f"{base_url}{health_path}"
    started = time.time()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            ok = 200 <= resp.status < 300
            resp.read(1)  # drain a byte; we don't need the body
    except Exception:  # noqa: BLE001 — any failure means "down"
        return False, None
    return ok, int((time.time() - started) * 1000)


def post_heartbeat(engine, ok, latency_ms):
    """Report one engine's up/down to kind_robots (best-effort)."""
    try:
        http_json(
            "POST",
            f"{KR_BASE_URL}/api/server/heartbeat",
            {"engine": engine, "ok": ok, "latencyMs": latency_ms},
            bearer=KR_RELAY_TOKEN,
            timeout=15,
        )
    except Exception as e:  # noqa: BLE001 — heartbeats must never crash the loop
        log(f"heartbeat({engine}) failed to post: {e}")


def send_heartbeats():
    """Check ComfyUI (:8188) and A1111/SD (:7860) and report both. ComfyUI's
    /system_stats and A1111's /sdapi/v1/progress are cheap liveness probes."""
    comfy_ok, comfy_ms = check_engine(COMFY_URL, "/system_stats")
    post_heartbeat("COMFY", comfy_ok, comfy_ms)
    sd_ok, sd_ms = check_engine(SD_URL, "/sdapi/v1/progress")
    post_heartbeat("A1111", sd_ok, sd_ms)


def claim_job():
    # supportsInputImages: capability handshake — kind_robots only hands out
    # jobs with payload images (Hair Studio kontext) to agents that declare
    # support, so a stale agent leaves them waiting instead of failing them.
    status, resp = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/queue/claim",
        {"agentId": AGENT_ID, "supportsInputImages": True},
        bearer=KR_RELAY_TOKEN,
    )
    if status == 404:
        detail = ""
        if isinstance(resp, dict):
            detail = str(resp.get("message") or resp.get("error") or "")[:200]
        log(f"claim got 404 — body: {detail or '(non-JSON body)'} — waiting")
        return None
    if status != 200 or not resp or not resp.get("success"):
        log(f"claim failed: HTTP {status} {resp and resp.get('message')}")
        return None
    return (resp.get("data") or {}).get("job")


def run_a1111(payload):
    """Drive local A1111 txt2img. Returns base64 image."""
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
    status, resp = http_json(
        "POST", f"{SD_URL}/sdapi/v1/txt2img", body, timeout=GEN_TIMEOUT
    )
    if status != 200 or not resp or not resp.get("images"):
        raise RuntimeError(f"A1111 returned HTTP {status}, no images")
    return resp["images"][0]


def decode_image_entry(entry):
    """Validate one payload images entry and return (name, raw_bytes).
    imageData may be a raw base64 string or a data URL."""
    name = (entry or {}).get("name")
    data = (entry or {}).get("imageData") or ""
    if not name or not data:
        raise ValueError('each images entry needs "name" and "imageData"')
    if data.lstrip().lower().startswith("data:") and "," in data:
        data = data.split(",", 1)[1]
    return name, base64.b64decode(data)


def build_image_upload_request(name, raw, boundary):
    """Build (body_bytes, content_type) for ComfyUI's /upload/image endpoint:
    multipart form with the file as "image", type=input, overwrite=true."""
    ext = os.path.splitext(name)[1].lstrip(".").lower() or "png"
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
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
    """Upload payload["images"] entries ({name, imageData}) to ComfyUI's input
    folder so LoadImage nodes can reference them by name. Image-to-image
    workflows (e.g. Flux Kontext from kind_robots' /api/comfy/kontext/enqueue)
    depend on this."""
    images = payload.get("images") or []
    if not isinstance(images, list):
        raise ValueError('COMFY payload "images" must be a list')
    for entry in images:
        name, raw = decode_image_entry(entry)
        boundary = "krrelay" + base64.b16encode(os.urandom(12)).decode().lower()
        body, content_type = build_image_upload_request(name, raw, boundary)

        req = urllib.request.Request(
            f"{COMFY_URL}/upload/image", data=body, method="POST"
        )
        req.add_header("Content-Type", content_type)
        with urllib.request.urlopen(req, timeout=120) as resp:
            uploaded = json.loads(resp.read().decode() or "null")
        if not uploaded or not uploaded.get("name"):
            raise RuntimeError(f"ComfyUI input upload failed for {name}")
        log(f"uploaded input image {uploaded['name']}")


def run_comfy(payload):
    """Submit a ComfyUI workflow, poll history, download the first output image."""
    workflow = payload.get("workflow")
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError('COMFY payload needs a "workflow" object (API format)')

    upload_comfy_input_images(payload)

    status, resp = http_json(
        "POST", f"{COMFY_URL}/prompt", {"prompt": workflow, "client_id": AGENT_ID}
    )
    if status != 200 or not resp or not resp.get("prompt_id"):
        raise RuntimeError(
            f"ComfyUI /prompt returned HTTP {status}: {resp and resp.get('node_errors')}"
        )
    prompt_id = resp["prompt_id"]

    deadline = time.time() + GEN_TIMEOUT
    while time.time() < deadline:
        time.sleep(2)
        status, hist = http_json("GET", f"{COMFY_URL}/history/{prompt_id}")
        if status != 200 or not hist:
            continue
        entry = hist.get(prompt_id)
        if not entry:
            continue
        for node_output in (entry.get("outputs") or {}).values():
            for image in node_output.get("images") or []:
                if not image.get("filename"):
                    continue
                from urllib.parse import urlencode

                query = urlencode(
                    {
                        "filename": image["filename"],
                        "subfolder": image.get("subfolder", ""),
                        "type": image.get("type", "output"),
                    }
                )
                req = urllib.request.Request(f"{COMFY_URL}/view?{query}")
                with urllib.request.urlopen(req, timeout=120) as img_resp:
                    return base64.b64encode(img_resp.read()).decode()
        comfy_status = (entry.get("status") or {}).get("status_str")
        if comfy_status == "error":
            raise RuntimeError("ComfyUI reported a workflow error")
    raise RuntimeError(f"ComfyUI job timed out after {GEN_TIMEOUT}s")


def upload_result(job, image_b64):
    payload = job.get("payload") or {}
    body = {
        "imageBase64": image_b64,
        "promptString": payload.get("promptString")
        or payload.get("prompt")
        or f"art job {job['id']}",
        "negativePrompt": payload.get("negativePrompt")
        or payload.get("negative_prompt"),
        "steps": payload.get("steps"),
        "seed": payload.get("seed"),
        "designer": f"relay:{AGENT_ID}",
        "userId": KR_RELAY_USER_ID,
    }
    status, resp = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/save-generated",
        body,
        bearer=KR_RELAY_TOKEN,
        timeout=180,
    )
    if status != 201 or not resp or not resp.get("success"):
        raise RuntimeError(
            f"save-generated failed: HTTP {status} {resp and resp.get('message')}"
        )
    return (resp.get("data") or {}).get("id")


def encode_webp(raw):
    """Re-encode raw image bytes (engines emit PNG) to WebP. Returns
    (bytes, ext). Uses Pillow when available; if Pillow isn't installed or the
    decode fails, falls back to the original bytes as .png so the relay still
    works stdlib-only. WebP keeps the site's images small and consistent."""
    try:
        from PIL import Image  # optional dependency

        with Image.open(io.BytesIO(raw)) as im:
            buf = io.BytesIO()
            # method=6 = best compression; quality 90 is visually lossless-ish.
            im.save(buf, format="WEBP", quality=90, method=6)
            return buf.getvalue(), "webp"
    except Exception as e:  # noqa: BLE001 — Pillow missing or undecodable
        log(f"webp encode skipped ({e}); keeping png")
        return raw, "png"


def write_local_copy(job, art_image_id, image_b64):
    """Local fast path: engines, kind_robots, and conductor share a drive, so
    drop the finished file straight into the local checkout's folder
    collection (a folder IS a collection). Re-encoded to WebP (see encode_webp)
    so we stop minting new PNGs. No-op unless KR_LOCAL_IMAGES_DIR is set.
    Failures here never fail the job - the DB record is the source of truth;
    this is a convenience copy awaiting commit."""
    if not KR_LOCAL_IMAGES_DIR:
        return
    try:
        payload = job.get("payload") or {}
        collection = str(payload.get("collection") or "sdxl").strip().lower()
        if not collection.replace("-", "").replace("_", "").isalnum():
            collection = "sdxl"
        # Normalize to forward slashes throughout. os.path.join on Windows
        # emits backslashes, which mixed with a forward-slash KR_LOCAL_IMAGES_DIR
        # produced ugly "D:/code/kind_robots/public/images\comfy\comfy-1.png".
        # Forward slashes are valid on Windows too, so keep one style everywhere.
        base = KR_LOCAL_IMAGES_DIR.replace("\\", "/").rstrip("/")
        folder = f"{base}/{collection}"
        os.makedirs(folder, exist_ok=True)
        data, ext = encode_webp(base64.b64decode(image_b64))
        file_path = f"{folder}/{collection}-{art_image_id}.{ext}"
        with open(file_path, "wb") as f:
            f.write(data)
        log(f"local copy: {file_path}")
    except Exception as e:  # noqa: BLE001
        log(f"local copy failed (job still DONE): {e}")


def complete_job(job_id, success, art_image_id=None, error=None):
    body = {"success": success}
    if art_image_id:
        body["artImageId"] = art_image_id
    if error:
        body["error"] = str(error)[:4000]
    status, resp = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/queue/{job_id}/complete",
        body,
        bearer=KR_RELAY_TOKEN,
    )
    if status != 200:
        log(f"complete({job_id}) failed: HTTP {status} {resp and resp.get('message')}")


def process(job):
    job_id = job["id"]
    engine = (job.get("engine") or "A1111").upper()
    payload = job.get("payload") or {}
    if isinstance(payload, str):
        payload = json.loads(payload)
    log(f"job {job_id}: {engine} attempt {job.get('attempts')}")

    image_b64 = run_comfy(payload) if engine == "COMFY" else run_a1111(payload)
    art_image_id = upload_result(job, image_b64)
    if not art_image_id:
        raise RuntimeError("upload returned no ArtImage id")
    complete_job(job_id, True, art_image_id=art_image_id)
    write_local_copy(job, art_image_id, image_b64)
    log(f"job {job_id}: DONE (ArtImage {art_image_id})")


def main():
    if not KR_RELAY_TOKEN or not KR_RELAY_USER_ID:
        log("KR_RELAY_TOKEN and KR_RELAY_USER_ID are required — exiting")
        sys.exit(1)

    log(f"agent {AGENT_ID} polling {KR_BASE_URL} every {POLL_SECONDS}s")
    last_heartbeat = 0.0
    while True:
        job = None
        try:
            # Report engine health on its own cadence (independent of the claim
            # loop) so the dashboard sees ComfyUI/SD up/down even when idle.
            if HEARTBEAT_SECONDS > 0 and time.time() - last_heartbeat >= HEARTBEAT_SECONDS:
                send_heartbeats()
                last_heartbeat = time.time()

            job = claim_job()
            if job:
                process(job)
                continue  # drain the queue before idling
        except KeyboardInterrupt:
            raise
        except Exception as e:  # noqa: BLE001 — relay must survive anything
            log(f"error: {e}")
            if job:
                try:
                    complete_job(job["id"], False, error=e)
                except Exception as report_error:  # noqa: BLE001
                    log(f"could not report failure: {report_error}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
