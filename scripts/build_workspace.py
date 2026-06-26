#!/usr/bin/env python3
"""
build_workspace.py — Regenerate workspace.html from projects/*/roadmap.yaml and pitches/*.md

Run from repo root: python scripts/build_workspace.py
"""

import os
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"
PITCHES_DIR = REPO_ROOT / "pitches"
WORKSPACE_FILE = REPO_ROOT / "workspace.html"
ART_PROMPTS_FILE = REPO_ROOT / "projects" / "art-prompts.yaml"
IMAGES_DIR = REPO_ROOT / "projects" / "images"
PLACEHOLDER_CARD  = "projects/images/coming-soon-card.svg"
PLACEHOLDER_HERO  = "projects/images/coming-soon-hero.svg"

STATUS_COLORS = {
    "ready": "#3b82f6",
    "waiting": "#64748b",
    "claimed": "#f59e0b",
    "review": "#a855f7",
    "done": "#22c55e",
    "blocked": "#ef4444",
    "needs-human": "#ec4899",
    "in-progress": "#f59e0b",
    "not-started": "#475569",
}

KIND_COLORS = {
    "software": "#6366f1",
    "content": "#a855f7",
    "proposal": "#3b82f6",
}


def load_art_prompts():
    if not ART_PROMPTS_FILE.exists():
        return {}
    with open(ART_PROMPTS_FILE) as f:
        data = yaml.safe_load(f) or {}
    return {entry["project"]: entry for entry in data.get("images", [])}


def _resolve_image(slug, variant, entry, placeholder):
    """Return (src_path, is_done) for one image variant (card or hero)."""
    sub = (entry or {}).get(variant, {})
    if sub:
        path = REPO_ROOT / sub["image_path"]
        if path.exists():
            return sub["image_path"], True
    for ext in (".webp", ".png", ".jpg", ".jpeg"):
        candidate = IMAGES_DIR / f"{slug}-{variant}{ext}"
        if candidate.exists():
            return f"projects/images/{slug}-{variant}{ext}", True
    return placeholder, False


def resolve_card_image(slug, art_prompts):
    return _resolve_image(slug, "card", art_prompts.get(slug), PLACEHOLDER_CARD)


def resolve_hero_image(slug, art_prompts):
    return _resolve_image(slug, "hero", art_prompts.get(slug), PLACEHOLDER_HERO)


def compute_progress(milestones):
    if not milestones:
        return 0
    total = sum(m.get("weight", 10) for m in milestones)
    done = sum(
        m.get("weight", 10) * (1.0 if m.get("status") == "done" else 0.5 if m.get("status") == "in-progress" else 0.0)
        for m in milestones
    )
    return round(done / total * 100, 1) if total else 0


def status_badge(status):
    color = STATUS_COLORS.get(status, "#64748b")
    return f'<span class="badge" style="color:{color};border-color:{color}">{status}</span>'


def kind_badge(kind):
    color = KIND_COLORS.get(kind, "#64748b")
    return f'<span class="badge" style="color:{color};border-color:{color}">{kind}</span>'


def render_project_card(slug, roadmap, art_prompts):
    kind = roadmap.get("kind", "software")
    milestones = roadmap.get("milestones") or []
    tasks = roadmap.get("tasks") or []
    progress = compute_progress(milestones)
    name = roadmap.get("project", slug)

    img_src, img_done = resolve_card_image(slug, art_prompts)
    img_title = f"{name} card image" if img_done else "Card art pending — see projects/art-prompts.yaml"
    img_html = f'<img class="card-img" src="{img_src}" alt="{name}" title="{img_title}" />'

    task_rows = ""
    for t in tasks[:6]:
        status = t.get("status", "ready")
        color = STATUS_COLORS.get(status, "#64748b")
        title = t.get("title", t.get("id", "?"))[:60]
        task_rows += f"""
        <div class="task-row">
          <span>{title}</span>
          <span style="color:{color}">{status}</span>
        </div>"""

    if len(tasks) > 6:
        task_rows += f'\n        <div class="task-row" style="color:#64748b"><span>…and {len(tasks) - 6} more</span></div>'

    return f"""
    <div class="card">
      {img_html}
      <div class="card-title">{name}</div>
      <div class="badges">{kind_badge(kind)}</div>
      <div class="progress-bar"><div class="progress-fill" style="width:{progress}%"></div></div>
      <div class="progress-label">{progress}% complete · {len(milestones)} milestones · {len(tasks)} tasks</div>
      {task_rows}
    </div>"""


