#!/usr/bin/env python3
"""Audit the built Daily Dream catalog against today's creative and visual standards.

Conductor issue #3184 treats the Daily Dream catalog as mutable creative material: every
built bundle is re-read under the *current* contract, not the one it shipped under, and
classified by how much intervention it deserves. This script is the read-only half of
that pass. It never calls Kind Robots and never mutates a proposal; it writes an audit
manifest that `scripts/remaster_dream_catalog.py` consumes.

Each bundle is scored on signals the live contract cannot see, because the live contract
only ever looks at one unbuilt proposal against a 12-day history window:

* motif ruts, by family, weighted harder when the motif reached an asset *name*
  (`scripts/dream_creative_ruts.py`);
* premise echo against the whole catalog rather than the recent window;
* name construction — ornamental noun surnames, civil-service honorifics, repeated roots;
* visual fields, judged by the rules in CREATIVE-SEED-CONTRACT.md ("describe what is
  visible"), which most of the pre-2026-08-08 catalog predates;
* Facet fusion — a Facet whose vocabulary never surfaces in the prose was pasted on;
* art, audited independently of text: style-lane crowding, missing renders, and any
  bundle whose text is about to change out from under its image.

Classifications follow the issue's four bands: keep, light-refresh, substantial-rewrite,
retire-replace. Art carries its own verdict, because "the words are fine but the picture
is the ninth cousin of the same diffusion look" is a real and separate outcome.

Usage:
    python scripts/audit_dream_catalog.py                    # write manifest + report
    python scripts/audit_dream_catalog.py --check            # CI/advisory exit code
    python scripts/audit_dream_catalog.py --stdout-summary   # print, write nothing
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_dream_proposal as proposals  # noqa: E402
import dream_creative_ruts as ruts  # noqa: E402
from author_dream_proposal import PREMISE_STOPWORDS  # noqa: E402
from dream_art_prompts import STYLE_DIRECTIONS, style_for_world  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
REMASTER_DIR = ROOT / "projects" / "dream-cycle" / "remaster"

KEEP = "keep"
LIGHT = "light-refresh"
SUBSTANTIAL = "substantial-rewrite"
RETIRE = "retire-replace"
ORDER = (KEEP, LIGHT, SUBSTANTIAL, RETIRE)

ART_KEEP = "keep-art"
ART_RESTYLE = "restyle"
ART_REGENERATE = "regenerate"

# Score bands. Deliberately generous at the bottom: a bundle with one passing motif
# mention should not be dragged into a rewrite queue.
BANDS = ((9, RETIRE), (6, SUBSTANTIAL), (3, LIGHT), (0, KEEP))

SATURATION_SHARE = 0.30
PREMISE_ECHO_STRONG = 0.30
PREMISE_ECHO_WEAK = 0.20
THIN_VISUAL_CHARS = 60

ELEMENTS = ("vibe", "location", "character", "reward_item", "reward_skill", "scenario")

# Appearance vocabulary. A visual field with none of this is telling the renderer what
# the thing *does*, which is exactly the failure CREATIVE-SEED-CONTRACT.md documents.
CONCRETE_MARKERS = {
    "amber", "ash", "backlit", "black", "blue", "bone", "brass", "brick", "bright",
    "bronze", "brown", "canvas", "chalk", "chrome", "clay", "cloth", "copper", "cord",
    "cracked", "crimson", "crystal", "dark", "dented", "dusty", "enamel", "fabric",
    "feather", "felt", "fur", "glass", "glazed", "glow", "glowing", "gold", "golden",
    "granite", "green", "grey", "gray", "hide", "iron", "ivory", "lacquer", "lamplight",
    "leather", "lit", "luminous", "marble", "matte", "metal", "moonlight", "mud",
    "neon", "orange", "paint", "pale", "paper", "pearl", "pink", "plaster", "polished",
    "porcelain", "purple", "red", "resin", "ribbed", "rope", "rust", "rusted", "salt",
    "sand", "scarlet", "shadow", "silk", "silver", "skin", "slate", "smoke", "steel",
    "stone", "sunlight", "tarnished", "teal", "tin", "translucent", "velvet", "violet",
    "wax", "white", "wood", "wooden", "worn", "woven", "yellow",
}

# A Reward's `look` is an object or a visible effect, never a person (2026-08-08 rut).
PERSON_MARKERS = {
    "bystanders", "child", "children", "clerk", "crowd", "crowds", "faces", "figure",
    "figures", "man", "men", "onlookers", "people", "person", "player", "players",
    "spectators", "villagers", "woman", "women", "worker", "workers",
}

VISUAL_FIELDS = {
    "vibe": ("art_direction",),
    "location": ("art_direction",),
    "character": ("look",),
    "reward_item": ("look",),
    "reward_skill": ("look",),
    "scenario": (),  # the scenario prompt is built from `setup`; it has no own field
}


def _rel(path: Path) -> str:
    """Repo-relative path where possible; absolute under a temp-dir catalog."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _data_block(text: str, name: str) -> dict[str, Any] | None:
    match = re.search(rf"<!--\s*{re.escape(name)}\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else ""


def _clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _words(text: object) -> set[str]:
    return set(re.findall(r"[a-z]+", str(text or "").casefold()))


def _premise_terms(text: object) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z]{5,}", str(text or "").casefold())
        if word not in PREMISE_STOPWORDS
    }


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


