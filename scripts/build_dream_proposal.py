#!/usr/bin/env python3
"""Create a deterministic Facet-seeded six-asset daily dream proposal."""
from __future__ import annotations

import argparse, copy, hashlib, json, random, re, subprocess, sys
import urllib.error, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo
import yaml

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "projects/dream-cycle/backlog"
KR_BASE_URL = "https://kind-robots.vercel.app"
PACIFIC = ZoneInfo("America/Los_Angeles")

# Network-free keys known to exist in the live catalog. The sidecar resolves slugs.
FALLBACK_FACETS = {
 "GENRE": ["artificial-intelligence|Artificial Intelligence", "horror-comedy|Horror Comedy",
   "bureaucratic-fantasy|Bureaucratic Fantasy", "archive-horror|Archive Horror",
   "absurdist-comedy|Absurdist Comedy", "cartoon-noir|Cartoon Noir", "biopunk|Biopunk",
   "anachronism-mystery|Anachronism Mystery", "academic-eldritch|Academic Eldritch", "carnival|Carnival"],
 "ANIMAL": ["capybara|Capybara", "axolotl|Axolotl", "cassowary|Cassowary", "binturong|Binturong", "atlantic-puffin|Atlantic Puffin"],
 "SPECIES": ["catfolk|Catfolk", "birdfolk|Birdfolk", "android|Android", "changeling|Changeling", "butterfly|Butterfly"],
 "OCCUPATION": ["alien-biologist|Alien Biologist", "accountant|Accountant", "cactus-wrangler|Cactus Wrangler", "chaos-consultant|Chaos Consultant", "accidental-diplomat|Accidental Diplomat"],
 "MATERIAL": ["aether-silk|Aether Silk", "astral-ore|Astral Ore", "bone-glass|Bone Glass", "ancient-marble|Ancient Marble", "arcane-silver|Arcane Silver"],
 "PERSONALITY": ["bookworm|Bookworm", "cautious|Cautious", "charismatic|Charismatic", "analytical|Analytical", "personality-buoyant|Buoyant"],
}
FIELDS = {
 "location": ("title", "known_for", "local_rule", "best_scene", "art_direction"),
 "character": ("name", "role_drive", "carries", "complication", "look"),
 # `look` is required as of 2026-08-08. Without it a Reward's only visual input
 # was what it *does* ("surfaces the hidden fortune buried in a person"), which
 # gives Krea 2 nothing to draw and lets the style tail take over the subject —
 # that is how item-tidefortune-ladle rendered as a crowd of people.
 "reward": ("name", "reward_type", "rarity", "grants", "best_used_when", "catch", "look"),
 "scenario": ("title", "setup"),
}


def _target_date(now: datetime | None = None) -> str:
    now = now or datetime.now(PACIFIC)
    if now.tzinfo is None: now = now.replace(tzinfo=PACIFIC)
    return now.astimezone(PACIFIC).date().isoformat()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-") or "daily-dream"


def _clean(raw: dict[str, Any]) -> dict[str, Any]:
    out = {"title": str(raw.get("title") or raw.get("canonicalValue") or raw.get("slug") or "").strip(),
           "slug": str(raw.get("slug") or "").strip(),
           "taxonomy": str(raw.get("taxonomy") or "").upper(),
           "randomWeight": max(float(raw.get("randomWeight") or 1), .0001)}
    if isinstance(raw.get("id"), int): out["id"] = raw["id"]
    if raw.get("canonicalValue"): out["canonicalValue"] = str(raw["canonicalValue"])
    return out


def _fallback(taxonomy: str) -> list[dict[str, Any]]:
    return [_clean({"slug": pair.split("|", 1)[0], "title": pair.split("|", 1)[1], "taxonomy": taxonomy})
            for pair in FALLBACK_FACETS[taxonomy]]


