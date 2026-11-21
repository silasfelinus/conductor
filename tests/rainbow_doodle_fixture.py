"""Shared, real-image Rainbow DOODLE-SET-2 ledger fixture for export and review."""

from pathlib import Path

import yaml
from PIL import Image

ART = "rainbow-princess-art"
LANE = "kontext"


def make_doodle_subject(
    root,
    rel: str,
    image_id: int | None,
    *,
    status: str = "DONE",
    green: bool = True,
    classic: bool = True,
) -> dict:
    """Create genuine classic/cache pixels and a DOODLE-SET-2 shaped subject."""
    root = Path(root)
    if classic:
        if rel.startswith("portraits/"):
            path = (
                root / "kind_robots/public/rainbow-princess-portraits"
                / (rel.split("/", 1)[1] + ".webp")
            )
        else:
            path = root / "kind_robots/public" / ART / f"{rel}.webp"
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (64, 48), (120, 50, 200, 255)).save(path, "WEBP")

    if image_id is not None:
        cached = root / "cache" / f"{rel}-{image_id}.png"
        cached.parent.mkdir(parents=True, exist_ok=True)
        matte = (0, 255, 0) if green else (200, 20, 60)
        render = Image.new("RGB", (64, 48), matte)
        for x in range(16, 48):
            for y in range(10, 38):
                render.putpixel((x, y), (180, 50, 200))
        render.save(cached)

    key = rel.replace("/", "-")
    return {
        "key": f"test-{key}",
        "lane": LANE,
        "title": f"Fixture {rel}",
        "asset": f"{ART}/doodle/{rel}",
        "size": "64x48",
        "seed": 880007,
        "prompt_prose": "Single centred illustrated subject, fully visible.",
        "source_image_id": 246032,
        "jobs": {LANE: 63796},
        "art": {LANE: {"status": status, "art_image_id": image_id}},
    }


def write_doodle_ledger(root, subjects, filename="DOODLE-SET-2.yaml"):
    """Write the same top-level ledger lanes and subject fields as SET-2."""
    path = Path(root) / filename
    path.write_text(
        yaml.safe_dump(
            {
                "round": "test-rainbow-doodle-set-2",
                "project_slug": "rainbow-bullet-hell-space-princess",
                "auto_submit": False,
                "lanes": [
                    {"key": LANE, "engine": LANE, "prompt": "prose"},
                ],
                "subjects": subjects,
            },
            sort_keys=False,
        )
    )
    return path