def _art_row(slug, variant, sub, placeholder):
    image_path = sub.get("image_path", f"projects/images/{slug}-{variant}.webp")
    actual = REPO_ROOT / image_path
    if actual.exists():
        thumb_src = image_path
        status_html = '<span class="art-status-done">done</span>'
    else:
        thumb_src = placeholder
        status_html = '<span class="art-status-pending">pending</span>'
    size = sub.get("size", "")
    prompt_text = (sub.get("prompt") or "").strip().replace("\n", " ")
    label = f"{slug} · {variant} ({size})" if size else f"{slug} · {variant}"
    return f"""
    <div class="art-card">
      <img class="art-thumb art-thumb-{variant}" src="{thumb_src}" alt="{slug} {variant}" />
      <div>
        <div class="art-slug">{label} {status_html}</div>
        <div class="art-path">{image_path}</div>
        <div class="art-prompt">{prompt_text}</div>
      </div>
    </div>"""


def render_art_prompts_section(art_prompts):
    if not art_prompts:
        return ""
    rows = ""
    for entry in sorted(art_prompts.values(), key=lambda e: e["project"]):
        slug = entry["project"]
        if "card" in entry:
            rows += _art_row(slug, "card", entry["card"], PLACEHOLDER_CARD)
        if "hero" in entry:
            rows += _art_row(slug, "hero", entry["hero"], PLACEHOLDER_HERO)
    return rows