def fetch_live_facets(taxonomy: str, timeout: int = 12) -> list[dict[str, Any]] | None:
    found, skip, take = [], 0, 250
    while True:
        url = f"{KR_BASE_URL}/api/facets?" + urllib.parse.urlencode({"taxonomy": taxonomy, "take": take, "skip": skip})
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "conductor-daily-dream/2"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as res: payload = json.loads(res.read())
        except (OSError, ValueError, urllib.error.URLError): return None
        rows = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(rows, list): return None
        for row in rows:
            if not isinstance(row, dict) or row.get("isActive") is False or row.get("isPublic") is False: continue
            if row.get("isRandomizable") is False or float(row.get("randomWeight") or 0) <= 0: continue
            facet = _clean(row)
            if facet["title"] and facet["slug"]: found.append(facet)
        if len(rows) < take: break
        skip += take
    return list({row["slug"].casefold(): row for row in found}.values()) or None


def fetch_facet_catalog() -> tuple[dict[str, list[dict[str, Any]]], str]:
    catalog, live = {}, True
    for taxonomy in FALLBACK_FACETS:
        rows = fetch_live_facets(taxonomy)
        if not rows: rows, live = _fallback(taxonomy), False
        catalog[taxonomy] = rows
    return catalog, "live" if live else "mixed-fallback"


def _draw(rng: random.Random, pool: list[dict[str, Any]], count: int = 1) -> list[dict[str, Any]]:
    if len(pool) < count: raise ValueError(f"Facet pool has {len(pool)} entries; {count} required")
    left, chosen = list(pool), []
    for _ in range(count):
        pick = copy.deepcopy(rng.choices(left, weights=[max(float(x.get("randomWeight") or 1), .0001) for x in left], k=1)[0])
        chosen.append(pick); left = [x for x in left if x["slug"].casefold() != pick["slug"].casefold()]
    return chosen


def facet_seed_plan(day: str, catalog: dict[str, list[dict[str, Any]]] | None = None) -> dict[str, Any]:
    source = "provided"
    if catalog is None: catalog, source = fetch_facet_catalog()
    seed = int.from_bytes(hashlib.sha256(f"daily-dream-v2:{day}".encode()).digest()[:8], "big")
    rng = random.Random(seed); genres = _draw(rng, catalog["GENRE"], 7)
    creature = _draw(rng, catalog["ANIMAL"] + catalog["SPECIES"])[0]
    occupation = _draw(rng, catalog["OCCUPATION"])[0]
    material = _draw(rng, catalog["MATERIAL"])[0]
    personality = _draw(rng, catalog["PERSONALITY"])[0]
    umbrella = genres[:2]
    extras = dict(zip(("location", "character", "reward_item", "reward_skill", "scenario"), genres[2:]))
    elements = {
      "vibe": [*umbrella, creature, occupation],
      "location": [*umbrella, extras["location"], creature, material],
      "character": [*umbrella, extras["character"], creature, occupation, personality],
      "reward_item": [*umbrella, extras["reward_item"], material],
      "reward_skill": [*umbrella, extras["reward_skill"], occupation],
      "scenario": [*umbrella, extras["scenario"], extras["location"], extras["character"], creature],
    }
    return {"version": 2, "date": day, "deterministic_seed": seed, "catalog_source": source,
      "umbrella": {"genres": umbrella, "creature": creature, "wildcard": occupation, "wildcard_role": "occupation"},
      "shared": {"material": material, "personality": personality}, "extra_genres": extras, "elements": elements}


def build_brief(day: str | None = None, catalog=None) -> dict[str, Any]:
    day = day or _target_date(); seeds = facet_seed_plan(day, catalog)
    return {"proposal_date": day, "seed_facets": seeds,
      "instructions": ["Create one coherent bundle under the vibe, not unrelated mini-pitches.",
        "Return exactly one location, one character, one ITEM, one SKILL, and one scenario; no narrator.",
        "Use the Facets as creative constraints and persist seed_facets unchanged.",
        "Author scenario last and name the vibe, location, and character in its setup.",
        "Every `look` and `art_direction` field feeds Krea 2 directly. Write what is "
        "physically visible — material, shape, scale, colour, wear, how light hits it — "
        "not what the thing does. 'A dented tin ladle the length of a forearm, its bowl "
        "worn to mirror-bright, handle wrapped in salt-stiffened cord' is usable; "
        "'it surfaces hidden fortune' is not.",
        "A reward's `look` must describe an object or a visible effect, never a person. "
        "For a SKILL, describe the visible signature of the technique in use."],
      "required_counts": {"vibe": 1, "locations": 1, "characters": 1, "reward_item": 1, "reward_skill": 1, "scenarios": 1}}


