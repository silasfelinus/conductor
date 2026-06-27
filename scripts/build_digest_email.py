#!/usr/bin/env python3
"""Build the daily digest email JSON from digest JSON."""
import html
import json
import sys
from pathlib import Path


def ul(items):
    safe_items = [html.escape(str(item)) for item in items]
    return "<ul>" + "".join(f"<li>{item}</li>" for item in safe_items) + "</ul>"


def build_payload(digest):
    project_html = ""
    for project in digest["projects"]:
        project_name = html.escape(str(project["name"]))
        project_kind = html.escape(str(project["kind"]))
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
    digest_date = html.escape(str(digest["date"]))
    greeting = html.escape(str(digest.get("greeting", "Hello, Silas!")))
    activity_since = [html.escape(s) for s in digest.get("activity_since", [])]
    autonomous = [html.escape(s) for s in digest.get("autonomous_work", [])]
    html_content = f"""
    <p style="font-size:1.15em;color:#444;margin-bottom:4px">{greeting}</p>
    <h2>AI_Networker — Daily Digest ({digest_date})</h2>
    <h3>🗳️ Awaiting your vote (pitches)</h3>{ul(digest['pitches_awaiting_vote'] or ['(no pitches waiting)'])}
    <h3>📋 Activity in last 24h</h3>{ul(activity_since or ['(nothing recorded — most work may have landed earlier)'])}
    <h3>🤖 What your agents did autonomously</h3>{ul(autonomous or ['(no autonomous activity in this window)'])}
    <h3>Needs your attention</h3>{ul(digest['all_needs_attention'] or ['(all clear)'])}
    <h3>🌿 Open branches</h3>{ul(open_branches or ['(none — all merged)'])}
    <hr>{project_html}
    """

    return {
        "subject": f"AI_Networker Digest {digest['date']}",
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
