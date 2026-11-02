#!/usr/bin/env python3
"""art_ledger_authoring.py -- catch round-ledger prompts that were filled in by a template.

WHY THIS EXISTS. On 2026-11-02 PR #6951 queued 192 Slime City card renders whose every prompt
was the same four sentences with blanks filled in:

    An original collectible illustration of <card name>: <rotating camera phrase>. Belongs to
    <faction blurb>. Visual story to paint: <the card's rules text, verbatim>. Strong focal
    storytelling, humorous character attitude, sharply distinguished subject and environment.

Every prompt passed kind_robots' prompt contract, because the contract checks wording hazards
(frame nouns, negations, conditionals), not whether a prompt describes anything. Krea is
caption-conditioned and paints only visible nouns. It cannot know what a "Last-Stand Matchbook"
is, so ArtJob 57166 came back as four people in pink jumpsuits in a stadium: the faction blurb,
with no matchbook and no joke. Equipment cards showed no equipment, and 190 renders became
interchangeable faction posters. "A street medic with REGEN heals one HP each round" was sent
to an image model as a scene.

Two rules, both checked across the whole ledger because a template is visible only in bulk:

* ``templated-prompt``: once every five-word run a prompt shares with at least a tenth of its
  ledger is removed, fewer than MIN_OWN_WORDS words are left. A
  shared style tail is fine; a prompt with no subject of its own is not.
* ``rules-text``: game keywords in capitals (VOLATILE, REGEN, PIERCE) or rules vocabulary
  (HP, mana, "each round"). Show the effect instead of naming the mechanic.

``enqueue_art_requests.py`` refuses a failing cell before it is posted, and
``tests/test_art_ledger_authoring.py`` fails CI on any unsubmitted cell that breaks a rule.

    python scripts/art_ledger_authoring.py                 # unsubmitted cells in every ledger
    python scripts/art_ledger_authoring.py --all           # audit submitted cells too
    python scripts/art_ledger_authoring.py projects/slime-city/art/X.yaml

Exit 0 = clean, 1 = problems listed.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = ("projects/*/art/*.yaml", "projects/*/art/**/*.yaml")

MIN_LEDGER_SUBJECTS = 8   # below this a "template" is just a small consistent batch
RUN = 5                   # a run of five words ...
SHARE_FRACTION = 0.1      # ... found in >= 10% of the ledger's prompts is shared boilerplate
MIN_SHARE_COUNT = 4
MIN_OWN_WORDS = 15        # the words a prompt must have that are its own

# Capitalised words that are not game keywords.
CAPS_ALLOW = {"NASA", "NATO", "UNESCO", "NYPD", "LAPD", "ASCII", "HVAC", "CCTV", "SCUBA", "LASER", "RADAR"}
CAPS_WORD = re.compile(r"\b[A-Z]{4,}\b")
RULES_WORDS = re.compile(
    r"\b(?:\d+\s*HP|HP\b|hit points?|mana\b|each round|per round|once per turn|end of (?:the )?turn|"
    r"visual story to paint)",
    re.I,
)
WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def prose(subject) -> str:
    """The prose a subject sends, or '' for subjects that use a different prompt shape."""
    value = subject.get("prompt_prose") if isinstance(subject, dict) else None
    return " ".join(str(value).split()) if isinstance(value, str) else ""


def _words(text: str) -> list[str]:
    return [w.lower() for w in WORD.findall(text)]


def _runs(words: list[str]) -> set[tuple[str, ...]]:
    return {tuple(words[i:i + RUN]) for i in range(len(words) - RUN + 1)}


def shared_runs(prompts: list[str]) -> set[tuple[str, ...]]:
    """Five-word runs that recur across enough of a ledger's prompts to be boilerplate."""
    counts = Counter()
    for text in prompts:
        counts.update(_runs(_words(text)))
    floor = max(MIN_SHARE_COUNT, int(len(prompts) * SHARE_FRACTION + 0.999))
    return {run for run, n in counts.items() if n >= floor}


def own_words(text: str, shared: set[tuple[str, ...]]) -> int:
    """Words of the prompt not covered by any shared five-word run."""
    words = _words(text)
    covered = [False] * len(words)
    for i in range(len(words) - RUN + 1):
        if tuple(words[i:i + RUN]) in shared:
            covered[i:i + RUN] = [True] * RUN
    return covered.count(False)


def rules_text(text: str) -> list[str]:
    found = [w for w in CAPS_WORD.findall(text) if w not in CAPS_ALLOW]
    found += [m.group(0) for m in RULES_WORDS.finditer(text)]
    return found


def ledger_problems(ledger, only_unsubmitted: bool = True) -> list[tuple[str, str, str]]:
    """[(subject key, rule, detail)] for one parsed ledger."""
    subjects = [s for s in (ledger or {}).get("subjects") or [] if isinstance(s, dict)]
    prompts = [prose(s) for s in subjects]
    templated = len([p for p in prompts if p]) >= MIN_LEDGER_SUBJECTS
    shared = shared_runs([p for p in prompts if p]) if templated else frozenset()
    out = []
    for subject, text in zip(subjects, prompts):
        if not text:
            continue
        if only_unsubmitted and any((subject.get("jobs") or {}).values()):
            continue
        key = str(subject.get("key") or "?")
        if templated:
            mine = own_words(text, shared)
            if mine < MIN_OWN_WORDS:
                out.append((key, "templated-prompt",
                            f"only {mine} words are this subject's own; the rest is shared with the ledger. "
                            "Describe what is visibly in this image: who or what, doing what, holding what."))
        caps = rules_text(text)
        if caps:
            out.append((key, "rules-text",
                        f"{', '.join(dict.fromkeys(caps))} is game or prompt-writing vocabulary, which Krea paints "
                        "as words or ignores. Show the effect as a physical moment instead."))
    return out


def find_ledgers(root: Path = ROOT) -> list[Path]:
    found = set()
    for pattern in PATTERNS:
        found.update(root.glob(pattern))
    return sorted(found)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ledgers", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true", help="also audit cells that already have job ids")
    args = parser.parse_args(argv)
    total = 0
    for path in args.ledgers or find_ledgers():
        try:
            ledger = yaml.safe_load(path.read_text())
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(ledger, dict):
            continue
        for key, rule, detail in ledger_problems(ledger, only_unsubmitted=not args.all):
            total += 1
            print(f"{path.relative_to(ROOT) if path.is_absolute() else path}: {key} [{rule}] {detail}")
    print(f"{total} problem(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
