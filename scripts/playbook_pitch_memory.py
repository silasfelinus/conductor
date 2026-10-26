"""Deterministic, human-curated memory for the daily evolving playbook lab.

Dated pitch dockets are immutable creative history. MEMORY.yaml stores editorial
judgment and concepts' growth priorities, not duplicate snapshots. No AI calls.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

VERSION = re.compile(r"^(\d{4}-\d{2}-\d{2})/([a-z0-9]+(?:-[a-z0-9]+)*)$")
STATES = ("incubating", "promising", "parked", "rejected", "approved")
NOTES_FILE = "SILAS-NOTES.yaml"
NOTE_STATES = ("open", "addressed", "dismissed")


def review_memory(dockets: Path) -> dict:
    """Explicit human/editorial priorities are separate from authored snapshots."""
    path = dockets / "MEMORY.yaml"
    if not path.exists():
        return {"concepts": {}, "rejected_first_pass": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or not isinstance(data.get("concepts", {}), dict):
        raise ValueError("MEMORY.yaml must contain a concepts mapping")
    for cid, meta in data["concepts"].items():
        if not isinstance(meta, dict) or meta.get("status", "incubating") not in STATES:
            raise ValueError(f"invalid editorial state for {cid}")
    return data


def silas_notes(dockets: Path) -> dict[str, list[dict]]:
    """Silas's notes per concept, written from the Playbook Forge Gestation screen.

    Each note is {at, by, note, status: open|addressed|dismissed, addressed_in?}.
    The next development of a concept answers its open notes first.
    """
    path = dockets / NOTES_FILE
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw = data.get("notes") or {}
    if not isinstance(raw, dict):
        raise TypeError(f"{NOTES_FILE} must contain a notes mapping")
    notes: dict[str, list[dict]] = {}
    for cid, rows in raw.items():
        if not isinstance(rows, list):
            raise TypeError(f"{NOTES_FILE}: notes for {cid} must be a list")
        clean = []
        for row in rows:
            if not isinstance(row, dict) or not str(row.get("note") or "").strip():
                continue
            if row.get("status", "open") not in NOTE_STATES:
                raise ValueError(f"{NOTES_FILE}: invalid note status for {cid}")
            clean.append(row)
        notes[str(cid)] = clean
    return notes


def build_index(dockets: Path, before: str | None = None) -> dict:
    """Read ALL prior daily files. The archive is never mistaken for live ideas."""
    versions: dict[str, dict] = {}
    concepts: dict[str, dict] = {}
    for path in sorted(dockets.glob("????-??-??.yaml")):
        if before is not None and path.stem >= before:
            continue
        docket = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if docket.get("date") != path.stem:
            raise ValueError(f"{path.name}: date mismatch")
        for item in docket.get("pitches", []):
            slug = item["slug"]
            key = f"{path.stem}/{slug}"
            if key in versions:
                raise ValueError(f"duplicate version {key}")
            cid = item.get("concept_id", slug)
            mode = item.get("mode", "new")
            parents = item.get("parents", [])
            snapshot = {
                "version": key, "date": path.stem, "slug": slug,
                "concept_id": cid, "title": item["title"], "mode": mode,
                "parents": parents, "genre": item.get("genre_pillar", ""),
                "next_questions": item.get("next_questions", []),
                "preserve": item.get("preserve", ""),
                "challenge": item.get("challenge", ""),
                "change": item.get("evolution", ""),
            }
            versions[key] = snapshot
            group = concepts.setdefault(cid, {"concept_id": cid, "versions": [], "latest": None})
            group["versions"].append(key)
            group["latest"] = snapshot
    editorial = review_memory(dockets)
    silas = silas_notes(dockets)
    for cid, group in concepts.items():
        group["silas_notes"] = silas.get(cid, [])
        notes = editorial.get("concepts", {}).get(cid, {})
        group["editorial"] = {
            "status": notes.get("status", "incubating"),
            "tags": notes.get("tags", []),
            "strengths": notes.get("strengths", []),
            "guardrails": notes.get("guardrails", []),
            "next_moves": notes.get("next_moves", []),
            "decision_note": notes.get("decision_note", ""),
        }
    # A deliberately compact shelf, sorted by editorial relevance and freshness.
    rank = {"promising": 0, "incubating": 1, "approved": 2, "parked": 3, "rejected": 4}
    shelf = sorted(concepts.values(), key=lambda c: (
        rank[c["editorial"]["status"]], -int(c["latest"]["date"].replace("-", "")),
        c["concept_id"],
    ))
    return {
        "concepts": concepts, "versions": versions,
        "shelf": shelf, "rejected_first_pass": editorial.get("rejected_first_pass", []),
    }


def memory_summary(index: dict, limit: int | None = None) -> str:
    """A curator's shortlist with canon, provenance, pitfalls and next directions."""
    sections = [
        "LONG-RUN PITCH MEMORY (from every dated docket; editorial notes from MEMORY.yaml):",
        "Keep previously rejected drafts as learning, NEVER relabel them live.",
        "Select three substantial pitches per Pacific day. At least one should "
        "continue an existing lineage once any earlier root exists; do NOT force "
        "a merger if no two concepts gain a genuinely new game loop.",
    ]
    waiting = [
        item for item in index["shelf"]
        if any(n.get("status", "open") == "open" for n in item.get("silas_notes", []))
    ]
    if waiting:
        sections.append(
            "OPEN NOTES FROM SILAS (Playbook Forge Gestation). Answer these before anything "
            "else: a concept with open notes is today's expand slot unless you say why not, and "
            "the version that answers a note sets it to status: addressed with addressed_in: "
            "<date>/<slug> in SILAS-NOTES.yaml."
        )
        for item in waiting:
            for n in item["silas_notes"]:
                if n.get("status", "open") == "open":
                    sections.append(f"- {item['concept_id']} ({n.get('at', '')[:10]}): {n['note']}")
    for item in index["shelf"][:limit]:
        note = item["editorial"]
        latest = item["latest"]
        sections.append(
            f"- {item['concept_id']} | {note['status']} | last {latest['version']} "
            f"({latest['mode']}; {len(item['versions'])} revisions) | {latest['title']}\n"
            f"  Genre: {latest['genre']}\n"
            f"  KEEP: {'; '.join(note['strengths']) or latest['preserve']}\n"
            f"  AVOID: {'; '.join(note['guardrails']) or latest['challenge']}\n"
            f"  NEXT: {'; '.join(note['next_moves']) or '; '.join(latest['next_questions'])}"
        )
    for note in index.get("rejected_first_pass", []):
        sections.append(f"- REJECTED ARCHIVE: {note.get('title')}: {note.get('reason')}")
    return "\n".join(sections)


