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
  GEN_TIMEOUT        default 600 (max seconds per generation)
  AGENT_ID           default hostname (shows up as ArtJob.claimedBy)

A1111 job payload: either raw txt2img keys (prompt, negative_prompt,
cfg_scale, sampler_name, ...) or KR-style keys (promptString, negativePrompt,
cfg, sampler) — both accepted, KR-style is translated.
COMFY job payload: {"workflow": <full ComfyUI API-format graph>} plus
optional "promptString" for the ArtImage record.
"""

import base64
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
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
SD_URL = os.environ.get("SD_URL", "http://127.0.0.1:7860").rstrip("/")
POLL_SECONDS = float(os.environ.get("POLL_SECONDS", "10"))
GEN_TIMEOUT = float(os.environ.get("GEN_TIMEOUT", "600"))
AGENT_ID = os.environ.get("AGENT_ID", socket.gethostname())


def log(msg):
    print(f"[relay] {msg}", flush=True)


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


def claim_job():
    status, resp = http_json(
        "POST",
        f"{KR_BASE_URL}/api/art/queue/claim",
        {"agentId": AGENT_ID},
        bearer=KR_RELAY_TOKEN,
    )
    if status == 404:
        log("queue endpoints not deployed yet (404) — waiting")
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


def run_comfy(payload):
    """Submit a ComfyUI workflow, poll history, download the first output image."""
    workflow = payload.get("workflow")
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError('COMFY payload needs a "workflow" object (API format)')

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
    log(f"job {job_id}: DONE (ArtImage {art_image_id})")


def main():
    if not KR_RELAY_TOKEN or not KR_RELAY_USER_ID:
        log("KR_RELAY_TOKEN and KR_RELAY_USER_ID are required — exiting")
        sys.exit(1)

    log(f"agent {AGENT_ID} polling {KR_BASE_URL} every {POLL_SECONDS}s")
    while True:
        job = None
        try:
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
