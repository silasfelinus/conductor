#!/usr/bin/env python3
"""check_art_prompts_live_contract.py -- run kind_robots' real prompt contract locally.

tests/test_project_art_prompts_contract.py checks art-prompts.yaml against the
Python mirror of the *negation* rules only. Every other rule in kind_robots'
server/utils/artPromptContract.ts is caught at enqueue, as a 422 that sits in
ops/art-queue-health.yaml until an art-medic session fixes it. On 2026-10-14
fifteen hand-written Save the Plumber requests (#6142, #6145) went that way:
seven sprite sheets said "six frames" / "every frame" ([frame-noun]) and eight
ground tiles said "crisp readable detail" ([art-direction-jargon]).

This runs the authoritative TypeScript itself (no copied regexes) under Node's
type stripping, read from a kind_robots checkout with `git show <ref>:<path>`,
over every active request and project image, and every unsubmitted cell of a
round ledger (projects/*/art/*.yaml, submitted by enqueue_art_requests.py, which
also calls run_contract() before it posts). Run it before pushing hand-written
art rows, and after rewriting a contract-rejected prompt:

    python scripts/check_art_prompts_live_contract.py
    python scripts/check_art_prompts_live_contract.py --project save-the-plumber
    python scripts/check_art_prompts_live_contract.py --kr-repo ../kind_robots --ref origin/main

Exit 0 = every checked prompt passes, 1 = violations listed, 2 = could not run
(no kind_robots checkout, or Node too old to strip types).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ACTIVE = {"pending", "queued", "running", "processing"}
CONTRACT = "server/utils/artPromptContract.ts"
QUALITY = "server/utils/artPromptQuality.ts"

RUNNER = """
import { readFileSync } from 'node:fs'
import { checkArtPromptContract } from './contract.ts'
const rows = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const out = rows.map((r) => ({ id: r.id, violations: checkArtPromptContract(r) }))
process.stdout.write(JSON.stringify(out))
"""


def rows(project: str | None) -> list[dict]:
    data = yaml.safe_load((ROOT / "projects" / "art-prompts.yaml").read_text())
    found = []
    for row in data.get("requests") or []:
        if str(row.get("status", "pending")).strip().lower() not in ACTIVE:
            continue
        if project and row.get("project_slug") != project:
            continue
        if isinstance(row.get("prompt"), str):
            found.append({"id": row.get("id") or row.get("image_path"),
                          "prompt": row["prompt"], "engine": row.get("engine")})
    for entry in data.get("images") or []:
        if project and entry.get("project") != project:
            continue
        for variant, asset in entry.items():
            if isinstance(asset, dict) and isinstance(asset.get("prompt"), str):
                found.append({"id": asset.get("image_path", variant),
                              "prompt": asset["prompt"], "engine": asset.get("engine")})
    return found


def git_show(repo: Path, ref: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def ledger_rows(paths: list[Path] | None = None) -> list[dict]:
    """Unsubmitted cells of the round ledgers (projects/*/art/*.yaml with lanes and subjects).

    enqueue_art_requests.py submits these. Its own guard mirrored only the negation rules,
    so on 2026-10-20 weird-humboldt ck-grove went out twice with "rising out of frame"
    ([frame-noun]: ArtJobs 40921, 40923, 40962)."""
    try:
        from scripts import enqueue_art_requests as enq
    except ImportError:  # pragma: no cover - direct script execution
        import enqueue_art_requests as enq
    found = []
    for path in paths if paths is not None else sorted(ROOT.glob("projects/*/art/*.yaml")):
        try:
            ledger = yaml.safe_load(Path(path).read_text()) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(ledger, dict) or not ledger.get("lanes") or not ledger.get("subjects"):
            continue
        cells = [(s, lane) for s, lane in enq.iter_cells(ledger) if not enq.job_id_of(s, lane.get("key"))]
        for (subject, lane), row in zip(cells, enq.contract_rows(cells)):
            found.append({**row, "id": f"{Path(path).name}:{subject.get('key')}[{lane.get('key')}]"})
    return found


def run_contract(checked: list[dict], kr_repo: str | Path = ROOT.parent / "kind_robots",
                 ref: str = "origin/main") -> list[dict] | None:
    """[{id, violations}] from the real artPromptContract.ts, or None when it cannot run here."""
    try:
        contract = git_show(Path(kr_repo), ref, CONTRACT)
        quality = git_show(Path(kr_repo), ref, QUALITY)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"cannot read the contract from {kr_repo} at {ref}: {exc}", file=sys.stderr)
        return None
    # The two edits that let Node run the server file standalone: h3 is only
    # used to throw in assertArtPromptContract, and ESM needs the extension.
    contract = contract.replace("import { createError } from 'h3'",
                                "const createError = (e: unknown) => new Error(String(e))")
    contract = contract.replace("from './artPromptQuality'", "from './artPromptQuality.ts'")

    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "contract.ts").write_text(contract)
        (t / "artPromptQuality.ts").write_text(quality)
        (t / "run.ts").write_text(RUNNER)
        (t / "rows.json").write_text(json.dumps(checked))
        try:
            proc = subprocess.run(["node", "--experimental-strip-types", "--no-warnings",
                                   str(t / "run.ts"), str(t / "rows.json")],
                                  capture_output=True, text=True)
        except FileNotFoundError:
            print("node is not installed", file=sys.stderr)
            return None
    if proc.returncode != 0:
        print(f"node could not run the contract:\n{proc.stderr.strip()}", file=sys.stderr)
        return None
    return json.loads(proc.stdout)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kr-repo", default=str(ROOT.parent / "kind_robots"))
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--project", help="only this project_slug")
    args = ap.parse_args(argv)

    checked = rows(args.project)
    if args.project:
        checked += ledger_rows(sorted(ROOT.glob(f"projects/{args.project}/art/*.yaml")))
    else:
        checked += ledger_rows()
    results = run_contract(checked, args.kr_repo, args.ref)
    if results is None:
        return 2

    bad = [r for r in results if r["violations"]]
    for r in bad:
        for v in r["violations"]:
            print(f"  [{v['rule']}] {r['id']}: {v['detail'][:200]}")
    print(f"live contract: {len(checked) - len(bad)}/{len(checked)} prompts pass ({args.ref})")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
