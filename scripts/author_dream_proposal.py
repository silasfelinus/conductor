#!/usr/bin/env python3
"""Author the day's canonical six-asset Daily Dream proposal.

The scheduled Daily Dream loop must make a genuinely new world, not merely a new
set of names attached to the same story machinery. This module therefore keeps
three independent history-aware variation layers:

* names and title construction,
* narrative premise / conflict engine,
* visible world ontology and art direction.

The actual rendered media style is selected later by dream_art_prompts.py so all
six assets from a world stay coherent while different worlds can look radically
different.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import build_dream_proposal as dreams  # noqa: E402
import dream_creative_ruts as ruts  # noqa: E402
import dream_prose_quality as prose  # noqa: E402

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
MODEL = os.environ.get("DREAM_AUTHOR_MODEL", "claude-sonnet-5")
MAX_TOKENS = 6000
MAX_ATTEMPTS = 2

REPO_ROOT = Path(__file__).resolve().parents[1]
DREAM_BACKLOG_DIR = REPO_ROOT / "projects" / "dream-cycle" / "backlog"
HISTORY_CATEGORIES = ("dreams", "locations", "characters", "rewards", "scenarios")
HISTORY_PROPOSAL_LIMIT = 45
HISTORY_PROMPT_LIMIT = 20
PREMISE_HISTORY_LIMIT = 12
PREMISE_PROMPT_LIMIT = 8

NAMING_DIRECTIONS = (
    "Use a grounded two-part name with an ordinary, non-compound family name; "
    "the world can be strange without the name announcing it.",
    "Use a one-token mononym, nickname, or callsign that sounds lived-in rather "
    "than deliberately edgy.",
    "Use a three-part name or a name with an initial; keep the surname plausible "
    "rather than ornamental or compound-built.",
    "Use a speculative one- or two-token name, but avoid clipped X-heavy first "
    "names and avoid English noun+noun fantasy surnames.",
    "Use an understated conventional full name. Do not literalize the character's "
    "species, occupation, personality, or magic in the name.",
)

# These are story engines, not genres. Facets still decide genre and creature.
# Rotation prevents the model from finding one comfortable plot machine and
# applying it to every new Facet combination.
STORY_DIRECTIONS = (
    "Kinetic pressure: center a rescue, confrontation, chase, escape, or public crisis. "
    "Something visible must be changing while the character acts.",
    "Discovery pressure: center exploration of a place, organism, machine, portal, or "
    "phenomenon whose rules are learned through direct encounter rather than records.",
    "Relationship pressure: center an intimate promise, rivalry, family bond, friendship, "
    "betrayal, or act of care whose choice visibly changes the world around it.",
    "Caper pressure: center a theft, con, performance, infiltration, jailbreak, sabotage, "
    "or audacious trick with moving pieces and a concrete target.",
    "Survival pressure: center adaptation, transformation, weather, hunger, pursuit, "
    "containment, or environmental danger where bodies and terrain matter.",
    "Mythic pressure: center prophecy, monster, god, impossible scale, cosmic bargain, "
    "or reality-changing event. Let awe or dread be structurally important.",
    "Mystery pressure: center physical clues, testimony, behavior, landscape, or impossible "
    "evidence. Solve through encounters, not paperwork, archives, ledgers, or permits.",
    "Competition pressure: center a race, tournament, audition, ritual contest, festival, "
    "hunt, election, or game whose rules create visible action and reversals.",
    "Journey pressure: force travel across meaningfully changing terrain or social worlds; "
    "each leg should expose a new rule or danger rather than another desk to visit.",
    "Collective pressure: center a neighborhood, crew, pack, colony, team, rebellion, or "
    "crowd responding to change through coordinated action rather than administration.",
)

# A deliberately narrow guard for the rut visible in August 2026. These are not
# permanently forbidden concepts. They are rejected when the day's Facets did
# not actually ask for bureaucracy/record-keeping, so a future bureaucracy Facet
# can still produce one intentionally.
BUREAUCRACY_MARKERS = {
    "ledger", "ledgers", "filing", "file", "files", "archive", "archives",
    "archivist", "permit", "permits", "registry", "register", "quota", "quotas",
    "charter", "requisition", "requisitions", "clerk", "clerks", "bureau",
    "paperwork", "accounting", "bookkeeping", "tally", "office",
}
BUREAUCRACY_FACET_MARKERS = BUREAUCRACY_MARKERS | {
    "bureaucracy", "bureaucratic", "administration", "administrative",
}

# Common words do not constitute a repeated premise. We care about distinctive
# nouns/verbs that make two worlds feel built from the same kit.
PREMISE_STOPWORDS = {
    "about", "after", "again", "against", "along", "another", "around", "because",
    "before", "being", "between", "character", "could", "dream", "during", "every",
    "first", "from", "grants", "known", "location", "moment", "people", "place",
    "reward", "scenario", "someone", "something", "their", "there", "these", "thing",
    "through", "under", "until", "where", "while", "whose", "world", "would",
}

SYSTEM_PROMPT = """You are the creative generator for Kind Robots' Daily Dream cycle.
Each day is a portal into a different universe in a multidimensional storytelling
app. Write one coherent six-asset bundle: a dream vibe, a dream location, a
Character, an ITEM Reward, a SKILL Reward, and a Scenario.

