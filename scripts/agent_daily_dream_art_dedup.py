#!/usr/bin/env python3
"""One-shot, self-removing patch for dream-cycle art queue deduplication."""

from __future__ import annotations

from pathlib import Path
from collections import Counter
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_dream_records.py"
TESTS = ROOT / "tests" / "test_daily_dream_bundle_art_queue.py"
QUEUE = ROOT / "projects" / "art-prompts.yaml"
LAUNCHER = ROOT / ".github" / "workflows" / "agent-apply-daily-dream-art-dedup.yml"
SELF = Path(__file__)


def patch_builder() -> None:
    source = BUILDER.read_text(encoding="utf-8")
    start_marker = "def append_art_requests(entries: list[str], dry_run: bool) -> None:\n"
    end_marker = "\n\n# ── Backlog file bookkeeping"
    if source.count(start_marker) != 1 or source.count(end_marker) != 1:
        raise SystemExit("art queue function boundaries changed; refusing patch")
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    replacement = '''def _art_request_id(entry: str) -> Optional[str]:
    """Extract one request ID from a comment-preserving YAML fragment."""
    match = re.search(r"(?m)^-\\s+id:\\s*(['\\\"]?)([^'\\\"\\n]+)\\1\\s*$", entry)
    return match.group(2).strip() if match else None


def append_art_requests(entries: list[str], dry_run: bool) -> None:
    if not entries:
        return
    text = ART_PROMPTS.read_text(encoding="utf-8")
    if "\\nrequests:" not in text and not text.startswith("requests:"):
        text += "\\nrequests:\\n"

    # Only inspect the requests collection. Other top-level collections can
    # legitimately contain unrelated id fields.
    request_header = re.search(r"(?m)^requests:\\s*$", text)
    if request_header is None:
        raise ValueError("art prompt queue has no requests section")
    request_start = request_header.end()
    next_section = re.search(
        r"(?m)^[A-Za-z][A-Za-z0-9_-]*:\\s*$",
        text[request_start:],
    )
    insertion = request_start + next_section.start() if next_section else len(text)
    request_id_pattern = re.compile(
        r"(?m)^-\\s+id:\\s*(['\\\"]?)([^'\\\"\\n]+)\\1\\s*$"
    )
    existing_ids = {
        match.group(2).strip()
        for match in request_id_pattern.finditer(text[request_start:insertion])
    }

    unique_entries: list[str] = []
    seen_ids = set(existing_ids)
    skipped = 0
    for entry in entries:
        request_id = _art_request_id(entry)
        if request_id and request_id in seen_ids:
            skipped += 1
            continue
        if request_id:
            seen_ids.add(request_id)
        unique_entries.append(entry)

    if not unique_entries:
        print(f"  skipped {skipped} already-queued art request(s)")
        return

    request_yaml = "".join(unique_entries)
    if next_section:
        before = text[:insertion].rstrip() + "\\n"
        after = text[insertion:].lstrip("\\n")
        text = before + request_yaml + "\\n" + after
    else:
        if not text.endswith("\\n"):
            text += "\\n"
        text += request_yaml
    if dry_run:
        print(
            f"  [dry-run] would append {len(unique_entries)} art request(s) "
            f"and skip {skipped} duplicate(s)"
        )
        return
    ART_PROMPTS.write_text(text, encoding="utf-8")
    print(
        f"  appended {len(unique_entries)} art request(s) "
        f"and skipped {skipped} duplicate(s)"
    )
'''
    BUILDER.write_text(source[:start] + replacement.rstrip() + source[end:], encoding="utf-8")


