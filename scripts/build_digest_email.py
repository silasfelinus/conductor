#!/usr/bin/env python3
"""Build the daily digest email JSON from digest JSON.

The digest is art-forward: it leads with tomorrow's dream proposal (facsimile
pitch cards mirroring kind_robots' dream-pitch-sheet, with a comment/edit link),
then yesterday's built output, the day's highest-scored art, and a highlight
reel of new creations — followed by the usual project-management sections.
"""
import html
import json
import sys
from pathlib import Path

# Per-type card theming, mirroring kind_robots components/dreams/dream-pitch-sheet.vue
# (theme accents) and stores/helpers/sheetHelper.ts (pitchSheetDefaults labels).
THEME = {
    "CHARACTER": {"accent": "#be185d", "paper": "#fff3e6", "soft": "#ffe3ef", "ink": "#4a1233", "icon": "👤"},
    "LOCATION": {"accent": "#1e3a8a", "paper": "#fff4df", "soft": "#e3efff", "ink": "#182943", "icon": "📍"},
    "NARRATOR": {"accent": "#1d4ed8", "paper": "#fff7e8", "soft": "#e8f1ff", "ink": "#14264b", "icon": "📖"},
    "REWARD": {"accent": "#b91c1c", "paper": "#fff5df", "soft": "#ffe3d3", "ink": "#531313", "icon": "🎁"},
    "SCENARIO": {"accent": "#0f766e", "paper": "#fff8e9", "soft": "#dff8f4", "ink": "#123c42", "icon": "🔀"},
    "PITCH": {"accent": "#7e22ce", "paper": "#fff5e7", "soft": "#f5e6ff", "ink": "#32165c", "icon": "✨"},
}


def esc(value):
    return html.escape(str(value))


def ul(items):
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def pitch_card(ctype, title, subtitle, hook, highlights, image_url=None):
    """One facsimile pitch card: per-type accent + icon, a highlight trio, optional image."""
    t = THEME.get(ctype, THEME["PITCH"])
    rows = ""
    for label, value in highlights:
        if not value:
            continue
        rows += (
            f'<div style="margin:6px 0"><span style="display:block;font-size:10px;'
            f'letter-spacing:.06em;text-transform:uppercase;color:{t["accent"]};'
            f'font-weight:700">{esc(label)}</span>'
            f'<span style="color:{t["ink"]}">{esc(value)}</span></div>'
        )
    img = ""
    if image_url:
        img = (
            f'<img src="{esc(image_url)}" alt="{esc(title)}" '
            f'style="width:100%;max-width:100%;border-radius:8px;display:block;'
            f'margin-bottom:8px;border:1px solid {t["soft"]}">'
        )
    sub = (
        f'<div style="font-size:11px;color:{t["accent"]};font-weight:700;'
        f'letter-spacing:.04em;text-transform:uppercase">{esc(subtitle)}</div>'
    ) if subtitle else ""
    hook_html = (
        f'<div style="font-style:italic;color:{t["ink"]};opacity:.85;'
        f'margin:6px 0 2px;font-size:13px">{esc(hook)}</div>'
    ) if hook else ""
    return (
        f'<div style="display:inline-block;vertical-align:top;width:230px;'
        f'margin:6px;padding:14px;border:1px solid {t["accent"]};border-radius:12px;'
        f'background:{t["paper"]};box-shadow:0 1px 3px rgba(0,0,0,.08);'
        f'font-family:Georgia,serif">'
        f'{img}'
        f'<div style="font-size:11px;color:{t["accent"]};font-weight:700">'
        f'{t["icon"]} {esc(ctype.title())}</div>'
        f'<div style="font-size:16px;font-weight:700;color:{t["ink"]};margin:2px 0">{esc(title)}</div>'
        f'{sub}{hook_html}'
        f'<div style="margin-top:8px;border-top:1px dashed {t["accent"]}55;padding-top:6px">{rows}</div>'
        f'</div>'
    )


