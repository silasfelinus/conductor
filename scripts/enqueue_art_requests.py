#!/usr/bin/env python3
"""Submit an A/B art ledger to Kind Robots ``POST /api/art/enqueue``.

WHY THIS EXISTS. ``consume_art_queue.py`` builds its own ComfyUI graphs and only
knows krea2, flux and flux2-klein; it even aliases ``sdxl`` to krea2. Kind Robots'
enqueue route already builds correct graphs for every lane it supports (SDXL /
Illustrious / Pony checkpoints with their family sampler profiles, Z-Image, ...),
so a ledger that wants to compare checkpoints sends requests there instead of
re-implementing those graphs here.

A ledger is YAML with ``lanes`` (engine + optional checkpoint + prompt style) and
``subjects`` (one prompt pair per subject). Every subject renders once per lane;
the returned ArtJob id is written back under ``subjects[].jobs[<lane>]`` so a
re-run never submits the same cell twice. See
projects/comic-creator/issues/zuzu-koala-assassin-01/ART-ROUND-3.yaml.

A subject may carry ``source_image_id`` (an ArtImage id). Kontext lanes need one:
the image is fetched and sent as ``sourceImageBase64``, so an approved design can be
re-posed (the 8-angle renders, comic-creator t-015). Kontext lanes may set ``steps``
and ``guidance``. ``source_crop: [l, t, r, b]`` (fractions) cuts one figure out of a
turnaround sheet, ``source_flip: true`` mirrors it (a back view with the sword on the wrong
shoulder), and ``reference_image_id`` (with optional ``reference_crop``) is
stitched to the LEFT of the source at the same height, so Kontext can dress the right
figure like the left one (the ImageStitch trick of Kind Robots' kontext/kombine route).
``mask_box: [l, t, r, b]`` (fractions of the composed source) makes the edit masked: only that box may
change, and the job goes to ``/api/comfy/kontext/enqueue`` with a generated mask (white = change).

Usage:
    python scripts/enqueue_art_requests.py LEDGER            # dry run, print requests
    python scripts/enqueue_art_requests.py LEDGER --live     # submit missing cells
    python scripts/enqueue_art_requests.py LEDGER --status   # record job status + ArtImage ids

Environment: KR_API_TOKEN (required for --live/--status), KR_BASE_URL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

try:
    from scripts import consume_art_queue_core as core
except ImportError:  # pragma: no cover - direct script execution
    import consume_art_queue_core as core

TERMINAL_STATUSES = {"DONE", "FAILED", "CANCELLED"}


def compose_prompt(lane, subject):
    """The prompt string one lane sends for one subject."""
    style = str(lane.get("prompt") or "prose").strip().lower()
    base = subject.get("prompt_tags") if style == "tags" else subject.get("prompt_prose")
    base = base or subject.get("prompt_prose") or ""
    parts = [lane.get("prefix"), base, lane.get("suffix")]
    return ", ".join(" ".join(str(p).split()) for p in parts if p and str(p).strip())


def build_request(ledger, lane, subject, source_image=None):
    """The /api/art/enqueue body for one (subject, lane) cell.

    ``source_image`` is the data URL of the subject's ``source_image_id``; only a
    Kontext lane sends it.
    """
    width, height = core.parse_size(subject.get("size"))
    body = {
        "engine": lane["engine"],
        "promptString": compose_prompt(lane, subject),
        "width": width,
        "height": height,
        "isPublic": bool(ledger.get("is_public", False)),
        "isMature": bool(ledger.get("is_mature", False)),
    }
    if lane.get("checkpoint"):
        body["checkpoint"] = lane["checkpoint"]
    if lane["engine"] == "comfy":
        # Optional per-lane overrides (a checkpoint author's recommended settings).
        # Absent, Kind Robots applies the checkpoint family's sampler profile. The
        # scheduler always stays the profile's: enqueue does not forward one for comfy.
        for field in ("steps", "cfg", "sampler"):
            if lane.get(field):
                body[field] = lane[field]
    if lane["engine"] == "kontext":
        if not source_image:
            raise ValueError(f"{subject.get('key')}: a kontext lane needs the subject's source_image_id")
        body["sourceImageBase64"] = source_image
        for field in ("steps", "guidance"):
            if lane.get(field):
                body[field] = lane[field]
    if lane["engine"] == "comfy" and subject.get("negative"):
        body["negativePrompt"] = " ".join(str(subject["negative"]).split())
    for field, key in (("projectSlug", "project_slug"), ("designer", "designer")):
        if ledger.get(key):
            body[field] = ledger[key]
    return body


def iter_cells(ledger, lane_filter=None, subject_filter=None):
    lanes = ledger.get("lanes") or []
    for subject in ledger.get("subjects") or []:
        if subject_filter and subject.get("key") not in subject_filter:
            continue
        for lane in lanes:
            if lane_filter and lane.get("key") not in lane_filter:
                continue
            yield subject, lane


def split_header(text):
    """Leading comment block, kept verbatim when the ledger is rewritten."""
    lines = text.splitlines(keepends=True)
    header = []
    for line in lines:
        if line.startswith("#") or not line.strip():
            header.append(line)
        else:
            break
    return "".join(header)


def load_ledger(path):
    text = Path(path).read_text()
    return split_header(text), yaml.safe_load(text) or {}


def save_ledger(path, header, ledger):
    Path(path).write_text(
        header + yaml.safe_dump(ledger, sort_keys=False, width=110, allow_unicode=True)
    )


def job_id_of(subject, lane_key):
    return (subject.get("jobs") or {}).get(lane_key)


def fetch_source_image(image_id):
    """An ArtImage as a data URL, for a Kontext lane's sourceImageBase64."""
    import base64
    import urllib.request

    status, resp = core.http_json("GET", f"{core.KR_BASE_URL}/api/art/image/{image_id}", None, timeout=60)
    data = resp.get("data", resp) if isinstance(resp, dict) else {}
    path = data.get("imagePath") if isinstance(data, dict) else None
    if status != 200 or not path:
        raise RuntimeError(f"ArtImage {image_id}: HTTP {status}, no imagePath")
    url = path if path.startswith("http") else core.KR_BASE_URL.rstrip("/") + path
    with urllib.request.urlopen(url, timeout=60) as response:
        raw = response.read()
        mime = response.headers.get_content_type() or "image/png"
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def _decode_data_url(data_url):
    import base64
    import io

    from PIL import Image

    raw = base64.b64decode(data_url.split(",", 1)[1])
    return Image.open(io.BytesIO(raw)).convert("RGB")


