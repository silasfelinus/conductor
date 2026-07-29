"""kr-download — pull-based model download agent for Kind Robots.

The companion to relay_agent.py. Where the relay claims ArtJobs and generates
media, this agent claims model *downloads* (LoRAs and checkpoints a user queued
from the Discover browser) and fetches the files onto the home server's engine
directories.

Pull model, same as the relay: the kind_robots server never dials the home
network. This agent polls /api/lora/download/claim, downloads the binary,
catalogs it as a Resource, and reports the outcome to
/api/lora/download/{id}/complete.

Flow per claimed row:
  1. resolve a download URL (explicit downloadUrl, or Civitai by version id)
  2. pick the target dir from resourceType (LORA -> loras, CHECKPOINT -> ckpts)
  3. stream the file to disk (atomic .part -> rename), hashing as we go
  4. POST /api/resources to catalog it, capturing the new resourceId
  5. POST .../complete with {success, resourceId} (or {success:false, error})

Reuses relay_agent's log() / http_json() / auth token so the two agents share
one convention. Auth is Authorization: Bearer <KR_RELAY_TOKEN>, which the lora
download + resource endpoints accept (x-api-key OR bearer).

Run via pm2 as the `kr-download` app (see ecosystem.config.js). Env:
  KR_BASE_URL, KR_RELAY_TOKEN            (shared with the relay)
  KR_LORA_DIR         default Z:/ai/models/Lora
  KR_CHECKPOINT_DIR   default Z:/ai/models/Stable-diffusion
  KR_DOWNLOAD_POLL_SECONDS  default 30
  KR_CIVITAI_TOKEN    optional; appended as ?token= for Civitai downloads
"""

import hashlib
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import relay_agent as relay

LORA_DIR = os.environ.get("KR_LORA_DIR", "Z:/ai/models/Lora").strip()
CHECKPOINT_DIR = os.environ.get(
    "KR_CHECKPOINT_DIR", "Z:/ai/models/Stable-diffusion"
).strip()
POLL_SECONDS = float(os.environ.get("KR_DOWNLOAD_POLL_SECONDS", "30"))
CIVITAI_TOKEN = os.environ.get("KR_CIVITAI_TOKEN", "").strip()
DOWNLOAD_TIMEOUT = float(os.environ.get("KR_DOWNLOAD_TIMEOUT", "1800"))
AGENT_ID = os.environ.get("AGENT_ID", socket.gethostname())
USER_AGENT = "kr-download/1.0 (+https://github.com/silasfelinus/kind_robots)"

# Extensions a model file is expected to carry; anything else keeps its own.
MODEL_EXTENSIONS = (".safetensors", ".ckpt", ".pt", ".pth", ".bin", ".gguf")


def target_dir(resource_type):
    """Engine directory for a resource type. Checkpoints load from the
    Stable-diffusion dir; everything else (LoRA/LyCORIS/etc.) from the loras dir."""
    if str(resource_type or "").upper() == "CHECKPOINT":
        return CHECKPOINT_DIR
    return LORA_DIR


def claim_download():
    status, response = relay.http_json(
        "POST",
        f"{relay.KR_BASE_URL}/api/lora/download/claim",
        {"agentId": AGENT_ID},
        bearer=relay.KR_RELAY_TOKEN,
    )
    if status == 200:
        return (response or {}).get("data", {}).get("request")
    detail = response and response.get("message")
    relay.log(f"claim failed: HTTP {status} {detail or '(no body)'}")
    return None


def resolve_download_url(request):
    """Explicit downloadUrl wins; otherwise build the Civitai by-version URL."""
    explicit = (request.get("downloadUrl") or "").strip()
    if explicit:
        return explicit
    version_id = request.get("civitaiModelVersionId")
    if version_id:
        return f"https://civitai.com/api/download/models/{int(version_id)}"
    return None


def with_civitai_token(url):
    """Civitai gates many downloads behind an API token; append it when set and
    the URL is a Civitai one (never leak the token to arbitrary hosts)."""
    if not CIVITAI_TOKEN or "civitai.com" not in url:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}token={CIVITAI_TOKEN}"


def filename_from_disposition(header):
    if not header:
        return None
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^\";]+)"?', header)
    return match.group(1).strip() if match else None


def safe_filename(name):
    """Strip path separators / dodgy chars so a claimed row can't write outside
    the target dir. Keeps the basename only."""
    base = os.path.basename(str(name or "").replace("\\", "/"))
    cleaned = re.sub(r'[<>:"|?*\x00-\x1f]', "", base).strip()
    return cleaned


def pick_filename(request, url, disposition):
    for candidate in (
        request.get("fileName"),
        filename_from_disposition(disposition),
        url.split("?")[0].rstrip("/").split("/")[-1],
    ):
        cleaned = safe_filename(candidate)
        if cleaned and cleaned.lower().endswith(MODEL_EXTENSIONS):
            return cleaned
    # Last resort: name by request id, default to safetensors.
    return f"download-{request.get('id')}.safetensors"


