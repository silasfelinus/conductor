#!/usr/bin/env python3
"""Rewrite every live artPrompt that tells Krea 2 what NOT to draw.

WHY THIS EXISTS

Krea 2 renders at cfg 1 (kind_robots `KREA2_DEFAULT_CFG`), where the ComfyUI
negative prompt is wired but inert. Nothing a prompt excludes can be acted on,
so an exclusion is simply a noun in positive conditioning on a Qwen-Image
lineage model -- the strongest open text renderer there is. ART-PROMPTS.md has
said since 2026-08-25 that this means "`no face` is how you commission a face".

The code never enforced it. `server/utils/artPromptContract.ts` had one negation
rule and it counted only TEXT nouns, in bulk (more than four). So:

  * 319 of 351 live Rewards carry a people negation. Reward 393, "Dr. Eliza
    Dolittle's Ring", asks for a ring on a leaf and ends "No figure."; it
    rendered as a crowd of Victorian faces and no ring.
  * The 2026-08-08 repair is the single largest producer of them. The clause
    written to STOP the crowds -- "an unpeopled frame, the subject stands alone
    with no bystanders, no onlookers, and no crowd" -- names three kinds of
    people. "unpeopled" was doing the work; the tail was undoing it.
  * A suggested prompt ending "no readable text, no logo, no watermark, no
    collage" passed the gate on 2026-09-19 with three text nouns, one under the
    threshold, and painted a block of garbled caption into the image.

The forward fixes are in kind_robots (`artPromptContract.ts` rule 7,
`artJobNormalization.ts`, `kreaSemanticPrompt.ts`, `artAssetSuggest.ts`) and in
this repo (`dream_art_prompts.py`, `repair_queued_cast_prompts.py`,
`queue_monster_recast_art.py`, `consume_coloring_book_color_art.py`). This
script cleans up what is already stored.

WHAT IT DOES

Deterministic clause surgery, never a rewrite of the subject. It removes the
offending clause and, where the clause was carrying real intent, states that
intent positively instead:

  people exclusion   -> "an unpeopled frame, the subject alone, the space
                        around it bare and deserted"   (once, only if the
                        prompt does not already say something equivalent)
  text exclusion     -> "every surface bare and unmarked"
  layout exclusion   -> "one single image filling the frame"
  crowd cast clause  -> removed outright (the 2026-08-08 defect)
  art-direction jargon / contextual wrapper -> removed outright

Every rewrite is re-checked against the same detectors afterwards, and a prompt
that does not come out clean is reported and skipped rather than written.

Usage:
  python scripts/repair_negation_art_prompts.py                  # audit only
  python scripts/repair_negation_art_prompts.py --show 20        # with diffs
  python scripts/repair_negation_art_prompts.py --apply          # PATCH prompts
  python scripts/repair_negation_art_prompts.py --apply --render # ...and re-render
  python scripts/repair_negation_art_prompts.py --apply --render --limit 40
  python scripts/repair_negation_art_prompts.py --kind reward --apply --render

`--render` queues EVERY repaired record by default. An earlier draft capped it,
on a misread of /api/art/queue/stats: its `windowThroughput` groups jobs by
CREATION time, so "DONE: 8" means eight of the jobs created today have finished,
not that the renderer managed eight all day. Measured from completion
timestamps the relay turns one around every 3-4 minutes -- ~120 on the day this
was written -- so a full pass is a couple of days of queue time, and a queue
left half empty between batches is slower than one kept full. Silas,
2026-09-19: "do not cap renders, that's just silly. we should be filling the
queue so it doesn't sit idle between generations." `--limit` still exists for
a deliberate smoke test.

Priority is the lever that makes this safe to bulk-queue (see
kind_robots utils/artJobPriority.ts). The relay claims by `priority DESC, id
ASC`. Interactive work -- a human clicking Generate and waiting -- enters at
100, and a repair must not outrank that. The stale bulk lanes (Facet catalog,
daily-dream coverage) sit at 0 and below. So repairs land in between, high
enough to keep the renderer busy ahead of a four-day-old backlog and low
enough that a person waiting on a redo still wins:

  reward   60   the cards an owner actually looks at
  others   40

Re-renders use preserveOriginal, so the old image stays in the record's art
history rather than being destroyed.

Environment:
  KR_API_TOKEN   required for --apply / --render
  KR_BASE_URL    defaults to https://kindrobots.org

Exit codes:
  0  nothing to repair, or the run applied cleanly
  1  violations found (audit mode), or some writes failed
  2  could not check (no token, or the API was unreachable)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any, Iterable, Optional

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

# ── The detectors ───────────────────────────────────────────────────────────
#
# Mirrors server/utils/artPromptContract.ts. The noun sets are deliberately the
# same ones, including its exclusions: `hand`, `body`, `cast`, `man`,
# `portrait` and `silhouette` stay OUT, because "a clock with no hands" and "no
# man's land" are subjects, not casting notes, and a false positive here
# rewrites a prompt that was fine.

PEOPLE_NOUNS = (
    "figures?|persons?|people|humans?|characters?|faces?|crowds?|bystanders?|"
    "onlookers?|spectators?|men|wom[ae]n|child|children|audiences?"
)
TEXT_NOUNS = (
    "text|lettering|letters|words|wording|logos?|watermarks?|signatures?|"
    "captions?|typography|writing|brand marks?|explanations?|labels?|"
    "titles?|subtitles?|numerals?"
)
LAYOUT_NOUNS = (
    "collages?|contact sheets?|grids?|borders?|framing panels?|comic panels?|panels?"
)
NEG = r"(?:no|not|without|avoid|avoiding|never|free of|devoid of|absent of|excluding)"
# Up to two adjectives between the negation and the noun: the live wordings are
# "no FULL figure", "no CLEAR face", "no MORTAL figure", "no LITERAL person".
ADJ = r"(?:[a-z][a-z-]*\s+){0,2}"

def _clause(nouns: str) -> re.Pattern[str]:
    """A negation and everything it governs, including a trailing noun list.

    "no readable text, no lettering, no logos" is ONE clause, not three: the
    repeated "no" is part of the same run and removing them one at a time
    leaves ", ," debris behind.
    """
    one = rf"{NEG}\s+{ADJ}(?:{nouns})"
    return re.compile(
        rf"(?:^|[,;.]|\s)\s*{one}(?:\s*(?:,|and|or)\s*(?:{NEG}\s+)?{ADJ}(?:{nouns}))*",
        re.I,
    )

PEOPLE_CLAUSE = _clause(PEOPLE_NOUNS)
TEXT_CLAUSE = _clause(TEXT_NOUNS)
LAYOUT_CLAUSE = _clause(LAYOUT_NOUNS)

# The 2026-08-08 unconditional casting block, anchored on both ends.
CROWD_CAST_CLAUSE = re.compile(
    r"[,;]?\s*cast characters naturally across many species"
    r"(?:.*?conventional attractiveness)?"
    r"(?:\s*;\s*include robots only when the subject or scene "
    r"explicitly calls for them)?",
    re.I,
)

JARGON_CLAUSE = re.compile(
    r"[,;.]?\s*(?:"
    r"[Ii]conic scene(?:,\s*concrete focal subject)?(?:,\s*environment)?"
    r"(?:,\s*action)?(?:,\s*strong atmosphere)?"
    r"|concrete\s+(?:focal\s+)?subject"
    r"|(?:unmistakable|clean)\s+silhouette(?:,\s*workplace cues)?"
    r"|excellent thumbnail readability|legible at thumbnail size"
    r"|crisp subject separation|subject separation"
    r")\.?",
    re.I,
)

# Contract rule 2, the half this script can repair mechanically. "2:3 portrait
# card composition" is framing language to a person and a trading CARD to a
# caption-conditioned model -- three rewards came back as literal cards with a
# title bar and a rules box full of invented text. The geometry is the part
# worth keeping, so the format noun is dropped and the shape stays.
#
# Deliberately ONLY this phrasing. The other format hits in the live catalog are
# not mistakes: rewards 249 and 284 and scenarios 159 and 175 depict a wanted
# poster because a wanted poster is what is in the picture, and six Resource
# rows ("Movie Poster", "vintage comic book cover") are LoRA trigger text where
# the format IS the concept being trained. Rewriting those would remove the
# subject. A format noun is only a bug when it names the artefact the image is
# printed ON rather than the thing the image is OF, and no regex can tell those
# apart -- so this one is pinned to the phrasing with rendered evidence behind
# it.
CARD_COMPOSITION = re.compile(
    r"\b(?:2:3\s+)?(?:vertical\s+)?(?:portrait\s+)?card composition\b", re.I
)

# Contract rule "format-vocabulary", the other half of it. `CARD_COMPOSITION`
# above rewrites the FRAMING ("2:3 portrait card composition"); seven Reward
# prompts also name the card as an OBJECT a few clauses later -- "rare-tier
# ability card illustration", "uncommon-tier treasure card illustration". Fixing
# only the framing left all seven still rejected, because the contract flags
# `(?:treasure|ability|item|reward)[- ]card` on its own evidence: rewards came
# back as literal cards with a title bar and a rules box.
#
# Removed rather than substituted, unlike the framing. The aspect ratio in
# "2:3 portrait card composition" is real direction worth keeping; "rare-tier"
# is a database rarity and "ability card illustration" is the artefact the
# picture would be printed on. Neither describes anything visible, and each of
# these prompts already carries its full subject, lighting and style tail.
TIER_CARD_CLAUSE = re.compile(
    r"[,;.]?\s*(?:[a-z]+-tier\s+)?(?:ability|treasure|item|reward)[- ]card"
    r"(?:\s+(?:illustration|art|artwork))?\.?",
    re.I,
)

# Rule 3 in a place the clause anchors could not see. `_clause` starts at `^`,
# a `,;.` separator, or whitespace -- and a negation opening a parenthetical
# has `(` in front of it, which is none of those. Two Rewards survived the
# whole pass that way: 424's "(no specific copyrighted character -- just
# classic comic styling)" and 249's "(no readable text)". Krea reads both
# parentheses as ordinary words, so "no readable text" is still an order for
# lettering whatever bracket it sits in.
#
# The half after the dash is real direction, so it is kept rather than dropped
# with the rest: 424 means "classic comic styling", and that survives.
NEGATED_PARENTHETICAL = re.compile(rf"\s*\(\s*(?P<inner>{NEG}\b[^)]*)\)", re.I)
PAREN_PIVOT = re.compile(r"\s*(?:\u2014|\u2013|--)\s*")
PAREN_FILLER = re.compile(r"^(?:just|only|simply|merely)\s+", re.I)


def strip_negated_parenthetical(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        halves = PAREN_PIVOT.split(match.group("inner"), maxsplit=1)
        if len(halves) == 2 and halves[1].strip():
            kept = PAREN_FILLER.sub("", halves[1].strip())
            if kept:
                return f", {kept}"
        return ""

    return NEGATED_PARENTHETICAL.sub(replace, text)


# Contract rule "vague-brand-style". Three dream prompts still end "cohesive
# Kind Robots visual style", which the contract rejects because it carries no
# visual information -- and all three are the thin, logline-only prompts that
# rule 4 warns are exactly where a boilerplate clause becomes the whole prompt.
#
# The replacement is not invented: it is the tail this catalog already uses
# most often on its own illustrated entities, and it answers the contract's
# own instruction to write the medium, linework, colour and surface out.
BRAND_STYLE_CLAUSE = re.compile(
    r"\b(?:(?:rich|cohesive|friendly)\s+)?Kind Robots\s+(?:visual\s+)?(?:style|language)\b",
    re.I,
)
BRAND_STYLE_REPLACEMENT = (
    "detailed mature western animation illustration, confident ink-like "
    "linework, dimensional forms, rich controlled color, tactile surface texture"
)

WRAPPER_CLAUSE = re.compile(
    r"(?:"
    r"Illustrate the Facet concept[^.]*\.?"
    r"|Create (?:this as|a|one) [^.\n]{0,200}\bfor Kind Robots\b[^.]*\.?"
    r"|Compose this as [^.\n]{0,240} for the following [a-z]+\.?"
    r"|Create this artwork for the following [a-z]+\.?"
    r"|Treat the first paragraph as (?:the )?(?:primary )?art direction[^.]*\.?"
    r"|Use the (?:entity|dream|facet|character|scenario|reward|bot) context[^.]*\.?"
    # Database bookkeeping that reached the prompt with the Facet wrapper. Its
    # sibling "Scientific identity: Ambystoma mexicanum" is deliberately NOT
    # matched -- a species name is visual information.
    r"|Catalog category:\s*[a-z-]+\.?"
    r")",
    re.I,
)

RULES: tuple[tuple[str, re.Pattern[str], Optional[str], re.Pattern[str]], ...] = (
    # (rule name, clause to remove, positive replacement to ensure, "already said it" test)
    (
        "people-negation",
        PEOPLE_CLAUSE,
        "an unpeopled frame, the subject alone, the space around it bare and deserted",
        re.compile(r"\bunpeopled\b|\bdeserted\b|\buninhabited\b", re.I),
    ),
    (
        "text-exclusion",
        TEXT_CLAUSE,
        "every surface bare and unmarked",
        re.compile(r"\b(?:bare and )?unmarked\b|\bblank\b", re.I),
    ),
    (
        "layout-exclusion",
        LAYOUT_CLAUSE,
        "one single image filling the frame",
        re.compile(r"\bone single image\b|\bfull-bleed\b|\bedge to edge\b", re.I),
    ),
    ("crowd-cast-clause", CROWD_CAST_CLAUSE, None, re.compile(r"(?!)")),
    ("art-direction-jargon", JARGON_CLAUSE, None, re.compile(r"(?!)")),
    ("contextual-wrapper", WRAPPER_CLAUSE, None, re.compile(r"(?!)")),
)


# A removed clause can strand the word that introduced it. "the subject stands
# alone with no bystanders, no onlookers, and no crowd" loses its object and
# becomes "the subject stands alone with," -- debris that then goes back into
# positive conditioning as a broken sentence.
DANGLING = re.compile(
    r"\b(?:with|and|or|plus|including|featuring|containing|of|but)\s*(?=[,;.]|$)",
    re.I,
)


def tidy(text: str) -> str:
    """Close the holes a removed clause leaves behind."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,;.])", r"\1", text)
    text = DANGLING.sub("", text)
    text = re.sub(r"(?:\s*,){2,}", ",", text)
    text = re.sub(r"\.\s*,", ".", text)
    text = re.sub(r",\s*\.", ".", text)
    text = re.sub(r"(?:\s*\.){2,}", ".", text)
    text = re.sub(r"\s+([,;.])", r"\1", text)
    text = re.sub(r"^[\s,;.]+", "", text)
    text = re.sub(r"[\s,;]+$", "", text)
    return text.strip()