def verify_lineage(date: str, pitches: list[dict], index: dict) -> list[str]:
    """Check ancestry against strictly earlier snapshots, not today's other pitches."""
    errors: list[str] = []
    versions, concepts = index["versions"], index["concepts"]
    day_slugs: set[str] = set()
    day_ids: set[str] = set()
    day_titles: set[str] = set()
    used_new = set()
    for pos, pitch in enumerate(pitches, 1):
        if not isinstance(pitch, dict):
            continue
        prefix = f"pitch {pos}"
        slug = pitch.get("slug")
        cid = pitch.get("concept_id")
        mode = pitch.get("mode")
        parents = pitch.get("parents")
        title = str(pitch.get("title", "")).casefold().strip()
        if not isinstance(slug, str) or not isinstance(cid, str):
            errors.append(f"{prefix}: slug/concept_id required")
            continue
        if not isinstance(mode, str) or mode not in ("new", "expand", "meld"):
            errors.append(f"{prefix}: mode must be new, expand, or meld")
            continue
        if not isinstance(parents, list) or any(not isinstance(p, str) or not VERSION.fullmatch(p) for p in parents):
            errors.append(f"{prefix}: parents must be prior YYYY-MM-DD/slug version refs")
            continue
        if slug != cid:
            errors.append(f"{prefix}: slug must be the stable concept_id")
        if slug in day_slugs or cid in day_ids or title in day_titles:
            errors.append(f"{prefix}: same-day duplicate lineage or title")
        day_slugs.add(slug)
        day_ids.add(cid)
        day_titles.add(title)
        if len(parents) != len(set(parents)):
            errors.append(f"{prefix}: repeated parent reference")
        parents_known = []
        for ref in parents:
            parent = versions.get(ref)
            if parent is None:
                errors.append(f"{prefix}: unknown, same-day or future parent {ref}")
                continue
            parents_known.append(parent)
        if mode == "new":
            if parents:
                errors.append(f"{prefix}: new concept cannot have parents")
            if cid in concepts:
                errors.append(f"{prefix}: new concept duplicates historical identity {cid}")
        elif mode == "expand":
            if len(parents) != 1:
                errors.append(f"{prefix}: expansion needs exactly one parent snapshot")
            if len(parents_known) == 1 and parents_known[0]["concept_id"] != cid:
                errors.append(f"{prefix}: expansion must retain its parent's concept_id")
            if cid not in concepts:
                errors.append(f"{prefix}: expansion concept_id has no established root")
            if cid in concepts and concepts[cid]["editorial"]["status"] == "rejected":
                errors.append(f"{prefix}: rejected parent needs explicit reactivation in MEMORY.yaml")
        else:  # meld
            if len(parents) < 2 or len({p["concept_id"] for p in parents_known}) < 2:
                errors.append(f"{prefix}: merger requires two different earlier concept families")
            if cid in concepts or cid in used_new:
                errors.append(f"{prefix}: merger must create a new stable concept identity")
            for parent in parents_known:
                state = concepts[parent["concept_id"]]["editorial"]["status"]
                if state == "rejected":
                    errors.append(f"{prefix}: cannot merge a rejected concept without reactivation")
        if mode in ("new", "meld"):
            used_new.add(cid)
            if any(v["title"].casefold().strip() == title for v in versions.values()):
                errors.append(f"{prefix}: duplicated historical title for new identity")
        for field in ("evolution", "preserve", "challenge"):
            if not isinstance(pitch.get(field), str) or len(pitch[field].strip()) < 35:
                errors.append(f"{prefix}: {field} must describe substantive continuity or changes")
        questions = pitch.get("next_questions")
        if not isinstance(questions, list) or len(questions) < 2 or any(
            not isinstance(q, str) or len(q.strip()) < 15 for q in questions
        ):
            errors.append(f"{prefix}: include at least two actionable next_questions")
    if versions and not any(isinstance(p, dict) and p.get("mode") in ("expand", "meld") for p in pitches):
        errors.append("daily pitch trio must include at least one evolution of an earlier idea")
    return errors
