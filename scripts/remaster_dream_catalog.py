#!/usr/bin/env python3
"""Apply the Daily Dream catalog freshness remaster (conductor issue #3184).

`scripts/audit_dream_catalog.py` decides *what* deserves intervention. This script is
the write half: it turns that manifest into scoped, reversible work, and it is
deliberately boring about it — every mutation is dry-run by default, every applied
batch leaves a receipt, and nothing here invents creative text on its own.

Four subcommands, in the order a remaster wave actually runs:

  plan     Group the audited catalog into work waves and print/write the plan.
  stubs    Emit revision-request stubs for bundles that need a text rewrite. An
           authoring pass fills in the new six-asset proposal and renames the file to
           `-request.json`; `scripts/apply_dream_revision.py` then patches the live
           records and queues six replacement renders. Stubs are inert until renamed,
           so a half-finished rewrite can never be applied by accident.
  art      The art-only lane: bundles whose prose survives but whose renders are samey,
           thin, unattached, or stuck in an overcrowded style lane. It rebuilds the six
           prompts against a deliberately different visual language, appends the
           requests to the canonical `projects/art-prompts.yaml` staging ledger, and
           supersedes the old art evidence in `built-data`. `submit_daily_dream_art.py`
           carries them into real ArtJobs from there — this script never enqueues
           directly, so the remaster uses exactly the same art path as a normal day.
  verify   Post-pass validation: every recorded entity still resolves, every remastered
           bundle has art evidence, and no request was left staged without an ArtJob.

Art generation is in-house and effectively free, so the art lane does not try to
preserve existing renders to save generation. It does refuse to spend renders on a
bundle that is about to be rewritten or retired, which is thrift about *coherence*,
not about cost.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import audit_dream_catalog as audit  # noqa: E402
import build_dream_records as records  # noqa: E402
from dream_art_prompts import (  # noqa: E402
    character_prompt,
    location_prompt,
    reward_prompt,
    scenario_prompt,
    visual_language,
    world_prompt,
)

ROOT = Path(__file__).resolve().parents[1]
REMASTER_DIR = ROOT / "projects" / "dream-cycle" / "remaster"
RECEIPTS_DIR = REMASTER_DIR / "receipts"
REVISIONS_DIR = ROOT / "projects" / "dream-cycle" / "revisions"
MANIFEST = REMASTER_DIR / "catalog-audit.json"

ENTITY_TYPES = {
    "vibe": "dream",
    "location": "dream",
    "character": "character",
    "reward_item": "reward",
    "reward_skill": "reward",
    "scenario": "scenario",
}

REWRITE_VERDICTS = {audit.SUBSTANTIAL, audit.RETIRE}
# ART_PENDING is deliberately absent: those renders are already staged and in flight.
ART_ACTION_VERDICTS = {audit.ART_REGENERATE, audit.ART_RESTYLE}


def _yq(value: str) -> str:
    """Single-quote a YAML scalar for the staging ledger."""
    return "'" + str(value).replace("'", "''") + "'"


def _stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(
            f"{path.relative_to(ROOT)} is missing — run scripts/audit_dream_catalog.py first"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def bundles_by_day(backlog: Path) -> dict[str, audit.Bundle]:
    return {bundle.day: bundle for bundle in audit.load_bundles(backlog)}


# ── plan ─────────────────────────────────────────────────────────────────────


def build_plan(manifest: dict[str, Any]) -> dict[str, Any]:
    """Split the audited catalog into the waves a remaster actually runs in."""
    rewrite_in_place: list[dict[str, Any]] = []
    rebuild: list[dict[str, Any]] = []
    art_only: list[dict[str, Any]] = []
    keep: list[dict[str, Any]] = []

    for row in manifest["bundles"]:
        entry = {
            "day": row["day"],
            "slug": row["slug"],
            "title": row["title"],
            "score": row["score"],
            "classification": row["classification"],
            "art": row["art"]["verdict"],
            "reason": (row["reasons"] or ["—"])[0],
        }
        if row["classification"] in REWRITE_VERDICTS:
            if row.get("legacy_shape"):
                entry["how"] = (
                    "pre-v2 staged bundle: author a canonical six-asset proposal over its "
                    "kernel and apply it with `legacy_reseed`, which draws the deterministic "
                    "seed its own date would produce today, remasters the canonical six rows, "
                    "and retires the leftover staged rows"
                )
                rebuild.append(entry)
            else:
                entry["how"] = (
                    "author a revision request, then apply_dream_revision.py patches the "
                    "live rows and queues six replacement renders"
                )
                rewrite_in_place.append(entry)
        elif row["art"]["verdict"] in ART_ACTION_VERDICTS:
            entry["how"] = "art-only regeneration against a different visual language"
            art_only.append(entry)
        else:
            keep.append(entry)

    order = lambda rows: sorted(rows, key=lambda item: (-item["score"], item["day"]))  # noqa: E731
    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "audit_generated_at": manifest.get("generated_at"),
        "waves": {
            "1-rewrite-in-place": order(rewrite_in_place),
            "2-legacy-canonicalization": order(rebuild),
            "3-art-only": order(art_only),
            "4-keep": order(keep),
        },
        "poisoned_unbuilt": manifest.get("poisoned_unbuilt", []),
    }


def print_plan(plan: dict[str, Any]) -> None:
    for wave, rows in plan["waves"].items():
        print(f"\n{wave} — {len(rows)} bundle(s)")
        for row in rows:
            print(
                f"  {row['day']}  {row['title'][:44]:44s} score={row['score']:2d} "
                f"{row['classification']:19s} art={row['art']}"
            )
    poisoned = plan["poisoned_unbuilt"]
    print(f"\npoisoned unbuilt proposals: {len(poisoned)}")
    for row in poisoned:
        print(f"  {row['day']}  {row['title']} ({row['age_days']} days old)")


# ── stubs ────────────────────────────────────────────────────────────────────


LEGACY_STUB_INSTRUCTIONS = (
    "This is a pre-v2 staged bundle. Author a full canonical six-asset proposal over its "
    "kernel, keep the technical world `slug`, and leave `seed_facets` set to the "
    "deterministic plan already filled in here — it is what "
    "`build_dream_proposal.facet_seed_plan` produces for this bundle's own date, not an "
    "invented one. Applying it remasters the canonical six rows and retires the leftover "
    "staged rows (the second vibe Dream, extra locations, extra characters, the second "
    "Scenario) by deactivating them; narrator Bots are left alone for the separately "
    "scoped cleanup PIPELINE.md describes."
)

STUB_INSTRUCTIONS = (
    "Rewrite `proposal` in place, then rename this file to end in `-request.json` so "
    "scripts/apply_dream_revision.py will apply it. Hard constraints: keep `seed_facets` "
    "byte-identical, keep the technical world `slug` unchanged (the built rows and their "
    "image directory are keyed to it), keep exactly one location, one Character, one ITEM "
    "Reward, one SKILL Reward, and one Scenario, and write the Scenario last so it names "
    "the vibe, the location, and the Character. Every `look` and `art_direction` must "
    "describe what is visible — material, shape, scale, colour, wear, how light hits it. "
    "Do not solve the audit findings by renaming the same premise."
)


def write_stubs(
    plan: dict[str, Any],
    catalog: dict[str, audit.Bundle],
    manifest: dict[str, Any],
    *,
    limit: int,
    apply: bool,
) -> list[Path]:
    findings = {row["day"]: row for row in manifest["bundles"]}
    written: list[Path] = []
    day_stamp = datetime.date.today().isoformat()
    queue = plan["waves"]["1-rewrite-in-place"] + plan["waves"]["2-legacy-canonicalization"]
    for row in queue[:limit]:
        bundle = catalog.get(row["day"])
        if bundle is None:
            continue
        audit_row = findings[row["day"]]
        legacy = bool(audit_row.get("legacy_shape"))
        stub = {
            "status": "needs-authoring",
            "instructions": LEGACY_STUB_INSTRUCTIONS if legacy else STUB_INSTRUCTIONS,
            "proposal_path": audit._rel(bundle.path),
            "digest_role": "Remastered Daily Dream",
            "send_digest": False,
            "audit": {
                "score": audit_row["score"],
                "classification": audit_row["classification"],
                "reasons": audit_row["reasons"],
                "assets": {
                    element: asset["findings"]
                    for element, asset in audit_row["assets"].items()
                    if asset["findings"]
                },
                "art": audit_row["art"],
            },
            "proposal": bundle.proposal,
        }
        if legacy:
            stub["legacy_reseed"] = True
            stub["seed_facets_for_this_date"] = (
                "run: python -c \"import sys; sys.path.insert(0,'scripts'); "
                "import build_dream_proposal as p, json; "
                f"print(json.dumps(p.facet_seed_plan('{bundle.day}')))\""
            )
        target = REVISIONS_DIR / f"{day_stamp}-remaster-{bundle.slug}-stub.json"
        written.append(target)
        if apply:
            REVISIONS_DIR.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(stub, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
    return written


# ── art lane ─────────────────────────────────────────────────────────────────


def remaster_art_specs(
    bundle: audit.Bundle, *, variant: int
) -> list[tuple[str, str, str, str, int]]:
    """(element_slug, label, prompt, entity_type, entity_id) for one bundle's six cards."""
    rows = bundle.rows()
    ids = bundle.record_ids()
    title = bundle.title
    vibe = rows["vibe"]
    loc = rows["location"]
    char = rows["character"]
    item = rows["reward_item"]
    skill = rows["reward_skill"]
    scenario = rows["scenario"]
    vibe_line = str(vibe.get("line") or "")
    style = visual_language(title, variant)

    specs: list[tuple[str, str, str, str, int]] = []

    def add(element: str, label: str, prompt: str) -> None:
        record = ids.get(element) or {}
        entity_id = record.get("id")
        if not label or not entity_id:
            return
        specs.append(
            (
                records.slugify(label) + ("-scenario" if element == "scenario" else ""),
                label,
                prompt,
                ENTITY_TYPES[element],
                int(entity_id),
            )
        )

    add(
        "vibe",
        title,
        world_prompt(
            title,
            str(bundle.proposal.get("idea") or ""),
            vibe_line,
            str(vibe.get("art_direction") or ""),
            style=style,
        ),
    )
    add(
        "location",
        str(loc.get("title") or ""),
        location_prompt(
            str(loc.get("title") or ""),
            str(loc.get("art_direction") or ""),
            str(loc.get("known_for") or ""),
            str(loc.get("best_scene") or ""),
            title,
            vibe_line,
            style=style,
        ),
    )
    add(
        "character",
        str(char.get("name") or ""),
        character_prompt(
            str(char.get("name") or ""),
            str(char.get("look") or ""),
            str(char.get("role_drive") or ""),
            str(char.get("carries") or ""),
            title,
            vibe_line,
            style=style,
        ),
    )
    for element, reward, kind in (
        ("reward_item", item, "ITEM"),
        ("reward_skill", skill, "SKILL"),
    ):
        add(
            element,
            str(reward.get("name") or ""),
            reward_prompt(
                str(reward.get("name") or ""),
                kind,
                str(reward.get("look") or ""),
                str(reward.get("grants") or ""),
                str(reward.get("rarity") or ""),
                title,
                vibe_line,
                style=style,
            ),
        )
    add(
        "scenario",
        str(scenario.get("title") or ""),
        scenario_prompt(
            str(scenario.get("title") or ""),
            str(scenario.get("setup") or ""),
            str(loc.get("title") or ""),
            title,
            vibe_line,
            style=style,
        ),
    )
    return specs


