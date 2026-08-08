#!/usr/bin/env python3
"""Rewrite stale daily-dream prompts persisted in projects/art-prompts.yaml.

The missing half of the 2026-08-08 art repair. Fixing the prompt *builder* and
the live ArtJob queue was not enough, because `art_request_entry` writes each
element's prompt into the `requests:` block of `projects/art-prompts.yaml` at
build time, and that file is a durable replay queue: `consume_art_requests.py`
drains pending entries and mints brand-new ArtJobs from whatever text is stored
there.

So every repair kept getting undone. Jobs created hours after the builder fix
still carried `iconic treasure-card illustration of Mythroot Whisper (SKILL)...
cast characters naturally across many species...`, re-rendered the crowd, and
overwrote the corrected image on the record.

This rewrites those stored prompts to what `dream_art_prompts` produces today,
using each entry's `image_path` to identify the element (the same mapping the
queue sweep uses). Edits are surgical single-line replacements: the file carries
a curated header and hand-written `images:`/`inspirations:` collections that a
yaml round-trip would flatten and strip of comments.

Usage:
  python scripts/repair_art_prompt_yaml.py            # dry run, shows a diff
  python scripts/repair_art_prompt_yaml.py --apply

Non-dream entries are left alone; they belong to other lanes with their own
prompt conventions.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repair_queued_cast_prompts import (  # noqa: E402
    CAST_CLAUSE,
    dream_cycle_prompt,
    rewrite as strip_cast_clause,
)

ROOT = Path(__file__).resolve().parents[1]
ART_PROMPTS = ROOT / "projects" / "art-prompts.yaml"

REQUESTS_HEADER = re.compile(r"(?m)^requests:\s*$")
ENTRY_START = re.compile(r"(?m)^-\s+id:\s*(\S+)\s*$")
FIELD = re.compile(r"(?m)^  (\w+):\s*(.*)$")


def yaml_single_quoted(value: str) -> str:
    """A YAML single-quoted scalar on one line, matching art_request_entry."""
    return "'" + " ".join(value.split()).replace("'", "''") + "'"


def entry_blocks(body: str) -> list[tuple[int, int, str]]:
    """(start, end, id) for each `- id:` item in the requests: section."""
    starts = [(m.start(), m.group(1)) for m in ENTRY_START.finditer(body)]
    blocks = []
    for index, (start, req_id) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(body)
        blocks.append((start, end, req_id))
    return blocks


def prompt_span(block: str) -> tuple[int, int] | None:
    """Character span of the whole `prompt:` value, continuation lines included.

    A prompt is not always one line. Entries written by other lanes use folded
    block scalars (`prompt: >-` followed by indented text), and replacing only
    the `prompt:` line leaves those continuation lines behind as orphaned
    mapping keys — which is exactly how the first attempt at this repair
    produced a YAML file that would no longer parse.

    The value ends at the next line indented two spaces or less that is not
    blank, i.e. the next sibling key or the next list item.
    """
    lines = block.splitlines(keepends=True)
    offset = 0
    start = None
    for index, line in enumerate(lines):
        if start is None:
            if re.match(r"^  prompt:", line):
                start, start_index = offset, index
            offset += len(line)
            continue
        if line.strip() and not re.match(r"^   ", line):
            return start, offset
        offset += len(line)
    return (start, offset) if start is not None else None


def field_value(block: str, name: str) -> str:
    for match in FIELD.finditer(block):
        if match.group(1) == name:
            return match.group(2).strip().strip("'\"")
    return ""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true",
                        help="write the file (default is a dry run)")
    args = parser.parse_args(argv)

    text = ART_PROMPTS.read_text(encoding="utf-8")
    header = REQUESTS_HEADER.search(text)
    if not header:
        print("No requests: section in art-prompts.yaml; nothing to do.")
        return 0

    head, body = text[: header.end()], text[header.end():]
    rewritten = skipped = unresolved = 0
    out = []
    cursor = 0

    for start, end, req_id in entry_blocks(body):
        out.append(body[cursor:start])
        block = body[start:end]
        cursor = end

        image_path = field_value(block, "image_path")
        new_prompt = dream_cycle_prompt(image_path)

        if not new_prompt:
            # Entries from other lanes (missing-image, user uploads) have no
            # proposal to rebuild from, but they carry the same crowd-summoning
            # casting clause. Strip it the way the live-queue sweep does rather
            # than leaving 40 pending jobs to replay it.
            span = prompt_span(block)
            current = " ".join(block[span[0]:span[1]].split())[len("prompt: "):] if span else ""
            current = current.strip().strip("'\"")
            if span and CAST_CLAUSE.search(current):
                new_prompt, _ = strip_cast_clause(current)
            elif req_id.startswith("dream-cycle-"):
                unresolved += 1
                print(f"  ! {req_id}: no proposal element matches {image_path}",
                      file=sys.stderr)

        if not new_prompt:
            out.append(block)
            continue

        span = prompt_span(block)
        if not span:
            out.append(block)
            continue
        first, last = span

        replacement = f"  prompt: {yaml_single_quoted(new_prompt)}"
        if block[first:last].rstrip("\n") == replacement:
            skipped += 1
            out.append(block)
            continue

        rewritten += 1
        print(f"\n[{req_id}]")
        print(f"  old: {' '.join(block[first:last].split())[:150]}")
        print(f"  new: {new_prompt[:150]}")
        out.append(block[:first] + replacement + "\n" + block[last:])

    out.append(body[cursor:])
    updated = head + "".join(out)

    print(f"\n{rewritten} prompt(s) to rewrite, {skipped} already current, "
          f"{unresolved} unresolved.")
    if not args.apply:
        print("Dry run. Re-run with --apply to write the file.")
        return 0
    if rewritten:
        ART_PROMPTS.write_text(updated, encoding="utf-8")
        print(f"Wrote {ART_PROMPTS}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
