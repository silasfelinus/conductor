#!/usr/bin/env python3
"""Media-aware wrapper for the proven Kind Robots ArtJob relay.

Kind Robots-targeted jobs that carry both:

- targetRepo: silasfelinus/kind_robots
- imagePath: public/images/<path>

are written beneath KR_MEDIA_IMAGES_DIR before the ArtJob is marked
successful. There is ONE media root: everything Kind Robots serves lives under
``images/``, and ``rewards/`` is a folder inside it -- ``/images/rewards/...``
is what the media origin actually serves and what 227 of 261 live Rewards
store. Historical ``images/...``, ``rewards/...`` and ``public/rewards/...``
spellings are folded to that canonical root before validation, matching
kind_robots' own server/utils/artJobNormalization.ts. If the filesystem write or
manifest update fails, the job is reported FAILED and remains retryable
instead of silently completing with a missing public file.

All other jobs use relay_agent.py unchanged, except that Comfy prompt submission
uses a longer timeout, can recover a prompt id from /queue when Comfy accepted
the prompt but its HTTP response arrived too late, and preserves the exact
prompt/output/image provenance required by Kind Robots completion verification.
"""

import base64
import io
import json
import os
import threading
import time
import urllib.parse
from pathlib import Path, PurePosixPath

import relay_agent as relay
import lora_import_agent as lora

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
MEDIA_ROOT_VALUE = (
    os.environ.get("KR_MEDIA_IMAGES_DIR", "").strip()
    or os.environ.get("KR_LOCAL_IMAGES_DIR", "").strip()
)
MEDIA_ROOT_ENV_HINT = "KR_MEDIA_IMAGES_DIR (or KR_LOCAL_IMAGES_DIR)"
IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg"}
GENERATED_IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv", ".webp"}
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


def normalize_kindrobots_image_path(value):
    """Normalize historical frontend/media paths to their canonical ``public/...`` root.

    Jobs created before the direct-media contract used several equivalent forms:
    ``/images/...``, ``images/...``, ``/public/images/...``, Windows separators,
    full media URLs, and the legacy ``rewards/...``/``public/rewards/...``
    spellings. The relay accepts those only long enough to canonicalize them to
    ``public/images/...``. Unrelated paths remain unchanged and fail the safety
    validation below.
    """

    image_path = str(value or "").strip().replace("\\", "/")
    if not image_path:
        return ""

    raw_path = image_path.split("?", 1)[0].split("#", 1)[0]
    if ".." in raw_path.split("/"):
        raise ValueError(f"Unsafe media imagePath: {image_path}")

    parsed = urllib.parse.urlparse(image_path)
    if parsed.scheme in ("http", "https") or parsed.netloc:
        image_path = urllib.parse.unquote(parsed.path or "")
    else:
        image_path = raw_path

    while image_path.startswith("./"):
        image_path = image_path[2:]
    image_path = image_path.lstrip("/")

    if image_path.startswith("public/images/"):
        return image_path
    if image_path.startswith("images/"):
        return f"public/{image_path}"
    # Legacy reward spellings fold UNDER the images root -- `rewards/` is a
    # folder inside it, not a sibling of it. This mirrors kind_robots'
    # server/utils/artJobNormalization.ts:normalizeKindRobotsImagePath, which
    # has applied exactly this rule since art-job ingestion was written.
    if image_path.startswith("public/rewards/"):
        return f"public/images/{image_path[len('public/'):]}"
    if image_path.startswith("rewards/"):
        return f"public/images/{image_path}"
    return image_path


def direct_media_target(job):
    payload = job_payload(job)
    target_repo = str(payload.get("targetRepo") or "").strip()
    image_path = normalize_kindrobots_image_path(payload.get("imagePath"))

    if target_repo != KIND_ROBOTS_REPO or not image_path:
        return None

    logical = PurePosixPath(image_path)
    parts = logical.parts
    if len(parts) < 3 or parts[0] != "public" or parts[1] != "images":
        raise ValueError(
            "Kind Robots media job imagePath must begin with public/images/"
        )

    relative_parts = parts[2:]
    if any(part in ("", ".", "..") for part in relative_parts):
        raise ValueError(f"Unsafe media imagePath: {image_path}")

    return Path(*relative_parts)


def direct_media_relative(job):
    return direct_media_target(job)


