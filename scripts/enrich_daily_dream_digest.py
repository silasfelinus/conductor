#!/usr/bin/env python3
"""Replace the legacy digest's fuzzy daily-dream selection with calendar truth.

The legacy collector labels the newest built proposal "yesterday" forever. This
post-processor keeps every unrelated digest field, but selects proposals by Pacific
calendar date, creates one readable asset row per six-part bundle element, and probes
known public image paths so freshly generated art can appear even before a later
metadata attachment pass flips ``attached`` to true.
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
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "conductor-digest/2"})
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
        ("location", "Dream location", location.get("title"), location.get("known_for"), slugify(location.get("title") or "")),
        ("character", "Character", character.get("name"), character.get("role_drive"), slugify(character.get("name") or "")),
        ("reward_item", "Reward item", item.get("name"), item.get("grants"), slugify(item.get("name") or "")),
        ("reward_skill", "Reward skill", skill.get("name"), skill.get("grants"), slugify(skill.get("name") or "")),
        ("scenario", "Scenario", scenario.get("title"), scenario.get("setup"), slugify(scenario.get("title") or "")),
    ]
    rows: list[dict[str, Any]] = []
    for key, label, title, summary, element_slug in specs:
        if not title:
            continue
        art = art_by_element.get(str(element_slug)) or {}
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
            "art_status": "ready" if available else ("queued" if art else "not queued"),
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
        payload["page"] = built.get("page") or "https://kind-robots.vercel.app/daily-dream"
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

    current = by_date.get(today_key)
    output["tomorrow_proposal"] = proposal_payload(current, probe_images=probe_images) if current else None

    exact_yesterday = by_date.get(yesterday_key)
    if exact_yesterday and exact_yesterday.get("built"):
        output["yesterday_output"] = proposal_payload(exact_yesterday, probe_images=probe_images)
        output["yesterday_output"]["calendar_label"] = f"Created from the {yesterday_key} proposal"
        output["daily_dream_output_status"] = "ready"
    else:
        output["yesterday_output"] = None
        reason = "proposal missing" if not exact_yesterday else "proposal exists but has not built"
        output["daily_dream_output_status"] = f"No {yesterday_key} output: {reason}."

    recent: list[dict[str, Any]] = []
    wanted_dates = {today, today - timedelta(days=1)}
    for proposal in proposals:
        if proposal.get("built") and (_built_date(proposal) in wanted_dates or proposal["proposal_date"] in {today_key, yesterday_key}):
            recent.append(proposal_payload(proposal, probe_images=probe_images))
    recent.sort(key=lambda row: (str(row.get("built_at") or ""), str(row.get("proposal_date") or "")), reverse=True)
    output["recent_dream_outputs"] = recent
    output["daily_dream_calendar"] = {"today": today_key, "yesterday": yesterday_key, "timezone": "America/Los_Angeles"}
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Legacy digest JSON")
    parser.add_argument("--output", help="Output path; stdout when omitted")
    parser.add_argument("--date", help="Pacific calendar date override (YYYY-MM-DD)")
    parser.add_argument("--no-probe", action="store_true", help="Do not HEAD-check queued image paths")
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
