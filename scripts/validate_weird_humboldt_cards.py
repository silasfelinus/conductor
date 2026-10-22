#!/usr/bin/env python3
"""Validate the Weird Humboldt v1 card deck against the card contract.

Usage:
    python scripts/validate_weird_humboldt_cards.py                # validate, exit 1 on problems
    python scripts/validate_weird_humboldt_cards.py --playtest 7   # text-only hand-playtest, seeded

The contract lives in projects/weird-humboldt/design/card.schema.json (enums are read from it).
Stdlib + PyYAML only. No Kind Robots runtime, art or ArtJobs.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "projects" / "weird-humboldt"
SCHEMA = PROJECT / "design" / "card.schema.json"
CARD_DIR = PROJECT / "cards"
SEEDS = PROJECT / "ENCOUNTER-SEEDS.md"
EXPECTED_CARDS = 30
PER_CHAPTER = 5
EFFECT_RE = re.compile(r"^((goodwill|nerve|time|weird|clarity)[+-][0-9]|flag:[a-z0-9_]+|evidence:[a-z_]+|lose:free_draw)$")
BANNED = re.compile(r"\b(dosage|milligram|snort|inject|how to (cook|make|score)|where to buy)\b", re.I)
STATES = ["sober", "tipsy", "stoned", "tripping_balls"]
LEADS = ["mara", "kit", "juniper", "cedar"]


def load_cards() -> list[dict]:
    cards: list[dict] = []
    for path in sorted(CARD_DIR.glob("ch*.yaml")):
        for card in yaml.safe_load(path.read_text()) or []:
            card["_file"] = path.name
            cards.append(card)
    return cards


def words(text: str) -> int:
    return len(str(text).split())


def check_option(cid: str, opt: dict, enums: dict, problems: list[str], where: str) -> None:
    tag = f"{cid}.{where}{opt.get('id')}"
    skill, target = opt.get("skill"), opt.get("target")
    if skill not in enums["skill"]:
        problems.append(f"{tag}: bad skill {skill!r}")
    if skill == "none":
        if target is not None:
            problems.append(f"{tag}: no-roll option must have target null")
        if "failure" in opt:
            problems.append(f"{tag}: no-roll option cannot have a failure branch")
    else:
        if target not in (7, 9, 11):
            problems.append(f"{tag}: target must be 7, 9 or 11, got {target!r}")
        if "failure" not in opt:
            problems.append(f"{tag}: rolled option needs authored failure")
    for branch in ("success", "failure"):
        if branch not in opt:
            continue
        out = opt[branch]
        if words(out.get("text", "")) < 10:
            problems.append(f"{tag}.{branch}: prose under 10 words")
        for eff in out.get("effects", []):
            if not EFFECT_RE.match(eff):
                problems.append(f"{tag}.{branch}: bad effect {eff!r}")
    if not opt.get("label"):
        problems.append(f"{tag}: missing label")


def effects_of(card: dict) -> set[str]:
    out: set[str] = set()
    opts = list(card["options"]) + [v["extra_option"] for v in (card.get("by_state") or {}).values() if "extra_option" in v]
    for opt in opts:
        for br in ("success", "failure"):
            out.update(opt.get(br, {}).get("effects", []))
    return out


def validate(cards: list[dict]) -> list[str]:
    problems: list[str] = []
    schema = json.loads(SCHEMA.read_text())
    enums = {"skill": schema["$defs"]["option"]["properties"]["skill"]["enum"],
             "tier": schema["properties"]["tier"]["enum"], "rarity": schema["properties"]["rarity"]["enum"]}
    seeds_text = SEEDS.read_text()
    required = schema["required"]
    seen: set[str] = set()
    per_chapter: dict[int, int] = {}
    all_flags: set[str] = set()
    for c in cards:
        cid = c.get("id", "?")
        for key in required:
            if key not in c:
                problems.append(f"{cid}: missing {key}")
        if cid in seen:
            problems.append(f"{cid}: duplicate id")
        seen.add(cid)
        if f"**{cid} ·" not in seeds_text:
            problems.append(f"{cid}: not a seed in ENCOUNTER-SEEDS.md")
        per_chapter[c.get("chapter")] = per_chapter.get(c.get("chapter"), 0) + 1
        if c.get("tier") not in enums["tier"]:
            problems.append(f"{cid}: bad tier")
        if c.get("rarity") not in enums["rarity"]:
            problems.append(f"{cid}: bad rarity")
        if words(c.get("scene", "")) < 40:
            problems.append(f"{cid}: scene under 40 words")
        if len(c.get("canon", [])) < 2:
            problems.append(f"{cid}: needs at least 2 canon facts")
        if len(c.get("provenance", "")) < 40:
            problems.append(f"{cid}: provenance too thin")
        opts = c.get("options", [])
        if not 2 <= len(opts) <= 4:
            problems.append(f"{cid}: needs 2-4 options, has {len(opts)}")
        ids = [o.get("id") for o in opts]
        if len(set(ids)) != len(ids):
            problems.append(f"{cid}: duplicate option ids")
        for o in opts:
            check_option(cid, o, enums, problems, "")
        # the shared (sober-reachable) route must be consequential on its own
        if not any(e.startswith(("flag:", "evidence:")) for o in opts for e in o.get("success", {}).get("effects", [])):
            problems.append(f"{cid}: no shared option yields a flag or evidence on success")
        lr = c.get("lead_reactions", {})
        for lead in LEADS:
            if words(lr.get(lead, "")) < 8:
                problems.append(f"{cid}: lead_reactions.{lead} missing or under 8 words")
        fx = effects_of(c)
        all_flags |= {e[5:] for e in fx if e.startswith("flag:")}
        for cb in c.get("callbacks", []):
            if f"flag:{cb}" not in fx:
                problems.append(f"{cid}: callback {cb!r} is never set by an effect")
        bs = c.get("by_state")
        if bs is not None:
            if sorted(bs) != sorted(STATES):
                problems.append(f"{cid}: by_state must define exactly {STATES}")
            else:
                if bs["sober"].get("check_mods"):
                    problems.append(f"{cid}: sober carries no check modifiers")
                for st, v in bs.items():
                    if words(v.get("narration", "")) < 15:
                        problems.append(f"{cid}.{st}: narration under 15 words")
                    mods = v.get("check_mods", {})
                    for oid, m in mods.items():
                        if oid not in ids:
                            problems.append(f"{cid}.{st}: check_mod for unknown option {oid}")
                        if m not in (-1, 0, 1):
                            problems.append(f"{cid}.{st}: check_mod out of range")
                    if sum(mods.values()) > 1:
                        problems.append(f"{cid}.{st}: state sums above +1 (power-up tier)")
                    if st == "sober" and "extra_option" in v:
                        problems.append(f"{cid}: sober extra_option not allowed (shared options are the sober route)")
                    if "extra_option" in v:
                        eo = v["extra_option"]
                        if eo.get("id") in ids:
                            problems.append(f"{cid}.{st}: extra_option id collides")
                        check_option(cid, eo, enums, problems, f"{st}.")
        if BANNED.search(json.dumps(c, ensure_ascii=False)):
            problems.append(f"{cid}: contains real-world drug instruction wording")
    for ch in range(1, 7):
        if per_chapter.get(ch, 0) != PER_CHAPTER:
            problems.append(f"chapter {ch}: expected {PER_CHAPTER} cards, has {per_chapter.get(ch, 0)}")
    if len(cards) != EXPECTED_CARDS:
        problems.append(f"deck has {len(cards)} cards, expected {EXPECTED_CARDS}")
    for c in cards:
        for key in ("requires_flags", "excludes_flags"):
            for fl in c.get("eligibility", {}).get(key, []):
                if fl not in all_flags:
                    problems.append(f"{c['id']}: eligibility references unknown flag {fl}")
    return problems


def playtest(cards: list[dict], seed: int, state: str, skills: dict[str, int], lead: str) -> str:
    rng = random.Random(seed)
    by_ch: dict[int, list[dict]] = {}
    for c in cards:
        by_ch.setdefault(c["chapter"], []).append(c)
    deal = [rng.choice(by_ch[ch]) for ch in sorted(by_ch)]
    flags: set[str] = set()
    res = {"goodwill": 0, "nerve": 3, "time": 6, "weird": 0,
           "clarity": {"sober": 3, "tipsy": 2, "stoned": 2, "tripping_balls": 1}[state]}
    lines = [f"# Hand-playtest: seed {seed}, opening {state}, lead {lead}", ""]
    for c in deal:
        lines.append(f"## Ch{c['chapter']} · {c['id']} {c['title']} ({c['location']})")
        lines.append(c["scene"].strip())
        v = (c.get("by_state") or {}).get(state)
        mods = (v or {}).get("check_mods", {})
        if v:
            lines.append(f"*[{state}]* {v['narration']}")
        lines.append(f"*{lead.title()}:* {c['lead_reactions'][lead]}")
        opts = list(c["options"]) + ([v["extra_option"]] if v and "extra_option" in v else [])
        # policy: take the best rolled margin; fall back to the no-roll option
        opt = max(opts, key=lambda o: -99 if o["skill"] == "none" else skills.get(o["skill"], 0) + mods.get(o["id"], 0) - o["target"])
        if opt["skill"] == "none":
            lines.append(f"> Chose **{opt['label']}** (no roll).")
            branch = opt["success"]
        else:
            dice = (rng.randint(1, 6), rng.randint(1, 6))
            mod = mods.get(opt["id"], 0)
            total = sum(dice) + skills.get(opt["skill"], 0) + mod
            ok = total >= opt["target"]
            lines.append(f"> Chose **{opt['label']}** ({opt['skill']} {opt['target']}): 2d6={dice[0]}+{dice[1]}, skill {skills.get(opt['skill'], 0)}, mod {mod:+d} = {total} → **{'success' if ok else 'failure'}**.")
            branch = opt["success"] if ok else opt["failure"]
        lines.append(branch["text"])
        for eff in branch["effects"]:
            if eff.startswith("flag:"):
                flags.add(eff[5:])
            m = re.match(r"^(goodwill|nerve|time|weird|clarity)([+-][0-9])$", eff)
            if m:
                res[m.group(1)] += int(m.group(2))
        lines.append(f"`state: {', '.join(f'{k}={x}' for k, x in res.items())}; flags={sorted(flags)}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--playtest", type=int, metavar="SEED")
    ap.add_argument("--state", default="sober", choices=STATES)
    ap.add_argument("--lead", default="mara", choices=LEADS)
    args = ap.parse_args()
    cards = load_cards()
    problems = validate(cards)
    if problems:
        print("\n".join(problems), file=sys.stderr if args.playtest is not None else sys.stdout)
        return 1
    if args.playtest is not None:
        skills = {"rizz": 1, "burly": 1, "wits": 2, "local_lore": 1, "psyche": 1}
        print(playtest(cards, args.playtest, args.state, skills, args.lead))
        return 0
    pivotal = sum(1 for c in cards if c.get("by_state"))
    print(f"weird-humboldt deck OK: {len(cards)} cards, {pivotal} with four-state lenses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