def normalize(proposal: dict[str, Any], avoid: set[str] | None = None) -> dict[str, Any]:
    out = copy.deepcopy(proposal); out["title"] = str(out.get("title") or "Untitled Daily Dream").strip()
    base = slugify(out.get("slug") or out["title"]); used = {x.casefold() for x in (avoid or set())}; out["slug"] = base
    n = 2
    while out["slug"].casefold() in used: out["slug"], n = f"{base}-{n}", n + 1
    for reward in out.get("rewards", []) if isinstance(out.get("rewards"), list) else []:
        if isinstance(reward, dict):
            reward["reward_type"] = str(reward.get("reward_type") or "").strip().upper()
    out.pop("narrator", None)
    return out


def _text(value: Any) -> bool: return isinstance(value, str) and bool(value.strip())


def validate_proposal(proposal: Any) -> list[str]:
    if not isinstance(proposal, dict): return ["proposal must be an object"]
    bad = []
    for field in ("title", "slug", "idea"):
        if not _text(proposal.get(field)): bad.append(f"missing {field}")
    for label, obj, fields in [("vibe", proposal.get("vibe"), ("title", "line", "art_direction"))]:
        if not isinstance(obj, dict): bad.append(f"{label} must be an object")
        else:
            for field in fields:
                if not _text(obj.get(field)): bad.append(f"{label} missing {field}")
    for key, count, kind in (("locations",1,"location"),("characters",1,"character"),("rewards",2,"reward"),("scenarios",1,"scenario")):
        rows = proposal.get(key)
        if not isinstance(rows, list) or len(rows) != count: bad.append(f"{key} must be a list of exactly {count}"); continue
        for i, row in enumerate(rows):
            if not isinstance(row, dict): bad.append(f"{key}[{i}] must be an object"); continue
            for field in FIELDS[kind]:
                if not _text(row.get(field)): bad.append(f"{key}[{i}] missing {field}")
    rewards = proposal.get("rewards") if isinstance(proposal.get("rewards"), list) else []
    if sorted(str(x.get("reward_type") or "").upper() for x in rewards if isinstance(x, dict)) != ["ITEM","SKILL"]:
        bad.append("rewards must contain exactly one ITEM and one SKILL")
    if proposal.get("narrator"): bad.append("narrator is not part of the six-asset daily bundle")
    seeds = proposal.get("seed_facets"); elements = seeds.get("elements") if isinstance(seeds, dict) else None
    if not isinstance(seeds, dict): bad.append("seed_facets must be an object")
    elif not isinstance(seeds.get("umbrella",{}).get("genres"), list) or len(seeds["umbrella"]["genres"]) != 2:
        bad.append("seed_facets.umbrella.genres must contain exactly 2 Facets")
    if not isinstance(elements, dict): bad.append("seed_facets.elements must be an object")
    else:
        for key in ("vibe","location","character","reward_item","reward_skill","scenario"):
            if not isinstance(elements.get(key), list) or not elements[key]: bad.append(f"seed_facets.elements.{key} must be a non-empty list")
            else:
                for facet in elements[key]:
                    if not isinstance(facet, dict) or not _text(facet.get("title")) or not _text(facet.get("taxonomy")) or not (_text(facet.get("slug")) or isinstance(facet.get("id"), int)):
                        bad.append(f"seed_facets.elements.{key} contains an invalid Facet")
    if all(isinstance(proposal.get(k), list) and proposal[k] for k in ("locations","characters","scenarios")) and isinstance(proposal.get("vibe"), dict):
        setup = str(proposal["scenarios"][0].get("setup") or "").casefold()
        for label, name in (("vibe",proposal["vibe"].get("title")),("location",proposal["locations"][0].get("title")),("character",proposal["characters"][0].get("name"))):
            if _text(name) and str(name).casefold() not in setup: bad.append(f"scenario setup must name the {label}: {name}")
    return bad


def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8"); end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0: return {}
    value = yaml.safe_load(text[4:end]); return value if isinstance(value, dict) else {}


