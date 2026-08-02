#!/usr/bin/env python3
"""Build the daily digest email with full six-asset dream cards.

This wraps the established digest email so project/activity sections remain untouched,
while replacing the tiny image strip with readable, per-asset cards. Every asset is
shown: generated art appears large, and unfinished art gets an explicit queue state.
Seed Facets are printed on the same card that they shaped.
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


def asset_card(asset: dict[str, Any]) -> str:
    key = str(asset.get("key") or "vibe")
    accent, paper, icon = TYPE_THEME.get(key, TYPE_THEME["vibe"])
    title = esc(asset.get("title"))
    label = esc(asset.get("label"))
    summary = esc(asset.get("summary"))
    image_url = str(asset.get("image_url") or "")
    status = str(asset.get("art_status") or "not queued")
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
    request = (
        f'<div style="font-size:9px;color:#777;margin-top:7px">Queue: {esc(asset.get("request_id"))}</div>'
        if asset.get("request_id") else ""
    )
    return (
        f'<div style="width:300px;min-height:410px;border:1px solid {accent};border-radius:12px;'
        f'background:{paper};padding:12px;font-family:Arial,sans-serif;box-sizing:border-box">'
        f'{visual}'
        f'<div style="font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:{accent};font-weight:700">'
        f'{icon} {label}</div>'
        f'<div style="font-family:Georgia,serif;font-size:19px;line-height:1.15;color:#242033;'
        f'font-weight:700;margin:5px 0 7px">{title}</div>'
        f'<div style="font-size:13px;line-height:1.45;color:#454052">{summary}</div>'
        f'<div style="border-top:1px dashed {accent}66;margin-top:10px;padding-top:7px">'
        f'<div style="font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:{accent};font-weight:700">Seed Facets</div>'
        f'{_facet_chips([str(value) for value in facets]) or "<span style=\"font-size:11px;color:#777\">Legacy proposal, no structured Facets recorded.</span>"}'
        f'{request}</div></div>'
    )


def asset_grid(assets: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for index in range(0, len(assets), 2):
        pair = assets[index:index + 2]
        cells = "".join(
            f'<td width="50%" valign="top" style="padding:6px">{asset_card(asset)}</td>'
            for asset in pair
        )
        if len(pair) == 1:
            cells += '<td width="50%" style="padding:6px"></td>'
        rows.append(f"<tr>{cells}</tr>")
    return '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:660px">' + "".join(rows) + "</table>"


def proposal_section(heading: str, proposal: dict[str, Any] | None, cta: bool = False,
                     images: list[dict[str, Any]] | None = None, page_link: str = "") -> str:
    del images
    if not proposal:
        wording = "No completed built output is available yet." if "Previous" in heading else "No proposal is available yet."
        return f'<h2 style="margin-bottom:2px">{esc(heading)}</h2><p style="color:#777"><i>{wording}</i></p>'
    title = esc(proposal.get("title"))
    idea = esc(proposal.get("idea"))
    assets = proposal.get("assets") if isinstance(proposal.get("assets"), list) else []
    buttons = ""
    if cta and proposal.get("edit_link"):
        buttons += legacy._button(proposal["edit_link"], "💬 Comment / edit the bundle")
    target_page = page_link or proposal.get("page")
    if target_page:
        buttons += legacy._button(target_page, "🌙 View the Daily Dream page", color="#1d4ed8")
    buttons = f"<p>{buttons}</p>" if buttons else ""
    calendar_label = str(proposal.get("calendar_label") or "")
    calendar_line = (
        f'<p style="color:#475569;font-size:12px;margin:3px 0 8px">{esc(calendar_label)}</p>'
        if calendar_label else ""
    )
    ready = sum(asset.get("art_status") == "ready" for asset in assets)
    art_line = (
        f'<p style="color:#334155;background:#f8fafc;border-left:4px solid #64748b;'
        f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px">'
        f'🖼️ {ready}/{len(assets)} asset images ready; every asset is represented below.</p>'
    ) if assets else ""
    assignment = proposal.get("facet_assignments")
    facet_line = ""
    if isinstance(assignment, dict):
        facet_line = (
            f'<p style="color:#166534;background:#f0fdf4;border-left:4px solid #16a34a;'
            f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px">'
            f'🧩 Record Facets: {esc(assignment.get("status", "unknown"))}</p>'
        )
    return (
        f'<h2 style="margin-bottom:2px">{esc(heading)}</h2>'
        f'<p style="font-size:1.15em;color:#2e1065;margin:2px 0"><strong>{title}</strong></p>'
        f'<p style="color:#444;line-height:1.5;margin-top:4px;max-width:660px">{idea}</p>'
        f'{calendar_line}{art_line}{facet_line}{buttons}{asset_grid(assets)}'
    )


def build_payload(digest: dict[str, Any]) -> dict[str, Any]:
    # The legacy payload builder reads its globals at call time, so replacing this
    # one function upgrades both tomorrow and yesterday without copying the rest.
    legacy.proposal_section = proposal_section
    payload = legacy.build_payload(digest)

    shown_slugs = {
        str((digest.get("tomorrow_proposal") or {}).get("slug") or ""),
        str((digest.get("yesterday_output") or {}).get("slug") or ""),
    }
    additional = [
        proposal for proposal in digest.get("recent_dream_outputs", [])
        if isinstance(proposal, dict) and str(proposal.get("slug") or "") not in shown_slugs
    ]
    if additional:
        recent_html = (
            '<h2 style="margin-bottom:2px">📅 Earlier completed bundles</h2>'
            + "".join(proposal_section("Built bundle", proposal) for proposal in additional)
        )
        divider = '<hr style="margin:22px 0;border:none;border-top:2px solid #eee">'
        if divider in payload["htmlContent"]:
            payload["htmlContent"] = payload["htmlContent"].replace(
                divider, recent_html + divider, 1
            )
        else:
            payload["htmlContent"] += recent_html

    status = str(digest.get("daily_dream_output_status") or "")
    if status and not digest.get("yesterday_output"):
        marker = '<h2 style="margin-bottom:2px">🖼️ Previous completed output</h2>'
        note = f'<p style="color:#92400e;background:#fffbeb;padding:8px 12px;border-left:4px solid #f59e0b">{esc(status)}</p>'
        payload["htmlContent"] = payload["htmlContent"].replace(marker, marker + note, 1)
    return payload


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    input_path = Path(args[0] if args else "digest.json")
    output_path = Path(args[1] if len(args) > 1 else "digest-email.json")
    digest = json.loads(input_path.read_text(encoding="utf-8"))
    output_path.write_text(json.dumps(build_payload(digest), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
