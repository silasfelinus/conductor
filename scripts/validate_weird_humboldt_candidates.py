#!/usr/bin/env python3
"""Validate Ecotone (weird-humboldt) t-027 offline encounter candidates.

Checks: required fields, 2-4 consequences, known axis, curation decision enum, art never enqueued,
nothing published, no excluded Wiyot/Tuluwat or substance-instruction content, no near-duplicate of an
existing card/seed title, and that referenced card ids exist. Stdlib + PyYAML.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "projects" / "weird-humboldt"
CAND_DIR = PROJECT / "candidates"
AXES = {"autonomy_solidarity", "continuity_reinvention", "ecology_engineering", "agency_fate"}
DECISIONS = {"pending", "keep", "modify", "reject"}
REQUIRED = ["id", "title", "axis", "premise", "counterexample", "prerequisites", "consequences",
            "choice_provenance", "leverage", "art_brief", "curation"]
BANNED = re.compile(r"wiyot|tuluwat|indian island|\b(dosage|milligram|snort|inject)\b|how to (cook|make|score)|where to buy", re.I)


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 3}


def existing_titles() -> list[tuple[str, set[str]]]:
    out = []
    for f in sorted((PROJECT / "cards").glob("*.yaml")):
        for card in yaml.safe_load(f.read_text()) or []:
            out.append((card["id"], _tokens(card.get("title", ""))))
    for m in re.finditer(r"\*\*(WH-\d+) · ([^:*]+)", (PROJECT / "ENCOUNTER-SEEDS.md").read_text()):
        out.append((m.group(1), _tokens(m.group(2))))
    return out


def validate(path: Path) -> list[str]:
    errs: list[str] = []
    data = yaml.safe_load(path.read_text())
    if data.get("publish") is not False:
        errs.append("publish must be false")
    if data.get("art_enqueue") is not False:
        errs.append("art_enqueue must be false")
    known = {i for i, _ in existing_titles()}
    titles = existing_titles()
    seen_ids: set[str] = set()
    seen_titles: list[set[str]] = []
    for c in data.get("candidates", []):
        cid = c.get("id", "?")
        for k in REQUIRED:
            if not c.get(k):
                errs.append(f"{cid}: missing {k}")
        if cid in seen_ids:
            errs.append(f"{cid}: duplicate id")
        seen_ids.add(cid)
        if c.get("axis") not in AXES:
            errs.append(f"{cid}: unknown axis {c.get('axis')}")
        n = len(c.get("consequences") or [])
        if not 2 <= n <= 4:
            errs.append(f"{cid}: needs 2-4 consequences, has {n}")
        if (c.get("curation") or {}).get("decision") not in DECISIONS:
            errs.append(f"{cid}: bad curation decision")
        if (c.get("art_brief") or {}).get("status") != "not_enqueued":
            errs.append(f"{cid}: art_brief.status must be not_enqueued")
        for ref in (c.get("choice_provenance") or {}).get("cards", []):
            if ref not in known:
                errs.append(f"{cid}: provenance card {ref} not found")
        blob = yaml.safe_dump(c)
        if BANNED.search(blob):
            errs.append(f"{cid}: contains excluded or unsafe content")
        tk = _tokens(c.get("title", ""))
        for other, ot in titles:
            if tk and ot and len(tk & ot) / len(tk | ot) >= 0.6:
                errs.append(f"{cid}: near-duplicate of existing {other}")
        for ot in seen_titles:
            if tk and len(tk & ot) / len(tk | ot) >= 0.6:
                errs.append(f"{cid}: near-duplicate of another candidate")
        seen_titles.append(tk)
    return errs


def main() -> int:
    files = sorted(CAND_DIR.glob("*.yaml"))
    if not files:
        print("no candidate files")
        return 1
    bad = 0
    for f in files:
        errs = validate(f)
        for e in errs:
            print(f"{f.name}: {e}")
        bad += len(errs)
    print("ok" if not bad else f"{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
