"""Reject character-art prompts that erase canonical anatomy or silhouettes.

The 48 stable identities and their distinguishing visible markers are transcribed
from Kind Robots utils/cometAcademy/castLooks.ts. This is a *pre-enqueue* text
check, not an approval of generated pixels. Historic ArtJobs are not requeued.
"""

from __future__ import annotations

import re
from typing import Any

# Match physically recognizable traits, allowing equivalent literal descriptions
# rather than requiring an entire verbatim castLooks sentence.
# Ordered (label, regular expression) pairs describe the most conspicuous
# morphology/silhouette cues for every origin x affinity identity.
CANON_TRAITS: dict[str, tuple[tuple[str, str], ...]] = {
    "accident-fire": (
        ("orange-lit forearms", r"\b(?:orange.{0,25}(?:glow|light).{0,45}forearms?|forearms?.{0,40}orange)\b"),
    ),
    "accident-air": (
        ("branching lightning scar", r"\b(?:lightning|branching).{0,24}\bscar\b|\bscar.{0,24}\blightning\b"),
    ),
    "accident-earth": (
        ("granite skin patches", r"\bgranite.{0,35}\b(?:patches|knuckles|cheekbones)\b"),
    ),
    "accident-water": (
        ("wet hair or blue gill skin", r"\b(?:dripping|wet).{0,20}\bhair\b|\b(?:blue|gill).{0,24}\bgill\b"),
    ),
    "accident-discipline": (
        ("starburst temple scar", r"\bstarburst.{0,20}\bscar\b|\bscar.{0,20}\bstarburst\b"),
    ),
    "accident-genius": (
        ("copper-red pencil bun", r"\b(?:copper|red).{0,32}\bbun\b|\bpencils?.{0,24}\bbun\b"),
    ),
    "accident-birthright": (
        ("slicked-back blond hair", r"\b(?:slicked.back.{0,22}blond|blond.{0,22}slicked.back)\b"),
    ),
    "accident-social": (
        ("green mullet", r"\b(?:green.{0,25}mullet|mullet.{0,25}green)\b"),
    ),
    "mutant-fire": (
        ("flaming ember hair", r"\b(?:ember.{0,20}hair|flames?.{0,26}hair|hair.{0,30}flames?)\b"),
    ),
    "mutant-air": (
        ("feathered wings", r"\b(?:feather(?:ed|s)?.{0,65}wings?|wings?.{0,65}feather(?:ed|s)?)\b"),
    ),
    "mutant-earth": (
        ("slate mineral plates", r"\b(?:slate|mineral|stone).{0,35}\bplates?\b"),
    ),
    "mutant-water": (
        ("gills and webbed fingers", r"\bgill(?:s|[- ]slits)?\b.{0,130}\bwebbed\b|\bwebbed\b.{0,130}\bgill"),
    ),
    "mutant-discipline": (
        ("four biological arms", r"\b(?:four|4)\s+(?:\w+\s+){0,3}arms\b|\b(?:second|lower)\s+pair\s+of\s+(?:\w+\s+){0,3}arms\b|\btwo\s+pairs\s+of\s+(?:\w+\s+){0,3}arms\b"),
    ),
    "mutant-genius": (
        ("crystalline temple growth", r"\b(?:crystalline|crystal).{0,35}\b(?:growth|temples?)\b"),
    ),
    "mutant-birthright": (
        ("white wings and silver braids", r"\b(?:white.{0,35}wings?|wings?.{0,35}white)\b"),
    ),
    "mutant-social": (
        ("neck adhesive patch", r"\b(?:adhesive|beige).{0,25}\bpatch\b|\bpatch.{0,35}\bneck\b"),
    ),
    "tech-fire": (
        ("burn-scarred knuckles", r"\bburn.{0,25}\bscar|\bscars?.{0,30}\bknuckles\b"),
    ),
    "tech-air": (
        ("blue-tipped hair or racing goggles", r"\b(?:blue.{0,24}tips?|racing.{0,20}goggles?)\b"),
    ),
    "tech-earth": (
        ("bandana-tied locs", r"\b(?:locs?.{0,35}bandana|bandana.{0,35}locs?)\b"),
    ),
    "tech-water": (
        ("long wavy ponytail", r"\b(?:wavy.{0,40}ponytail|ponytail.{0,40}wavy|high ponytail)\b"),
    ),
    "tech-discipline": (
        ("running-blade prosthetics", r"\b(?:running[- ]blades?|prosthetic.{0,30}blades?|blades?.{0,30}prosthetic)\b"),
    ),
    "tech-genius": (
        ("adult human inventor", r"\b(?:adult.{0,18}human|human.{0,20}inventor)\b"),
        ("brass goggles", r"\b(?:brass.{0,25}goggles?|goggles?.{0,25}brass)\b"),
    ),
    "tech-birthright": (
        ("styled chestnut hair", r"\b(?:chestnut.{0,25}hair|hair.{0,25}chestnut)\b"),
    ),
    "tech-social": (
        ("bleached hair streaks", r"\b(?:bleached.{0,25}streaks?|streaks?.{0,25}bleached)\b"),
    ),
    "magic-fire": (
        ("grey-streaked auburn braid", r"\b(?:auburn.{0,35}braid|braid.{0,35}auburn)\b"),
    ),
    "magic-air": (
        ("wavy light-brown hair", r"\b(?:wavy.{0,32}brown hair|light.brown.{0,25}wavy)\b"),
    ),
    "magic-earth": (
        ("elderly woman", r"\b(?:elderly|senior|older woman|aged woman)\b"),
        ("silver hair buns", r"\b(?:silver|white|grey|gray).{0,45}\b(?:hair|braid|buns?)\b|\b(?:two|double)\s+buns\b"),
    ),
    "magic-water": (
        ("pencil mustache", r"\bpencil.{0,20}\b(?:mustache|moustache)\b"),
    ),
    "magic-discipline": (
        ("iron rings on ear", r"\biron.{0,22}\brings?\b|\brings?.{0,25}\bear\b"),
    ),
    "magic-genius": (
        ("ink-stained fingers", r"\bink[- ]stained.{0,24}\bfingers\b|\bfingers.{0,24}\bink"),
    ),
    "magic-birthright": (
        ("silver crescent pendant", r"\b(?:crescent.{0,25}pendant|silver.{0,25}crescent)\b"),
    ),
    "magic-social": (
        ("gold tooth", r"\bgold.{0,14}\btooth\b"),
    ),
    "alien-fire": (
        ("luminous golden skin", r"\b(?:golden.{0,24}skin|skin.{0,24}golden|luminous.{0,25}skin)\b"),
    ),
    "alien-air": (
        ("lilac translucent skin", r"\b(?:lilac.{0,25}skin|translucent.{0,25}skin)\b"),
    ),
    "alien-earth": (
        ("quartz-veined stone", r"\b(?:quartz.{0,40}(?:veins?|stone)|crystalline.{0,25}stone)\b"),
    ),
    "alien-water": (
        ("ear fins", r"\b(?:fins?.{0,25}ears?|ears?.{0,25}fins?)\b"),
    ),
    "alien-discipline": (
        ("koala ears", r"\b(?:koala|round.{0,25}fluffy.{0,25}ears)\b"),
    ),
    "alien-genius": (
        ("elongated hairless skull", r"\b(?:elongated|hairless).{0,28}\bskull\b"),
        ("four long fingers", r"\b(?:four|4).{0,24}\bfingers\b"),
    ),
    "alien-birthright": (
        ("forehead scales", r"\b(?:scales?.{0,25}forehead|forehead.{0,25}scales?)\b"),
    ),
    "alien-social": (
        ("amber chitin", r"\b(?:amber.{0,25}chitin|chitin.{0,25}amber)\b"),
    ),
    "psychic-fire": (
        ("copper-red shag hair", r"\b(?:copper.{0,30}shag|shag.{0,30}copper)\b"),
    ),
    "psychic-air": (
        ("asymmetric haircut", r"\b(?:asymmetric|asymmetrical).{0,30}\b(?:hair|cut)\b"),
    ),
    "psychic-earth": (
        ("wavy dark hair and beard", r"\b(?:wavy.{0,28}hair|neat.{0,16}beard)\b"),
    ),
    "psychic-water": (
        ("sea-grey eyes", r"\b(?:sea[- ]gr[ae]y.{0,16}eyes?|eyes?.{0,16}sea[- ]gr[ae]y)\b"),
    ),
    "psychic-discipline": (
        ("black bob and blunt bangs", r"\b(?:black.{0,24}bob|blunt.{0,24}bangs)\b"),
    ),
    "psychic-genius": (
        ("violet-lit temples", r"\b(?:violet.{0,28}temples?|temples?.{0,28}violet)\b"),
    ),
    "psychic-birthright": (
        ("milky white irises", r"\b(?:milky.{0,25}irises|white.{0,25}irises)\b"),
    ),
    "psychic-social": (
        ("two natural hair puffs", r"\b(?:two.{0,28}puffs|hair.{0,24}puffs)\b"),
    ),
}

ASSET_IDENTITY = re.compile(
    r"(?:^|/)identities/((?:accident|mutant|tech|magic|alien|psychic)-"
    r"(?:fire|air|earth|water|discipline|genius|birthright|social))(?:/|$)"
)


def identity_for_subject(subject: dict[str, Any]) -> str | None:
    """Use structured stable asset/identity metadata, never narrative name guesses."""
    asset = subject.get("asset")
    match = ASSET_IDENTITY.search(asset) if isinstance(asset, str) else None
    if match:
        return match.group(1)
    entity = subject.get("entity")
    return entity if isinstance(entity, str) and entity in CANON_TRAITS else None


def missing_canon_traits(subject: dict[str, Any], prompt: str | None = None) -> list[str]:
    """Return missing physical features; no job status or API reads occur here."""
    signature = identity_for_subject(subject)
    if signature is None:
        return []
    if prompt is None:
        prompt = str(subject.get("prompt_prose") or subject.get("prompt_tags") or "")
    return [
        f"canon-anatomy:{signature}:{label}"
        for label, pattern in CANON_TRAITS[signature]
        if not re.search(pattern, prompt, re.IGNORECASE)
    ]
