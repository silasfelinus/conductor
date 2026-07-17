#!/usr/bin/env python3
"""Media-aware wrapper for the proven Kind Robots ArtJob relay.

Kind Robots-targeted jobs that carry both:

- targetRepo: silasfelinus/kind_robots
- imagePath: public/images/<path>

are written to the exact equivalent path under KR_MEDIA_IMAGES_DIR before the
ArtJob is marked successful. If the filesystem write or manifest update fails,
the job is reported FAILED and remains retryable instead of silently completing
with a missing public file.

All other jobs use relay_agent.py unchanged.
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


def process_with_media(job):
    relative = direct_media_relative(job)
    if relative is None:
        return ORIGINAL_PROCESS(job)

    job_id = job["id"]
    engine = (job.get("engine") or "A1111").upper()
    payload = job_payload(job)
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


relay.process = process_with_media


if __name__ == "__main__":
    relay.main()
