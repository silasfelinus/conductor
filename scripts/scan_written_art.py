#!/usr/bin/env python3
"""scan_written_art.py -- find art that is WRITTEN but neither queued nor delivered.

WHY THIS EXISTS. Silas, 2026-11-02 PT: "we spent about 12 hours today not making art, if it's
written, it should be in the queue." That night the render box sat idle while thousands of authored
prompts waited: Crystal Street's 2,728 outcome plates, Ruler Hooked's Forge beats, The Lantern
Ferry's briefs. Nothing reported them, because every existing check (art_queue_health,
sweep_art_ledgers) only looks at prompts someone had already put in a ledger.

This reads the prompts where they are authored, in a kind_robots checkout:
  * every Playbook Studio game's beats (artPrompt + needsArt + runtime path), and
  * game-owned prompt lists outside the Forge (Crystal Street's allArtPrompts()),
then drops everything already accounted for:
  * a conductor ledger subject with the same asset or the same prompt text,
  * a file already shipped in the kind_robots checkout (extras) or verified on the production
    image store (GET /api/admin/playbook-ledger/<game>?inventory=1),
  * a live or finished ArtJob: the Forge's art-request notes, or any job for the project whose
    prompt contains this prompt.
What is left is written art nobody has queued.

    python scripts/scan_written_art.py                 # report; exit 1 when anything is left
    python scripts/scan_written_art.py --json          # machine-readable
    python scripts/scan_written_art.py --write         # also write auto_submit backlog ledgers

--write writes projects/<project>/art/WRITTEN-BACKLOG-<date>.yaml (priority 1: renders only when
no game, Hybridizer or interactive job waits; auto_submit, private), which the Auto Art Generate
sweep submits after merge. Very large rounds are split into parts of --part-size subjects.

Needs: a kind_robots checkout (--kind-robots, default ../kind_robots), Node with npx (tsx), and
KR_API_TOKEN for the production checks. Without the token the job and inventory checks are skipped
and the run exits 2 (unresolved), never 0.
Exit codes: 0 nothing unqueued, 1 unqueued written art found, 2 could not check.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

TSX = "tsx@4.19.2"
# 426 ledger files take ~22s with the pure-Python loader and ~3s with libyaml's.
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
PRIORITY = 1
DUMPER = r"""// Dump every authored art prompt Kind Robots carries, for scripts/scan_written_art.py.
//
// Run from a kind_robots checkout (tsx resolves its imports there):
//   KR_DIR=../kind_robots npx -y tsx@4.19.2 scripts/ts/dump_written_art.ts > written-art.json
//
// Two sources:
//   playbooks  every Playbook Studio game: each beat's authored artPrompt, whether the game
//              still needs a picture for it, and its runtime path when it has one.
//   extras     game-owned prompt lists that are not Playbook beats (Crystal Street's
//              allArtPrompts(): outcome plates, endings, items...), keyed by runtime asset.
async function main() {
  const root = process.env.KR_DIR
  if (!root) throw new Error('KR_DIR must point at a kind_robots checkout')
  const { PLAYBOOK_GAMES, buildPlaybook } = await import(
    root + '/utils/playbook/games'
  )
  const playbooks = []
  for (const game of PLAYBOOK_GAMES) {
    try {
      const book = buildPlaybook(game.id)
      playbooks.push({
        game: game.id,
        title: book.title,
        artProject: book.artProject,
        artStyle: book.artStyle ?? null,
        artNegative: book.artNegative ?? null,
        nodes: Object.values(book.nodes).map((n: any) => ({
          key: n.key,
          kind: n.kind,
          title: n.title,
          needsArt: n.needsArt,
          artUrl: n.artUrl,
          artPath: n.artPath ?? null,
          art: n.art,
          prompt: n.artPrompt?.trim() || null,
        })),
      })
    } catch (error) {
      playbooks.push({ game: game.id, error: String(error) })
    }
  }

  const cs = await import(root + '/utils/crystalStreet/artPrompts')
  const r = await import(root + '/utils/crystalStreet/rules')
  const crystal = cs.allArtPrompts({
    villains: r.VILLAINS,
    companions: r.COMPANIONS,
    locations: r.LOCATIONS,
    decks: r.DECKS,
    items: r.ITEMS,
    avatars: r.AVATARS,
    cliques: r.ARCHETYPES,
    characters: r.CHARACTERS,
    specialEndings: r.SPECIAL_ENDINGS,
    title: r.TITLE_ART,
  })
  const extras = [
    {
      project: 'crystal-street',
      publicDir: 'public/crystal-street',
      suffix: cs.BEAT_ART_MEDIUM,
      prompts: crystal,
    },
  ]
  console.log(JSON.stringify({ playbooks, extras }))
}