# A `resource` row's artPrompt is LoRA trigger text, not a picture: it is never
# sent to Krea on its own, and its words are the trained concept rather than a
# description of a frame. resource/3590 "detailed_notrigger" reads "extremely
# detailed (no trigger) - sliders.ntcai.xyz", where "(no trigger)" is catalog
# bookkeeping that matches the row's own name -- deleting it would say the LoRA
# has a trigger word. Same carve-out the six "Movie Poster page" / "vintage
# comic book cover" rows get from the format rules: a format noun (or here a
# negation) is a bug when it names the artefact the image is printed ON, and
# metadata when it names the row.
PROSE_EXEMPT_KINDS = {"resource"}


def violations(prompt: str, kind: Optional[str] = None) -> list[str]:
    found = [name for name, pattern, _, _ in RULES if pattern.search(prompt or "")]
    if CARD_COMPOSITION.search(prompt or "") or TIER_CARD_CLAUSE.search(prompt or ""):
        found.append("format-vocabulary")
    if kind not in PROSE_EXEMPT_KINDS and NEGATED_PARENTHETICAL.search(prompt or ""):
        found.append("negated-parenthetical")
    if BRAND_STYLE_CLAUSE.search(prompt or ""):
        found.append("vague-brand-style")
    return found


def repair(prompt: str, kind: Optional[str] = None) -> str:
    """Remove every offending clause, then restate the intent positively."""
    text = prompt or ""
    restore: list[str] = []

    # A substitution, not a removal: the aspect ratio is real direction and only
    # the word "card" is the bug.
    text = CARD_COMPOSITION.sub("vertical 2:3 portrait composition", text)
    # The card as an object, though, has no geometry worth keeping.
    text = TIER_CARD_CLAUSE.sub("", text)
    text = BRAND_STYLE_CLAUSE.sub(BRAND_STYLE_REPLACEMENT, text)
    if kind not in PROSE_EXEMPT_KINDS:
        text = strip_negated_parenthetical(text)

    for _name, pattern, replacement, already in RULES:
        if not pattern.search(text):
            continue
        text = pattern.sub(" ", text)
        if replacement and not already.search(text):
            restore.append(replacement)

    text = tidy(text)
    if restore:
        addition = ", ".join(restore)
        if not text:
            text = addition[:1].upper() + addition[1:]
        elif text.endswith("."):
            # A sentence-shaped prompt gets a sentence, not a trailing fragment.
            text = f"{text} {addition[:1].upper() + addition[1:]}."
        else:
            text = f"{text}, {addition}"
    return tidy(text)