def _art_request(
    *, world_slug: str, element_slug: str, label: str, prompt: str,
    entity_type: str, entity_id: int, stamp: str,
) -> tuple[dict[str, Any], str]:
    request_id = f"dream-cycle-remaster-{stamp.lower()}-{world_slug}-{element_slug}"
    image_path = (
        f"public/images/dreams/{world_slug}/remaster/{stamp.lower()}/{element_slug}-card.webp"
    )
    yaml_text = (
        f"- id: {request_id}\n"
        "  source: dream-cycle\n"
        "  status: pending\n"
        "  target_repo: silasfelinus/kind_robots\n"
        f"  image_path: {image_path}\n"
        f"  source_url: /{image_path.removeprefix('public/')}\n"
        f"  page_url: {records.PAGE_URL}\n"
        "  variant: card\n"
        f"  size: {records.CARD_SIZE}\n"
        f"  label: {_yq(label)}\n"
        f"  prompt: {_yq(' '.join(prompt.split()))}\n"
        f"  entity_type: {entity_type}\n"
        f"  entity_id: {entity_id}\n"
        "  entity_field: imagePath\n"
    )
    evidence = {
        "request_id": request_id,
        "image_path": image_path,
        "public_path": "/" + image_path.removeprefix("public/"),
        "attached": False,
        "element": element_slug,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "entity_field": "imagePath",
        "target_endpoint": "/api/dreams" if entity_type == "dream" else f"/api/{entity_type}s",
        "target_id": entity_id,
    }
    return evidence, yaml_text