def _files(): return sorted(BACKLOG.glob("*.md")) if BACKLOG.exists() else []
def proposal_exists_for(day: str) -> bool: return any(str(_frontmatter(p).get("proposal_date") or "") == day for p in _files())
def existing_slugs() -> set[str]: return {str(_frontmatter(p).get("slug")) for p in _files() if _frontmatter(p).get("slug")}


def fetch_main(quiet: bool=True) -> bool:
    try: return subprocess.run(["git","fetch","origin","main"],cwd=ROOT,check=False,capture_output=quiet,text=True).returncode == 0
    except OSError: return False


def remote_proposal_for(day: str) -> str | None:
    try:
        names = subprocess.run(["git","ls-tree","-r","--name-only","origin/main","--","projects/dream-cycle/backlog"],cwd=ROOT,capture_output=True,text=True).stdout
        for name in names.splitlines():
            shown = subprocess.run(["git","show",f"origin/main:{name}"],cwd=ROOT,capture_output=True,text=True)
            if shown.returncode == 0 and re.search(rf"(?m)^proposal_date:\s*['\"]?{re.escape(day)}['\"]?\s*$", shown.stdout): return Path(name).name
    except OSError: pass
    return None


def _titles(values): return " · ".join(str(x.get("title") or x.get("slug")) for x in values)


def render_markdown(p: dict[str, Any], day: str) -> str:
    s=p["seed_facets"]; e=s["elements"]; loc=p["locations"][0]; ch=p["characters"][0]; sc=p["scenarios"][0]
    item=next(x for x in p["rewards"] if x["reward_type"]=="ITEM"); skill=next(x for x in p["rewards"] if x["reward_type"]=="SKILL")
    lines=["---",f"slug: {p['slug']}",f"title: {p['title']}","type: dream","status: outline","priority: normal","narrator: 'no'",f"created: '{day}'","proposal: true",f"proposal_date: '{day}'","built_pr: null","---","","## Seed Facets",
      f"- **Deterministic seed:** `{s.get('deterministic_seed')}` ({s.get('catalog_source','unknown')} catalog)",
      *[f"- **{label}:** {_titles(e[key])}" for label,key in (("Dream vibe","vibe"),("Dream location","location"),("Character","character"),("Reward item","reward_item"),("Reward skill","reward_skill"),("Scenario","scenario"))],
      "","## The idea",p["idea"],"","## Dream vibe (1)",f"**{p['vibe']['title']}** — {p['vibe']['line']}",f"Art: {p['vibe']['art_direction']}","","## Dream location (1)",f"- **{loc['title']}** — known for {loc['known_for']}. Local rule: {loc['local_rule']}. Best scene: {loc['best_scene']}. Art: {loc['art_direction']}","","## Character (1)",f"- **{ch['name']}** — {ch['role_drive']}. Carries {ch['carries']}. Complication: {ch['complication']}. Look: {ch['look']}","","## Reward item (1)",f"- **{item['name']}** (ITEM, {item['rarity']}) — {item['grants']}. Best used when {item['best_used_when']}. The catch: {item['catch']}. Look: {item['look']}","","## Reward skill (1)",f"- **{skill['name']}** (SKILL, {skill['rarity']}) — {skill['grants']}. Best used when {skill['best_used_when']}. The catch: {skill['catch']}. Look: {skill['look']}","","## Scenario (1, authored last)",f"- **{sc['title']}** — {sc['setup']}","","## Notes from Silas","- (leave notes here — agents fold them in before building and never edit this section)","","## Build log",f"- {day} | proposed | deterministic Facet-seeded six-asset bundle","","<!-- proposal-data",json.dumps(p,ensure_ascii=False,sort_keys=True),"-->",""]
    return "\n".join(lines)


def write_proposal(proposal: dict[str, Any], *, date: str|None=None, fetch: bool=True,
                   dry_run: bool=False, force: bool=False) -> Path|None:
    day=date or _target_date()
    if not force and (proposal_exists_for(day) or (fetch and fetch_main() and remote_proposal_for(day))):
        print(f"Proposal already exists for {day}; refusing duplicate.",file=sys.stderr); return None
    proposal=normalize(proposal,existing_slugs()); bad=validate_proposal(proposal)
    if bad: raise ValueError("Invalid proposal:\n- " + "\n- ".join(bad))
    path=BACKLOG/f"{day}-{proposal['slug']}.md"; rendered=render_markdown(proposal,day)
    if dry_run:
        print(rendered); print(f"# would write: {path}", file=sys.stderr); return path
    BACKLOG.mkdir(parents=True,exist_ok=True); path.write_text(rendered,encoding="utf-8"); print(path); return path


