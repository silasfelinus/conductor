#!/usr/bin/env python3
"""Media-aware wrapper for the proven Kind Robots ArtJob relay.

Kind Robots-targeted jobs that carry both:

- targetRepo: silasfelinus/kind_robots
- imagePath: public/images/<path> or public/rewards/<path>

are written beneath KR_MEDIA_IMAGES_DIR (images) or KR_MEDIA_REWARDS_DIR
(rewards) before the ArtJob is marked successful. ``public/rewards/...`` is a
real top-level directory in the kind_robots repo, a sibling of
``public/images/...`` -- not nested under it -- so it gets its own root
config instead of being folded into the images root. Historical
``images/...`` and ``rewards/...`` forms are normalized to their canonical
``public/...`` spelling before validation. If the filesystem write or
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
REWARDS_ROOT_VALUE = (
    os.environ.get("KR_MEDIA_REWARDS_DIR", "").strip()
    or os.environ.get("KR_LOCAL_REWARDS_DIR", "").strip()
)
MEDIA_ROOT_ENV_HINT = {
    "images": "KR_MEDIA_IMAGES_DIR (or KR_LOCAL_IMAGES_DIR)",
    "rewards": "KR_MEDIA_REWARDS_DIR (or KR_LOCAL_REWARDS_DIR)",
}
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
    full media URLs, and the separate ``rewards/...``/``public/rewards/...``
    logical root. The relay accepts those historical spellings only long enough
    to canonicalize them to ``public/images/...`` or ``public/rewards/...``.
    Unrelated paths remain unchanged and fail the safety validation below.
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
    if image_path.startswith("public/rewards/"):
        return image_path
    if image_path.startswith("rewards/"):
        return f"public/{image_path}"
    return image_path


def direct_media_target(job):
    payload = job_payload(job)
    target_repo = str(payload.get("targetRepo") or "").strip()
    image_path = normalize_kindrobots_image_path(payload.get("imagePath"))

    if target_repo != KIND_ROBOTS_REPO or not image_path:
        return None

    logical = PurePosixPath(image_path)
    parts = logical.parts
    if len(parts) < 3 or parts[0] != "public" or parts[1] not in MEDIA_ROOT_ENV_HINT:
        raise ValueError(
            "Kind Robots media job imagePath must begin with public/images/ "
            "or public/rewards/"
        )

    relative_parts = parts[2:]
    if any(part in ("", ".", "..") for part in relative_parts):
        raise ValueError(f"Unsafe media imagePath: {image_path}")

    return parts[1], Path(*relative_parts)


def direct_media_relative(job):
    target = direct_media_target(job)
    return target[1] if target is not None else None


def media_root(kind="images"):
    if kind not in MEDIA_ROOT_ENV_HINT:
        raise ValueError(f"Unknown media root kind: {kind}")
    value = REWARDS_ROOT_VALUE if kind == "rewards" else MEDIA_ROOT_VALUE
    if not value:
        raise RuntimeError(
            f"{MEDIA_ROOT_ENV_HINT[kind]} is required for direct Kind Robots "
            f"{kind} media jobs"
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

    media_kind, relative = target
    root = media_root(media_kind)
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
    if media_kind == "images":
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

    media_kind, relative = target
    job_id = job["id"]
    engine = (job.get("engine") or "A1111").upper()
    payload = job_payload(job)
    payload["_relayClientId"] = f"{relay.AGENT_ID}-artjob-{job_id}"
    relay.log(
        f"job {job_id}: {engine} direct media -> "
        f"{relative.as_posix()} (logical root: {media_kind})"
    )

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
    """Log each recognized direct-media root and whether it's configured.

    Both roots (``images``, ``rewards``) are independently optional -- a job
    only discovers a missing root when a direct-media write actually fails,
    hours after the box was misconfigured. Logging the configured/missing
    state once at startup, alongside ``start_lora_watcher()``'s pattern of
    logging why a subsystem is enabled or disabled, makes a misconfigured box
    visible in the relay's own logs immediately."""
    root_values = {"images": MEDIA_ROOT_VALUE, "rewards": REWARDS_ROOT_VALUE}
    for kind, hint in MEDIA_ROOT_ENV_HINT.items():
        value = root_values[kind]
        if value:
            relay.log(f"media root '{kind}' configured ({hint} = {value})")
        else:
            relay.log(f"media root '{kind}' not configured (missing {hint})")


if __name__ == "__main__":
    log_media_roots()
    start_lora_watcher()
    relay.main()