def _crop(image, box):
    """Crop by fractions [left, top, right, bottom] of the image size."""
    if not box:
        return image
    left, top, right, bottom = (float(v) for v in box)
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise ValueError(f"crop {box} must be fractions with left < right and top < bottom")
    w, h = image.size
    return image.crop((round(left * w), round(top * h), round(right * w), round(bottom * h)))


def stitch_images(reference, source):
    """Reference on the left, source on the right, both scaled to the source's height."""
    from PIL import Image

    height = source.height
    width = round(reference.width * height / reference.height)
    reference = reference.resize((width, height), Image.LANCZOS)
    canvas = Image.new("RGB", (width + source.width, height), "white")
    canvas.paste(reference, (0, 0))
    canvas.paste(source, (width, 0))
    return canvas


def compose_source(subject, fetch):
    """The sourceImageBase64 for one subject: its source image, cropped and stitched as asked.

    ``fetch(image_id)`` returns a data URL. A plain source passes through untouched, so
    PIL is only needed when a subject crops or stitches.
    """
    source = fetch(subject["source_image_id"])
    crop, reference_id = subject.get("source_crop"), subject.get("reference_image_id")
    flip = bool(subject.get("source_flip"))
    if not crop and not reference_id and not flip:
        return source
    import base64
    import io

    image = _crop(_decode_data_url(source), crop)
    if flip:
        from PIL import ImageOps

        image = ImageOps.mirror(image)
    if reference_id:
        reference = _crop(_decode_data_url(fetch(reference_id)), subject.get("reference_crop"))
        image = stitch_images(reference, image)
    buffer = io.BytesIO()
    image.save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


def make_mask(source, box):
    """A PNG data URL the size of ``source``: white inside ``box`` (fractions), black elsewhere.

    ``box`` may also be a list of boxes, for an edit that touches two places (moving a holster).
    """
    import base64
    import io

    from PIL import Image, ImageDraw

    width, height = _decode_data_url(source).size
    boxes = box if box and isinstance(box[0], (list, tuple)) else [box]
    mask = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(mask)
    for one in boxes:
        left, top, right, bottom = (float(v) for v in one)
        if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
            raise ValueError(f"mask_box {one} must be fractions with left < right and top < bottom")
        draw.rectangle(
            (round(left * width), round(top * height), round(right * width) - 1, round(bottom * height) - 1),
            fill="white",
        )
    buffer = io.BytesIO()
    mask.save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


def build_masked_request(ledger, lane, subject, source_image, mask):
    """The /api/comfy/kontext/enqueue body for a masked Kontext edit."""
    width, height = core.parse_size(subject.get("size"))
    body = {
        "prompt": compose_prompt(lane, subject),
        "imageData": source_image,
        "maskData": mask,
        "width": width,
        "height": height,
        "isPublic": bool(ledger.get("is_public", False)),
        "isMature": bool(ledger.get("is_mature", False)),
    }
    for field in ("steps", "guidance"):
        if lane.get(field):
            body[field] = lane[field]
    if ledger.get("designer"):
        body["designer"] = ledger["designer"]
    return body