# ── The API ─────────────────────────────────────────────────────────────────

# Every model that carries an artPrompt AND can be re-rendered through
# /api/art/enqueue's entityArt path (server/utils/entityArt.ts EntityArtType).
KINDS: dict[str, dict[str, str]] = {
    "reward": {"list": "/api/rewards", "detail": "/api/rewards"},
    "facet": {"list": "/api/facets?take=250", "detail": "/api/facets", "paged": "1"},
    "character": {"list": "/api/characters", "detail": "/api/characters"},
    "scenario": {"list": "/api/scenarios", "detail": "/api/scenarios"},
    "dream": {"list": "/api/dreams", "detail": "/api/dreams"},
    "bot": {"list": "/api/bots", "detail": "/api/bots"},
    "achievement": {"list": "/api/achievements", "detail": "/api/achievements"},
    "resource": {"list": "/api/resources", "detail": "/api/resources"},
}

# Rewards first: their failure is the one Silas can see from the card, and the
# one with a 91% hit rate. Facets are the largest population but their damage is
# subtler (a desk lamp in a fantasy scene, a painted caption on a quirk card).
ORDER = ("reward", "facet", "character", "scenario", "dream", "bot", "achievement", "resource")

# Between /api/art/enqueue's interactive default (100) and the bulk lanes (0 and
# below). See the note in the module docstring: a repair should keep the relay
# busy ahead of a four-day-old Facet-catalog backlog without ever making a human
# who just clicked Generate wait behind 1,156 of them.
RENDER_PRIORITY = {"reward": 60}
DEFAULT_RENDER_PRIORITY = 40
PRIMARY_FIELD = {"bot": "avatarImage"}
DEFAULT_PRIMARY_FIELD = "imagePath"


