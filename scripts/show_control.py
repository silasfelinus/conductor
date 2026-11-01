#!/usr/bin/env python3
"""show_control.py — print only the parts of CONTROL.md a session needs.

CONTROL.md is Silas's steering sheet (~125KB): a global overview every agent must
read, then one `### <slug>` block per project. A session needs the global overview
plus the block for the project it is working on, not all ~60 blocks
(2026-11-01 token-essentialization pass 2).

Usage:
  python scripts/show_control.py                  # global overview only
  python scripts/show_control.py memory-dungeon   # global overview + that block
  python scripts/show_control.py memory-dungeon --block-only
  python scripts/show_control.py --list           # project blocks with sizes

Exit codes: 0 = printed; 1 = no block for that slug (the global overview still
prints, so the session never loses the global direction).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOBAL_RE = re.compile(r"^## Global overview")
PER_PROJECT_RE = re.compile(r"^## Per-project direction")
BLOCK_RE = re.compile(r"^### ([A-Za-z0-9._-]+)")


def split_control(text: str) -> tuple[str, dict[str, str]]:
    lines = text.splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if GLOBAL_RE.match(l)), 0)
    end = next((i for i, l in enumerate(lines) if PER_PROJECT_RE.match(l)), len(lines))
    global_text = "".join(lines[start:end])
    blocks: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in lines[end:]:
        m = BLOCK_RE.match(line)
        if m or line.startswith("## "):
            if current is not None:
                blocks[current] = "".join(buf)
            current, buf = (m.group(1), [line]) if m else (None, [])
            continue
        if current is not None:
            buf.append(line)
    if current is not None:
        blocks[current] = "".join(buf)
    return global_text, blocks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", nargs="?")
    parser.add_argument("--block-only", action="store_true", help="skip the global overview")
    parser.add_argument("--list", action="store_true", help="list project blocks and sizes")
    parser.add_argument("--control", default=str(ROOT / "CONTROL.md"))
    args = parser.parse_args(argv)

    global_text, blocks = split_control(Path(args.control).read_text(encoding="utf-8"))
    if args.list:
        for slug, body in blocks.items():
            print(f"{len(body):>7}  {slug}")
        return 0
    if not args.block_only:
        sys.stdout.write(global_text)
    if not args.project:
        return 0
    block = blocks.get(args.project)
    if block is None:
        print(f"\n(no CONTROL.md block for {args.project!r})", file=sys.stderr)
        return 1
    sys.stdout.write("\n" + block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
