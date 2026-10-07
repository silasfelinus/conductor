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