@dataclass
class Bundle:
    path: Path
    day: str
    slug: str
    status: str
    proposal: dict[str, Any]
    built: dict[str, Any] | None

    @property
    def title(self) -> str:
        return _clean(self.proposal.get("title"))

    @property
    def is_built(self) -> bool:
        return self.built is not None

    def rows(self) -> dict[str, dict[str, Any]]:
        """The six authored assets, keyed by element."""
        proposal = self.proposal
        locations = proposal.get("locations") or [{}]
        characters = proposal.get("characters") or [{}]
        rewards = proposal.get("rewards") or []
        scenarios = proposal.get("scenarios") or [{}]
        by_type = {str(row.get("reward_type") or "").upper(): row for row in rewards}
        return {
            "vibe": dict(proposal.get("vibe") or {}),
            "location": dict(locations[0] if locations else {}),
            "character": dict(characters[0] if characters else {}),
            "reward_item": dict(by_type.get("ITEM") or {}),
            "reward_skill": dict(by_type.get("SKILL") or {}),
            "scenario": dict(scenarios[0] if scenarios else {}),
        }

    def record_ids(self) -> dict[str, dict[str, Any]]:
        """element -> {model, id} from the built-data ledger."""
        out: dict[str, dict[str, Any]] = {}
        records = (self.built or {}).get("records") or {}
        world = records.get("world") or {}
        if world:
            out["vibe"] = {"model": world.get("model", "Dream"), "id": world.get("id")}
        for element, key in (("location", "locations"), ("character", "characters")):
            rows = records.get(key) or []
            if rows:
                out[element] = {"model": rows[0].get("model"), "id": rows[0].get("id")}
        for row in records.get("rewards") or []:
            element = (
                "reward_item"
                if str(row.get("reward_type") or "").upper() == "ITEM"
                else "reward_skill"
            )
            out[element] = {"model": row.get("model", "Reward"), "id": row.get("id")}
        scenarios = records.get("scenarios") or []
        if scenarios:
            out["scenario"] = {
                "model": scenarios[0].get("model", "Scenario"),
                "id": scenarios[0].get("id"),
            }
        return out

    def facet_keys(self) -> dict[str, list[str]]:
        assignments = ((self.built or {}).get("facet_assignments") or {}).get("targets") or []
        out = {
            str(row.get("element")): [str(key) for key in (row.get("facet_keys") or [])]
            for row in assignments
        }
        if out:
            return out
        seeds = (self.proposal.get("seed_facets") or {}).get("elements") or {}
        for element, rows in seeds.items():
            keys: list[str] = []
            for row in rows if isinstance(rows, list) else []:
                if isinstance(row, dict):
                    keys.append(str(row.get("slug") or row.get("title") or ""))
            out[str(element)] = [key for key in keys if key]
        return out

    def names(self) -> list[str]:
        rows = self.rows()
        return [
            value
            for value in (
                self.title,
                _clean(rows["vibe"].get("title")),
                _clean(rows["location"].get("title")),
                _clean(rows["character"].get("name")),
                _clean(rows["reward_item"].get("name")),
                _clean(rows["reward_skill"].get("name")),
                _clean(rows["scenario"].get("title")),
            )
            if value
        ]

    def creative_text(self) -> str:
        return " ".join(
            _clean(value)
            for value in _flatten(self.proposal)
            if isinstance(value, str)
        )

    def premise_text(self) -> str:
        rows = self.rows()
        return " ".join(
            _clean(value)
            for value in (
                self.proposal.get("idea"),
                rows["vibe"].get("line"),
                rows["location"].get("known_for"),
                rows["location"].get("best_scene"),
                rows["character"].get("role_drive"),
                rows["scenario"].get("setup"),
            )
        )

    def facet_text(self) -> str:
        return json.dumps(self.proposal.get("seed_facets") or {}, ensure_ascii=False)


