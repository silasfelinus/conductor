#!/usr/bin/env python3
"""Repair legacy Kind Robots request paths and vague prompt defaults.

The edit is deliberately limited to the ``requests:`` section of
projects/art-prompts.yaml. It is idempotent and preserves the hand-written YAML
header, ordering, comments, and folded prompt formatting.
"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART_PROMPTS_FILE = ROOT / "projects" / "art-prompts.yaml"

DEFAULT_ASSET_ART_DIRECTION = (
    "detailed mature western animation with multidimensional worldbuilding, "
    "expressive anatomy and faces, confident ink-like linework, dimensional "
    "shapes, rich controlled color, cinematic lighting, tactile environments, "
    "and clear readable silhouettes; cast characters naturally across many "
    "species, ages, body sizes, body shapes, gender presentations, and levels "
    "of conventional attractiveness; include robots only when the subject or "
    "scene explicitly calls for them"
)

VAGUE_ART_DIRECTION = re.compile(
    r"\b(?:(?:rich|cohesive|friendly)\s+)?Kind\s+Robots\s+"
    r"(?:visual\s+)?(?:style|language)\b",
    re.IGNORECASE,
)

IMAGE_PATH_LINE = re.compile(
    r"^(?P<prefix>\s*image_path:\s*[\"']?)(?P<path>[^\"'\n]+)(?P<suffix>[\"']?\s*)$",
    re.MULTILINE,
)


def canonical_request_path(path: str) -> str:
    clean = path.strip().replace("\\", "/").lstrip("/")
    if clean.startswith("public/images/"):
        return clean
    if clean.startswith("images/"):
        return f"public/{clean}"
    if clean.startswith("public/rewards/"):
        return f"public/images/{clean[len('public/'):]}"
    if clean.startswith("rewards/"):
        return f"public/images/{clean}"
    return path.strip()


def repair_requests(text: str) -> tuple[str, int, int]:
    marker = re.search(r"(?m)^requests:\s*$", text)
    if not marker:
        return text, 0, 0

    head = text[: marker.end()]
    tail = text[marker.end() :]
    path_changes = 0

    def replace_path(match: re.Match[str]) -> str:
        nonlocal path_changes
        original = match.group("path")
        canonical = canonical_request_path(original)
        if canonical != original.strip():
            path_changes += 1
        return f"{match.group('prefix')}{canonical}{match.group('suffix')}"

    tail = IMAGE_PATH_LINE.sub(replace_path, tail)
    tail, prompt_changes = VAGUE_ART_DIRECTION.subn(
        DEFAULT_ASSET_ART_DIRECTION,
        tail,
    )
    return f"{head}{tail}", path_changes, prompt_changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write repairs to projects/art-prompts.yaml",
    )
    args = parser.parse_args()

    original = ART_PROMPTS_FILE.read_text(encoding="utf-8")
    repaired, path_changes, prompt_changes = repair_requests(original)

    print(
        f"art request repair: {path_changes} path(s), "
        f"{prompt_changes} vague style token(s)"
    )

    if args.write and repaired != original:
        ART_PROMPTS_FILE.write_text(repaired, encoding="utf-8")
        print(f"updated {ART_PROMPTS_FILE.relative_to(ROOT)}")
    elif args.write:
        print("no changes needed")
    else:
        print("dry run; pass --write to persist")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