def proposal_cards(data, images=None):
    """Map a proposal's structured data into ordered facsimile cards."""
    images = images or []
    cards = []
    for loc in data.get("locations", []):
        cards.append(pitch_card(
            "LOCATION", loc.get("title", ""), "",
            loc.get("art_direction", ""),
            [("Known For", loc.get("known_for")), ("Local Rule", loc.get("local_rule")),
             ("Best Scene", loc.get("best_scene"))],
        ))
    for ch in data.get("characters", []):
        cards.append(pitch_card(
            "CHARACTER", ch.get("name", ""), "", ch.get("look", ""),
            [("Wants", ch.get("role_drive")), ("Carries", ch.get("carries")),
             ("Complication", ch.get("complication"))],
        ))
    nar = data.get("narrator")
    if nar:
        cards.append(pitch_card(
            "NARRATOR", nar.get("name", ""), "Narrator bot", nar.get("voice", ""),
            [("Mission", nar.get("personality")), ("Appears As", nar.get("appears_as")),
             ("Best For", nar.get("best_for"))],
        ))
    for rw in data.get("rewards", []):
        cards.append(pitch_card(
            "REWARD", rw.get("name", ""),
            f'{rw.get("reward_type", "")} · {rw.get("rarity", "")}', "",
            [("Grants", rw.get("grants")), ("Best Used When", rw.get("best_used_when")),
             ("The Catch", rw.get("catch"))],
        ))
    # Attach any matched images to the first card as a header (yesterday's output).
    if images and cards:
        strip = "".join(
            f'<img src="{esc(im["url"])}" alt="{esc(im.get("name", ""))}" '
            f'style="height:90px;border-radius:6px;margin:3px;border:1px solid #ddd">'
            for im in images
        )
        cards.insert(0, f'<div style="width:100%;margin:4px 0">{strip}</div>')
    return "".join(cards)


def _button(href, text, color="#7e22ce"):
    return (
        f'<a href="{esc(href)}" '
        f'style="display:inline-block;background:{color};color:#fff;text-decoration:none;'
        f'padding:9px 16px;border-radius:8px;font-weight:700;margin-right:8px">{text}</a>'
    )


def proposal_section(heading, proposal, cta=False, images=None, page_link=""):
    if not proposal:
        return (f'<h2 style="margin-bottom:2px">{heading}</h2>'
                f'<p style="color:#888"><i>No proposal yet — the next morning run will generate one.</i></p>')
    title = esc(proposal.get("title", ""))
    idea = esc(proposal.get("idea", ""))
    buttons = ""
    if cta and proposal.get("edit_link"):
        buttons += _button(proposal["edit_link"], "💬 Comment / edit tomorrow's dream")
    if page_link:
        buttons += _button(page_link, "🌙 View the Daily Dream page", color="#1d4ed8")
    buttons = f"<p>{buttons}</p>" if buttons else ""
    # Phase 2: when the record builder has run, say what's live on the site.
    built_line = ""
    summary = proposal.get("records_summary")
    if summary:
        parts = ", ".join(f"{count} {key}" for key, count in summary.items() if count)
        built_line = (
            f'<p style="color:#166534;background:#f0fdf4;border-left:4px solid #16a34a;'
            f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px">'
            f'✅ Built into live records: {esc(parts)}</p>'
        )
    cards = proposal_cards(proposal.get("data", {}), images=images)
    return (
        f'<h2 style="margin-bottom:2px">{heading}</h2>'
        f'<p style="font-size:1.1em;color:#333;margin:2px 0"><strong>{title}</strong></p>'
        f'<p style="color:#444;margin-top:2px">{idea}</p>'
        f'{built_line}{buttons}'
        f'<div style="margin:6px 0">{cards}</div>'
    )


def gallery_section(highlights):
    if not highlights:
        return ""
    tiles = ""
    for h in highlights:
        badge = ""
        if isinstance(h.get("score"), int):
            badge = (
                f'<span style="position:absolute;top:6px;right:6px;background:#111;color:#fff;'
                f'font-size:11px;font-weight:700;padding:2px 7px;border-radius:10px">{h["score"]}</span>'
            )
        caption = f'<div style="font-size:12px;color:#555;margin-top:4px">{esc(h.get("caption", ""))}</div>' if h.get("caption") else ""
        tiles += (
            f'<div style="display:inline-block;vertical-align:top;width:200px;margin:6px;position:relative">'
            f'<div style="position:relative">'
            f'<img src="{esc(h.get("url", ""))}" style="width:200px;height:150px;object-fit:cover;'
            f'border-radius:10px;border:1px solid #ddd;display:block">{badge}</div>'
            f'{caption}</div>'
        )
    return (
        '<h2 style="margin-bottom:2px">🏆 Top-scored art today</h2>'
        '<p style="color:#666;margin-top:2px;font-size:13px">Highest aesthetic scores from the style assessor.</p>'
        f'<div>{tiles}</div>'
    )


