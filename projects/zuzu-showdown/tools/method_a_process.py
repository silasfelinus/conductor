"""zuzu-showdown t-007, method A: pixelize the Kontext renders from T007-METHOD-A.yaml.

Each finished cell (`art.<lane>.art_image_id`, filled in by `enqueue_art_requests.py --status`)
is downloaded once into CACHE_DIR, keyed out of its off-white backdrop, scaled with the SAME factor
as the reference build (so a figure Kontext drew bigger or smaller stays bigger or smaller, which is
exactly the frame-to-frame drift this method has to be judged on), quantized to one shared palette
and written as strips and GIFs. a-meta.json keeps every frame's prompt, seed, job and image id.

    python projects/zuzu-showdown/tools/method_a_process.py LEDGER REFERENCE.png CACHE_DIR OUT_DIR
"""

from __future__ import annotations

import base64
import io
import json
import statistics
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
import sprite_common as sc


def download(image_id: int, cache: Path) -> Image.Image:
    path = cache / f"{image_id}.png"
    if not path.exists():
        import enqueue_art_requests as enq  # needs KR_API_TOKEN; only imported when a download is due

        data_url = enq.fetch_source_image(image_id)
        raw = base64.b64decode(data_url.split(",", 1)[1])
        cache.mkdir(parents=True, exist_ok=True)
        Image.open(io.BytesIO(raw)).convert("RGB").save(path)
    return Image.open(path).convert("RGB")


def render_seconds(job_id) -> float | None:
    """GPU wall time for one ArtJob: claimed -> verified (queue wait excluded)."""
    if not job_id:
        return None
    from datetime import datetime

    import enqueue_art_requests as enq

    status, resp = enq.core.http_json("GET", f"{enq.core.KR_BASE_URL}/api/art/queue/{job_id}")
    job = ((resp or {}).get("data") or {}).get("job") or {}
    done = ((job.get("payload") or {}).get("provenance") or {}).get("completion", {}).get("verifiedAt")
    if status != 200 or not job.get("claimedAt") or not done:
        return None

    def parse(stamp):
        return datetime.fromisoformat(stamp.replace("Z", "+00:00"))

    return round((parse(done) - parse(job["claimedAt"])).total_seconds(), 1)


def main(ledger_path: str, reference_path: str, cache_dir: str, out_dir: str) -> None:
    ledger = yaml.safe_load(Path(ledger_path).read_text())
    lane = ledger["lanes"][0]
    reference = sc.crop_to_content(sc.key_background(ImageOps.mirror(Image.open(reference_path).convert("RGB"))))
    figure_height = reference.height
    cache, out = Path(cache_dir), Path(out_dir)
    frames: dict[str, list[Image.Image]] = {}
    hd: dict[str, list[Image.Image]] = {}
    meta = {"method": "A pose-locked generation (Flux Kontext re-pose)", "lane": lane, "frames": {}}
    heights = []
    for subject in ledger["subjects"]:
        cell = (subject.get("art") or {}).get(lane["key"]) or {}
        image_id = cell.get("art_image_id")
        name, index = subject["key"].removeprefix("zuzu-sprite-").rsplit("-", 1)
        if not image_id:
            meta["frames"].setdefault(name, []).append({"frame": int(index), "status": cell.get("status", "PENDING")})
            continue
        raw = download(image_id, cache)
        # Kontext does not follow "facing right": frames it turned around are mirrored back.
        mirrored = subject.get("post_mirror", lane.get("post_mirror", False))
        if mirrored:
            raw = ImageOps.mirror(raw)
        keyed = sc.crop_to_content(sc.key_background(raw))
        heights.append(keyed.height)
        frames.setdefault(name, []).append(sc.to_game_size(keyed, figure_height))
        hd.setdefault(name, []).append(sc.to_hd(keyed, figure_height))
        meta["frames"].setdefault(name, []).append({
            "frame": int(index),
            "art_image_id": image_id,
            "job_id": (subject.get("jobs") or {}).get(lane["key"]),
            "seed": subject.get("seed", lane.get("seed")),
            "source_image_id": subject["source_image_id"],
            "source_flip": subject.get("source_flip", False),
            "post_mirror": mirrored,
            "prompt": subject["prompt_prose"],
            "figure_height_px": keyed.height,
            "render_seconds": render_seconds((subject.get("jobs") or {}).get(lane["key"])),
        })
    every = [f for fs in frames.values() for f in fs]
    if not every:
        print("no finished frames yet")
        return
    palette = sc.shared_palette(every, 16)
    width = max(f.width for f in every) + 2
    height = max(f.height for f in every) + 2
    final_all = []
    for name, fs in frames.items():
        final = sc.anchor_frames([sc.outer_outline(sc.quantize(f, palette)) for f in fs], width, height)
        final_all.extend(final)
        sc.write_previews(final, out, f"a-{name}", sc.FPS[name])
        sc.write_hd_gif(hd[name], out, f"a-{name}", sc.FPS[name])
    meta["palette_colours"] = sc.palette_size(final_all)
    meta["frame_size"] = [width, height]
    # Size drift: how much the figure's height wanders between frames, in game pixels.
    game_heights = [h * sc.GAME_HEIGHT / figure_height for h in heights]
    meta["figure_height_game_px"] = {
        "min": round(min(game_heights), 1),
        "max": round(max(game_heights), 1),
        "stdev": round(statistics.pstdev(game_heights), 1),
    }
    seconds = [f["render_seconds"] for fs in meta["frames"].values() for f in fs if f.get("render_seconds")]
    if seconds:
        meta["render_seconds_per_frame"] = {"mean": round(statistics.mean(seconds), 1), "max": max(seconds)}
    (out / "a-meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({k: v for k, v in meta.items() if k not in ("frames", "lane")}))


if __name__ == "__main__":
    main(*sys.argv[1:5])