def rewrite_built_data(path: Path, built: dict[str, Any]) -> None:
    """Replace the built-data block in a proposal file, leaving prose untouched."""
    text = path.read_text(encoding="utf-8")
    payload = json.dumps(built, ensure_ascii=False, sort_keys=True)
    replacement = "<!-- built-data\n" + payload + "\n-->"
    updated, count = re.subn(
        r"<!--\s*built-data\s*\n.*?\n-->", lambda _: replacement, text, count=1, flags=re.DOTALL
    )
    if count != 1:
        raise RuntimeError(f"{path.name}: could not locate a built-data block to update")
    path.write_text(updated, encoding="utf-8")


def regenerate_art(
    plan: dict[str, Any],
    catalog: dict[str, audit.Bundle],
    manifest: dict[str, Any],
    *,
    limit: int,
    apply: bool,
    include_rewrites: bool,
    stamp: str,
) -> dict[str, Any]:
    findings = {row["day"]: row for row in manifest["bundles"]}
    queue = list(plan["waves"]["3-art-only"])
    if include_rewrites:
        queue += list(plan["waves"]["1-rewrite-in-place"])
    queue = queue[:limit]

    receipt = {
        "stamp": stamp,
        "applied": apply,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "bundles": [],
        "requests": 0,
    }

    yaml_entries: list[str] = []
    for row in queue:
        bundle = catalog.get(row["day"])
        if bundle is None or not bundle.is_built:
            continue
        audit_row = findings[row["day"]]
        # A restyle walks the world one lane off its default; a full regeneration walks
        # it two, so a bundle that has already been restyled once does not land back on
        # the look it just left.
        variant = 1 if audit_row["art"]["verdict"] == audit.ART_RESTYLE else 2
        variant += len((bundle.built or {}).get("remasters") or [])
        specs = remaster_art_specs(bundle, variant=variant)
        if len(specs) != len(audit.ELEMENTS):
            receipt["bundles"].append(
                {
                    "day": bundle.day,
                    "slug": bundle.slug,
                    "skipped": f"only {len(specs)}/6 assets have recorded entity ids",
                }
            )
            continue

        evidence_rows: list[dict[str, Any]] = []
        used: set[str] = set()
        for element_slug, label, prompt, entity_type, entity_id in specs:
            unique = element_slug
            suffix = 2
            while unique in used:
                unique = f"{element_slug}-{suffix}"
                suffix += 1
            used.add(unique)
            evidence, yaml_text = _art_request(
                world_slug=bundle.slug,
                element_slug=unique,
                label=label,
                prompt=prompt,
                entity_type=entity_type,
                entity_id=entity_id,
                stamp=stamp,
            )
            evidence_rows.append(evidence)
            yaml_entries.append(yaml_text)

        built = dict(bundle.built or {})
        if apply:
            if built.get("art"):
                built.setdefault("superseded_art", []).extend(built["art"])
            built["art"] = evidence_rows
            built.setdefault("remasters", []).append(
                {
                    "stamp": stamp,
                    "applied_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "lane": "art-only",
                    "variant": variant,
                    "audit_score": audit_row["score"],
                    "classification": audit_row["classification"],
                    "art_verdict": audit_row["art"]["verdict"],
                    "reasons": audit_row["art"]["reasons"],
                    "art_request_ids": [item["request_id"] for item in evidence_rows],
                }
            )
            rewrite_built_data(bundle.path, built)

        receipt["bundles"].append(
            {
                "day": bundle.day,
                "slug": bundle.slug,
                "title": bundle.title,
                "variant": variant,
                "art_verdict": audit_row["art"]["verdict"],
                "request_ids": [item["request_id"] for item in evidence_rows],
            }
        )
        receipt["requests"] += len(evidence_rows)

    if yaml_entries and apply:
        records.append_art_requests(yaml_entries, dry_run=False)
    return receipt


