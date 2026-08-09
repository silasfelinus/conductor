#!/usr/bin/env python3
"""Replace the legacy digest's fuzzy daily-dream selection with creation truth.

The morning cycle has three different generations in flight and they must not be
presented as interchangeable:

* today's freshly authored proposal is the steering input for the NEXT build;
* the most recently completed bundle is what was JUST built this cycle and should
  be shown compactly without reserving empty image boxes;
* the completed bundle before that is the art-rich output, because its renders have
  had a full cycle to finish.

This post-processor keeps unrelated digest fields untouched, derives those three
roles from proposal/built-data timestamps, and probes public art only for the older
art-rich output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
PACIFIC = ZoneInfo("America/Los_Angeles")
PUBLIC_BASE = "https://kind-robots.vercel.app"
PROPOSAL_RE = re.compile(r"<!-- proposal-data\s*\n(.*?)\n-->", re.DOTALL)
BUILT_RE = re.compile(r"<!-- built-data\s*\n(.*?)\n-->", re.DOTALL)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


def builder_slugify(value: str) -> str:
    """Mirror build_dream_records.slugify so digest joins survive article cleanup."""
    slug = slugify(value)
    for article in ("the-", "a-", "an-"):
        if slug.startswith(article):
            rest = slug[len(article):]
            if rest and "-" in rest:
                slug = rest
            break
    return slug


def _frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    loaded = yaml.safe_load(text[4:end])
    return loaded if isinstance(loaded, dict) else {}


def _comment(pattern: re.Pattern[str], text: str) -> dict[str, Any] | None:
    match = pattern.search(text)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def collect_proposals(backlog: Path = BACKLOG) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for path in sorted(backlog.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = _frontmatter(text)
        data = _comment(PROPOSAL_RE, text)
        if not data or not meta.get("proposal"):
            continue
        built = _comment(BUILT_RE, text)
        proposals.append({
            "path": path,
            "meta": meta,
            "data": data,
            "built": built,
            "proposal_date": str(meta.get("proposal_date") or meta.get("created") or ""),
        })
    return proposals


def _public_url(public_path: str) -> str:
    if public_path.startswith("http://") or public_path.startswith("https://"):
        return public_path
    return f"{PUBLIC_BASE}/{public_path.lstrip('/')}"


def _url_exists(url: str, timeout: int = 5) -> bool:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "conductor-digest/3"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400
    except (OSError, urllib.error.HTTPError, urllib.error.URLError):
        return False


def _facet_label(facet: dict[str, Any]) -> str:
    title = str(facet.get("title") or facet.get("slug") or "Unknown Facet")
    taxonomy = str(facet.get("taxonomy") or "FACET")
    return f"{taxonomy}: {title}"


def _asset_rows(proposal: dict[str, Any], *, probe_images: bool = True) -> list[dict[str, Any]]:
    data = proposal["data"]
    built = proposal.get("built") or {}
    seed = data.get("seed_facets") if isinstance(data.get("seed_facets"), dict) else {}
    elements = seed.get("elements") if isinstance(seed.get("elements"), dict) else {}
    art_entries = built.get("art") if isinstance(built.get("art"), list) else []
    art_by_element = {
        str(item.get("element") or ""): item
        for item in art_entries if isinstance(item, dict) and item.get("element")
    }

    def art_for(key: str, title: str, element_slug: str) -> dict[str, Any]:
        candidates = [element_slug, builder_slugify(title), slugify(title)]
        if key == "scenario":
            candidates = [f"{candidate}-scenario" for candidate in candidates] + candidates
        for candidate in candidates:
            if candidate and candidate in art_by_element:
                return art_by_element[candidate]
        return {}

    locations = data.get("locations") if isinstance(data.get("locations"), list) else []
    characters = data.get("characters") if isinstance(data.get("characters"), list) else []
    rewards = data.get("rewards") if isinstance(data.get("rewards"), list) else []
    scenarios = data.get("scenarios") if isinstance(data.get("scenarios"), list) else []
    item = next((row for row in rewards if str(row.get("reward_type") or "").upper() == "ITEM"), {})
    skill = next((row for row in rewards if str(row.get("reward_type") or "").upper() == "SKILL"), {})
    vibe = data.get("vibe") if isinstance(data.get("vibe"), dict) else {}
    location = locations[0] if locations else {}
    character = characters[0] if characters else {}
    scenario = scenarios[0] if scenarios else {}

    specs = [
        ("vibe", "Dream vibe", vibe.get("title") or data.get("title"), vibe.get("line") or data.get("idea"), data.get("slug")),
        ("location", "Dream location", location.get("title"), location.get("known_for"), builder_slugify(location.get("title") or "")),
        ("character", "Character", character.get("name"), character.get("role_drive"), builder_slugify(character.get("name") or "")),
        ("reward_item", "Reward item", item.get("name"), item.get("grants"), builder_slugify(item.get("name") or "")),
        ("reward_skill", "Reward skill", skill.get("name"), skill.get("grants"), builder_slugify(skill.get("name") or "")),
        ("scenario", "Scenario", scenario.get("title"), scenario.get("setup"), builder_slugify(scenario.get("title") or "")),
    ]
    rows: list[dict[str, Any]] = []
    for key, label, title, summary, element_slug in specs:
        if not title:
            continue
        art = art_for(key, str(title or ""), str(element_slug))
        public_path = str(art.get("public_path") or "")
        image_url = _public_url(public_path) if public_path else ""
        available = bool(art.get("attached"))
        if image_url and not available and probe_images:
            available = _url_exists(image_url)
        facets = elements.get(key) if isinstance(elements.get(key), list) else []
        rows.append({
            "key": key,
            "label": label,
            "title": str(title),
            "summary": str(summary or ""),
            "facets": [_facet_label(facet) for facet in facets if isinstance(facet, dict)],
            "facet_objects": facets,
            "image_url": image_url if available else "",
            "image_path": public_path,
            "art_status": "ready" if available else ("queued" if art else ("awaiting build" if not built else "queue metadata missing")),
            "request_id": art.get("request_id"),
        })
    return rows


def _records_summary(built: dict[str, Any] | None) -> dict[str, int]:
    if not built:
        return {}
    records = built.get("records") if isinstance(built.get("records"), dict) else {}
    return {
        "dreams": sum(bool(records.get(key)) for key in ("world", "vibe")) + len(records.get("locations") or []),
        "characters": len(records.get("characters") or []),
        "rewards": len(records.get("rewards") or []),
        "scenarios": len(records.get("scenarios") or []),
    }


def proposal_payload(proposal: dict[str, Any], *, probe_images: bool = True) -> dict[str, Any]:
    data = proposal["data"]
    built = proposal.get("built")
    assets = _asset_rows(proposal, probe_images=probe_images)
    images = [
        {"url": asset["image_url"], "name": asset["title"], "asset": asset["key"]}
        for asset in assets if asset.get("image_url")
    ]
    try:
        repo_path = proposal["path"].relative_to(ROOT).as_posix()
    except ValueError:
        repo_path = proposal["path"].name
    payload = {
        "title": data.get("title"),
        "slug": data.get("slug"),
        "idea": data.get("idea"),
        "data": data,
        "proposal_date": proposal["proposal_date"],
        "edit_link": f"https://github.com/silasfelinus/conductor/blob/main/{repo_path}",
        "assets": assets,
        "images": images,
        "seed_facets": data.get("seed_facets"),
        "built": bool(built),
        "records_summary": _records_summary(built),
    }
    if built:
        payload["built_at"] = built.get("built_at")
        payload["page"] = built.get("page") or PUBLIC_BASE
        payload["facet_assignments"] = built.get("facet_assignments")
    return payload


def _built_date(proposal: dict[str, Any]) -> date | None:
    built = proposal.get("built")
    raw = built.get("built_at") if isinstance(built, dict) else None
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=PACIFIC)
        return parsed.astimezone(PACIFIC).date()
    except ValueError:
        return None


def _completed_sort_key(proposal: dict[str, Any]) -> tuple[str, str]:
    return (
        str((proposal.get("built") or {}).get("built_at") or ""),
        str(proposal.get("proposal_date") or ""),
    )


def _completed_payload(
    proposal: dict[str, Any], *, display_mode: str, probe_images: bool
) -> dict[str, Any]:
    payload = proposal_payload(proposal, probe_images=probe_images)
    built_on = _built_date(proposal)
    built_label = built_on.isoformat() if built_on else "an unknown date"
    payload["display_mode"] = display_mode
    if display_mode == "art-rich":
        payload["calendar_label"] = (
            f"Previous completed bundle; built {built_label} "
            f"from the {proposal['proposal_date']} proposal"
        )
    else:
        payload["calendar_label"] = (
            f"Just built {built_label} from the {proposal['proposal_date']} proposal. "
            "Its art belongs to the next digest cycle."
        )
    return payload


def enrich_digest(
    digest: dict[str, Any],
    proposals: list[dict[str, Any]],
    *,
    today: date,
    probe_images: bool = True,
) -> dict[str, Any]:
    output = dict(digest)
    by_date = {proposal["proposal_date"]: proposal for proposal in proposals}
    today_key = today.isoformat()
    yesterday_key = (today - timedelta(days=1)).isoformat()

    # Today's freshly authored proposal is steering input for the NEXT build. Keep
    # it in the JSON for diagnostics, but it is deliberately not a showcase section
    # in the email. Empty art boxes for an unbuilt proposal taught the wrong story.
    next_proposal = by_date.get(today_key)
    output["next_dream_proposal"] = (
        proposal_payload(next_proposal, probe_images=False) if next_proposal else None
    )

    completed = [proposal for proposal in proposals if proposal.get("built")]
    completed.sort(key=_completed_sort_key)

    current = completed[-1] if completed else None
    previous = completed[-2] if len(completed) >= 2 else None

    # The newest completed bundle was just built this cycle. Do not spend network
    # probes or reserve visual space for its art: the six ArtJobs were only just
    # submitted. The older completed bundle is the art-rich section and gets the
    # public-path probes because its renders have had a full cycle to settle.
    output["current_dream_output"] = (
        _completed_payload(current, display_mode="just-built", probe_images=False)
        if current else None
    )
    output["previous_dream_output"] = (
        _completed_payload(previous, display_mode="art-rich", probe_images=probe_images)
        if previous else None
    )

    # Remove the old two-state aliases. They conflated an unbuilt proposal with a
    # built output and made the email look perpetually one day behind.
    output.pop("tomorrow_proposal", None)
    output.pop("yesterday_output", None)

    if previous:
        output["daily_dream_output_status"] = "ready"
    elif current:
        output["daily_dream_output_status"] = (
            "The first current bundle exists, but there is no earlier completed bundle for the art-rich section yet."
        )
    else:
        output["daily_dream_output_status"] = "No completed Daily Dream bundle exists yet."

    output["recent_dream_outputs"] = []
    output["daily_dream_calendar"] = {
        "today": today_key,
        "yesterday": yesterday_key,
        "timezone": "America/Los_Angeles",
    }
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Legacy digest JSON")
    parser.add_argument("--output", help="Output path; stdout when omitted")
    parser.add_argument("--date", help="Pacific calendar date override (YYYY-MM-DD)")
    parser.add_argument("--no-probe", action="store_true", help="Do not HEAD-check prior output image paths")
    args = parser.parse_args(argv)
    digest = json.loads(Path(args.input).read_text(encoding="utf-8"))
    current_date = date.fromisoformat(args.date) if args.date else datetime.now(PACIFIC).date()
    enriched = enrich_digest(digest, collect_proposals(), today=current_date, probe_images=not args.no_probe)
    rendered = json.dumps(enriched, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
