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
ANCHOR_FILE = PROJECT / "anchors" / "anchors.yaml"
ENDING_FILE = PROJECT / "endings" / "endings.yaml"
ARCHETYPE_FILE = PROJECT / "archetypes" / "archetypes.yaml"
SEEDS = PROJECT / "ENCOUNTER-SEEDS.md"
# The seed catalog is the source of truth for the deck's size and chapter placement.
# Only bold bullet premises beneath numbered chapter headings count as seeds.
SEED_CHAPTER_RE = re.compile(r"^## ([1-6]) · ")
SEED_ID_RE = re.compile(r"^- \\*\\*(WH-[0-9]+) · ")
EFFECT_RE = re.compile(r"^((goodwill|nerve|time|weird|clarity)[+-][0-9]|flag:[a-z0-9_]+|evidence:[a-z_]+|lose:free_draw)$")
BANNED = re.compile(r"\b(dosage|milligram|snort|inject|how to (cook|make|score)|where to buy)\b", re.I)
STATES = ["sober", "tipsy", "stoned", "tripping_balls"]
LEADS = ["mara", "kit", "juniper", "cedar"]


def parse_seed_chapters(text: str) -> tuple[dict[str, int], list[str]]:
    """Map catalogued seed IDs to their chapter, excluding prose-only references.

    A malformed or duplicate premise must fail validation rather than silently
    changing the expected deck size. WH-121 is counted in chapter 2 because it
    has its own seed bullet; WH-122..126 appear only in editorial prose.
    """
    chapter = None
    chapters: dict[str, int] = {}
    problems: list[str] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        heading = SEED_CHAPTER_RE.match(line)
        if heading:
            chapter = int(heading.group(1))
            continue
        match = SEED_ID_RE.match(line)
        if not match:
            continue
        cid = match.group(1)
        if chapter is None:
            problems.append(f"seed {cid}: no chapter heading (line {line_no})")
        elif cid in chapters:
            problems.append(f"seed {cid}: duplicate premise (line {line_no})")
        else:
            chapters[cid] = chapter
    for ch in range(1, 7):
        if ch not in chapters.values():
            problems.append(f"seed catalog: chapter {ch} has no premises")
    return chapters, problems


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
    seed_chapters, seed_problems = parse_seed_chapters(SEEDS.read_text())
    problems.extend(seed_problems)
    expected_per_chapter = {ch: sum(v == ch for v in seed_chapters.values()) for ch in range(1, 7)}
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
        if cid not in seed_chapters:
            problems.append(f"{cid}: not a seed in ENCOUNTER-SEEDS.md")
        elif c.get("chapter") != seed_chapters[cid]:
            problems.append(f"{cid}: chapter {c.get('chapter')} disagrees with seed chapter {seed_chapters[cid]}")
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
    for ch, expected in expected_per_chapter.items():
        if per_chapter.get(ch, 0) != expected:
            problems.append(f"chapter {ch}: expected {expected} cards, has {per_chapter.get(ch, 0)}")
    if len(cards) != len(seed_chapters):
        problems.append(f"deck has {len(cards)} cards, expected {len(seed_chapters)}")
    for ch in per_chapter:
        if ch not in expected_per_chapter:
            problems.append(f"deck contains invalid chapter {ch!r}")
    for c in cards:
        for key in ("requires_flags", "excludes_flags"):
            for fl in c.get("eligibility", {}).get(key, []):
                if fl not in all_flags:
                    problems.append(f"{c['id']}: eligibility references unknown flag {fl}")
    problems += no_dead_end_problems(cards)
    problems += validate_anchors(load_anchors(), enums)
    problems += validate_endings(load_endings(), cards)
    return problems


def load_anchors() -> list[dict]:
    return yaml.safe_load(ANCHOR_FILE.read_text()) or []


def load_endings() -> list[dict]:
    return yaml.safe_load(ENDING_FILE.read_text()) or []


def load_archetypes() -> list[dict]:
    return yaml.safe_load(ARCHETYPE_FILE.read_text()) or []


ARCHETYPE_IDS = ["reporter", "student", "rower", "local", "organizer", "mechanic", "gardener", "dealer"]
SKILL_KEYS = ["rizz", "burly", "wits", "local_lore", "psyche"]
MYSTIC_TERMS = re.compile(r"\b(mystic|shaman|spirit guide|ancestral power|sacred)\b", re.I)