def http_json(method: str, url: str, body: Any = None, timeout: int = 300):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Accept", "application/json")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        request.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode()
            return response.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as error:
        raw = error.read().decode(errors="replace")
        try:
            return error.code, json.loads(raw)
        except json.JSONDecodeError:
            return error.code, {"message": raw[:300]}
    except OSError as error:
        return 0, {"message": str(error)}


def fetch(kind: str) -> list[dict[str, Any]]:
    config = KINDS[kind]
    if not config.get("paged"):
        status, payload = http_json("GET", f"{KR_BASE_URL}{config['list']}")
        if status != 200:
            raise RuntimeError(f"GET {config['list']} -> {status} {str(payload)[:160]}")
        return list(payload.get("data") or [])

    # /api/facets caps `take` at 250 and its `count` reports the page, not the
    # catalog -- reading it as a total stops after 250 of 1,734 rows.
    rows: list[dict[str, Any]] = []
    skip = 0
    while skip < 20000:
        status, payload = http_json("GET", f"{KR_BASE_URL}{config['list']}&skip={skip}")
        if status != 200:
            raise RuntimeError(f"GET {config['list']} -> {status} {str(payload)[:160]}")
        page = list(payload.get("data") or [])
        if not page:
            break
        rows.extend(page)
        skip += 250
    seen: set[int] = set()
    unique = []
    for row in rows:
        if row.get("id") in seen:
            continue
        seen.add(row["id"])
        unique.append(row)
    return unique


