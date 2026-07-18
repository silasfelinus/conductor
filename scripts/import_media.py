#!/usr/bin/env python3
"""Parse projects/media-watchlist/media_list.md into structured entries.

Implements PARSER-RULES.md (media-watchlist/t-002), extended for the format
variants the real 2014-2026 log contains that the 2025/2026-era design docs
did not cover: extra sections (ANIME, PODCASTS, THEATRE, SHORTS, VIDEO GAME
SHORTS, GAMES alias, NOVELLAS/NOVELINIS spellings), release years in titles
(both "(2024)" and bare "Naked Gun 2025"), comic issue ranges outside parens
("Hellblazer 134-150 (17)"), the historical TYPE: stats table, and prose
year-retrospective blocks (captured as narrative, not errors).

Outputs (relative to projects/media-watchlist/):
  data/media-entries.json   — one record per parsed entry
  data/import-report.md     — coverage stats, flagged entries, narrative blocks

Usage:
  python scripts/import_media.py            # parse + write outputs
  python scripts/import_media.py --check    # parse only, print stats, no writes
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT / "projects" / "media-watchlist"
DATA_DIR = PROJECT_DIR / "data"


def source_files():
    """The main log plus any supplemental year files (media_2021.md etc.)."""
    main = PROJECT_DIR / "media_list.md"
    extras = sorted(p for p in PROJECT_DIR.glob("media_*.md") if p != main)
    return [main] + extras

# Section-header aliases -> MediaType. SCHEMA-PROPOSAL.md defined 7 types for
# 2025/2026; the full log needs 12 (additions noted in the import report).
SECTION_TYPES = {
    "MOVIES": "MOVIE",
    "SHORTS": "SHORT",
    "TV": "TV",
    "TV SHOWS": "TV",
    "ANIME": "ANIME",
    "BOOKS": "BOOK",
    "NOVELLAE": "NOVELLA",
    "NOVELLAS": "NOVELLA",
    "NOVELINIS": "NOVELLA",
    "AUDIOBOOKS": "AUDIOBOOK",
    "COMICS": "COMIC",
    "COMIC BOOKS": "COMIC",
    "VIDEO GAMES": "VIDEO_GAME",
    "GAMES": "VIDEO_GAME",
    "VIDEO GAME SHORTS": "VIDEO_GAME_SHORT",
    "PODCASTS": "PODCAST",
    "THEATRE": "THEATRE",
}

BOOKISH = {"BOOK", "NOVELLA", "AUDIOBOOK"}

# Titles that legitimately end in a 2000+ year (the year is part of the name,
# not a release-year disambiguator like "Naked Gun 2025").
KNOWN_YEAR_TITLES = {"Death Race 2000", "Wonder Woman 1984", "Blade Runner 2049"}

YEAR_HEADER = re.compile(r"^\s*(?:MEDIA\s+(\d{4})|(\d{4})\s+MEDIA)\s*$", re.IGNORECASE)
SECTION_HEADER = re.compile(r"^\s*([A-Za-z][A-Za-z ]+?)\s*:?\s*(?:\((\d+)\))?\s*$")
STATS_HEADER = re.compile(r"^\s*TYPE:")
STATS_ROW = re.compile(r"^\s*[A-Z ]+:\s*\d+[\s/]")
DATE_TOKEN = re.compile(r"\b(\d{1,2})\s*//?\s*(\d?[xX]|\?|\d{1,2})(?![\d/])")
REWATCH_TOKEN = re.compile(r"\bx(\d)\b")
SEASON_TOKEN = re.compile(r"\b(?:s|season\s+)(\d{1,2})\b", re.IGNORECASE)
PAREN_RELEASE_YEAR = re.compile(r"\(((?:19|20)\d{2})\)")
BARE_RELEASE_YEAR = re.compile(r"(?<=\s)((?:19|20)\d{2})(?=\s|$)")
DURATION = re.compile(r"\((\d+(?:\.\d+)?)\s*(?:hrs?|h)\)", re.IGNORECASE)
AMBIG_DURATION = re.compile(r"\((\d+)(?:th|st|nd|rd)\s*s\)", re.IGNORECASE)
PAREN_RANGE = re.compile(r"\((\d+)\s*-\s*(\d+)\)")
PAREN_NUMBER = re.compile(r"\((\d+)\)")
BARE_ISSUE_RANGE = re.compile(r"\b(\d+)\s*-\s*(\d+)\b")
AUTHOR_SPLIT = re.compile(r"\s*-\s+(?=[A-Z])")
STAR_PREFIX = re.compile(r"^(\*+)\s*")
BRACKET_NOTE = re.compile(r"^\s*\[.*\]\s*$")
RULE_LINE = re.compile(r"^\s*[`\-—=~_]{3,}\s*$")


def parse_date(text):
    """Return (month, day, dateRaw, note) for the LAST date token, or Nones."""
    matches = list(DATE_TOKEN.finditer(text))
    if not matches:
        return None, None, None, None, text
    m = matches[-1]
    raw = m.group(0)
    month = int(m.group(1))
    if month < 1 or month > 12:
        return None, None, None, None, text
    day_tok = m.group(2)
    day = int(day_tok) if day_tok.isdigit() else None
    if day is not None and not 1 <= day <= 31:
        day = None
    note = "date typo normalized" if "//" in raw else None
    remainder = text[: m.start()] + " " + text[m.end():]
    return month, day, raw, note, remainder


def parse_entry(line, lineno, year, media_type):
    raw = line.rstrip("\n")
    text = raw.strip()
    entry = {
        "line": lineno,
        "year": year,
        "mediaType": media_type,
        "title": None,
        "starred": False,
        "releaseYear": None,
        "season": None,
        "author": None,
        "watchedMonth": None,
        "watchedDay": None,
        "dateRaw": None,
        "pageCount": None,
        "durationHours": None,
        "issueCount": None,
        "issueRange": None,
        "rewatch": None,
        "notes": [],
        "raw": raw,
    }

    star = STAR_PREFIX.match(text)
    if star:
        entry["starred"] = True
        text = text[star.end():]

    m = REWATCH_TOKEN.search(text)
    if m:
        entry["rewatch"] = int(m.group(1))
        text = text[: m.start()] + " " + text[m.end():]

    month, day, date_raw, date_note, text = parse_date(text)
    entry["watchedMonth"], entry["watchedDay"], entry["dateRaw"] = month, day, date_raw
    if date_note:
        entry["notes"].append(date_note)

    m = DURATION.search(text)
    if m:
        entry["durationHours"] = float(m.group(1))
        text = text[: m.start()] + " " + text[m.end():]

    m = AMBIG_DURATION.search(text)
    if m:
        entry["notes"].append(f"ambiguous: '{m.group(0)}' is a series ordinal, not a duration")
        text = text[: m.start()] + " " + text[m.end():]

    m = PAREN_RELEASE_YEAR.search(text)
    if m:
        entry["releaseYear"] = int(m.group(1))
        text = text[: m.start()] + " " + text[m.end():]

    if media_type == "TV" or media_type == "ANIME":
        m = SEASON_TOKEN.search(text)
        if m:
            entry["season"] = int(m.group(1))
            text = text[: m.start()] + " " + text[m.end():]

    if entry["releaseYear"] is None:
        m = BARE_RELEASE_YEAR.search(text)
        # Only contemporary years: Silas writes bare release years for recent
        # works ("Naked Gun 2025"); older years in titles are the title
        # ("Wonder Woman 1984"). Every capture is noted so it can be audited.
        if m and 2000 <= int(m.group(1)) <= 2029:
            before = text[: m.start()].strip()
            candidate = re.sub(r"\s+", " ", f"{before} {m.group(1)}")
            if before and candidate not in KNOWN_YEAR_TITLES:
                entry["releaseYear"] = int(m.group(1))
                entry["notes"].append(f"bare release year {m.group(1)} read from title")
                text = text[: m.start()] + " " + text[m.end():]

    m = PAREN_RANGE.search(text)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        entry["issueRange"] = f"{lo}-{hi}"
        entry["issueCount"] = hi - lo + 1
        text = text[: m.start()] + " " + text[m.end():]

    m = PAREN_NUMBER.search(text)
    if m:
        n = int(m.group(1))
        text = text[: m.start()] + " " + text[m.end():]
        if media_type == "COMIC":
            entry["issueCount"] = n
        elif media_type in ("BOOK", "NOVELLA"):
            entry["pageCount"] = n
        elif media_type == "AUDIOBOOK":
            # PARSER-RULES §3: bare (N) in an audiobook section reads as hours
            # when small, pages when book-sized.
            if n <= 60:
                entry["durationHours"] = float(n)
            else:
                entry["pageCount"] = n
        else:
            entry["notes"].append(f"unexpected numeric parens ({n}) in {media_type} section")

    if media_type == "COMIC":
        m = BARE_ISSUE_RANGE.search(text)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if entry["issueRange"] is None:
                entry["issueRange"] = f"{lo}-{hi}"
                if entry["issueCount"] is None:
                    entry["issueCount"] = hi - lo + 1
            else:
                entry["issueRange"] = f"{lo}-{hi}"
            text = text[: m.start()] + " " + text[m.end():]

    if media_type in ("BOOK", "NOVELLA", "AUDIOBOOK"):
        parts = AUTHOR_SPLIT.split(text, maxsplit=1)
        if len(parts) == 2 and parts[0].strip() and parts[1].strip():
            text, author = parts[0], parts[1]
            entry["author"] = re.sub(r"\s+", " ", author).strip()

    title = re.sub(r"\s+", " ", text).strip(" -–—\t")
    if not title:
        return None
    entry["title"] = title
    entry["notes"] = "; ".join(entry["notes"]) or None
    return entry


def parse_file(paths=None):
    entries, narrative, skipped, flagged = [], [], [], []
    section_counts = []  # (year, mediaType, declared_count)
    for path in paths or source_files():
        _parse_one(path, entries, narrative, skipped, flagged, section_counts)
    return entries, narrative, skipped, flagged, section_counts


def _parse_one(path, entries, narrative, skipped, flagged, section_counts):
    year = None
    media_type = None
    in_stats = False
    seen_sections = set()

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or RULE_LINE.match(line):
            continue

        m = YEAR_HEADER.match(line)
        if m:
            year = int(m.group(1) or m.group(2))
            media_type = None
            in_stats = False
            seen_sections = set()
            continue

        # Known quirk: two year blocks have no "MEDIA <year>" header — 2020
        # begins at a bare MOVIES section right after 2022's sections (2021 is
        # absent from the file entirely), and 2017 likewise follows 2018.
        # Detect structurally: a section type repeating within the current
        # year block means an unheadered new year started. Verified against
        # the log's own TYPE stats table (2020: 161 movies, 2017: 120) and
        # internal evidence ("Wonder Woman 1984 12/26", "Lala Land 1/18").
        # Any repeat outside these two known jumps gets flagged, not guessed.
        UNHEADERED_JUMPS = {2022: 2020, 2018: 2017}
        sec = SECTION_HEADER.match(line)
        sec_name = sec.group(1).strip().upper() if sec else None
        if sec_name in SECTION_TYPES and SECTION_TYPES[sec_name] in seen_sections:
            if year in UNHEADERED_JUMPS:
                year = UNHEADERED_JUMPS[year]
                seen_sections = set()
            else:
                flagged.append((lineno, raw, f"repeated section {sec_name} within {year} — unheadered year block?"))
                seen_sections = set()

        if STATS_HEADER.match(line):
            in_stats = True
            media_type = None
            skipped.append((lineno, raw, "historical stats table"))
            continue
        if in_stats:
            if STATS_ROW.match(line) or len(line) <= 3:
                skipped.append((lineno, raw, "historical stats table"))
                continue
            in_stats = False  # fall through: first non-stats line resumes normal parsing

        if sec_name in SECTION_TYPES:
            media_type = SECTION_TYPES[sec_name]
            seen_sections.add(media_type)
            if sec.group(2):
                section_counts.append((year, media_type, int(sec.group(2)), lineno))
            continue

        if BRACKET_NOTE.match(line):
            skipped.append((lineno, raw, "bracketed aside"))
            continue

        if media_type is None:
            narrative.append((lineno, year, raw))
            continue

        if year is None:
            flagged.append((lineno, raw, "entry before any year header"))
            continue

        entry = parse_entry(raw, lineno, year, media_type)
        if entry is None:
            flagged.append((lineno, raw, "unparseable in section " + media_type))
        else:
            entry["sourceFile"] = path.name
            entries.append(entry)


def build_report(entries, narrative, skipped, flagged, section_counts):
    by_year = Counter(e["year"] for e in entries)
    by_type = Counter(e["mediaType"] for e in entries)
    by_year_type = Counter((e["year"], e["mediaType"]) for e in entries)
    starred = sum(1 for e in entries if e["starred"])
    dated = sum(1 for e in entries if e["watchedMonth"] is not None)
    noted = [e for e in entries if e["notes"]]

    lines = []
    lines.append("# Media Watchlist — Import Report")
    lines.append("")
    sources = ", ".join(f"`{p.name}`" for p in source_files())
    lines.append(f"Generated by `scripts/import_media.py` from {sources}. Regenerate any time; do not hand-edit.")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Parsed entries: **{len(entries)}**")
    lines.append(f"- Starred: {starred}")
    lines.append(f"- With at least a watched month: {dated}")
    lines.append(f"- Entries carrying parse notes: {len(noted)}")
    lines.append(f"- Narrative lines preserved (year retrospectives etc.): {len(narrative)}")
    lines.append(f"- Skipped non-entry lines (stats table, asides, rules): {len(skipped)}")
    lines.append(f"- Flagged unparseable lines: {len(flagged)}")
    lines.append("")
    lines.append("## Entries by year")
    lines.append("")
    lines.append("| Year | Entries |")
    lines.append("|---|---|")
    for y in sorted(by_year):
        lines.append(f"| {y} | {by_year[y]} |")
    lines.append("")
    lines.append("## Entries by type")
    lines.append("")
    lines.append("| Type | Entries |")
    lines.append("|---|---|")
    for t, n in by_type.most_common():
        lines.append(f"| {t} | {n} |")
    lines.append("")
    lines.append("## Declared section counts vs parsed")
    lines.append("")
    lines.append("Sections that declared a count in their header (`AUDIOBOOKS: (14)`), compared against what parsed.")
    lines.append("")
    lines.append("| Year | Type | Declared | Parsed | Match |")
    lines.append("|---|---|---|---|---|")
    for y, t, declared, _ in section_counts:
        parsed = by_year_type.get((y, t), 0)
        shown = parsed
        # Comic section headers count ISSUES, not lines ("COMICS:(73)" over 6
        # series entries) — compare against the summed issue counts instead.
        if t == "COMIC":
            shown = sum(
                e["issueCount"] or 1
                for e in entries
                if e["year"] == y and e["mediaType"] == t
            )
        ok = "yes" if shown == declared else "CHECK"
        lines.append(f"| {y} | {t} | {declared} | {shown} | {ok} |")
    lines.append("")
    lines.append("## Schema additions the full log needs (vs SCHEMA-PROPOSAL.md)")
    lines.append("")
    lines.append("- MediaType additions: `ANIME`, `PODCAST`, `THEATRE`, `SHORT`, `VIDEO_GAME_SHORT` (log spans 2014-2026, not just 2025/2026)")
    lines.append("- `releaseYear` (already recommended by FORMAT-COMPARISON.md; the log embeds it as `(2024)` and bare `Naked Gun 2025`)")
    lines.append("- `issueRange` string alongside `issueCount` (comics log runs like `Hellblazer 134-150 (17)`)")
    lines.append("")
    if flagged:
        lines.append("## Flagged lines (manual review)")
        lines.append("")
        for lineno, raw, why in flagged:
            lines.append(f"- L{lineno} ({why}): `{raw.strip()}`")
        lines.append("")
    if narrative:
        lines.append("## Narrative blocks preserved")
        lines.append("")
        current = None
        for lineno, y, raw in narrative:
            if y != current:
                lines.append(f"### {y}")
                lines.append("")
                current = y
            lines.append(f"> {raw.strip()}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="parse and print stats without writing outputs")
    args = ap.parse_args()

    entries, narrative, skipped, flagged, section_counts = parse_file()
    total_lines = sum(
        1 for p in source_files() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()
    )
    print(f"parsed {len(entries)} entries from {total_lines} non-blank lines")
    print(f"narrative={len(narrative)} skipped={len(skipped)} flagged={len(flagged)}")
    for y, t, declared, _ in section_counts:
        if t == "COMIC":
            parsed = sum(e["issueCount"] or 1 for e in entries if e["year"] == y and e["mediaType"] == t)
        else:
            parsed = sum(1 for e in entries if e["year"] == y and e["mediaType"] == t)
        marker = "" if parsed == declared else "  <-- CHECK"
        print(f"  declared {y} {t}: {declared} vs parsed {parsed}{marker}")
    if flagged:
        print("flagged:")
        for lineno, raw, why in flagged[:20]:
            print(f"  L{lineno} ({why}): {raw.strip()}")

    if args.check:
        return 0

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "media-entries.json").write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "import-report.md").write_text(
        build_report(entries, narrative, skipped, flagged, section_counts), encoding="utf-8"
    )
    print(f"wrote {DATA_DIR / 'media-entries.json'}")
    print(f"wrote {DATA_DIR / 'import-report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
