#!/usr/bin/env python3
"""Build the Daily Dream digest with two deliberately different output sections.

The older completed bundle is art-rich because its six renders have had a full cycle
to finish. The bundle built this morning is text/facet-forward and never reserves
blank image rectangles for art that was only just submitted. Today's freshly authored
proposal is steering input for tomorrow and is not shown as a third near-duplicate.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

import build_digest_email as legacy

TYPE_THEME = {
    "vibe": ("#7e22ce", "#faf5ff", "🌙"),
    "location": ("#1d4ed8", "#eff6ff", "📍"),
    "character": ("#be185d", "#fdf2f8", "👤"),
    "reward_item": ("#b45309", "#fffbeb", "🎁"),
    "reward_skill": ("#047857", "#ecfdf5", "✨"),
    "scenario": ("#0f766e", "#f0fdfa", "🎭"),
}


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _facet_chips(values: list[str]) -> str:
    return "".join(
        f'<span style="display:inline-block;border:1px solid #d8d8e5;background:#fff;'
        f'border-radius:999px;padding:4px 8px;margin:3px 3px 0 0;font-size:10px;'
        f'line-height:1.25;color:#3f3f55">{esc(value)}</span>'
        for value in values
    )


def asset_card(asset: dict[str, Any], *, show_art: bool) -> str:
    key = str(asset.get("key") or "vibe")
    accent, paper, icon = TYPE_THEME.get(key, TYPE_THEME["vibe"])
    title = esc(asset.get("title"))
    label = esc(asset.get("label"))
    summary = esc(asset.get("summary"))
    image_url = str(asset.get("image_url") or "")
    status = str(asset.get("art_status") or "not queued")

    visual = ""
    if show_art:
        if image_url:
            visual = (
                f'<img src="{esc(image_url)}" alt="{title}" width="300" height="190" '
                f'style="display:block;width:100%;height:190px;object-fit:cover;border-radius:9px;'
                f'border:1px solid {accent}44;margin:0 0 10px">'
            )
        else:
            visual = (
                f'<div style="height:188px;border-radius:9px;border:1px dashed {accent};'
                f'background:#ffffffaa;display:table;width:100%;margin-bottom:10px">'
                f'<div style="display:table-cell;vertical-align:middle;text-align:center;color:{accent};'
                f'font-size:13px;padding:12px">🖼️ Art {esc(status)}</div></div>'
            )

    facets = asset.get("facets") if isinstance(asset.get("facets"), list) else []
    request = ""
    if show_art and asset.get("request_id"):
        job_id = asset.get("art_job_id")
        queue_text = f"ArtJob {job_id}" if job_id else str(asset.get("request_id"))
        request = f'<div style="font-size:9px;color:#777;margin-top:7px">Queue: {esc(queue_text)}</div>'

    min_height = "410px" if show_art else "220px"
    no_facets_html = '<span style="font-size:11px;color:#777">Legacy proposal, no structured Facets recorded.</span>'
    facet_chips_html = _facet_chips([str(value) for value in facets]) or no_facets_html
    return (
        f'<div style="width:300px;min-height:{min_height};border:1px solid {accent};border-radius:12px;'
        f'background:{paper};padding:12px;font-family:Arial,sans-serif;box-sizing:border-box">'
        f'{visual}'
        f'<div style="font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:{accent};font-weight:700">'
        f'{icon} {label}</div>'
        f'<div style="font-family:Georgia,serif;font-size:19px;line-height:1.15;color:#242033;'
        f'font-weight:700;margin:5px 0 7px">{title}</div>'
        f'<div style="font-size:13px;line-height:1.45;color:#454052">{summary}</div>'
        f'<div style="border-top:1px dashed {accent}66;margin-top:10px;padding-top:7px">'
        f'<div style="font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:{accent};font-weight:700">Seed Facets</div>'
        f'{facet_chips_html}'
        f'{request}</div></div>'
    )


def asset_grid(assets: list[dict[str, Any]], *, show_art: bool) -> str:
    rows: list[str] = []
    for index in range(0, len(assets), 2):
        pair = assets[index:index + 2]
        cells = "".join(
            f'<td width="50%" valign="top" style="padding:6px">{asset_card(asset, show_art=show_art)}</td>'
            for asset in pair
        )
        if len(pair) == 1:
            cells += '<td width="50%" style="padding:6px"></td>'
        rows.append(f"<tr>{cells}</tr>")
    return (
        '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" '
        'style="max-width:660px">' + "".join(rows) + "</table>"
    )


def proposal_section(
    _heading: str,
    proposal: dict[str, Any] | None,
    cta: bool = False,
    images: list[dict[str, Any]] | None = None,
    page_link: str = "",
) -> str:
    del cta, images
    if not proposal:
        return ""

    mode = str(proposal.get("display_mode") or "art-rich")
    show_art = mode == "art-rich"
    heading = "🖼️ Previous completed output" if show_art else "✨ Just built this cycle"
    title = esc(proposal.get("title"))
    idea = esc(proposal.get("idea"))
    assets = proposal.get("assets") if isinstance(proposal.get("assets"), list) else []

    target_page = proposal.get("page") or page_link
    buttons = ""
    if target_page:
        buttons = f'<p>{legacy._button(target_page, "🌙 View the Daily Dream page", color="#1d4ed8")}</p>'

    calendar_label = str(proposal.get("calendar_label") or "")
    calendar_line = (
        f'<p style="color:#475569;font-size:12px;margin:3px 0 8px">{esc(calendar_label)}</p>'
        if calendar_label else ""
    )

    assignment = proposal.get("facet_assignments")
    facet_line = ""
    if isinstance(assignment, dict):
        facet_line = (
            f'<p style="color:#166534;background:#f0fdf4;border-left:4px solid #16a34a;'
            f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px">'
            f'🧩 Record Facets: {esc(assignment.get("status", "unknown"))}</p>'
        )

    if show_art:
        ready = sum(asset.get("art_status") == "ready" for asset in assets)
        art_line = (
            f'<p style="color:#334155;background:#f8fafc;border-left:4px solid #64748b;'
            f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px">'
            f'🖼️ {ready}/{len(assets)} asset images ready; this is the art-bearing output from the prior cycle.</p>'
        ) if assets else ""
    else:
        submitted = sum(bool(asset.get("art_job_id")) for asset in assets)
        art_line = (
            f'<p style="color:#334155;background:#f8fafc;border-left:4px solid #64748b;'
            f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px">'
            f'🎨 {submitted}/{len(assets)} ArtJobs submitted. No image space is reserved here; '
            f'these renders belong in the next cycle’s art-rich section.</p>'
        ) if assets else ""

    return (
        f'<h2 style="margin-bottom:2px">{heading}</h2>'
        f'<p style="font-size:1.15em;color:#2e1065;margin:2px 0"><strong>{title}</strong></p>'
        f'<p style="color:#444;line-height:1.5;margin-top:4px;max-width:660px">{idea}</p>'
        f'{calendar_line}{art_line}{facet_line}{buttons}'
        f'{asset_grid(assets, show_art=show_art)}'
    )


def build_payload(digest: dict[str, Any]) -> dict[str, Any]:
    # Reuse the legacy project/activity shell, but feed its two Daily Dream slots
    # the new roles in the order Silas expects: older art-rich output first, then
    # the bundle just built this cycle. proposal_section ignores the legacy labels
    # and renders from display_mode instead.
    legacy.proposal_section = proposal_section
    legacy_digest = dict(digest)
    legacy_digest["tomorrow_proposal"] = digest.get("previous_dream_output")
    legacy_digest["yesterday_output"] = digest.get("current_dream_output")
    payload = legacy.build_payload(legacy_digest)

    # Old history is intentionally suppressed. The digest is a two-beat handoff,
    # not an archive dump.
    status = str(digest.get("daily_dream_output_status") or "")
    if status and not digest.get("previous_dream_output"):
        marker = '<h2 style="margin-bottom:2px">✨ Just built this cycle</h2>'
        note = (
            f'<p style="color:#92400e;background:#fffbeb;padding:8px 12px;'
            f'border-left:4px solid #f59e0b">{esc(status)}</p>'
        )
        if marker in payload["htmlContent"]:
            payload["htmlContent"] = payload["htmlContent"].replace(marker, note + marker, 1)
    return payload


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    input_path = Path(args[0] if args else "digest.json")
    output_path = Path(args[1] if len(args) > 1 else "digest-email.json")
    digest = json.loads(input_path.read_text(encoding="utf-8"))
    output_path.write_text(
        json.dumps(build_payload(digest), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Built {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