def label(row: dict[str, Any]) -> str:
    for field in ("name", "title", "label", "slug"):
        if row.get(field):
            return str(row[field])
    return f"#{row.get('id')}"


def patch_prompt(kind: str, row_id: int, prompt: str) -> bool:
    status, payload = http_json(
        "PATCH", f"{KR_BASE_URL}{KINDS[kind]['detail']}/{row_id}", {"artPrompt": prompt}
    )
    if status not in (200, 201):
        print(f"    PATCH FAILED {status} {kind}/{row_id}: {str(payload)[:160]}", file=sys.stderr)
        return False
    return True


def enqueue_render(kind: str, row: dict[str, Any], prompt: str,
                   priority: Optional[int] = None) -> Optional[int]:
    body = {
        "engine": "krea2",
        "promptString": prompt,
        "width": 1024,
        "height": 1024,
        "isPublic": bool(row.get("isPublic", True)),
        "isMature": bool(row.get("isMature", False)),
        "designer": "negation-repair",
        "priority": RENDER_PRIORITY.get(kind, DEFAULT_RENDER_PRIORITY)
        if priority is None
        else priority,
        "entityArt": {
            "entityType": kind,
            "entityId": row["id"],
            # bot's primary slot is avatarImage, not imagePath; sending the
            # latter is refused with 400 "Invalid bot image field."
            "field": PRIMARY_FIELD.get(kind, DEFAULT_PRIMARY_FIELD),
            # The crowd images stay in object history rather than being destroyed.
            "preserveOriginal": True,
            "mode": "recreate",
        },
    }
    status, payload = http_json("POST", f"{KR_BASE_URL}/api/art/enqueue", body)
    if status not in (200, 201):
        print(f"    ENQUEUE FAILED {status} {kind}/{row['id']}: {str(payload)[:200]}", file=sys.stderr)
        return None
    job = ((payload or {}).get("data") or {}).get("jobId")
    return int(job) if job else None


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind", choices=ORDER, action="append",
                        help="limit to one entity kind (repeatable)")
    parser.add_argument("--apply", action="store_true", help="PATCH the repaired prompts")
    parser.add_argument("--render", action="store_true",
                        help="also enqueue a re-render for every repaired record")
    parser.add_argument("--limit", type=int, default=0, metavar="N",
                        help="cap --render at N jobs (default: no cap)")
    parser.add_argument("--priority", type=int, default=None, metavar="P",
                        help="override the per-kind render priority (-1000..1000)")
    parser.add_argument("--show", type=int, default=0, metavar="N",
                        help="print N before/after pairs")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if (args.apply or args.render) and not KR_API_TOKEN:
        print("KR_API_TOKEN is required for --apply/--render.", file=sys.stderr)
        return 2

    kinds = args.kind or list(ORDER)
    findings: list[dict[str, Any]] = []
    by_rule: dict[str, int] = {}
    scanned = 0

    for kind in kinds:
        try:
            rows = fetch(kind)
        except RuntimeError as error:
            print(f"{kind}: {error}", file=sys.stderr)
            return 2
        for row in rows:
            prompt = (row.get("artPrompt") or "").strip()
            if not prompt:
                continue
            scanned += 1
            found = violations(prompt, kind)
            if not found:
                continue
            fixed = repair(prompt, kind)
            remaining = violations(fixed, kind)
            for rule in found:
                by_rule[rule] = by_rule.get(rule, 0) + 1
            findings.append({
                "kind": kind, "row": row, "rules": found,
                "before": prompt, "after": fixed, "remaining": remaining,
            })

    print(f"Scanned {scanned} live artPrompts across {len(kinds)} entity kinds.")
    print(f"Violating: {len(findings)}"
          f" ({100 * len(findings) / scanned:.1f}%)" if scanned else "")
    if by_rule:
        print("\nBy rule:")
        for rule, count in sorted(by_rule.items(), key=lambda item: -item[1]):
            print(f"  {count:6d}  {rule}")
        print("\nBy kind:")
        for kind in kinds:
            count = sum(1 for f in findings if f["kind"] == kind)
            if count:
                print(f"  {count:6d}  {kind}")

    unclean = [f for f in findings if f["remaining"]]
    if unclean:
        print(f"\n{len(unclean)} prompt(s) did not come out clean and will be SKIPPED:")
        for finding in unclean[:10]:
            print(f"  {finding['kind']}/{finding['row']['id']} {label(finding['row'])}"
                  f" -> still {finding['remaining']}")

    for finding in findings[: args.show]:
        print("\n" + "-" * 76)
        print(f"{finding['kind']}/{finding['row']['id']}  {label(finding['row'])}  {finding['rules']}")
        print(f"  BEFORE: {finding['before']}")
        print(f"  AFTER : {finding['after']}")

    if not args.apply:
        if findings:
            print("\nAudit only. Re-run with --apply to write the repaired prompts.")
        return 1 if findings else 0

    writable = [f for f in findings if not f["remaining"]]
    patched = failed = refused = 0
    for finding in writable:
        if patch_prompt(finding["kind"], finding["row"]["id"], finding["after"]):
            patched += 1
        else:
            failed += 1
    print(f"\nPatched {patched} prompt(s); {failed} failed; {len(unclean)} skipped.")

    if args.render:
        cap = args.limit or len(writable)
        rendered = 0
        for kind in ORDER:
            for finding in writable:
                if rendered >= cap:
                    break
                if finding["kind"] != kind:
                    continue
                job = enqueue_render(kind, finding["row"], finding["after"], args.priority)
                if job:
                    rendered += 1
                    if rendered % 25 == 0:
                        print(f"  ... {rendered} queued")
                else:
                    refused += 1
            if rendered >= cap:
                break
        print(f"Enqueued {rendered} re-render(s); {refused} refused.")

    return 1 if failed or refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