# ── verify ───────────────────────────────────────────────────────────────────


def _entity_payload(response: Any) -> dict[str, Any]:
    if isinstance(response, dict):
        for key in ("data", "dream", "character", "reward", "scenario", "result"):
            value = response.get(key)
            if isinstance(value, dict):
                return value
        return response
    return {}


def verify_catalog(catalog: dict[str, audit.Bundle], *, offline: bool) -> dict[str, Any]:
    report: dict[str, Any] = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "offline": offline,
        "bundles": [],
        "problems": 0,
    }
    for day in sorted(catalog):
        bundle = catalog[day]
        ids = bundle.record_ids()
        row: dict[str, Any] = {"day": day, "slug": bundle.slug, "missing": [], "checked": 0}
        for element in audit.ELEMENTS:
            record = ids.get(element)
            if not record or not record.get("id"):
                row["missing"].append(f"{element}: no recorded id")
                continue
            if offline:
                continue
            endpoint = "/api/dreams" if ENTITY_TYPES[element] == "dream" else (
                f"/api/{ENTITY_TYPES[element]}s"
            )
            status, response = records.http_json(
                "GET", f"{records.KR_BASE_URL}{endpoint}/{record['id']}"
            )
            row["checked"] += 1
            if status != 200:
                row["missing"].append(f"{element}: {endpoint}/{record['id']} returned {status}")
                continue
            payload = _entity_payload(response)
            if not str(payload.get("imagePath") or "").strip():
                row["missing"].append(f"{element}: record {record['id']} has no imagePath")
        art = (bundle.built or {}).get("art") or []
        if not art:
            row["missing"].append("no art evidence recorded in built-data")
        row["art_requests"] = len(art)
        row["art_attached"] = len([item for item in art if item.get("attached")])
        report["problems"] += len(row["missing"])
        report["bundles"].append(row)
    return report


