#!/usr/bin/env python3
"""
check_ruler_hooked_docs.py — guardrail for the ruler-hooked design docs (t-011).

The m1 design docs under projects/ruler-hooked/docs/ share a vocabulary that must
stay in sync BY HAND today: region keys, slider axes, the `regionOverride` field,
and the `{region}-{state}` asset-naming convention. Nothing stops one doc from
being edited (e.g. a region renamed) while the others keep the old spelling, and
nothing checks that queued art-prompts.yaml `inspirations:` entries still parse
against the schema scripts/distribute_images.py actually reads.

This script is that check. Two parts:

  1. VOCAB — the shared region/axis vocabulary stays consistent across the docs:
     no drifted variant spellings (far-shore / farshore for far_shore, etc.), the
     canonical snake_case tokens remain in use, and the asset-naming convention is
     documented in both the compositing spec and the art-direction doc.
  2. PROMPTS — every `inspirations:` entry in projects/art-prompts.yaml carries the
     fields distribute_images.py depends on (project + images[] each with a
     non-empty image_path), so a prompt edit can't silently break the art pipeline.

Exit 0 = clean, 1 = one or more problems (printed). No writes, no network.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("check_ruler_hooked_docs: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "projects" / "ruler-hooked" / "docs"
ART_PROMPTS = REPO_ROOT / "projects" / "art-prompts.yaml"

# --- The canonical contract (the enforcement point) -------------------------
# Region keys are defined by compositing.md §1; axes by data-model.md §4.
CANONICAL_REGIONS = [
    "sky", "far_shore", "treeline", "village_edge",
    "castle_grounds", "lake", "near_bank", "ruler", "fx",
]
CANONICAL_AXES = ["nature", "prosperity", "treasury", "joy", "order"]

# Multiword code tokens whose *variant* spellings signal drift. For each, the
# hyphenated and concatenated forms are wrong (prose "far shore" with a space is
# fine — only code-token variants are flagged). `regionOverride` is camelCase.
MULTIWORD_TOKENS = ["far_shore", "village_edge", "castle_grounds", "near_bank"]
CAMEL_TOKENS = ["regionOverride"]

# Tokens that must remain in use somewhere across the doc set (the vocabulary
# can't be silently emptied/renamed). Core, not the full set, to stay lenient.
CORE_REQUIRED = ["treeline", "far_shore", "village_edge", "castle_grounds",
                 "nature", "prosperity", "regionOverride"]

ASSET_CONVENTION = "{region}-{state}"


def _variants(token: str) -> list[str]:
    """Drifted spellings of a snake_case or camelCase token."""
    if "_" in token:                      # snake_case multiword
        parts = token.split("_")
        joined = "".join(parts)
        return [f"{parts[0]}-{parts[1]}", joined]          # far-shore, farshore
    # camelCase -> snake_case / lowercase / hyphenated variants
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", token).lower()  # region_override
    hyphen = snake.replace("_", "-")                        # region-override
    flat = token.lower()                                    # regionoverride
    return [snake, hyphen, flat]


def check_vocab(problems: list[str]) -> None:
    if not DOCS_DIR.is_dir():
        problems.append(f"docs dir missing: {DOCS_DIR}")
        return
    docs = {p.name: p.read_text(encoding="utf-8") for p in sorted(DOCS_DIR.glob("*.md"))}
    if not docs:
        problems.append(f"no docs found under {DOCS_DIR}")
        return
    all_text = "\n".join(docs.values())

    # 1. No drifted variant spellings of the multiword / camel tokens.
    #    Multiword snake_case variants (far-shore/farshore) are matched
    #    case-insensitively; camelCase variants (region_override/regionoverride)
    #    are matched case-SENSITIVELY so the correct `regionOverride` token does
    #    not match its own lowercased variant.
    for token, flags in [(t, re.IGNORECASE) for t in MULTIWORD_TOKENS] + \
                        [(t, 0) for t in CAMEL_TOKENS]:
        for variant in _variants(token):
            pat = re.compile(rf"(?<![\w-]){re.escape(variant)}(?![\w-])", flags)
            for name, text in docs.items():
                if pat.search(text):
                    problems.append(
                        f"{name}: found drifted spelling '{variant}' — the canonical "
                        f"token is '{token}'. Keep the vocabulary consistent across docs."
                    )

    # 2. Core vocabulary must still appear (not silently dropped/renamed).
    for token in CORE_REQUIRED:
        pat = re.compile(rf"(?<![\w-]){re.escape(token)}(?![\w-])")
        if not pat.search(all_text):
            problems.append(
                f"core vocabulary token '{token}' appears in NONE of the docs — "
                f"it was renamed or dropped without updating this contract."
            )

    # 3. Asset-naming convention documented in both the spec and the art doc.
    for name in ("compositing.md", "art-direction.md"):
        text = docs.get(name)
        if text is None:
            problems.append(f"expected doc missing: {name}")
        elif ASSET_CONVENTION not in text:
            problems.append(
                f"{name}: the asset-naming convention '{ASSET_CONVENTION}' is not "
                f"documented here — it must stay defined in compositing.md and "
                f"referenced in art-direction.md so the naming contract can't drift."
            )


def check_inspirations(problems: list[str]) -> None:
    if not ART_PROMPTS.is_file():
        problems.append(f"art-prompts file missing: {ART_PROMPTS}")
        return
    try:
        data = yaml.safe_load(ART_PROMPTS.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        problems.append(f"art-prompts.yaml does not parse: {e}")
        return

    entries = data.get("inspirations") or []
    if not isinstance(entries, list):
        problems.append("art-prompts.yaml `inspirations:` is not a list")
        return

    for i, entry in enumerate(entries):
        where = f"inspirations[{i}]"
        if not isinstance(entry, dict):
            problems.append(f"{where}: entry is not a mapping")
            continue
        proj = entry.get("project")
        if not isinstance(proj, str) or not proj.strip():
            problems.append(f"{where}: missing non-empty `project`")
            where = f"inspirations[{i}]({proj})"
        images = entry.get("images")
        if not isinstance(images, list) or not images:
            problems.append(f"{where}: `images` must be a non-empty list "
                            f"(distribute_images.py iterates it)")
            continue
        for j, img in enumerate(images):
            if not isinstance(img, dict):
                problems.append(f"{where}.images[{j}]: not a mapping")
                continue
            path = img.get("image_path")
            if not isinstance(path, str) or not path.strip():
                problems.append(
                    f"{where}.images[{j}]: missing non-empty `image_path` — "
                    f"distribute_images.py keys the pipeline on it, so an entry "
                    f"without it is silently dropped."
                )
            status = img.get("status")
            if status is not None and not isinstance(status, str):
                problems.append(f"{where}.images[{j}]: `status` must be a string if present")


def main() -> int:
    problems: list[str] = []
    check_vocab(problems)
    check_inspirations(problems)

    if problems:
        print("check_ruler_hooked_docs: FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("check_ruler_hooked_docs: OK — docs vocabulary consistent, "
          "art-prompts inspirations well-formed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