Return ONLY a JSON object. No prose, no markdown fence, no commentary.

Shape:
{
  "title": str, "slug": "kebab-case", "idea": str,
  "vibe": {"title": str, "line": str, "art_direction": str},
  "locations": [{"title","known_for","local_rule","best_scene","art_direction"}],
  "characters": [{"name","role_drive","carries","complication","look"}],
  "rewards": [
    {"name","reward_type":"ITEM","rarity","grants","best_used_when","catch","look"},
    {"name","reward_type":"SKILL","rarity","grants","best_used_when","catch","look"}
  ],
  "scenarios": [{"title","setup"}]
}

Exactly one location, one character, two rewards (one ITEM, one SKILL), one
scenario. No narrator. rarity is one of COMMON, UNCOMMON, RARE, EPIC, LEGENDARY.

USER-FACING COPY IS A HARD CONTRACT, NOT DATABASE SHORTHAND.
These fields are displayed to people as prose, on cards that show one field by
itself with no surrounding sentence to complete:

  `idea`, `vibe.line`;
  every location's `known_for`, `local_rule`, `best_scene`;
  the character's `role_drive`, `carries`, `complication`;
  each reward's `grants`, `best_used_when`, `catch`;
  the Scenario `setup`.

Write every one of them as a complete, properly capitalized sentence with
terminal punctuation, not a telegraphic label or noun phrase. Critically, do NOT
write a field as a grammatical continuation of its own key: `known_for` must not
be phrased to follow the words "known for", `carries` must not be phrased to
follow "carries", `best_used_when` must not be phrased to follow "best used
when". Each value has to stand on its own as a sentence, because that is how it
is rendered. "Her herd is bred from the last wild cactus line, and every
hardened prod risks becoming their apocalypse." is usable; "keep her cactus herd
calm through the quakes" is not. Likewise "A story arrives suspiciously clean
and complete, with no loose ends." is usable for `best_used_when`; "a story is
too neat" is not, and neither is "Use it when a story is too neat" — the card
already prints the label, so restating it reads as a stutter.

They must explain enough to make sense when a card shows the field by itself.
Keep the sharpness of a good tagline, but do not confuse brevity with
incompleteness: the vibe line should communicate the world's governing mood,
pressure, or strange rule; each location field should add a distinct piece of
concrete world logic, consequence, or scene; the character fields should make
the person legible without the reader having seen any other card. Prefer one
substantial sentence to a tiny fragment. Do not omit punctuation merely because
the JSON key already names the field.