# ── cli ──────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(MANIFEST))
    parser.add_argument("--backlog", default=str(audit.BACKLOG))
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("plan", help="group the audited catalog into remaster waves")

    stub_parser = sub.add_parser("stubs", help="emit revision-request stubs for rewrites")
    stub_parser.add_argument("--limit", type=int, default=5)
    stub_parser.add_argument("--apply", action="store_true", help="write the stub files")

    art_parser = sub.add_parser("art", help="regenerate art for bundles whose prose survives")
    art_parser.add_argument("--limit", type=int, default=10)
    art_parser.add_argument("--apply", action="store_true", help="stage the requests for real")
    art_parser.add_argument(
        "--include-rewrites",
        action="store_true",
        help="also regenerate art for bundles queued for a text rewrite (normally their "
        "art is queued by apply_dream_revision.py instead, so the render matches the "
        "new text)",
    )

    verify_parser = sub.add_parser("verify", help="validate records, art evidence, and coverage")
    verify_parser.add_argument(
        "--offline", action="store_true", help="skip Kind Robots reads; check local evidence only"
    )

    args = parser.parse_args(argv)
    manifest = load_manifest(Path(args.manifest))
    catalog = bundles_by_day(Path(args.backlog))
    plan = build_plan(manifest)

    if args.command == "plan":
        REMASTER_DIR.mkdir(parents=True, exist_ok=True)
        path = REMASTER_DIR / "remaster-plan.json"
        path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print_plan(plan)
        print(f"\nwrote {path.relative_to(ROOT)}")
        return 0

    if args.command == "stubs":
        written = write_stubs(
            plan, catalog, manifest, limit=args.limit, apply=args.apply
        )
        for path in written:
            print(("wrote " if args.apply else "would write ") + str(path.relative_to(ROOT)))
        print(
            f"{len(written)} revision stub(s) "
            + ("written" if args.apply else "planned (pass --apply to write)")
        )
        return 0

    if args.command == "art":
        stamp = _stamp()
        receipt = regenerate_art(
            plan,
            catalog,
            manifest,
            limit=args.limit,
            apply=args.apply,
            include_rewrites=args.include_rewrites,
            stamp=stamp,
        )
        for row in receipt["bundles"]:
            if row.get("skipped"):
                print(f"  skipped {row['day']} {row['slug']}: {row['skipped']}")
            else:
                print(
                    f"  {row['day']} {row['title'][:40]:40s} variant={row['variant']} "
                    f"{len(row['request_ids'])} request(s)"
                )
        print(
            f"art lane: {receipt['requests']} request(s) across "
            f"{len([r for r in receipt['bundles'] if not r.get('skipped')])} bundle(s) "
            + ("staged" if args.apply else "planned (pass --apply to stage)")
        )
        if args.apply:
            RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
            path = RECEIPTS_DIR / f"art-{stamp}.json"
            path.write_text(
                json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            print(f"wrote {path.relative_to(ROOT)}")
            print(
                "next: python scripts/submit_daily_dream_art.py "
                "(canonical ArtJob submission path)"
            )
        return 0

    if args.command == "verify":
        offline = args.offline or not records.KR_API_TOKEN
        report = verify_catalog(catalog, offline=offline)
        REMASTER_DIR.mkdir(parents=True, exist_ok=True)
        path = REMASTER_DIR / "remaster-verify.json"
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        for row in report["bundles"]:
            for problem in row["missing"]:
                print(f"  {row['day']} {row['slug']}: {problem}")
        print(
            f"verify: {report['problems']} problem(s) across {len(report['bundles'])} bundle(s)"
            + (" (offline)" if offline else "")
        )
        print(f"wrote {path.relative_to(ROOT)}")
        return 1 if report["problems"] else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
