#!/usr/bin/env python3
"""Activate Arthemy img2img ONLY from visually accepted, verified Round-18 Krea art.

Inputs: private review receipt from the authenticated review workflow, a reviewer
selection ledger (four scores + critical scene objects), and durable Round 18
ArtJob results. Stage 19 remains auto_submit:false until every scene passes.
This tool never publishes media or sends API requests; commit the reviewed
Stage-19 ledger via a scoped PR to trigger the existing idempotent art runner.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "projects/zuzu-gamebook/art"
SCORES = ("scene_truth", "composition", "required_objects", "focus")
CRITICAL = {
    "a2-bell-view": {"bell", "high_overlook", "distant_pale_tower", "tiny_tracks"},
    "a2-gift": {"waterskin", "single_nail", "wooden_post", "scratched_eye_symbol", "no_characters"},
    "a4-bloom": {"dense_flowers", "yellow_white_violet", "damp_soil", "no_building_focus"},
}
PROMPTS = {
    "a2-bell-view": (
        "Preserve the source image exactly: large foreground hanging bell, open high tower lookout, "
        "distant slender pale tower and trail of tiny tracks across ochre and white wasteland. "
        "Only repaint textures in Zuzu western graphic novel house style, ink outlines, cinematic desert atmosphere.",
        "figure, face, corridor, tunnel, closed room, cabin, crowded scene, city, extra bells, logo, watermark, lettering",
    ),
    "a2-gift": (
        "Preserve the precise still-life arrangement from the source: one full hanging leather waterskin "
        "on a nail in a wooden post, tiny scratched eye symbol next to it. No new objects or characters. "
        "Only repaint material texture into western-comics ink and textured earthy painterly color.",
        "person, face, animal, portrait, statue, extra bags, empty post, house, logo, watermark, lettering",
    ),
    "a4-bloom": (
        "Preserve the exact dense carpet of tiny yellow white and violet desert wildflowers, wet earth "
        "and puddles under dawn sky. Keep the source flower coverage and camera position, no buildings. "
        "Only repaint into Zuzu's western-comic painted ink and brush style, natural muted pigments.",
        "figure, person, cabin, tree, house, empty field, architecture, sparse flowers, logo, watermark, lettering",
    ),
}
STRENGTHS = (("safe", 0.28), ("bold", 0.43))


def approved_sources(round18, selections, receipt):
    """Return scene -> vetted ArtImage ID; reject ambiguity or premature approval."""
    assert round18.get("round") == "gamebook-18-krea-composition"
    assert round18.get("is_public") is False
    assert round18.get("series") == "zuzu-koala-assassin"
    subjects = round18["subjects"]
    assert len(subjects) == 9
    by_key = {s["key"]: s for s in subjects}
    assert len(by_key) == 9
    assert set(selections.get("selections", {})) == set(CRITICAL)
    assert receipt.get("round") == round18["round"] and receipt.get("complete") is True
    assert receipt.get("fetched") == 9
    receipt_rows = {c["artImageId"]: c for c in receipt["candidates"]}
    assert len(receipt_rows) == 9
    chosen = {}
    for section, checklist in CRITICAL.items():
        choice = selections["selections"][section]
        key = choice.get("candidate_key")
        assert isinstance(key, str) and key in by_key, f"{section}: choose an existing Krea candidate"
        subject = by_key[key]
        assert subject["section"] == section
        assert subject.get("lane") == "krea-composition"
        assert not str(subject.get("verdict", "")).startswith("reject")
        job_id = (subject.get("jobs") or {}).get("krea-composition")
        art = (subject.get("art") or {}).get("krea-composition") or {}
        image_id = art.get("art_image_id")
        assert art.get("status") == "DONE"
        assert type(job_id) is int and job_id > 0
        assert type(image_id) is int and image_id > 0
        ratings = choice.get("ratings") or {}
        assert set(ratings) == set(SCORES)
        assert all(type(ratings[k]) is int and 0 <= ratings[k] <= 2 for k in SCORES)
        assert sum(ratings.values()) >= 7, f"{section}: needs 7/8 fidelity"
        critical = choice.get("critical") or {}
        assert set(critical) == checklist
        assert all(critical[k] is True for k in checklist), f"{section}: missing crucial picture detail"
        note = choice.get("notes", "")
        assert isinstance(note, str) and len(note.strip()) >= 20
        assert not note.startswith("Review actual Krea image"), "Replace template instructions with actual observation"
        verified = receipt_rows.get(image_id)
        assert verified is not None
        assert verified.get("section") == section and verified.get("artJobId") == job_id
        assert verified.get("seed") == subject.get("seed") and verified.get("verified") is True
        sha = verified.get("sha256", "")
        assert isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha)
        assert choice.get("image_sha256") == sha, "Only select the exact image reviewed in the authenticated receipt"
        chosen[section] = (subject, image_id)
    assert len({id for _, id in chosen.values()}) == 3
    return chosen


def build_stage19(stage19, chosen):
    """Returns brand-new idempotent cells and source-preserving strengths."""
    assert stage19["round"] == "gamebook-19-arthemy-stylepass"
    assert stage19["auto_submit"] is False, "Existing/active stage must never be rewritten"
    assert stage19["subjects"] == [], "Do not overwrite existing style jobs"
    assert stage19["is_public"] is False and stage19["cast_loras"] is False
    assert len(stage19["lanes"]) == 1
    lane = stage19["lanes"][0]
    assert lane["engine"] == "sdxl-img2img"
    assert lane["checkpoint"] == "Illustrious/arthemyWesternArt_v30.safetensors"
    for idx, section in enumerate(CRITICAL):
        source, image_id = chosen[section]
        prompt, negative = PROMPTS[section]
        for variant, strength in STRENGTHS:
            stage19["subjects"].append({
                "key": f"gb19-{section}-{variant}",
                "title": f"{section} Arthemy {variant} source-preserving style",
                "section": section,
                "entity": "scenery",
                "lane": lane["key"],
                "size": source["size"],
                "source_image_id": image_id,
                "source_krea_key": source["key"],
                "denoise": strength,
                "seed": 28900 + idx * 10 + (0 if variant == "safe" else 1),
                "negative": negative,
                "prompt_tags": prompt,
                "prompt_prose": prompt,
            })
    assert len(stage19["subjects"]) == 6
    stage19["auto_submit"] = True
    return stage19


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round18", type=Path, default=ART / "ROUND-18-KREA-COMPOSITION.yaml")
    parser.add_argument("--selections", type=Path, default=ART / "ROUND-18-SELECTIONS.yaml")
    parser.add_argument("--receipt", type=Path, required=True, help="Authenticated ephemeral Round 18 review receipt")
    parser.add_argument("--stage19", type=Path, default=ART / "ROUND-19-ARTHEMY-STYLEPASS.yaml")
    parser.add_argument("--output", type=Path, required=True, help="New YAML file to submit in reviewed PR")
    args = parser.parse_args(argv)
    inputs = [args.round18, args.selections, args.receipt, args.stage19]
    if args.output.exists():
        parser.error("output exists: refusing to overwrite any existing job ledger")
    ledger, selections, template = (
        yaml.safe_load(args.round18.read_text()),
        yaml.safe_load(args.selections.read_text()),
        yaml.safe_load(args.stage19.read_text()),
    )
    receipt = json.loads(args.receipt.read_text())
    chosen = approved_sources(ledger, selections, receipt)
    stage = build_stage19(template, chosen)
    args.output.write_text(yaml.safe_dump(stage, sort_keys=False))
    print("Activated six Arthemy img2img jobs with exact verified Krea source ArtImages")
    for section, (_, image_id) in chosen.items():
        print(f"  {section}: ArtImage {image_id}, denoise 0.28 / 0.43")
    print("Review generated output and commit by PR; do not ship automatically.")


if __name__ == "__main__":
    main()
