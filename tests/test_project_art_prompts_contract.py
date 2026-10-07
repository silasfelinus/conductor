"""Every project image prompt in projects/art-prompts.yaml must pass the negation rules.

kind_robots rejects a prompt with a 422 at enqueue, and a rejected prompt never heals
on its own (see docs/agents/roles/art-medic.md).
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from repair_negation_art_prompts import violations  # noqa: E402


def _image_prompts():
    data = yaml.safe_load((ROOT / "projects" / "art-prompts.yaml").read_text())
    for project in data.get("images") or []:
        for variant, asset in project.items():
            if isinstance(asset, dict) and isinstance(asset.get("prompt"), str):
                yield asset.get("image_path", variant), asset["prompt"]


def test_project_image_prompts_pass_contract():
    bad = {path: violations(prompt) for path, prompt in _image_prompts() if violations(prompt)}
    assert not bad, bad


ACTIVE_QUEUE_STATUSES = {"pending", "queued", "running", "processing"}


def test_pending_queue_prompts_match_catalog():
    """A prompt fix in art-prompts.yaml must reach its pending copy in art-generate.yaml.

    queue_missing_project_art.py preserves active queue entries verbatim (so a hand-written
    replacement survives a refresh), which means a catalog-only fix never renders: on
    2026-10-07 #5697 rewrote the comic-film card and hero, and the queue kept submitting
    the old "comic page"/"comic panel" text for 422s. A deliberate hand-written replacement
    marks itself `manual_prompt: true`; everything else must match the catalog.
    """
    catalog = {
        path: " ".join(prompt.split())
        for path, prompt in _image_prompts()
    }
    queue = yaml.safe_load((ROOT / "projects" / "art-generate.yaml").read_text())
    stale = [
        entry["image_path"]
        for entry in (queue.get("batch") or {}).get("entries") or []
        if str(entry.get("status", "pending")).strip().lower() in ACTIVE_QUEUE_STATUSES
        and not entry.get("manual_prompt")
        and entry.get("image_path") in catalog
        and " ".join(str(entry.get("prompt", "")).split()) != catalog[entry["image_path"]]
    ]
    assert not stale, (
        "pending art-generate.yaml entries still carry an old prompt; copy the "
        f"art-prompts.yaml text into them (or mark manual_prompt: true): {stale}"
    )