# Technical bookkeeping fields are not creative prose. The world slug in particular
# is deliberately frozen across a revision, so a remastered bundle would otherwise keep
# scoring against the motif it was just rescued from.
NON_CREATIVE_KEYS = {"seed_facets", "slug", "reward_type", "rarity"}


def _flatten(value: Any) -> Iterable[Any]:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in NON_CREATIVE_KEYS:
                continue
            yield from _flatten(item)
    elif isinstance(value, list):
        for item in value:
            yield from _flatten(item)
    else:
        yield value


def load_bundles(backlog: Path, *, include_unbuilt: bool = False) -> list[Bundle]:
    found: list[Bundle] = []
    for path in sorted(backlog.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        if _frontmatter_value(text, "proposal").casefold() not in {"true", "yes"}:
            continue
        proposal = _data_block(text, "proposal-data")
        if not proposal:
            continue
        built = _data_block(text, "built-data")
        if built is None and not include_unbuilt:
            continue
        found.append(
            Bundle(
                path=path,
                day=_frontmatter_value(text, "proposal_date")
                or _frontmatter_value(text, "created"),
                slug=_frontmatter_value(text, "slug") or path.stem,
                status=_frontmatter_value(text, "status") or "outline",
                proposal=proposal,
                built=built,
            )
        )
    return found


# ── signal extraction ────────────────────────────────────────────────────────


def visual_findings(element: str, row: dict[str, Any]) -> list[str]:
    """Contract-grade complaints about one asset's visual field."""
    findings: list[str] = []
    for field_name in VISUAL_FIELDS.get(element, ()):
        value = _clean(row.get(field_name))
        if not value:
            findings.append(f"missing `{field_name}` — the renderer has no subject to paint")
            continue
        if len(value) < THIN_VISUAL_CHARS:
            findings.append(f"`{field_name}` is thin ({len(value)} chars)")
        if not (_words(value) & CONCRETE_MARKERS):
            findings.append(
                f"`{field_name}` carries no material, colour, or light detail"
            )
        if element.startswith("reward") and (_words(value) & PERSON_MARKERS):
            examples = ", ".join(sorted(_words(value) & PERSON_MARKERS)[:3])
            findings.append(
                f"`{field_name}` describes people ({examples}); a Reward's look is an "
                "object or a visible effect"
            )
    return findings


def facet_fusion_findings(bundle: Bundle) -> list[str]:
    """Facets whose vocabulary never reaches the prose were pasted on afterwards."""
    text_words = _words(bundle.creative_text())
    findings: list[str] = []
    for element, keys in bundle.facet_keys().items():
        for key in keys:
            tokens = [token for token in re.split(r"[^a-z]+", key.casefold()) if len(token) >= 4]
            if not tokens:
                continue
            if any(
                any(word.startswith(token[:5]) for word in text_words) for token in tokens
            ):
                continue
            findings.append(f"{element}: Facet `{key}` never surfaces in the prose")
    return findings


def name_findings(bundle: Bundle, catalog: list[Bundle]) -> list[str]:
    rows = bundle.rows()
    findings: list[str] = []
    character = _clean(rows["character"].get("name"))
    surname = ruts.surname_factory_complaint(character)
    if surname:
        findings.append(f"character name: {surname}")
    honorifics = ruts.honorific_hits(bundle.names())
    if honorifics:
        findings.append(
            "civil-service honorific in an asset name (" + ", ".join(sorted(honorifics)) + ")"
        )
    # Repeated distinctive head-nouns across the catalog ("the <noun> of ...").
    own = {
        word
        for name in bundle.names()
        for word in re.findall(r"[a-z]{6,}", name.casefold())
    }
    shared: Counter[str] = Counter()
    for other in catalog:
        if other.day == bundle.day:
            continue
        other_words = {
            word
            for name in other.names()
            for word in re.findall(r"[a-z]{6,}", name.casefold())
        }
        for word in own & other_words:
            shared[word] += 1
    repeats = [word for word, count in shared.items() if count >= 2]
    if repeats:
        findings.append(
            "asset names reuse catalog-wide vocabulary ("
            + ", ".join(sorted(repeats)[:4])
            + ")"
        )
    return findings


def nearest_premise(bundle: Bundle, catalog: list[Bundle]) -> tuple[float, str]:
    own = _premise_terms(bundle.premise_text())
    best = (0.0, "")
    for other in catalog:
        if other.path == bundle.path:
            continue
        score = jaccard(own, _premise_terms(other.premise_text()))
        if score > best[0]:
            best = (score, f"{other.day} {other.title}")
    return best


def art_evidence(bundle: Bundle) -> dict[str, Any]:
    art = (bundle.built or {}).get("art") or []
    attached = [row for row in art if row.get("attached")]
    return {
        "requests": len(art),
        "attached": len(attached),
        "superseded": len((bundle.built or {}).get("superseded_art") or []),
        "revisions": len((bundle.built or {}).get("revisions") or []),
    }


def classify_score(score: int) -> str:
    for threshold, label in BANDS:
        if score >= threshold:
            return label
    return KEEP


# ── per-bundle audit ─────────────────────────────────────────────────────────


@dataclass
class BundleAudit:
    bundle: Bundle
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    assets: dict[str, dict[str, Any]] = field(default_factory=dict)
    art: dict[str, Any] = field(default_factory=dict)
    classification: str = KEEP
    legacy_shape: bool = False

    def as_dict(self) -> dict[str, Any]:
        bundle = self.bundle
        return {
            "day": bundle.day,
            "slug": bundle.slug,
            "title": bundle.title,
            "path": _rel(bundle.path),
            "status": bundle.status,
            "built": bundle.is_built,
            "classification": self.classification,
            "score": self.score,
            "legacy_shape": self.legacy_shape,
            "remaster_path": "rebuild" if self.legacy_shape else "in-place",
            "reasons": self.reasons,
            "records": bundle.record_ids(),
            "assets": self.assets,
            "art": self.art,
        }


def audit_bundle(
    bundle: Bundle,
    catalog: list[Bundle],
    *,
    lane_load: Counter[int],
    lane_cap: int,
    family_load: Counter[str],
    saturated: set[str],
) -> BundleAudit:
    audit = BundleAudit(bundle=bundle)
    rows = bundle.rows()
    facet_text = bundle.facet_text()
    score = 0

    # 1. schema, still measured against today's canonical shape
    schema_errors = proposals.validate_proposal(dict(bundle.proposal))
    if schema_errors:
        score += 2
        audit.legacy_shape = True
        audit.reasons.append(
            "pre-v2 bundle shape, so it cannot be revised in place by "
            "apply_dream_revision.py — mine it into a fresh proposal instead ("
            + "; ".join(schema_errors[:3])
            + ")"
        )

    # 2. motif ruts, name-weighted
    name_text = " ".join(bundle.names())
    body_hits = ruts.motif_hits(bundle.creative_text())
    title_hits = ruts.motif_hits(name_text)
    family_report: dict[str, dict[str, Any]] = {}
    named_families = 0
    body_families = 0
    saturation_hits = 0
    for family, hits in sorted(body_hits.items()):
        requested = ruts.facets_request(family, facet_text)
        in_name = sorted(title_hits.get(family, set()))
        family_report[family] = {
            "label": ruts.RUT_FAMILIES[family]["label"],
            "hits": sorted(hits),
            "in_names": in_name,
            "facets_requested": requested,
        }
        if family in saturated:
            saturation_hits += 1
            audit.reasons.append(
                f"{ruts.RUT_FAMILIES[family]['label']} motif is saturated across the "
                f"catalog ({family_load[family]}/{len(catalog)} bundles carry it)"
                + (" even though this day's Facets asked for it" if requested else "")
            )
        if requested:
            continue
        if in_name:
            named_families += 1
            audit.reasons.append(
                f"{ruts.RUT_FAMILIES[family]['label']} motif in asset names "
                f"({', '.join(in_name[:3])}), unrequested by the day's Facets"
            )
        else:
            body_families += 1
            audit.reasons.append(
                f"{ruts.RUT_FAMILIES[family]['label']} motif in the prose "
                f"({', '.join(sorted(hits)[:3])}), unrequested by the day's Facets"
            )
    score += min(named_families * 3, 6) + min(body_families, 4) + min(saturation_hits, 3)

    # 3. premise echo across the whole catalog, not a 12-day window
    echo_score, echo_with = nearest_premise(bundle, catalog)
    if echo_score >= PREMISE_ECHO_STRONG:
        score += 4
        audit.reasons.append(
            f"premise echoes {echo_with} (vocabulary overlap {echo_score:.2f})"
        )
    elif echo_score >= PREMISE_ECHO_WEAK:
        score += 2
        audit.reasons.append(
            f"premise leans on {echo_with} (vocabulary overlap {echo_score:.2f})"
        )

    # 4. naming
    naming = name_findings(bundle, catalog)
    if naming:
        score += min(len(naming), 3)
        audit.reasons.extend(naming)

    # 5. Facet fusion
    fusion = facet_fusion_findings(bundle)
    if fusion:
        score += min(len(fusion) // 2, 2)
        if len(fusion) >= 2:
            audit.reasons.append(
                f"{len(fusion)} assigned Facet(s) never reach the prose — "
                + "; ".join(fusion[:2])
            )

    # 6. visual fields, per asset
    visual_total = 0
    for element in ELEMENTS:
        row = rows.get(element) or {}
        findings = visual_findings(element, row)
        visual_total += len(findings)
        element_reasons = list(findings)
        element_families = [
            family
            for family, hits in ruts.motif_hits(" ".join(str(v) for v in row.values())).items()
            if not ruts.facets_request(family, facet_text)
        ]
        if element_families:
            element_reasons.append(
                "carries the "
                + ", ".join(ruts.RUT_FAMILIES[f]["label"] for f in element_families)
                + " motif"
            )
        audit.assets[element] = {
            "name": _clean(row.get("name") or row.get("title")),
            "record": bundle.record_ids().get(element),
            "findings": element_reasons,
            "visual_findings": findings,
        }
    score += min(visual_total, 3)
    if visual_total:
        audit.reasons.append(f"{visual_total} weak or missing visual field(s)")

    audit.score = score
    audit.classification = classify_score(score)

    # 7. art, audited independently of the text verdict
    lane = STYLE_DIRECTIONS.index(style_for_world(bundle.title))
    evidence = art_evidence(bundle)
    art_reasons: list[str] = []
    verdict = ART_KEEP
    if audit.classification in (SUBSTANTIAL, RETIRE):
        verdict = ART_REGENERATE
        art_reasons.append("text identity changes under this pass; the render no longer matches")
    if visual_total:
        verdict = ART_REGENERATE
        art_reasons.append("renders were built from weak visual fields")
    if bundle.is_built and evidence["requests"] and evidence["attached"] < evidence["requests"]:
        verdict = ART_REGENERATE
        art_reasons.append(
            f"only {evidence['attached']}/{evidence['requests']} renders ever attached"
        )
    if lane_load[lane] > lane_cap:
        art_reasons.append(
            f"style lane {lane} is carrying {lane_load[lane]} worlds (cap {lane_cap}); "
            "this world should move to an unused visual language"
        )
        if verdict == ART_KEEP:
            verdict = ART_RESTYLE
    audit.art = {
        "verdict": verdict,
        "reasons": art_reasons,
        "style_lane": lane,
        "lane_load": lane_load[lane],
        "evidence": evidence,
    }
    audit.family_report = family_report  # type: ignore[attr-defined]
    return audit


def catalog_family_load(bundles: list[Bundle]) -> Counter[str]:
    """How many bundles carry each motif family, requested or not."""
    load: Counter[str] = Counter()
    for bundle in bundles:
        for family in ruts.motif_hits(bundle.creative_text()):
            load[family] += 1
    return load


def audit_catalog(bundles: list[Bundle]) -> list[BundleAudit]:
    lane_load: Counter[int] = Counter(
        STYLE_DIRECTIONS.index(style_for_world(bundle.title)) for bundle in bundles
    )
    lane_cap = max(1, -(-len(bundles) // len(STYLE_DIRECTIONS)))
    family_load = catalog_family_load(bundles)
    # A motif carried by a third of the catalog is a groove even where an individual
    # day's Facets legitimately asked for it. That is the "renamed versions of the
    # same premise" failure the remaster exists to break.
    threshold = max(3, round(SATURATION_SHARE * len(bundles)))
    saturated = {family for family, count in family_load.items() if count >= threshold}
    return [
        audit_bundle(
            bundle,
            bundles,
            lane_load=lane_load,
            lane_cap=lane_cap,
            family_load=family_load,
            saturated=saturated,
        )
        for bundle in bundles
    ]


def stale_unbuilt(backlog: Path, *, window_days: int) -> list[dict[str, Any]]:
    """Unbuilt proposals the automatic builder must never build as written."""
    today = datetime.date.today()
    poisoned: list[dict[str, Any]] = []
    for bundle in load_bundles(backlog, include_unbuilt=True):
        if bundle.is_built or bundle.status in {"parked", "vetoed", "built"}:
            continue
        try:
            age = (today - datetime.date.fromisoformat(bundle.day)).days
        except ValueError:
            continue
        if age > window_days:
            poisoned.append(
                {
                    "day": bundle.day,
                    "slug": bundle.slug,
                    "title": bundle.title,
                    "path": _rel(bundle.path),
                    "age_days": age,
                    "disposition": "mine for ideas only; never build as written",
                }
            )
    return poisoned


# ── reporting ────────────────────────────────────────────────────────────────


def build_manifest(audits: list[BundleAudit], *, window_days: int, backlog: Path) -> dict[str, Any]:
    counts = Counter(audit.classification for audit in audits)
    art_counts = Counter(audit.art["verdict"] for audit in audits)
    families: Counter[str] = Counter()
    for audit in audits:
        for family, report in getattr(audit, "family_report", {}).items():
            if not report["facets_requested"]:
                families[family] += 1
    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generator": "scripts/audit_dream_catalog.py",
        "issue": "https://github.com/silasfelinus/conductor/issues/3184",
        "catalog": {
            "backlog": _rel(backlog),
            "bundles": len(audits),
            "assets": len(audits) * len(ELEMENTS),
        },
        "thresholds": {
            "bands": {label: threshold for threshold, label in BANDS},
            "saturation_share": SATURATION_SHARE,
            "premise_echo_strong": PREMISE_ECHO_STRONG,
            "premise_echo_weak": PREMISE_ECHO_WEAK,
            "thin_visual_chars": THIN_VISUAL_CHARS,
        },
        "summary": {
            "classification": {label: counts.get(label, 0) for label in ORDER},
            "art": {
                label: art_counts.get(label, 0)
                for label in (ART_KEEP, ART_RESTYLE, ART_REGENERATE)
            },
            "rut_families": dict(families.most_common()),
        },
        "poisoned_unbuilt": stale_unbuilt(backlog, window_days=window_days),
        "bundles": [audit.as_dict() for audit in audits],
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    summary = manifest["summary"]
    lines = [
        "# Daily Dream catalog remaster audit",
        "",
        f"Generated {manifest['generated_at']} by `{manifest['generator']}` "
        f"for [issue #3184]({manifest['issue']}).",
        "",
        f"**{manifest['catalog']['bundles']} built bundles** "
        f"({manifest['catalog']['assets']} assets) audited under the current creative contract.",
        "",
        "| Verdict | Bundles |",
        "| --- | --- |",
    ]
    for label in ORDER:
        lines.append(f"| {label} | {summary['classification'][label]} |")
    lines += ["", "| Art verdict | Bundles |", "| --- | --- |"]
    for label in (ART_KEEP, ART_RESTYLE, ART_REGENERATE):
        lines.append(f"| {label} | {summary['art'][label]} |")
    if summary["rut_families"]:
        lines += ["", "| Unrequested motif family | Bundles |", "| --- | --- |"]
        for family, count in summary["rut_families"].items():
            lines.append(f"| {ruts.RUT_FAMILIES[family]['label']} | {count} |")

    lines += [
        "",
        "## Worklist",
        "",
        "| Day | Bundle | Score | Verdict | Art | Leading reason |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in sorted(manifest["bundles"], key=lambda item: (-item["score"], item["day"])):
        reason = (row["reasons"] or ["—"])[0]
        lines.append(
            f"| {row['day']} | {row['title']} | {row['score']} | {row['classification']} "
            f"| {row['art']['verdict']} | {reason} |"
        )

    poisoned = manifest["poisoned_unbuilt"]
    lines += ["", "## Poisoned unbuilt proposals", ""]
    if poisoned:
        lines.append("| Day | Proposal | Age (days) | Disposition |")
        lines.append("| --- | --- | ---: | --- |")
        for row in poisoned:
            lines.append(
                f"| {row['day']} | {row['title']} | {row['age_days']} | {row['disposition']} |"
            )
    else:
        lines.append("None — every unbuilt proposal is inside the freshness window.")

    lines += ["", "## Per-bundle detail", ""]
    for row in sorted(manifest["bundles"], key=lambda item: item["day"]):
        lines.append(f"### {row['day']} — {row['title']} (`{row['slug']}`)")
        lines.append("")
        lines.append(
            f"- **Verdict:** {row['classification']} (score {row['score']}) · "
            f"**art:** {row['art']['verdict']} (lane {row['art']['style_lane']}, "
            f"{row['art']['lane_load']} worlds on it)"
        )
        for reason in row["reasons"]:
            lines.append(f"- {reason}")
        for reason in row["art"]["reasons"]:
            lines.append(f"- art: {reason}")
        for element, asset in row["assets"].items():
            if asset["findings"]:
                lines.append(f"- `{element}` ({asset['name']}): " + "; ".join(asset["findings"]))
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog", default=str(BACKLOG))
    parser.add_argument("--out-dir", default=str(REMASTER_DIR))
    parser.add_argument(
        "--window-days",
        type=int,
        default=2,
        help="freshness window for unbuilt proposals (matches run_daily_dream_build)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when any bundle needs a substantial rewrite or retirement",
    )
    parser.add_argument(
        "--stdout-summary",
        action="store_true",
        help="print the summary and write no files",
    )
    args = parser.parse_args(argv)

    backlog = Path(args.backlog)
    bundles = load_bundles(backlog)
    if not bundles:
        print(f"No built Daily Dream bundles found in {backlog}", file=sys.stderr)
        return 1
    audits = audit_catalog(bundles)
    manifest = build_manifest(audits, window_days=args.window_days, backlog=backlog)
    summary = manifest["summary"]

    if not args.stdout_summary:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = out_dir / "catalog-audit.json"
        report_path = out_dir / "CATALOG-AUDIT.md"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
            encoding="utf-8",
        )
        report_path.write_text(render_markdown(manifest), encoding="utf-8")
        print(f"wrote {manifest_path.relative_to(ROOT)}")
        print(f"wrote {report_path.relative_to(ROOT)}")

    print(
        "Daily Dream catalog audit: "
        + ", ".join(f"{label}={summary['classification'][label]}" for label in ORDER)
        + " | art: "
        + ", ".join(
            f"{label}={summary['art'][label]}"
            for label in (ART_KEEP, ART_RESTYLE, ART_REGENERATE)
        )
        + f" | poisoned unbuilt: {len(manifest['poisoned_unbuilt'])}"
    )
    if args.check:
        needs_work = summary["classification"][SUBSTANTIAL] + summary["classification"][RETIRE]
        return 1 if needs_work else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
