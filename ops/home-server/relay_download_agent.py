"""kr-download — pull-based model download agent for Kind Robots.

The companion to relay_agent.py. Where the relay claims ArtJobs and generates
media, this agent claims model *downloads* (file-backed Resources a user queued
from the Discover browser) and fetches the files onto the home server's engine
directories.

Pull model, same as the relay: the kind_robots server never dials the home
network. This agent polls /api/lora/download/claim, downloads the binary,
catalogs it as a Resource, and reports the outcome to
/api/lora/download/{id}/complete.

Flow per claimed row:
  1. resolve a download URL (explicit downloadUrl, or Civitai by version id)
  2. stage LoRA/LyCORIS/checkpoint files beside their canonical model root
  3. stream the file to disk (atomic .part -> rename), hashing as we go
  4. run the same scanner/importer as watched-folder drops, so Civitai metadata,
     canonical local placement, LoRA category classification, Resource upsert,
     and generated preview ArtJob behavior cannot drift between ingress paths
  5. POST .../complete with the canonical Resource id

Other file-backed resource types retain their direct category-root catalog path.

Reuses relay_agent's log() / http_json() / auth token so the two agents share
one convention. Auth is Authorization: Bearer <KR_RELAY_TOKEN>, which the lora
download + resource endpoints accept (x-api-key OR bearer).

Run via pm2 as the `kr-download` app (see ecosystem.config.js). Env:
  KR_BASE_URL, KR_RELAY_TOKEN            (shared with the relay)
  KR_MODEL_ROOT       default Z:/ai/models (base for all model categories)
  KR_LORA_DIR         optional override for the LoRA/LyCORIS directory
  KR_CHECKPOINT_DIR   optional override for the checkpoint directory
  KR_DOWNLOAD_POLL_SECONDS  default 30
  KR_CIVITAI_TOKEN    optional; appended as ?token= for Civitai downloads
"""

import hashlib
import os
import re
import shutil
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import lora_import_agent as model_import
import relay_agent as relay

MODEL_ROOT = os.environ.get("KR_MODEL_ROOT", "Z:/ai/models").strip()
LORA_DIR = os.environ.get("KR_LORA_DIR", os.path.join(MODEL_ROOT, "Lora")).strip()
CHECKPOINT_DIR = os.environ.get(
    "KR_CHECKPOINT_DIR", os.path.join(MODEL_ROOT, "checkpoints")
).strip()

RESOURCE_DIRS = {
    "CHECKPOINT": CHECKPOINT_DIR,
    "EMBEDDING": os.path.join(MODEL_ROOT, "embeddings"),
    "LORA": LORA_DIR,
    "LYCORIS": LORA_DIR,
    "HYPERNETWORK": os.path.join(MODEL_ROOT, "hypernetworks"),
    "CONTROLNET": os.path.join(MODEL_ROOT, "controlnet"),
    "VAE": os.path.join(MODEL_ROOT, "vae"),
    "TEXT_ENCODER": os.path.join(MODEL_ROOT, "text_encoders"),
    "DIFFUSION_MODEL": os.path.join(MODEL_ROOT, "diffusion_models"),
    "LATENT_UPSCALER": os.path.join(MODEL_ROOT, "latent_upscale_models"),
    "UPSCALER": os.path.join(MODEL_ROOT, "upscale_models"),
}
POLL_SECONDS = float(os.environ.get("KR_DOWNLOAD_POLL_SECONDS", "30"))
CIVITAI_TOKEN = os.environ.get("KR_CIVITAI_TOKEN", "").strip()
DOWNLOAD_TIMEOUT = float(os.environ.get("KR_DOWNLOAD_TIMEOUT", "1800"))
AGENT_ID = os.environ.get("AGENT_ID", socket.gethostname())
USER_AGENT = "kr-download/1.0 (+https://github.com/silasfelinus/kind_robots)"

# Extensions a model file is expected to carry; anything else keeps its own.
MODEL_EXTENSIONS = (".safetensors", ".ckpt", ".pt", ".pth", ".bin", ".gguf")
SCANNER_RESOURCE_TYPES = {"LORA", "LYCORIS", "CHECKPOINT"}


def target_dir(resource_type):
    """Return the canonical ComfyUI directory for one file-backed Resource."""
    key = str(resource_type or "LORA").upper()
    directory = RESOURCE_DIRS.get(key)
    if not directory:
        raise ValueError(
            f"resourceType {key!r} is not a downloadable model-file type"
        )
    return directory