Naming another asset from this same bundle is allowed and encouraged where it
helps — the Scenario in particular is a synthesis piece and must name the vibe,
location, and character. What is forbidden is copy that cannot be understood as
a sentence on its own.

VARIETY IS A PRIMARY REQUIREMENT, NOT A POLISH STEP.
The Facets must change the ontology and story machinery of the world, not merely
redecorate a familiar magical civic institution. A superhero combination can
produce powers, costumes, public stakes, collateral damage, secret identities or
superhuman institutions. Cosmic horror can produce impossible scale, alien
causality, body/space unease, forbidden perception, or existential stakes.
Anthropomorphic animals should be embodied animals whose anatomy, habitat,
senses, social behavior, scale, tools, or movement matter, not ordinary humans
with animal nouns pasted onto them. Other genres deserve the same commitment.

Do not default to whimsical bureaucracy. Unless today's Facets specifically ask
for administration or records, avoid ledgers, filing, archives, permit offices,
registries, quotas, charters, clerks, requisitions, accounting, and stories whose
main action is obtaining, filing, auditing, cataloguing, transferring, or balancing
paperwork. Recent premises are supplied in the user prompt. Treat their settings,
conflict mechanisms, institutions, signature objects, and narrative tricks as
spent material, not a palette to remix.

Naming is also part of variation. Recent names are supplied in the user prompt;
treat their distinctive words, roots, sounds, and constructions as spent
vocabulary. Do not default to a clipped fantasy first name plus a whimsical
compound surname. Vary register and structure across days: ordinary names,
mononyms, callsigns, multi-part names, and genuinely setting-native speculative
names can all belong here. Do not manufacture pseudo-ethnic names by vaguely
imitating a real culture. Names should fit the character without simply spelling
out species, job, personality, material, or genre Facets.

The same anti-echo rule applies to dream, location, reward, and scenario titles.
A new title may share ordinary glue words but should not recycle the distinctive
noun pair or signature construction of a recent title.

Every `look` and `art_direction` string is fed straight to an image model. Write
what is physically visible: material, shape, scale, colour, wear, anatomy,
architecture, atmosphere, and how light behaves. Describe the unique physical
world, not a generic house style. The renderer supplies a deliberately varied
visual medium later, so do not force everything into "western animation" or any
other universal style. A Reward's `look` describes an object or visible effect,
never a person.

Do not write conditional instructions an image model cannot evaluate. Decide and
state one outcome. Do not request a literal printed object such as a trading card,
book cover, or comic page; visual media language is fine, but the subject should
remain the world/object/character rather than a page layout. Do not pile up text
exclusions; say nothing about text at all.