def main(argv=None) -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check",action="store_true",help="exit 0 if the date has a proposal, otherwise 1")
    ap.add_argument("--brief",action="store_true",help="print the authoring brief and Facet seed")
    ap.add_argument("--from-json",metavar="FILE",help="validate and write JSON ('-' for stdin)")
    ap.add_argument("--sample",action="store_true",help="render or write the built-in sample")
    ap.add_argument("--date",help="override Pacific date (YYYY-MM-DD)")
    ap.add_argument("--fetch",action="store_true",help="with --check, consult fresh origin/main")
    ap.add_argument("--no-fetch",action="store_true",help="skip the origin/main write guard")
    ap.add_argument("--dry-run",action="store_true",help="print markdown without writing")
    ap.add_argument("--force",action="store_true",help="write even if the date exists")
    a=ap.parse_args(argv); day=a.date or _target_date()
    if a.check:
        exists=proposal_exists_for(day)
        if not exists and a.fetch and fetch_main(): exists=remote_proposal_for(day) is not None
        print(f"Proposal for {day} exists." if exists else
              f"No proposal for {day}. Run --brief, author the six-asset JSON, then pass it to --from-json.")
        return 0 if exists else 1
    if a.brief: print(json.dumps(build_brief(day),indent=2,ensure_ascii=False)); return 0
    if a.sample:
        return 0 if write_proposal(copy.deepcopy(SAMPLE_PROPOSAL),date=day,fetch=False,
                                   dry_run=a.dry_run,force=True) else 1
    if a.from_json:
        try:
            raw=sys.stdin.read() if a.from_json=="-" else Path(a.from_json).read_text(encoding="utf-8")
            proposal=json.loads(raw)
        except (OSError,json.JSONDecodeError) as error:
            print(f"Could not read proposal JSON: {error}",file=sys.stderr); return 1
        proposal.setdefault("seed_facets",facet_seed_plan(day))
        return 0 if write_proposal(proposal,date=day,fetch=not a.no_fetch,
                                   dry_run=a.dry_run,force=a.force) else 1
    ap.error("choose --check, --brief, --from-json, or --sample"); return 2


def _sample() -> dict[str,Any]:
    catalog={k:_fallback(k) for k in FALLBACK_FACETS}
    return {"title":"Prism Appeal","slug":"prism-appeal","idea":"A courthouse refracts testimony into living color.","vibe":{"title":"The Kindly Cross-Examination","line":"Every answer changes the room that asked it.","art_direction":"A luminous impossible courthouse."},"locations":[{"title":"The Refracted Court","known_for":"colored testimony","local_rule":"no statement repeats a hue","best_scene":"a disputed memory changes the room","art_direction":"prismatic courtroom"}],"characters":[{"name":"Mara Venn","role_drive":"protect an engineered witness","carries":"a cracked spectrum lens","complication":"it contains her deleted testimony","look":"mantis-shrimp advocate in a midnight suit"}],"rewards":[{"name":"Verdict Lens","reward_type":"ITEM","rarity":"RARE","grants":"reveals omissions","best_used_when":"a story is too neat","catch":"it reveals yours","look":"a palm-sized brass loupe with a cracked prismatic lens, verdigris in the knurling"},{"name":"Chromatic Recall","reward_type":"SKILL","rarity":"UNCOMMON","grants":"reconstructs memory from color","best_used_when":"records were altered","catch":"emotion returns","look":"ribbons of banded colour unspooling out of empty air above a bare table"}],"scenarios":[{"title":"The Color of Perjury","setup":"In The Kindly Cross-Examination at The Refracted Court, Mara Venn defends a witness whose testimony turned the chamber black."}],"seed_facets":facet_seed_plan("2026-07-31",catalog)}
SAMPLE_PROPOSAL=_sample()

if __name__ == "__main__": raise SystemExit(main())