def scanner_staging_dir(request_id, resource_type):
    """Per-request inbox whose parent preserves scanner classification context."""
    key = str(resource_type or "LORA").upper()
    if key in {"LORA", "LYCORIS"}:
        return os.path.join(LORA_DIR, f".download-import-{int(request_id)}")
    if key == "CHECKPOINT":
        # scan_models includes root.parent.name in classification_path, so a
        # child of checkpoints still reads as a checkpoint even before Civitai
        # enrichment succeeds.
        return os.path.join(CHECKPOINT_DIR, f".download-import-{int(request_id)}")
    return target_dir(key)


def scanner_work_dir(request_id):
    return os.path.join(MODEL_ROOT, ".download-import-work", str(int(request_id)))


def resource_id_from_import(result, request, file_hash):
    resources = list((result or {}).get("resources") or [])
    if not resources:
        return None

    version_id = request.get("civitaiModelVersionId")
    if version_id:
        for resource in resources:
            if resource.get("civitaiModelVersionId") == version_id:
                return resource.get("id")

    for resource in resources:
        if resource.get("hash") == file_hash:
            return resource.get("id")

    return resources[0].get("id")


def catalog_with_scanner(request, staging_dir, file_hash):
    """Canonical ingest path for LoRA/LyCORIS/checkpoint DownloadRequests."""
    request_id = int(request["id"])
    resource_type = str(request.get("resourceType") or "LORA").upper()
    work_dir = scanner_work_dir(request_id)
    if resource_type in {"LORA", "LYCORIS"}:
        result = model_import.process_lora_folder(staging_dir, work_dir)
    elif resource_type == "CHECKPOINT":
        result = model_import.process_model_folder(staging_dir, work_dir)
    else:
        raise ValueError(f"no canonical scanner for {resource_type}")

    if not result:
        raise RuntimeError(f"{resource_type} scanner/importer did not return a result")

    resource_id = resource_id_from_import(result, request, file_hash)
    if not resource_id:
        raise RuntimeError(
            f"{resource_type} scanner/importer completed without a Resource id"
        )
    return int(resource_id), work_dir


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


def catalog_resource(request, engine_path, filename, file_hash):
    """Create the Resource row for the downloaded file. Returns resourceId, or
    None if the name already exists (409) — the file is still on disk, so that's
    a benign 'already cataloged' outcome, not a failure."""
    model_id = request.get("civitaiModelId")
    name = (request.get("label") or "").strip() or os.path.splitext(filename)[0]
    body = {
        "name": name,
        # Resource.localPath is an engine-facing name, not an absolute SMB path.
        # Files downloaded into a category root therefore resolve by filename.
        "localPath": engine_path,
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
    resource_type = str(request.get("resourceType") or "LORA").upper()
    url = resolve_download_url(request)
    if not url:
        raise RuntimeError("no downloadUrl and no civitaiModelVersionId to fetch")

    use_scanner = resource_type in SCANNER_RESOURCE_TYPES
    dest_dir = (
        scanner_staging_dir(request_id, resource_type)
        if use_scanner
        else target_dir(resource_type)
    )
    relay.log(
        f"download {request_id}: {resource_type} <- {url} into "
        f"{dest_dir}{' (scanner staging)' if use_scanner else ''}"
    )

    final_path, filename, size, file_hash = download_binary(request, url, dest_dir)
    relay.log(
        f"download {request_id}: saved {filename} "
        f"({size / 1_048_576:.1f} MiB, sha256 {file_hash[:12]}…)"
    )

    work_dir = None
    if use_scanner:
        resource_id, work_dir = catalog_with_scanner(
            request, dest_dir, file_hash
        )
    else:
        resource_id = catalog_resource(request, filename, filename, file_hash)

    complete_download(request_id, True, resource_id=resource_id)
    relay.log(f"download {request_id}: DONE (Resource {resource_id})")

    # These are request-scoped scratch paths only. Keep failed staging intact
    # for inspection/retry, but clean successful scratch once the completion
    # API has acknowledged the canonical Resource id.
    if use_scanner:
        try:
            os.rmdir(dest_dir)
        except OSError:
            pass
        if work_dir:
            shutil.rmtree(work_dir, ignore_errors=True)


def main():
    if not relay.KR_RELAY_TOKEN:
        relay.log("KR_RELAY_TOKEN is required - exiting")
        sys.exit(1)

    relay.log(
        f"download agent {AGENT_ID} polling {relay.KR_BASE_URL} every "
        f"{POLL_SECONDS}s (model_root={MODEL_ROOT})"
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