Author the scenario LAST, and its `setup` must name the vibe title, location title,
and character name literally."""


def _proposal_data(text: str) -> dict:
    match = re.search(r"<!--\s*proposal-data\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return {}
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _append_unique(values: list[str], value) -> None:
    if not isinstance(value, str):
        return
    clean = value.strip()
    if clean and clean not in values:
        values.append(clean)


def _names_from_proposal(text: str) -> dict[str, list[str]]:
    out = {category: [] for category in HISTORY_CATEGORIES}
    data = _proposal_data(text)

    _append_unique(out["dreams"], data.get("title"))
    vibe = data.get("vibe")
    if isinstance(vibe, dict):
        _append_unique(out["dreams"], vibe.get("title"))
    for row in data.get("locations") or []:
        if isinstance(row, dict):
            _append_unique(out["locations"], row.get("title"))
    for row in data.get("characters") or []:
        if isinstance(row, dict):
            _append_unique(out["characters"], row.get("name"))
    for row in data.get("rewards") or []:
        if isinstance(row, dict):
            _append_unique(out["rewards"], row.get("name"))
    for row in data.get("scenarios") or []:
        if isinstance(row, dict):
            _append_unique(out["scenarios"], row.get("title"))

    if not out["characters"]:
        match = re.search(
            r"^## Character \(1\)\s*\n-\s+\*\*(.+?)\*\*\s+[—-]",
            text,
            re.MULTILINE,
        )
        if match:
            _append_unique(out["characters"], match.group(1))
    return out


def recent_name_history(
    day: str,
    proposal_limit: int = HISTORY_PROPOSAL_LIMIT,
    backlog_dir: Path | str | None = None,
) -> dict[str, list[str]]:
    root = Path(backlog_dir) if backlog_dir is not None else DREAM_BACKLOG_DIR
    history = {category: [] for category in HISTORY_CATEGORIES}
    if not root.exists():
        return history

    paths = [
        path
        for path in sorted(root.glob("20??-??-??-*.md"))
        if path.name[:10] < day
    ][-proposal_limit:]
    for path in paths:
        try:
            names = _names_from_proposal(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        for category in HISTORY_CATEGORIES:
            for name in names[category]:
                _append_unique(history[category], name)
    return history


def _flatten_creative_values(data: dict) -> list[str]:
    """Pull story-bearing prose from one proposal without seed/facet boilerplate."""
    values: list[str] = []
    for key in ("title", "idea"):
        _append_unique(values, data.get(key))
    vibe = data.get("vibe")
    if isinstance(vibe, dict):
        for key in ("title", "line"):
            _append_unique(values, vibe.get(key))
    for row in data.get("locations") or []:
        if isinstance(row, dict):
            for key in ("title", "known_for", "local_rule", "best_scene"):
                _append_unique(values, row.get(key))
    for row in data.get("characters") or []:
        if isinstance(row, dict):
            for key in ("role_drive", "carries", "complication"):
                _append_unique(values, row.get(key))
    for row in data.get("rewards") or []:
        if isinstance(row, dict):
            for key in ("name", "grants", "best_used_when", "catch"):
                _append_unique(values, row.get(key))
    for row in data.get("scenarios") or []:
        if isinstance(row, dict):
            for key in ("title", "setup"):
                _append_unique(values, row.get(key))
    return values


def recent_premise_history(
    day: str,
    proposal_limit: int = PREMISE_HISTORY_LIMIT,
    backlog_dir: Path | str | None = None,
) -> list[str]:
    """Return recent story summaries as anti-inspiration for the next authoring call."""
    root = Path(backlog_dir) if backlog_dir is not None else DREAM_BACKLOG_DIR
    if not root.exists():
        return []
    paths = [
        path
        for path in sorted(root.glob("20??-??-??-*.md"))
        if path.name[:10] < day
    ][-proposal_limit:]
    history: list[str] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        data = _proposal_data(text)
        values = _flatten_creative_values(data) if data else []
        if values:
            summary = " | ".join(values)
        else:
            summary = path.stem[11:].replace("-", " ")
        history.append(summary[:1200])
    return history


def naming_direction(day: str) -> str:
    try:
        ordinal = datetime.date.fromisoformat(day).toordinal()
    except ValueError:
        ordinal = sum(ord(char) for char in day)
    return NAMING_DIRECTIONS[ordinal % len(NAMING_DIRECTIONS)]


def story_direction(day: str) -> str:
    try:
        ordinal = datetime.date.fromisoformat(day).toordinal()
    except ValueError:
        ordinal = sum(ord(char) for char in day)
    return STORY_DIRECTIONS[ordinal % len(STORY_DIRECTIONS)]


def _name_words(name: str) -> list[str]:
    return re.findall(r"[a-z]+", str(name).casefold())


def _edit_distance(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)
    previous = list(range(len(right) + 1))
    for i, char_left in enumerate(left, 1):
        current = [i]
        for j, char_right in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (char_left != char_right),
                )
            )
        previous = current
    return previous[-1]


def _near_word(left: str, right: str) -> bool:
    if left == right:
        return True
    if min(len(left), len(right)) < 3 or abs(len(left) - len(right)) > 1:
        return False
    return _edit_distance(left, right) <= 1


def _common_prefix_length(left: str, right: str) -> int:
    length = 0
    for a, b in zip(left, right):
        if a != b:
            break
        length += 1
    return length


def name_diversity_complaints(name: str, recent_names: list[str]) -> list[str]:
    words = _name_words(name)
    if not words:
        return []
    normalized = " ".join(words)
    first = words[0]
    last = words[-1] if len(words) > 1 else ""
    complaints: list[str] = []

    for recent in recent_names:
        recent_words = _name_words(recent)
        if not recent_words:
            continue
        if normalized == " ".join(recent_words):
            return [
                f"character name {name!r} exactly repeats recent name {recent!r}; "
                "choose a genuinely different name"
            ]

    for recent in recent_names:
        recent_words = _name_words(recent)
        if recent_words and _near_word(first, recent_words[0]):
            complaints.append(
                f"character given name {first!r} repeats or nearly repeats recent "
                f"name {recent!r}; choose a different given-name root"
            )
            break

    if last:
        for recent in recent_names:
            recent_words = _name_words(recent)
            if len(recent_words) < 2:
                continue
            recent_last = recent_words[-1]
            if min(len(last), len(recent_last)) >= 6 and _common_prefix_length(last, recent_last) >= 6:
                complaints.append(
                    f"character surname {last!r} echoes the distinctive root of recent "
                    f"name {recent!r}; choose a different surname construction"
                )
                break
    return complaints


def _word_set(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z]{5,}", str(text).casefold())
        if word not in PREMISE_STOPWORDS
    }


def _proposal_creative_text(proposal: dict) -> str:
    return " ".join(_flatten_creative_values(proposal))


def _proposal_names(proposal: dict) -> list[str]:
    """Every asset name/title in a proposal — the surface the rut families guard."""
    names: list[str] = [str(proposal.get("title") or "")]
    vibe = proposal.get("vibe")
    if isinstance(vibe, dict):
        names.append(str(vibe.get("title") or ""))
    for key, field in (
        ("locations", "title"),
        ("characters", "name"),
        ("rewards", "name"),
        ("scenarios", "title"),
    ):
        for row in proposal.get(key) or []:
            if isinstance(row, dict):
                names.append(str(row.get(field) or ""))
    return [name for name in names if name]


def _proposal_character_names(proposal: dict) -> list[str]:
    """Character names only — the surface the surname-factory detector guards."""
    names = [
        str(row.get("name") or "")
        for row in proposal.get("characters") or []
        if isinstance(row, dict)
    ]
    return [name for name in names if name]


def story_diversity_complaints(
    proposal: dict,
    recent_premises: list[str],
    seed_facets: dict | None = None,
) -> list[str]:
    """Reject high-signal premise ruts so the model gets one corrective retry."""
    creative_text = _proposal_creative_text(proposal).casefold()
    facet_text = json.dumps(seed_facets or {}, ensure_ascii=False).casefold()
    creative_words = set(re.findall(r"[a-z]+", creative_text))
    facet_words = set(re.findall(r"[a-z]+", facet_text))
    complaints: list[str] = prose.complaints(proposal)

    bureaucratic_hits = creative_words & BUREAUCRACY_MARKERS
    facets_request_bureaucracy = bool(facet_words & BUREAUCRACY_FACET_MARKERS)
    if bureaucratic_hits and not facets_request_bureaucracy:
        examples = ", ".join(sorted(bureaucratic_hits)[:5])
        complaints.append(
            "story falls back into the overused bureaucracy/record-keeping motif "
            f"({examples}) even though today's Facets do not request it; replace the "
            "institution, conflict engine, and signature objects with a different kind of story"
        )

    all_names = _proposal_names(proposal)
    complaints.extend(ruts.name_rut_complaints(all_names, facet_text))

    # These two detectors already existed but were only ever consulted by the
    # after-the-fact catalog audit, so the authoring retry never saw them and
    # ornamental compound surnames kept shipping (Vex Thistlewick on 2026-08-05,
    # then Vex Thistlemaw on 2026-08-16). Same call shape as audit_dream_catalog.
    for character_name in _proposal_character_names(proposal):
        surname = ruts.surname_factory_complaint(character_name)
        if surname:
            complaints.append(
                f"character name {character_name!r}: {surname}; rename with a plausible "
                "family name instead of a noun-compound built from the recurring stem list"
            )
    honorifics = ruts.honorific_hits(all_names)
    if honorifics:
        complaints.append(
            "civil-service honorific in an asset name ("
            + ", ".join(sorted(honorifics))
            + "); drop the rank/title and name the character as a person"
        )

    candidate_terms = _word_set(creative_text)
    for recent in recent_premises[-PREMISE_HISTORY_LIMIT:]:
        recent_terms = _word_set(recent)
        overlap = candidate_terms & recent_terms
        distinctive = {word for word in overlap if len(word) >= 7}
        if len(distinctive) >= 5:
            examples = ", ".join(sorted(distinctive)[:6])
            complaints.append(
                "story substantially echoes a recent premise through distinctive vocabulary "
                f"({examples}); change the setting machinery, conflict, and key objects rather "
                "than paraphrasing the prior world"
            )
            break
    return complaints


def _brief_prompt(
    brief: dict,
    history: dict[str, list[str]] | None = None,
    premise_history: list[str] | None = None,
) -> str:
    facets = json.dumps(brief["seed_facets"], ensure_ascii=False, indent=2)
    rules = "\n".join(f"- {line}" for line in brief.get("instructions", []))
    history = history or {category: [] for category in HISTORY_CATEGORIES}
    history_lines = []
    for category in HISTORY_CATEGORIES:
        values = history.get(category) or []
        if values:
            history_lines.append(
                f"- {category.title()}: " + "; ".join(values[-HISTORY_PROMPT_LIMIT:])
            )
    history_text = "\n".join(history_lines) or "- No recent naming history available."

    premises = premise_history or []
    premise_lines = [f"- {value}" for value in premises[-PREMISE_PROMPT_LIMIT:]]
    premise_text = "\n".join(premise_lines) or "- No recent premise history available."

    return (
        f"Compose the Daily Dream bundle for {brief['proposal_date']}.\n\n"
        "These Facets are the creative constraints. The umbrella genres and creature "
        "govern the whole bundle; each element's own Facet list governs that element. "
        "Use them all. Awkward combinations are creative fuel, not permission to retreat "
        f"to a familiar setting.\n\n{facets}\n\n"
        f"House rules:\n{rules}\n\n"
        "Recent naming history, oldest to newest. This is spent vocabulary and construction, "
        f"not inspiration to remix:\n{history_text}\n\n"
        "Recent premise history, oldest to newest. Treat settings, institutions, conflict "
        "mechanisms, signature objects, jobs, rituals, and narrative tricks here as spent. "
        f"Do not reskin them with today's Facets:\n{premise_text}\n\n"
        f"Character naming direction for today: {naming_direction(str(brief['proposal_date']))}\n"
        "Follow its structural shape while fitting the character and world.\n\n"
        f"Narrative engine for today: {story_direction(str(brief['proposal_date']))}\n"
        "Use this to push plot structure away from recent days without overriding the Facets.\n\n"
        "Before returning JSON, ask yourself whether this could plausibly be a screenshot from "
        "one of the recent worlds with nouns swapped. If yes, rebuild it more radically.\n\n"
        "Return the JSON object only."
    )


def call_claude(prompt: str, system: str, api_key: str, timeout: float = 120.0) -> str:
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()
    request = urllib.request.Request(API_URL, data=body, method="POST")
    request.add_header("content-type", "application/json")
    request.add_header("x-api-key", api_key)
    request.add_header("anthropic-version", API_VERSION)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode())
    blocks = payload.get("content") or []
    text = "".join(block.get("text", "") for block in blocks if isinstance(block, dict))
    if not text.strip():
        raise RuntimeError("Claude returned an empty completion.")
    return text


def parse_json_object(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.rstrip().endswith("```"):
            cleaned = cleaned.rstrip()[:-3]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in the completion")
    return json.loads(cleaned[start:end + 1])


def author(day: str, api_key: str, verbose: bool = True) -> dict:
    brief = dreams.build_brief(day)
    history = recent_name_history(day)
    premise_history = recent_premise_history(day)
    prompt = _brief_prompt(brief, history, premise_history)
    complaints: list[str] = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        ask = prompt
        if complaints:
            ask += (
                "\n\nYour previous attempt failed validation:\n"
                + "\n".join(f"- {complaint}" for complaint in complaints)
                + "\n\nReturn a corrected JSON object addressing every point."
            )
        if verbose:
            print(f"authoring {day} (attempt {attempt}/{MAX_ATTEMPTS})", file=sys.stderr)

        try:
            proposal = parse_json_object(call_claude(ask, SYSTEM_PROMPT, api_key))
        except (ValueError, json.JSONDecodeError) as error:
            complaints = [f"completion was not valid JSON: {error}"]
            if verbose:
                print("  rejected: " + complaints[0], file=sys.stderr)
            continue

        proposal["seed_facets"] = brief["seed_facets"]
        proposal.pop("narrator", None)

        normalized = dreams.normalize(proposal, dreams.existing_slugs())
        complaints = dreams.validate_proposal(normalized)
        characters = proposal.get("characters") or []
        if characters and isinstance(characters[0], dict):
            complaints.extend(
                name_diversity_complaints(
                    characters[0].get("name", ""), history.get("characters", [])
                )
            )
        complaints.extend(
            story_diversity_complaints(proposal, premise_history, brief["seed_facets"])
        )
        if not complaints:
            return proposal
        if verbose:
            print("  rejected: " + "; ".join(complaints[:5]), file=sys.stderr)

    raise RuntimeError(
        "Could not author a valid proposal after "
        f"{MAX_ATTEMPTS} attempts: {'; '.join(complaints)}"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="Pacific date override (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="print rendered markdown without writing")
    parser.add_argument("--force", action="store_true", help="author even if the date already has a proposal")
    parser.add_argument("--no-fetch", action="store_true", help="skip the origin/main duplicate check")
    args = parser.parse_args(argv)

    day = args.date or dreams._target_date()
    if not args.force:
        exists = dreams.proposal_exists_for(day)
        if not exists and not args.no_fetch and dreams.fetch_main():
            exists = dreams.remote_proposal_for(day) is not None
        if exists:
            print(f"Proposal for {day} already exists; nothing to author.")
            return 0
        backlog = dreams.unbuilt_backlog()
        if len(backlog) >= dreams.TARGET_BUFFER_DAYS:
            print(
                f"Docket already holds {len(backlog)} unbuilt proposals "
                f"({backlog[0]}..{backlog[-1]}), at or above the "
                f"{dreams.TARGET_BUFFER_DAYS}-day buffer; skipping authoring. "
                "Spend the cycle on other work or on improving what is queued."
            )
            return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print(
            "ANTHROPIC_API_KEY is required to author a dream proposal. Refusing to write a "
            "placeholder because a hollow proposal can hide the missing real one.",
            file=sys.stderr,
        )
        return 1

    try:
        proposal = author(day, api_key)
    except (urllib.error.URLError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"Could not author the {day} proposal: {error}", file=sys.stderr)
        return 1

    path = dreams.write_proposal(
        proposal,
        date=day,
        fetch=not args.no_fetch,
        dry_run=args.dry_run,
        force=args.force,
    )
    return 0 if path else 1


if __name__ == "__main__":
    raise SystemExit(main())