def reel_section(creations):
    if not creations:
        return ""
    chips = "".join(
        f'<span style="display:inline-block;background:#eef;border:1px solid #ccd;'
        f'border-radius:14px;padding:5px 12px;margin:4px;color:#335;font-size:13px">✨ {esc(c)}</span>'
        for c in creations
    )
    return f'<h2 style="margin-bottom:2px">🎬 New creations</h2><div>{chips}</div>'


def build_payload(digest):
    project_html = ""
    for project in digest["projects"]:
        project_name = esc(project["name"])
        project_kind = esc(project["kind"])
        project_html += (
            f"<h3>{project_name} <span style='color:#888'>({project_kind})</span> — "
            f"{project['progress_pct']}%</h3>"
        )
        project_html += ul(
            f"{milestone['title']} — {milestone['status']}"
            for milestone in project["milestones"]
        )
        if project["in_flight"]:
            project_html += "<p><i>In flight:</i></p>" + ul(project["in_flight"])

    open_branches = digest.get("open_branches", [])
    digest_date = esc(digest["date"])
    greeting = esc(digest.get("greeting", "Hello, Silas!"))
    activity_since = digest.get("activity_since", [])
    autonomous = digest.get("autonomous_work", [])
    spark = digest.get("daily_spark", {})
    spark_label = esc(spark.get("label", "✨ Daily spark"))
    spark_text = esc(spark.get("text", ""))
    spark_html = (
        f'<p style="background:#f0f7ff;border-left:4px solid #7ab;padding:10px 14px;'
        f'border-radius:0 6px 6px 0;font-style:italic;color:#335">'
        f'<strong>{spark_label}:</strong> {spark_text}</p>'
    ) if spark_text else ""

    # Art-forward sections lead the digest.
    page_link = digest.get("daily_dream_page", "")
    tomorrow = proposal_section("🌙 Tomorrow's dream", digest.get("tomorrow_proposal"),
                                cta=True, page_link=page_link)
    yo = digest.get("yesterday_output")
    yesterday = proposal_section("🖼️ Yesterday's output", yo,
                                 images=(yo or {}).get("images") if yo else None,
                                 page_link=(yo or {}).get("page", "") if yo else "")
    gallery = gallery_section(digest.get("art_highlights", []))
    reel = reel_section(digest.get("new_creations", []))
    art_block = "".join(x for x in (tomorrow, yesterday, gallery, reel) if x)

    html_content = f"""
    <p style="font-size:1.15em;color:#444;margin-bottom:4px">{greeting}</p>
    {spark_html}
    <h1 style="color:#2e1065">Conductor — Daily Dream Digest ({digest_date})</h1>
    {art_block}
    <hr style="margin:22px 0;border:none;border-top:2px solid #eee">
    <h3>🗳️ Awaiting your vote (pitches)</h3>{ul(digest['pitches_awaiting_vote'] or ['(no pitches waiting)'])}
    <h3>📋 Activity in last 24h</h3>{ul(activity_since or ['(nothing recorded — most work may have landed earlier)'])}
    <h3>🤖 What your agents did autonomously</h3>{ul(autonomous or ['(no autonomous activity in this window)'])}
    <h3>Needs your attention</h3>{ul(digest['all_needs_attention'] or ['(all clear)'])}
    <h3>🌿 Open branches</h3>{ul(open_branches or ['(none — all merged)'])}
    <hr>{project_html}
    """

    return {
        "subject": f"Conductor Dream Digest {digest['date']}",
        "htmlContent": html_content,
    }


def main() -> int:
    input_path = Path(sys.argv[1] if len(sys.argv) > 1 else "digest.json")
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "digest-email.json")

    with input_path.open(encoding="utf-8") as digest_file:
        digest = json.load(digest_file)

    with output_path.open("w", encoding="utf-8") as payload_file:
        json.dump(build_payload(digest), payload_file, indent=2)

    print(f"Built {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
