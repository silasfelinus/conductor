#!/usr/bin/env python3
"""Audit authored X1-X4 gameplay art using local Rainbow production ledgers.

Read-only: a DONE ledger record is evidence of an ArtImage ID, not evidence
of quality approval, media delivery or in-game integration.

    python scripts/audit_rainbow_gen2_art.py
    python scripts/audit_rainbow_gen2_art.py --strict
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ART_DIR = ROOT / "projects/rainbow-bullet-hell-space-princess/art"
STAGES = ("X1", "X2", "X3", "X4")
ROLES = ("guardian", "pickup", "hazard")
ROLE_FOR_ENTITY = {
    "stage-guardian": "guardian",
    "stage-collectible": "pickup",
    "stage-hazard": "hazard",
}


@dataclass(frozen=True)
class Asset:
    stage: str
    role: str
    path: str
    image_id: int | None
    ledger: str
    key: str


def ledger_paths(art_dir: Path) -> list[Path]:
    """Gen-2 ledgers plus X4's separately authored guardian animation ledger."""
    return sorted({*art_dir.glob("GEN2-*.yaml"), art_dir / "MIRROR-SHOAL-X4.yaml"})


def scan(art_dir: Path) -> list[Asset]:
    """Resolve a DONE image in the chosen lane, not a merely queued job ID."""
    assets = []
    for ledger in ledger_paths(art_dir):
        if not ledger.is_file():
            continue
        data = yaml.safe_load(ledger.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("subjects"), list):
            raise ValueError(f"{ledger.name}: expected a subjects list")
        for subject in data["subjects"]:
            if not isinstance(subject, dict):
                raise ValueError(f"{ledger.name}: subject is not a mapping")
            path = subject.get("asset")
            role = ROLE_FOR_ENTITY.get(subject.get("entity"))
            stage = subject.get("stage")
            # The original X4 pose ledger predates explicit stage/entity fields.
            if (
                ledger.name == "MIRROR-SHOAL-X4.yaml"
                and isinstance(path, str)
                and path.startswith("rainbow-princess-art/doodle/alt/x4-shoalkoi-")
            ):
                stage, role = "X4", "guardian"
            if stage not in STAGES or role is None:
                continue
            key = str(subject.get("key") or "(unknown)")
            if not isinstance(path, str) or not path.strip():
                path = f"(missing asset path for {key})"
            lane = subject.get("lane")
            art = subject.get("art") or {}
            image = art.get(lane) if isinstance(art, dict) else None
            image = image if isinstance(image, dict) else {}
            raw_id = image.get("art_image_id")
            image_id = (
                raw_id
                if image.get("status") == "DONE"
                and type(raw_id) is int
                and raw_id > 0
                else None
            )
            assets.append(Asset(stage, role, path, image_id, ledger.name, key))
    return assets


def report(assets: list[Asset]) -> tuple[str, int]:
    """Show every authored path; call out both absent subjects and missing IDs."""
    grouped: dict[tuple[str, str], dict[str, list[Asset]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for asset in assets:
        grouped[(asset.stage, asset.role)][asset.path].append(asset)

    lines: list[str] = []
    missing = 0
    for stage in STAGES:
        lines.append(f"{stage}:")
        for role in ROLES:
            lines.append(f"  {role}:")
            paths = grouped[(stage, role)]
            if not paths:
                lines.append("    MISSING: no authored asset in the Gen-2 ledgers")
                missing += 1
                continue
            for path, matches in sorted(paths.items()):
                completed = {a.image_id for a in matches if a.image_id is not None}
                if len(completed) == 1:
                    image_id = next(iter(completed))
                    lines.append(f"    ArtImage {image_id}: {path}")
                elif len(completed) > 1:
                    lines.append(f"    CONFLICT: {path} (ArtImages {', '.join(map(str, sorted(completed)))})")
                    missing += 1
                else:
                    refs = ", ".join(sorted({f"{a.ledger}/{a.key}" for a in matches}))
                    lines.append(f"    MISSING: {path} ({refs})")
                    missing += 1
    lines.append(f"Missing or conflicting asset entries: {missing}")
    lines.append("DONE means a ledger ArtImage ID only; delivery and visual QA remain separate.")
    return "\n".join(lines) + "\n", missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--art-dir", type=Path, default=ART_DIR)
    parser.add_argument("--strict", action="store_true", help="fail if authored art is missing or conflicting")
    args = parser.parse_args(argv)
    output, missing = report(scan(args.art_dir))
    print(output, end="")
    return 1 if args.strict and missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