def validate_archetypes(archetypes: list[dict], anchors: list[dict]) -> list[str]:
    """Eight archetypes, six starting skill points each, one authored reaction per chapter anchor."""
    problems: list[str] = []
    if [a.get("id") for a in archetypes] != ARCHETYPE_IDS:
        problems.append(f"archetypes: ids must be exactly {ARCHETYPE_IDS}")
    anchor_ids = [a["id"] for a in anchors]
    for a in archetypes:
        aid = a.get("id", "?")
        skills = a.get("skills", {})
        if sorted(skills) != sorted(SKILL_KEYS):
            problems.append(f"{aid}: skills must be exactly {SKILL_KEYS}")
        elif sum(skills.values()) != 6 or not all(0 <= v <= 3 for v in skills.values()):
            problems.append(f"{aid}: skills must be 0-3 each and total 6 points")
        for key in ("name", "vantage", "perk", "hopeful_note"):
            if not a.get(key):
                problems.append(f"{aid}: missing {key}")
        reactions = a.get("anchor_reactions", {})
        if sorted(reactions) != sorted(anchor_ids):
            problems.append(f"{aid}: needs exactly one reaction per anchor {anchor_ids}")
        for anchor, text in reactions.items():
            if words(text) < 20:
                problems.append(f"{aid}.{anchor}: reaction under 20 words")
        blob = json.dumps(a, ensure_ascii=False)
        if EXCLUDED_TERMS.search(blob):
            problems.append(f"{aid}: touches excluded Wiyot/Tuluwat material")
        if BANNED.search(blob):
            problems.append(f"{aid}: contains real-world drug instruction wording")
        if MYSTIC_TERMS.search(blob):
            problems.append(f"{aid}: identity must not be framed as a mystical ability")
    return problems


MIN_ENDINGS = 10
ENDING_BEATS = ("one_year", "ten_year", "thirty_year")


def validate_endings(endings: list[dict], cards: list[dict]) -> list[str]:
    """10+ ending records: every companion core in both fates, earnable flags, no excluded material."""
    problems: list[str] = []
    if len(endings) < MIN_ENDINGS:
        problems.append(f"endings: need at least {MIN_ENDINGS}, have {len(endings)}")
    ids = [e.get("id") for e in endings]
    if len(set(ids)) != len(ids):
        problems.append("endings: duplicate ids")
    cores = {(e.get("lead"), e.get("fate")) for e in endings if e.get("kind") == "core"}
    for lead in LEADS:
        for fate in ("hope", "dark"):
            if (lead, fate) not in cores:
                problems.append(f"endings: missing core {lead}.{fate}")
    settable = set()
    for card in cards + load_anchors():
        for e in effects_of(card):
            if e.startswith("flag:"):
                settable.add(e[5:])
    for e in endings:
        eid = e.get("id", "?")
        for key in ("title", "civic_future", "cost", "quiet_scene", "requires_flags"):
            if not e.get(key):
                problems.append(f"{eid}: missing {key}")
        for flag in e.get("requires_flags", []):
            if flag not in settable:
                problems.append(f"{eid}: requires_flags {flag!r} is never set by any card or anchor")
        for beat in ENDING_BEATS:
            if e.get("kind") == "core" and words(e.get(beat, "")) < 15:
                problems.append(f"{eid}: {beat} missing or under 15 words")
        blob = json.dumps(e, ensure_ascii=False)
        if EXCLUDED_TERMS.search(blob):
            problems.append(f"{eid}: touches excluded Wiyot/Tuluwat material")
        if BANNED.search(blob):
            problems.append(f"{eid}: contains real-world drug instruction wording")
        if e.get("lead") == "cedar" and not re.search(r"parents|father and .*mother|mother and .*father", blob, re.I):
            problems.append(f"{eid}: Cedar's parents must stay together in every timeline")
    return problems


# Chapters 2-4 are the three stay/follow crossroads (JOURNEY-LOOP-CONTRACT.md).
CROSSROADS = {2: "crossroads1", 3: "crossroads2", 4: "crossroads3"}
EXCLUDED_TERMS = re.compile(r"wiyot|tuluwat", re.I)