def media_root():
    value = MEDIA_ROOT_VALUE
    if not value:
        raise RuntimeError(
            f"{MEDIA_ROOT_ENV_HINT} is required for direct Kind Robots media jobs"
        )
    root = Path(value).expanduser().resolve()
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

    index[folder.name] = folder_relative
    atomic_write_json(index_path, index)


def write_direct_media(job, media):
    target = direct_media_target(job)
    if target is None:
        return None

    relative = target
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

    # Resolve model/LoRA names against ComfyUI's live lists before POSTing,
    # exactly as relay_agent.run_comfy does. This wrapper reimplements
    # submission (longer timeout + /queue recovery) and, until 2026-08-13,
    # reimplemented it without this call -- so every job kr-relay runs went to
    # ComfyUI with whatever name the catalog happened to store, and the
    # resolver that exists to fix slash/case/prefix drift never ran on the only
    # path that actually executes. ArtJobs 8276/8278 died on
    # `lora_name: 'Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors' not in
    # (list of length 2231)` for a file sitting at exactly that path on the
    # share, which is the drift tests/test_relay_asset_resolution.py already
    # covers -- it was simply never invoked here.
    unresolved = relay.align_workflow_asset_names(workflow)
    if unresolved:
        raise relay.unresolved_asset_error(unresolved)

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
                f"{response and response.get('node_errors')} "
                f"{relay.last_resolution_note()}"
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
        result = relay.extract_comfy_output(
            entry.get("outputs") or {}, want_video, prompt_id=prompt_id
        )
        if result:
            return result
        comfy_status = (entry.get("status") or {}).get("status_str")
        if comfy_status == "error":
            detail = relay.describe_comfy_error(entry)
            message = "ComfyUI reported a workflow error"
            raise RuntimeError(f"{message}: {detail}" if detail else message)

    kind = "video" if want_video else "image"
    raise RuntimeError(
        f"ComfyUI {kind} job timed out after {relay.GEN_TIMEOUT}s"
    )


def process_with_media(job):
    target = direct_media_target(job)
    if target is None:
        return ORIGINAL_PROCESS(job)

    relative = target
    job_id = job["id"]
    engine = (job.get("engine") or "A1111").upper()
    payload = job_payload(job)
    payload["_relayClientId"] = f"{relay.AGENT_ID}-artjob-{job_id}"
    relay.log(f"job {job_id}: {engine} direct media -> {relative.as_posix()}")

    if engine == "COMFY":
        media = relay.run_comfy(payload)
        provenance = relay.completion_provenance(payload, media)
    else:
        media = {
            "data_b64": relay.run_a1111(payload),
            "file_type": "png",
            "is_video": False,
        }
        provenance = None

    staged_art_image_id = relay.upload_result(job, media)
    if not staged_art_image_id:
        raise RuntimeError("upload returned no ArtImage id")

    destination = write_direct_media(job, media)

    completed_job = relay.complete_job(
        job_id,
        True,
        art_image_id=staged_art_image_id,
        provenance=provenance,
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


def start_lora_watcher():
    """Start the LoRA auto-import watcher on a daemon thread inside this process.

    Folding it into kr-relay keeps deployment to a single pm2 app / token / log.
    A separate thread (not the relay's render loop) means a long import batch —
    a bulk drop can take minutes of hashing + Civitai lookups + moves — never
    stalls art-job claiming/rendering, and a watcher crash can't take the relay
    down. If the LoRA env isn't configured, we log why and skip it, so kr-relay
    still runs as a pure render relay."""
    missing = lora.missing_config()
    if missing:
        relay.log(f"lora-import watcher disabled (missing {', '.join(missing)})")
        return
    relay.log("lora-import watcher starting (embedded thread in kr-relay)")
    threading.Thread(target=lora.watch_loop, name="lora-import", daemon=True).start()


def log_media_roots():
    """Log the direct-media root and whether it is configured.

    There is exactly one. A job otherwise only discovers a missing root when a
    write actually fails, hours after the box was misconfigured, so this states
    it at startup alongside ``start_lora_watcher()``'s enabled/disabled line."""
    if MEDIA_ROOT_VALUE:
        relay.log(
            f"media root configured ({MEDIA_ROOT_ENV_HINT} = {MEDIA_ROOT_VALUE})"
        )
    else:
        relay.log(f"media root not configured (missing {MEDIA_ROOT_ENV_HINT})")


if __name__ == "__main__":
    log_media_roots()
    start_lora_watcher()
    relay.main()