def request_url(body):
    """Masked Kontext edits use the Kontext queue route; everything else the art enqueue route."""
    route = "/api/comfy/kontext/enqueue" if "maskData" in body else "/api/art/enqueue"
    return f"{core.KR_BASE_URL}{route}"


def submit(path, header, ledger, cells, post=None, fetch_source=None):
    """POST every cell that has no job id yet; write the id back after each one."""
    post = post or (lambda body: core.http_json("POST", request_url(body), body))
    fetch_source = fetch_source or fetch_source_image
    fetched = {}

    def fetch(image_id):
        if image_id not in fetched:
            fetched[image_id] = fetch_source(image_id)
        return fetched[image_id]

    submitted, failures = 0, 0
    for subject, lane in cells:
        if job_id_of(subject, lane["key"]):
            continue
        source = None
        if lane["engine"] == "kontext" and subject.get("source_image_id"):
            source = compose_source(subject, fetch)
        if source and subject.get("mask_box"):
            body = build_masked_request(ledger, lane, subject, source, make_mask(source, subject["mask_box"]))
        else:
            body = build_request(ledger, lane, subject, source)
        status, resp = post(body)
        job_id = ((resp or {}).get("data") or {}).get("jobId") if isinstance(resp, dict) else None
        if status in (200, 201) and job_id:
            subject.setdefault("jobs", {})[lane["key"]] = int(job_id)
            save_ledger(path, header, ledger)
            submitted += 1
            print(f"  queued job {job_id} for {subject['key']} [{lane['key']}]")
        else:
            failures += 1
            message = (resp or {}).get("message") if isinstance(resp, dict) else resp
            print(f"  FAILED {subject['key']} [{lane['key']}]: HTTP {status} {message}", file=sys.stderr)
    return submitted, failures


def refresh_status(path, header, ledger, get=None):
    """Record each job's status and ArtImage id under subjects[].art."""
    get = get or (lambda job_id: core.http_json("GET", f"{core.KR_BASE_URL}/api/art/queue/{job_id}"))
    counts = {}
    for subject in ledger.get("subjects") or []:
        for lane_key, job_id in (subject.get("jobs") or {}).items():
            if not job_id:
                continue
            status, resp = get(job_id)
            job = (((resp or {}).get("data") or {}).get("job") or {}) if isinstance(resp, dict) else {}
            job_status = job.get("status") or f"HTTP{status}"
            counts[job_status] = counts.get(job_status, 0) + 1
            art = subject.setdefault("art", {})
            art[lane_key] = {"status": job_status, "art_image_id": job.get("artImageId")}
    save_ledger(path, header, ledger)
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ledger")
    parser.add_argument("--live", action="store_true", help="submit cells that have no job id")
    parser.add_argument("--status", action="store_true", help="refresh job status and ArtImage ids")
    parser.add_argument("--lane", action="append", help="limit to a lane key (repeatable)")
    parser.add_argument("--subject", action="append", help="limit to a subject key (repeatable)")
    args = parser.parse_args(argv)

    header, ledger = load_ledger(args.ledger)
    cells = list(iter_cells(ledger, args.lane, args.subject))

    if (args.live or args.status) and not core.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live and --status.", file=sys.stderr)
        return 1

    if args.status:
        counts = refresh_status(args.ledger, header, ledger)
        print("status:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "no jobs")
        return 0

    if not args.live:
        pending = [(s, lane) for s, lane in cells if not job_id_of(s, lane["key"])]
        print(f"DRY RUN: {len(pending)} of {len(cells)} cells would be submitted via {core.KR_BASE_URL}")
        for subject, lane in pending:
            source = "data:image/png;base64," if lane["engine"] == "kontext" else None
            body = build_request(ledger, lane, subject, source)
            if source:
                extra = f", reference ArtImage {subject['reference_image_id']}" if subject.get("reference_image_id") else ""
                crop = f", crop {subject['source_crop']}" if subject.get("source_crop") else ""
                crop += f", masked {subject['mask_box']} via /api/comfy/kontext/enqueue" if subject.get("mask_box") else ""
                print(f"    source: ArtImage {subject.get('source_image_id')}{crop}{extra}")
            print(f"  {subject['key']} [{lane['key']}] {body['width']}x{body['height']} \"{body['promptString'][:70]}\"")
        return 0

    submitted, failures = submit(args.ledger, header, ledger, cells)
    print(f"{submitted} submitted, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