def render_pitch_card(filename, text):
    title = re.search(r"^#\s*Pitch:\s*(.+)$", text, re.MULTILINE)
    title = title.group(1).strip() if title else filename
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})-", filename)
    date = date_match.group(1) if date_match else ""
    target_match = re.search(r"^project-target:\s*(.+)$", text, re.MULTILINE)
    target = target_match.group(1).strip() if target_match else "—"
    idea_match = re.search(r"## The idea\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    idea = idea_match.group(1).strip()[:200] if idea_match else ""

    return f"""
    <div class="pitch-card">
      <div class="pitch-title">{title}</div>
      <div class="pitch-meta">{date} · target: {target}</div>
      <div class="pitch-idea">{idea}</div>
    </div>"""


def build_workspace():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    project_cards_html = ""
    pitch_cards_html = ""
    art_prompts = load_art_prompts()

    for project_dir in sorted((REPO_ROOT / "projects").iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue
        roadmap_path = project_dir / "roadmap.yaml"
        if not roadmap_path.exists():
            continue
        with open(roadmap_path) as f:
            roadmap = yaml.safe_load(f)
        project_cards_html += render_project_card(project_dir.name, roadmap or {}, art_prompts)

    art_section_html = render_art_prompts_section(art_prompts)

    for pitch_file in sorted(PITCHES_DIR.glob("*.md")):
        if pitch_file.name == "README.md":
            continue
        text = pitch_file.read_text()
        status_match = re.search(r"^status:\s*(\S+)", text, re.MULTILINE)
        status = status_match.group(1).rstrip("#").strip() if status_match else "awaiting-silas"
        if "awaiting" in status:
            pitch_cards_html += render_pitch_card(pitch_file.name, text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Conductor Workspace</title>
  <style>
    :root {{
      --bg: #0f172a; --surface: #1e293b; --border: #334155;
      --text: #e2e8f0; --muted: #94a3b8; --primary: #6366f1;
      --success: #22c55e; --warning: #f59e0b; --error: #ef4444;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; padding: 1.5rem; }}
    h1 {{ font-size: 1.5rem; font-weight: 800; margin-bottom: 0.25rem; }}
    .subtitle {{ color: var(--muted); font-size: 0.875rem; margin-bottom: 2rem; }}
    h2 {{ font-size: 1rem; font-weight: 700; color: var(--muted); text-transform: uppercase;
          letter-spacing: 0.05em; margin-bottom: 1rem; margin-top: 2rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 1rem; padding: 1rem; }}
    .card-img {{ width: 100%; aspect-ratio: 2/3; object-fit: cover; border-radius: 0.6rem; margin-bottom: 0.75rem; background: var(--bg); }}
    .card-title {{ font-weight: 700; font-size: 0.95rem; margin-bottom: 0.5rem; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.75rem; }}
    .badge {{ font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 99px; border: 1px solid; }}
    .progress-bar {{ height: 6px; background: var(--border); border-radius: 99px; overflow: hidden; margin-bottom: 0.4rem; }}
    .progress-fill {{ height: 100%; background: var(--primary); border-radius: 99px; }}
    .progress-label {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.5rem; }}
    .task-row {{ font-size: 0.8rem; color: var(--muted); padding: 0.25rem 0;
                 border-top: 1px solid var(--border); display: flex; justify-content: space-between; gap: 0.5rem; }}
    .task-row span:first-child {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .pitch-card {{ background: var(--surface); border: 1px solid var(--warning);
                   border-radius: 1rem; padding: 1rem; }}
    .pitch-title {{ font-weight: 700; font-size: 0.9rem; margin-bottom: 0.25rem; }}
    .pitch-meta {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.5rem; }}
    .pitch-idea {{ font-size: 0.8rem; opacity: 0.8; }}
    .art-card {{ background: var(--surface); border: 1px solid #4f46e5; border-radius: 1rem; padding: 1rem; display: flex; gap: 1rem; align-items: flex-start; }}
    .art-thumb {{ flex-shrink: 0; object-fit: cover; border-radius: 0.5rem; background: var(--bg); }}
    .art-thumb-card {{ width: 52px; height: 78px; }}
    .art-thumb-hero {{ width: 112px; height: 63px; }}
    .art-slug {{ font-weight: 700; font-size: 0.85rem; margin-bottom: 0.25rem; }}
    .art-path {{ font-size: 0.7rem; color: var(--muted); font-family: monospace; margin-bottom: 0.4rem; }}
    .art-prompt {{ font-size: 0.75rem; color: var(--muted); font-style: italic; line-height: 1.4; }}
    .art-status-done {{ color: #22c55e; font-size: 0.7rem; font-weight: 600; }}
    .art-status-pending {{ color: #f59e0b; font-size: 0.7rem; font-weight: 600; }}
    footer {{ margin-top: 2.5rem; font-size: 0.75rem; color: var(--muted); text-align: center; }}
  </style>
</head>
<body>
  <h1>⚡ Conductor Workspace</h1>
  <p class="subtitle">Generated {now} · <code>python scripts/build_workspace.py</code></p>

  <h2>Projects</h2>
  <div class="grid">
    {project_cards_html}
  </div>

  <h2>Art Prompts</h2>
  <p style="color:#94a3b8;font-size:0.8rem;margin-bottom:1rem">
    Two images per project: <strong style="color:#e2e8f0">card</strong> (2:3 portrait, 512×768 min) and
    <strong style="color:#e2e8f0">hero</strong> (16:9 landscape, 1280×720 min).
    Generate in ChatGPT/DALL-E 3 at the correct ratio, export .webp, drop into the listed path —
    placeholders swap automatically on next build.
  </p>
  <div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(360px, 1fr))">
    {art_section_html or '<p style="color:#64748b">No art prompts found (add projects/art-prompts.yaml).</p>'}
  </div>

  <h2>Pitches Awaiting Vote</h2>
  <div class="grid">
    {pitch_cards_html or '<p style="color:#64748b">No pitches pending.</p>'}
  </div>

  <footer>Conductor · {now}</footer>
</body>
</html>"""

    WORKSPACE_FILE.write_text(html)
    print(f"workspace.html written")


if __name__ == "__main__":
    build_workspace()