def download_binary(request, url, dest_dir):
    """Stream `url` into dest_dir. Returns (final_path, filename, size, sha256).
    Writes to a .part temp then atomically renames, so a crash never leaves a
    half file an engine might try to load. The filename is decided once here,
    using the request, the resolved URL, and the response's Content-Disposition."""
    Path(dest_dir).mkdir(parents=True, exist_ok=True)

    fetch_url = with_civitai_token(url)
    http_request = urllib.request.Request(
        fetch_url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"}
    )

    sha = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(http_request, timeout=DOWNLOAD_TIMEOUT) as response:
        # Civitai answers an un-authed gated download with an HTML login page and
        # a 200 — guard against silently saving that as a "model".
        content_type = (response.headers.get("Content-Type") or "").lower()
        if "text/html" in content_type:
            raise RuntimeError(
                "download returned an HTML page (login/gated?) - check KR_CIVITAI_TOKEN"
            )

        filename = pick_filename(
            request,
            response.geturl(),
            response.headers.get("Content-Disposition"),
        )
        final_path = os.path.join(dest_dir, filename)
        part_path = f"{final_path}.part"

        with open(part_path, "wb") as handle:
            while True:
                chunk = response.read(1024 * 256)
                if not chunk:
                    break
                handle.write(chunk)
                sha.update(chunk)
                size += len(chunk)

    os.replace(part_path, final_path)
    return final_path, filename, size, sha.hexdigest()


def catalog_resource(request, local_path, filename, file_hash):
    """Create the Resource row for the downloaded file. Returns resourceId, or
    None if the name already exists (409) — the file is still on disk, so that's
    a benign 'already cataloged' outcome, not a failure."""
    model_id = request.get("civitaiModelId")
    name = (request.get("label") or "").strip() or os.path.splitext(filename)[0]
    body = {
        "name": name,
        "localPath": local_path,
        "resourceType": request.get("resourceType") or "LORA",
        "isMature": bool(request.get("isMature")),
        "hash": file_hash,
        "civitaiModelId": model_id,
        "civitaiModelVersionId": request.get("civitaiModelVersionId"),
    }
    if model_id:
        body["civitaiUrl"] = f"https://civitai.com/models/{int(model_id)}"

    status, response = relay.http_json(
        "POST",
        f"{relay.KR_BASE_URL}/api/resources",
        body,
        bearer=relay.KR_RELAY_TOKEN,
    )
    if status in (200, 201):
        return (response or {}).get("data", {}).get("id")
    if status == 409:
        relay.log(f"resource '{name}' already cataloged - marking done anyway")
        return None
    detail = response and response.get("message")
    raise RuntimeError(f"catalog failed: HTTP {status} {detail or '(no body)'}")


def complete_download(request_id, success, resource_id=None, error=None):
    body = {"success": bool(success)}
    if resource_id is not None:
        body["resourceId"] = resource_id
    if error is not None:
        body["error"] = str(error)[:4000]
    status, response = relay.http_json(
        "POST",
        f"{relay.KR_BASE_URL}/api/lora/download/{int(request_id)}/complete",
        body,
        bearer=relay.KR_RELAY_TOKEN,
    )
    if status != 200:
        detail = response and response.get("message")
        relay.log(f"complete report failed: HTTP {status} {detail or '(no body)'}")


def process_download(request):
    request_id = request.get("id")
    resource_type = request.get("resourceType") or "LORA"
    url = resolve_download_url(request)
    if not url:
        raise RuntimeError("no downloadUrl and no civitaiModelVersionId to fetch")

    dest_dir = target_dir(resource_type)
    relay.log(
        f"download {request_id}: {resource_type} <- {url} into {dest_dir}"
    )

    final_path, filename, size, file_hash = download_binary(request, url, dest_dir)
    relay.log(
        f"download {request_id}: saved {filename} "
        f"({size / 1_048_576:.1f} MiB, sha256 {file_hash[:12]}…)"
    )

    resource_id = catalog_resource(request, final_path, filename, file_hash)
    complete_download(request_id, True, resource_id=resource_id)
    relay.log(
        f"download {request_id}: DONE (Resource {resource_id or 'existing'})"
    )


def main():
    if not relay.KR_RELAY_TOKEN:
        relay.log("KR_RELAY_TOKEN is required - exiting")
        sys.exit(1)

    relay.log(
        f"download agent {AGENT_ID} polling {relay.KR_BASE_URL} every "
        f"{POLL_SECONDS}s (loras={LORA_DIR}, checkpoints={CHECKPOINT_DIR})"
    )

    while True:
        request = None
        try:
            request = claim_download()
            if request:
                process_download(request)
                continue
        except KeyboardInterrupt:
            raise
        except Exception as error:  # noqa: BLE001 - agent must survive failures
            relay.log(f"error: {error}")
            if request:
                try:
                    complete_download(request["id"], False, error=error)
                except Exception as report_error:  # noqa: BLE001
                    relay.log(f"could not report failure: {report_error}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