def patch_tests() -> None:
    source = TESTS.read_text(encoding="utf-8")
    if "test_append_art_requests_skips_ids_already_in_requests" in source:
        raise SystemExit("deduplication tests already exist")
    additions = '''


def test_append_art_requests_skips_ids_already_in_requests(tmp_path, monkeypatch):
    art = tmp_path / "art-prompts.yaml"
    _, _, existing = bdr.art_request_entry(
        "repeat-dream", "existing", "Existing", "existing prompt"
    )
    _, _, fresh = bdr.art_request_entry(
        "repeat-dream", "fresh", "Fresh", "fresh prompt"
    )
    art.write_text(
        "requests:\\n"
        + existing
        + "inspirations:\\n"
        + "- project: reference-project\\n"
        + "  images:\\n"
        + "  - image_path: reference.webp\\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(bdr, "ART_PROMPTS", art)

    bdr.append_art_requests([existing, fresh], dry_run=False)

    parsed = yaml.safe_load(art.read_text(encoding="utf-8"))
    assert [request["id"] for request in parsed["requests"]] == [
        "dream-cycle-repeat-dream-existing",
        "dream-cycle-repeat-dream-fresh",
    ]
    assert parsed["inspirations"] == [{
        "project": "reference-project",
        "images": [{"image_path": "reference.webp"}],
    }]


def test_append_art_requests_deduplicates_one_incoming_batch(tmp_path, monkeypatch):
    art = tmp_path / "art-prompts.yaml"
    art.write_text("requests:\\n", encoding="utf-8")
    monkeypatch.setattr(bdr, "ART_PROMPTS", art)
    _, _, entry = bdr.art_request_entry(
        "same-batch", "only-once", "Only Once", "one prompt"
    )

    bdr.append_art_requests([entry, entry], dry_run=False)

    requests = yaml.safe_load(art.read_text(encoding="utf-8"))["requests"]
    assert [request["id"] for request in requests] == [
        "dream-cycle-same-batch-only-once"
    ]
'''
    TESTS.write_text(source.rstrip() + additions + "\n", encoding="utf-8")


def deduplicate_queue() -> None:
    source = QUEUE.read_text(encoding="utf-8")
    header = re.search(r"(?m)^requests:\s*$", source)
    if header is None:
        raise SystemExit("projects/art-prompts.yaml has no requests section")
    next_section = re.search(
        r"(?m)^[A-Za-z][A-Za-z0-9_-]*:\s*$",
        source[header.end():],
    )
    section_end = header.end() + next_section.start() if next_section else len(source)
    block = source[header.end():section_end]
    starts = list(re.finditer(
        r"(?m)^-\s+id:\s*(['\"]?)([^'\"\n]+)\1\s*$",
        block,
    ))
    if not starts:
        raise SystemExit("requests section contains no request rows")
    prefix = block[:starts[0].start()]
    kept: list[str] = []
    first_by_id: dict[str, str] = {}
    removed: list[str] = []
    for index, match in enumerate(starts):
        stop = starts[index + 1].start() if index + 1 < len(starts) else len(block)
        chunk = block[match.start():stop]
        request_id = match.group(2).strip()
        normalized = chunk.strip()
        if request_id in first_by_id:
            if first_by_id[request_id] != normalized:
                raise SystemExit(f"duplicate request {request_id} has conflicting content")
            removed.append(request_id)
            continue
        first_by_id[request_id] = normalized
        kept.append(chunk)

    expected = {
        "dream-cycle-the-filing-echidna-the-filing-echidna",
        "dream-cycle-the-filing-echidna-reef-cathedral-of-her-spine",
        "dream-cycle-the-filing-echidna-bramble-osei",
        "dream-cycle-the-filing-echidna-starlight-stamp",
        "dream-cycle-the-filing-echidna-wilderness-filing",
        "dream-cycle-the-filing-echidna-equinox-inspection-scenario",
    }
    if len(removed) != 6 or set(removed) != expected:
        raise SystemExit(f"expected six Filing Echidna duplicates, found {removed}")

    cleaned = prefix + "".join(kept)
    if cleaned and not cleaned.endswith("\n"):
        cleaned += "\n"
    QUEUE.write_text(
        source[:header.end()] + cleaned + source[section_end:],
        encoding="utf-8",
    )

    parsed = yaml.safe_load(QUEUE.read_text(encoding="utf-8"))
    ids = [row.get("id") for row in parsed.get("requests", []) if isinstance(row, dict)]
    duplicates = [request_id for request_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"duplicate request ids remain: {duplicates}")
    filing = [
        request_id for request_id in ids
        if str(request_id).startswith("dream-cycle-the-filing-echidna-")
    ]
    if len(filing) != 6:
        raise SystemExit(f"expected six Filing Echidna requests, found {len(filing)}")
    print(f"validated {len(ids)} unique art requests; six belong to The Filing Echidna")


def main() -> None:
    patch_builder()
    patch_tests()
    deduplicate_queue()
    if LAUNCHER.exists():
        LAUNCHER.unlink()
    SELF.unlink()


if __name__ == "__main__":
    main()