def validate_anchors(anchors: list[dict], enums: dict) -> list[str]:
    """The six guaranteed chapter anchors: one per chapter, never flag-gated, no dead ends."""
    problems: list[str] = []
    schema = json.loads(SCHEMA.read_text())
    if sorted(a.get("chapter") for a in anchors) != [1, 2, 3, 4, 5, 6]:
        problems.append("anchors: need exactly one anchor per chapter 1-6")
    for a in anchors:
        aid = a.get("id", "?")
        if not re.match(r"^WH-A[1-6]$", str(aid)):
            problems.append(f"{aid}: anchor id must be WH-A1..WH-A6")
        for key in schema["required"]:
            if key not in a:
                problems.append(f"{aid}: missing {key}")
        if not a.get("anchor"):
            problems.append(f"{aid}: missing anchor stage label")
        if a.get("eligibility", {}).get("requires_flags") or a.get("eligibility", {}).get("excludes_flags"):
            problems.append(f"{aid}: a guaranteed anchor cannot be flag-gated")
        if words(a.get("scene", "")) < 60:
            problems.append(f"{aid}: scene under 60 words")
        opts = a.get("options", [])
        if not 2 <= len(opts) <= 4:
            problems.append(f"{aid}: needs 2-4 options, has {len(opts)}")
        for o in opts:
            check_option(aid, o, enums, problems, "")
        if not any(o.get("skill") == "none" for o in opts):
            problems.append(f"{aid}: needs a no-roll option so no player can be blocked by dice")
        for lead in LEADS:
            if words(a.get("lead_reactions", {}).get(lead, "")) < 8:
                problems.append(f"{aid}: lead_reactions.{lead} missing or under 8 words")
        fx = effects_of(a)
        for cb in a.get("callbacks", []):
            if f"flag:{cb}" not in fx:
                problems.append(f"{aid}: callback {cb!r} is never set by an effect")
        prefix = CROSSROADS.get(a.get("chapter"))
        if prefix:
            for kind in ("stayed", "followed"):
                if f"flag:{prefix}_{kind}" not in fx:
                    problems.append(f"{aid}: crossroads needs a no-roll route that sets {prefix}_{kind}")
            for o in opts:
                if o.get("skill") != "none":
                    # a failed room-brokering roll must still resolve to a stay/follow flag
                    if not any(e.startswith(f"flag:{prefix}_") for e in o["failure"]["effects"] + o["success"]["effects"]):
                        problems.append(f"{aid}.{o['id']}: crossroads option sets no {prefix} flag")
        blob = json.dumps(a, ensure_ascii=False)
        if BANNED.search(blob):
            problems.append(f"{aid}: contains real-world drug instruction wording")
        if EXCLUDED_TERMS.search(blob):
            problems.append(f"{aid}: touches excluded Wiyot/Tuluwat material (EXCLUDED-CONTENT-2026-10-22.md)")
    return problems


MIN_GUARANTEED_PER_CHAPTER = 6


def guaranteed_pool(cards: list[dict], chapter: int) -> list[dict]:
    """Cards drawable in a chapter whatever the player's flags are.

    A card is guaranteed when it requires no flag and can only be excluded by a flag
    that its own effects set (so it can lock itself out after playing, never another card's).
    """
    pool = []
    for c in cards:
        if c.get("chapter") != chapter:
            continue
        el = c.get("eligibility", {})
        if el.get("requires_flags"):
            continue
        if set(el.get("excludes_flags", [])) <= {e[5:] for e in effects_of(c) if e.startswith("flag:")}:
            pool.append(c)
    return pool


def no_dead_end_problems(cards: list[dict]) -> list[str]:
    """No-dead-end proof: every chapter keeps a flag-independent draw pool, and every card has
    an option whose success path never needs a roll to be survivable (a rolled failure still
    authored, so no choice ends the run)."""
    out = []
    for ch in range(1, 7):
        n = len(guaranteed_pool(cards, ch))
        if n < MIN_GUARANTEED_PER_CHAPTER:
            out.append(f"chapter {ch}: only {n} flag-independent cards (need {MIN_GUARANTEED_PER_CHAPTER}); a player could draw a dead end")
    for c in cards:
        for o in c.get("options", []) + [v["extra_option"] for v in (c.get("by_state") or {}).values() if "extra_option" in v]:
            if o.get("skill") != "none" and not o.get("failure", {}).get("text"):
                out.append(f"{c['id']}.{o.get('id')}: failure branch is a dead end (no authored text)")
    return out


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
    arch_problems = validate_archetypes(load_archetypes(), load_anchors())
    if arch_problems:
        print("\n".join(arch_problems))
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