main().catch((error) => {
  console.error(error)
  process.exit(1)
})
"""

# Runtime sizes for extras by asset folder (the size each game reads); anything else is a scene.
EXTRA_SIZES = {
    "crystal-street": {"outcomes": "1216x832", "scenes": "1216x832", "endings": "1344x768",
                       "items": "1024x1024", "avatars": "832x1216", "characters": "832x1216",
                       "villains": "832x1216", "companions": "896x1152", "cliques": "1024x1024",
                       "locations": "1344x768", "title": "1216x832"},
}


def norm(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()[:160]


def asset_key(value: str | None) -> str | None:
    if not value or " " in value:
        return None
    key = re.sub(r"\.(webp|png|jpe?g|avif|gif)$", "", value.strip().lstrip("/")).lower()
    return key[len("images/"):] if key.startswith("images/") else key


def dump(kind_robots: Path) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "dump_written_art.ts"
        script.write_text(DUMPER)
        local = kind_robots / "node_modules" / ".bin" / "tsx"
        runner = [str(local)] if local.exists() else ["npx", "--prefer-offline", "-y", TSX]
        proc = subprocess.run([*runner, str(script)], cwd=kind_robots, capture_output=True,
                              text=True, env={**os.environ, "KR_DIR": str(kind_robots.resolve())}, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError("dumper failed: " + proc.stderr.strip()[-800:])
    return json.loads(proc.stdout)


def ledger_index(root: Path = ROOT) -> tuple[set[str], set[str]]:
    """Prompt texts and asset keys already written into any conductor ledger or queue file."""
    prompts: set[str] = set()
    assets: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str):
                    if (key.startswith("prompt") or key == "artPrompt") and len(value) > 40:
                        prompts.add(norm(value))
                    elif key in ("asset", "image_path", "target", "imagePath", "url", "src"):
                        found = asset_key(value)
                        if found:
                            assets.add(found)
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for path in list(root.glob("projects/**/*.yaml")) + list(root.glob("projects/**/*.json")):
        if path.name == "roadmap.yaml" or "HISTORY" in path.name:
            continue
        try:
            data = yaml.load(path.read_text(), Loader=LOADER) if path.suffix == ".yaml" else json.loads(path.read_text())
        except Exception:
            continue
        walk(data)
    return prompts, assets


def candidates(dumped: dict, kind_robots: Path) -> list[dict]:
    """Every authored prompt that still needs a picture, before any queue checks."""
    out: list[dict] = []
    for book in dumped.get("playbooks", []):
        if "error" in book:
            continue
        for node in book["nodes"]:
            if not (node.get("needsArt") and node.get("prompt")):
                continue
            target = node.get("artPath") or node.get("artUrl") or node.get("art")
            asset = asset_key(target) or f"playbook/{book['game']}/{node['key']}"
            out.append({
                "source": "playbook", "game": book["game"], "project": book["artProject"],
                "key": node["key"], "kind": node["kind"], "title": node["title"], "asset": asset,
                "prompt": node["prompt"], "suffix": book.get("artStyle"), "negative": book.get("artNegative"),
                "size": "832x1216" if node["kind"] == "follower" else "1344x768",
            })
    for extra in dumped.get("extras", []):
        public = kind_robots / extra["publicDir"]
        sizes = EXTRA_SIZES.get(extra["project"], {})
        for item in extra["prompts"]:
            if not (item.get("prompt") or "").strip():
                continue
            if (public / f"{item['key']}.webp").exists():
                continue
            folder = item["key"].split("/", 1)[0]
            out.append({
                "source": "extra", "game": extra["project"], "project": extra["project"],
                "key": item["key"], "kind": folder, "title": item["key"].split("/", 1)[-1].replace("-", " "),
                "asset": item["key"], "prompt": item["prompt"].strip(), "suffix": extra.get("suffix"),
                "negative": None, "size": sizes.get(folder, "1344x768"),
            })
    return out


def already_ledgered(cell: dict, prompts: set[str], assets: set[str]) -> bool:
    if norm(cell["prompt"]) in prompts:
        return True
    asset = cell["asset"].lower()
    tail = asset.split("/", 1)[1] if "/" in asset else asset
    return bool({asset, tail, f"{cell['project']}/{asset}"} & assets)


def production_filter(cells: list[dict]) -> list[dict]:
    """Drop cells the server shows as delivered or already rendering (needs KR_API_TOKEN)."""
    import consume_art_queue_core as core

    by_game: dict[str, list[dict]] = {}
    for cell in cells:
        by_game.setdefault(cell["game"], []).append(cell)

    def check(game: str, group: list[dict]) -> list[dict]:
        left: list[dict] = []
        verified, by_node = {}, {}
        if group[0]["source"] == "playbook":
            _, inv = core.http_json("GET", f"{core.KR_BASE_URL}/api/admin/playbook-ledger/{game}?inventory=1")
            verified = ((inv or {}).get("data") or {}).get("verified") or {}
            _, led = core.http_json("GET", f"{core.KR_BASE_URL}/api/admin/playbook-ledger/{game}")
            by_node = ((led or {}).get("data") or {}).get("byNode") or {}
        seen: set[str] = set()
        page = 1
        while page <= 60:
            _, res = core.http_json(
                "GET", f"{core.KR_BASE_URL}/api/art/queue?projectSlug={group[0]['project']}&pageSize=200&page={page}")
            data = (res or {}).get("data") or {}
            items = data.get("items") or data.get("jobs") or []
            for job in items:
                if job.get("status") in ("PENDING", "RUNNING", "DONE"):
                    text = job.get("promptString") or (job.get("payload") or {}).get("promptString") or ""
                    seen.add(norm(text))
            if len(items) < 200:
                break
            page += 1
        for cell in group:
            if cell["key"] in verified:
                continue
            if any(j.get("status") in ("PENDING", "RUNNING", "DONE") for j in by_node.get(cell["key"], [])):
                continue
            probe = norm(cell["prompt"])[:80]
            if any(probe in text for text in seen):
                continue
            left.append(cell)
        return left

    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda item: check(*item), by_game.items()))
    return [cell for left in results for cell in left]


def write_ledgers(cells: list[dict], part_size: int, today: str) -> list[Path]:
    written: list[Path] = []
    groups: dict[tuple[str, str], list[dict]] = {}
    for cell in cells:
        groups.setdefault((cell["project"], cell["game"]), []).append(cell)
    for (project, game), group in sorted(groups.items()):
        parts = [group[i:i + part_size] for i in range(0, len(group), part_size)]
        for index, part in enumerate(parts, 1):
            stem = f"WRITTEN-BACKLOG-{today}" + (f"-{game.upper()}" if game != project else "")
            stem += f"-PART-{index}" if len(parts) > 1 else ""
            path = ROOT / "projects" / project / "art" / f"{stem}.yaml"
            path.parent.mkdir(parents=True, exist_ok=True)
            lane = {"key": "krea2", "label": "Krea 2, written-art backlog", "engine": "krea2", "prompt": "prose"}
            if part[0].get("suffix"):
                lane["suffix"] = part[0]["suffix"]
            base = sum(ord(ch) for ch in f"{project}{game}") * 1000 + index * 100000
            subjects = []
            for offset, cell in enumerate(part):
                subject = {
                    "key": "wb-" + re.sub(r"[^a-z0-9-]+", "-", cell["key"].lower()).strip("-"),
                    "lane": "krea2", "entity": cell["kind"], "title": cell["title"], "asset": cell["asset"],
                    "size": cell["size"], "seed": base + offset, "prompt_prose": cell["prompt"],
                }
                if cell["source"] == "playbook":
                    subject["playbook_node"] = cell["key"]
                if cell.get("negative"):
                    subject["negative"] = cell["negative"]
                subjects.append(subject)
            header = (
                f"# Written-but-unqueued art for {project} ({game}), found by scripts/scan_written_art.py on {today}.\n"
                "# Authored prompts with no delivered file, no conductor ledger entry and no live or finished ArtJob.\n"
                "# Silas, 2026-11-02 PT: \"if it's written, it should be in the queue.\" Priority 1: renders only when no\n"
                "# game, Hybridizer or interactive job waits. auto_submit: true. Private. Queued is not delivered.\n"
            )
            ledger = {
                "round": f"{project}-{game}-written-backlog-{today}" + (f"-part-{index}" if len(parts) > 1 else ""),
                "project_slug": project, "designer": "written-art backlog", "is_public": False, "is_mature": False,
                "cast_loras": False, "priority": PRIORITY, "auto_submit": True, "lanes": [lane], "subjects": subjects,
            }
            path.write_text(header + yaml.safe_dump(ledger, sort_keys=False, width=110, allow_unicode=True))
            written.append(path)
    return written


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind-robots", default=str(ROOT.parent / "kind_robots"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true", help="write auto_submit backlog ledgers")
    parser.add_argument("--part-size", type=int, default=700)
    args = parser.parse_args(argv)

    kind_robots = Path(args.kind_robots)
    if not (kind_robots / "utils" / "playbook" / "games.ts").exists():
        print(f"scan_written_art: no kind_robots checkout at {kind_robots}", file=sys.stderr)
        return 2
    try:
        dumped = dump(kind_robots)
    except Exception as error:  # noqa: BLE001 -- surfaced as unresolved, never as clean
        print(f"scan_written_art: {error}", file=sys.stderr)
        return 2
    prompts, assets = ledger_index()
    cells = [c for c in candidates(dumped, kind_robots) if not already_ledgered(c, prompts, assets)]
    token = bool(os.environ.get("KR_API_TOKEN"))
    if token:
        cells = production_filter(cells)

    counts: dict[str, int] = {}
    for cell in cells:
        counts[cell["project"]] = counts.get(cell["project"], 0) + 1
    if args.json:
        print(json.dumps({"unqueued": counts, "checked_production": token}, indent=2))
    elif counts:
        total = sum(counts.values())
        print(f"Written but unqueued art: {total} picture(s) across {len(counts)} project(s)"
              + ("" if token else " (ledger check only: set KR_API_TOKEN for delivery and job checks)"))
        for project, count in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {project}: {count}")
        print("Queue it: python scripts/scan_written_art.py --write, then PR the new ledgers.")
    else:
        print("No written-but-unqueued art: every authored prompt is delivered, ledgered or rendering.")
    if args.write and cells:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        for path in write_ledgers(cells, args.part_size, today):
            print(f"wrote {path.relative_to(ROOT)}")
    if not token:
        return 2
    return 1 if counts else 0


if __name__ == "__main__":
    sys.exit(main())
