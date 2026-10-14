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
over every active request and project image. Run it before pushing hand-written
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kr-repo", default=str(ROOT.parent / "kind_robots"))
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--project", help="only this project_slug")
    args = ap.parse_args(argv)

    try:
        contract = git_show(Path(args.kr_repo), args.ref, CONTRACT)
        quality = git_show(Path(args.kr_repo), args.ref, QUALITY)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"cannot read the contract from {args.kr_repo} at {args.ref}: {exc}", file=sys.stderr)
        return 2
    # The two edits that let Node run the server file standalone: h3 is only
    # used to throw in assertArtPromptContract, and ESM needs the extension.
    contract = contract.replace("import { createError } from 'h3'",
                                "const createError = (e: unknown) => new Error(String(e))")
    contract = contract.replace("from './artPromptQuality'", "from './artPromptQuality.ts'")

    checked = rows(args.project)
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "contract.ts").write_text(contract)
        (t / "artPromptQuality.ts").write_text(quality)
        (t / "run.ts").write_text(RUNNER)
        (t / "rows.json").write_text(json.dumps(checked))
        proc = subprocess.run(["node", "--experimental-strip-types", "--no-warnings",
                               str(t / "run.ts"), str(t / "rows.json")],
                              capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"node could not run the contract:\n{proc.stderr.strip()}", file=sys.stderr)
        return 2

    bad = [r for r in json.loads(proc.stdout) if r["violations"]]
    for r in bad:
        for v in r["violations"]:
            print(f"  [{v['rule']}] {r['id']}: {v['detail'][:200]}")
    print(f"live contract: {len(checked) - len(bad)}/{len(checked)} prompts pass ({args.ref})")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
