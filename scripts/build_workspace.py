#!/usr/bin/env python3
"""
build_workspace.py — Regenerate workspace.html from projects/*/roadmap.yaml and pitches/*.md

Run from repo root: python scripts/build_workspace.py
"""

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

ART_VARIANTS = ("icon", "card", "hero")
ALLOWED_IMAGE_EXTS = (".webp", ".png", ".jpg", ".jpeg")

ART_PROMPTS_HEADER = """# art-prompts.yaml — Image queue for Conductor project assets and Kind Robots missing-image requests
#
# Project assets use `images:` and are pruned automatically when matching files
# exist in this repo's projects/images/ folder.
#
# Site-wide missing-image reports use `requests:`. Kind Robots writes those
# requests here when an admin sees a missing image. Requests should be removed
# once the image has been generated and committed to the target repo.
#
# Project image variants:
#   icon  — square 1:1 (256×256 min). Used in nav, sidebar, card headers, favicons.
#   card  — portrait 2:3 (512×768 min). Shown on the workspace project card.
#   hero  — landscape 16:9 (1280×720 min). Shown as a banner/header in project view.
#
# Workflow:
#   1. Copy the prompt into ChatGPT (image generation) or call the OpenAI Images API (model: gpt-image-1).
#   2. Set the correct aspect ratio in the generation UI (1:1 / 2:3 / 16:9).
#   3. Export as .webp at the minimum size listed.
#   4. Save to the image_path listed below.
#   5. Run `python scripts/build_workspace.py` to refresh the workspace.
#
# Status values: pending

"""

PLACEHOLDER = {
    "icon": "projects/images/coming-soon-icon.svg",
    "card": "projects/images/coming-soon-card.svg",
    "hero": "projects/images/coming-soon-hero.svg",
}

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

UPLOAD_JS = """
<script>
(function () {
  const ON_SERVER = location.protocol !== 'file:';

  function showBanner(msg, color) {
    const b = document.createElement('div');
    b.style.cssText = 'position:fixed;bottom:1rem;right:1rem;background:' + color +
      ';color:#fff;font-size:0.8rem;padding:0.5rem 1rem;border-radius:0.5rem;z-index:999;font-family:system-ui';
    b.textContent = msg;
    document.body.appendChild(b);
    setTimeout(() => b.remove(), 3000);
  }

  function initUploads() {
    if (ON_SERVER) document.body.classList.add('on-server');
    document.querySelectorAll('img[data-slug]').forEach(img => {
      img.classList.add('uploadable');
      img.title = (img.title ? img.title + ' · ' : '') +
        (ON_SERVER ? 'Click to upload replacement' : 'Run serve_workspace.py to enable uploads');
      if (!ON_SERVER) return;
      img.addEventListener('click', () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.webp,.png,.jpg,.jpeg';
        input.onchange = async () => {
          const file = input.files[0];
          if (!file) return;
          img.style.opacity = '0.4';
          const fd = new FormData();
          fd.append('slug', img.dataset.slug);
          fd.append('variant', img.dataset.variant);
          fd.append('file', file);
          try {
            const res = await fetch('/upload', { method: 'POST', body: fd });
            const data = await res.json();
            if (data.ok) {
              showBanner('Saved ' + data.saved + ' — reloading…', '#22c55e');
              setTimeout(() => location.reload(), 800);
            } else {
              showBanner('Upload failed: ' + (data.error || 'unknown'), '#ef4444');
              img.style.opacity = '';
            }
          } catch (e) {
            showBanner('Error: ' + e.message, '#ef4444');
            img.style.opacity = '';
          }
        };
        input.click();
      });
    });

    if (!ON_SERVER) {
      const hint = document.getElementById('upload-hint');
      if (hint) hint.style.display = 'block';
    }
  }

  document.addEventListener('DOMContentLoaded', initUploads);
})();
</script>
"""


def default_image_path(slug, variant):
    return f"projects/images/{slug}-{variant}.webp"


def image_exists(slug, variant, sub):
    image_path = sub.get("image_path") or default_image_path(slug, variant)
    if (REPO_ROOT / image_path).exists():
        return True

    for ext in ALLOWED_IMAGE_EXTS:
        candidate = IMAGES_DIR / f"{slug}-{variant}{ext}"
        if candidate.exists():
            return True

    return False


def normalize_pending_variant(slug, variant, sub):
    normalized = dict(sub)
    normalized["image_path"] = normalized.get("image_path") or default_image_path(slug, variant)
    normalized["status"] = "pending"
    return normalized


def pending_art_prompt_entries(data):
    pending = []

    for entry in data.get("images") or []:
        if not isinstance(entry, dict):
            continue

        slug = entry.get("project")
        if not slug:
            continue

        pending_entry = {"project": slug}

        for variant in ART_VARIANTS:
            sub = entry.get(variant)
            if not isinstance(sub, dict):
                continue

            if not image_exists(slug, variant, sub):
                pending_entry[variant] = normalize_pending_variant(slug, variant, sub)

        if len(pending_entry) > 1:
            pending.append(pending_entry)

    return pending


def request_is_complete(request):
    status = str(request.get("status") or "pending").strip().lower()
    if status == "done":
        return True

    target_repo = str(request.get("target_repo") or request.get("repo") or "").strip()
    image_path = str(request.get("image_path") or "").strip()

    if image_path and target_repo in ("", "silasfelinus/conductor"):
        return (REPO_ROOT / image_path).exists()

    return False


def normalize_art_requests(data):
    requests = []
    seen = set()

    for request in data.get("requests") or []:
        if not isinstance(request, dict):
            continue

        if request_is_complete(request):
            continue

        image_path = str(request.get("image_path") or "").strip()
        source_url = str(request.get("source_url") or "").strip()
        if not image_path and not source_url:
            continue

        target_repo = str(request.get("target_repo") or request.get("repo") or "").strip()
        key = (target_repo, image_path, source_url)
        if key in seen:
            continue
        seen.add(key)

        normalized = dict(request)
        normalized["id"] = str(normalized.get("id") or image_path or source_url).strip()
        normalized["status"] = "pending"
        if image_path:
            normalized["image_path"] = image_path
        if target_repo:
            normalized["target_repo"] = target_repo
        if source_url:
            normalized["source_url"] = source_url

        requests.append(normalized)

    return requests


def write_art_prompts(image_entries, request_entries):
    body = yaml.safe_dump(
        {"images": image_entries, "requests": request_entries},
        sort_keys=False,
        allow_unicode=True,
        width=88,
    )
    ART_PROMPTS_FILE.write_text(ART_PROMPTS_HEADER + body)


def load_art_prompts():
    if not ART_PROMPTS_FILE.exists():
        return {}, []

    with open(ART_PROMPTS_FILE) as f:
        data = yaml.safe_load(f) or {}

    image_entries = pending_art_prompt_entries(data)
    request_entries = normalize_art_requests(data)

    if (data.get("images") or []) != image_entries or (data.get("requests") or []) != request_entries:
        write_art_prompts(image_entries, request_entries)

    return {entry["project"]: entry for entry in image_entries}, request_entries


def resolve_image(slug, variant, entry):
    sub = (entry or {}).get(variant, {})
    if sub:
        path = REPO_ROOT / sub["image_path"]
        if path.exists():
            return sub["image_path"], True
    for ext in ALLOWED_IMAGE_EXTS:
        candidate = IMAGES_DIR / f"{slug}-{variant}{ext}"
        if candidate.exists():
            return f"projects/images/{slug}-{variant}{ext}", True
    return PLACEHOLDER[variant], False


def img_tag(src, done, slug, variant, css_class, alt=""):
    title = alt if done else f"{variant} art pending — see projects/art-prompts.yaml"
    return (f'<img class="{css_class}" src="{src}" alt="{alt or slug}" '
            f'title="{title}" data-slug="{slug}" data-variant="{variant}" />')


def compute_progress(milestones):
    if not milestones:
        return 0
    total = sum(m.get("weight", 10) for m in milestones)
    done = sum(
        m.get("weight", 10) * (1.0 if m.get("status") == "done"
                                else 0.5 if m.get("status") == "in-progress" else 0.0)
        for m in milestones
    )
    return round(done / total * 100, 1) if total else 0


def kind_badge(kind):
    color = KIND_COLORS.get(kind, "#64748b")
    return f'<span class="badge" style="color:{color};border-color:{color}">{kind}</span>'


def render_project_card(slug, roadmap, art_prompts):
    kind = roadmap.get("kind", "software")
    milestones = roadmap.get("milestones") or []
    tasks = roadmap.get("tasks") or []
    progress = compute_progress(milestones)
    name = roadmap.get("project", slug)
    entry = art_prompts.get(slug)

    card_src, card_done = resolve_image(slug, "card", entry)
    icon_src, icon_done = resolve_image(slug, "icon", entry)

    card_img = img_tag(card_src, card_done, slug, "card", "card-img", f"{name} card")
    icon_img = img_tag(icon_src, icon_done, slug, "icon", "card-icon", f"{name} icon")

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
      {card_img}
      <div class="card-header">
        {icon_img}
        <div class="card-title">{name}</div>
      </div>
      <div class="badges">{kind_badge(kind)}</div>
      <div class="progress-bar"><div class="progress-fill" style="width:{progress}%"></div></div>
      <div class="progress-label">{progress}% complete · {len(milestones)} milestones · {len(tasks)} tasks</div>
      {task_rows}
    </div>"""


def render_art_row(slug, variant, sub, placeholder_key):
    image_path = sub.get("image_path", f"projects/images/{slug}-{variant}.webp")
    actual = REPO_ROOT / image_path
    done = actual.exists()
    thumb_src = image_path if done else PLACEHOLDER[placeholder_key]
    status_html = ('<span class="art-status-done">done</span>' if done
                   else '<span class="art-status-pending">pending</span>')
    size = sub.get("size", "")
    prompt_text = (sub.get("prompt") or "").strip().replace("\n", " ")
    label = f"{slug} · {variant}" + (f" ({size})" if size else "")
    thumb = img_tag(thumb_src, done, slug, variant, f"art-thumb art-thumb-{variant}", f"{slug} {variant}")
    return f"""
    <div class="art-card">
      {thumb}
      <div>
        <div class="art-slug">{label} {status_html}</div>
        <div class="art-path">{image_path}</div>
        <div class="art-prompt">{prompt_text}</div>
      </div>
    </div>"""


def render_request_row(request):
    request_id = str(request.get("id") or "missing-image")
    variant = str(request.get("variant") or "image")
    size = str(request.get("size") or "")
    image_path = str(request.get("image_path") or "")
    target_repo = str(request.get("target_repo") or request.get("repo") or "")
    source_url = str(request.get("source_url") or "")
    page_url = str(request.get("page_url") or "")
    prompt_text = str(request.get("prompt") or "").strip().replace("\n", " ")
    label = f"{request_id} · {variant}" + (f" ({size})" if size else "")
    path_bits = [value for value in (target_repo, image_path, source_url, page_url) if value]
    thumb_key = variant if variant in PLACEHOLDER else "card"
    thumb = img_tag(PLACEHOLDER[thumb_key], False, request_id, variant, f"art-thumb art-thumb-{thumb_key}", request_id)

    return f"""
    <div class="art-card">
      {thumb}
      <div>
        <div class="art-slug">{label} <span class="art-status-pending">pending</span></div>
        <div class="art-path">{' · '.join(path_bits)}</div>
        <div class="art-prompt">{prompt_text}</div>
      </div>
    </div>"""


def render_art_prompts_section(art_prompts, art_requests):
    rows = ""
    for entry in sorted(art_prompts.values(), key=lambda e: e["project"]):
        slug = entry["project"]
        for variant in ART_VARIANTS:
            if variant in entry:
                rows += render_art_row(slug, variant, entry[variant], variant)

    for request in art_requests:
        rows += render_request_row(request)

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
    art_prompts, art_requests = load_art_prompts()

    for project_dir in sorted((REPO_ROOT / "projects").iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue
        roadmap_path = project_dir / "roadmap.yaml"
        if not roadmap_path.exists():
            continue
        with open(roadmap_path) as f:
            roadmap = yaml.safe_load(f)
        project_cards_html += render_project_card(project_dir.name, roadmap or {}, art_prompts)

    art_section_html = render_art_prompts_section(art_prompts, art_requests)

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
    .subtitle {{ color: var(--muted); font-size: 0.875rem; margin-bottom: 0.5rem; }}
    h2 {{ font-size: 1rem; font-weight: 700; color: var(--muted); text-transform: uppercase;
          letter-spacing: 0.05em; margin-bottom: 1rem; margin-top: 2rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }}
    /* Project cards */
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 1rem; padding: 1rem; }}
    .card-img {{ width: 100%; aspect-ratio: 2/3; object-fit: cover; border-radius: 0.6rem; margin-bottom: 0.75rem; background: var(--bg); display: block; }}
    .card-header {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }}
    .card-icon {{ width: 36px; height: 36px; flex-shrink: 0; object-fit: cover; border-radius: 0.4rem; background: var(--bg); }}
    .card-title {{ font-weight: 700; font-size: 0.95rem; }}
    .badges {{ display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.75rem; }}
    .badge {{ font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 99px; border: 1px solid; }}
    .progress-bar {{ height: 6px; background: var(--border); border-radius: 99px; overflow: hidden; margin-bottom: 0.4rem; }}
    .progress-fill {{ height: 100%; background: var(--primary); border-radius: 99px; }}
    .progress-label {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.5rem; }}
    .task-row {{ font-size: 0.8rem; color: var(--muted); padding: 0.25rem 0;
                 border-top: 1px solid var(--border); display: flex; justify-content: space-between; gap: 0.5rem; }}
    .task-row span:first-child {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    /* Pitches */
    .pitch-card {{ background: var(--surface); border: 1px solid var(--warning); border-radius: 1rem; padding: 1rem; }}
    .pitch-title {{ font-weight: 700; font-size: 0.9rem; margin-bottom: 0.25rem; }}
    .pitch-meta {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.5rem; }}
    .pitch-idea {{ font-size: 0.8rem; opacity: 0.8; }}
    /* Art prompts */
    .art-card {{ background: var(--surface); border: 1px solid #4f46e5; border-radius: 1rem; padding: 1rem; display: flex; gap: 1rem; align-items: flex-start; }}
    .art-thumb {{ flex-shrink: 0; object-fit: cover; border-radius: 0.4rem; background: var(--bg); }}
    .art-thumb-icon {{ width: 52px; height: 52px; }}
    .art-thumb-card {{ width: 44px; height: 66px; }}
    .art-thumb-hero {{ width: 100px; height: 56px; }}
    .art-slug {{ font-weight: 700; font-size: 0.85rem; margin-bottom: 0.25rem; }}
    .art-path {{ font-size: 0.7rem; color: var(--muted); font-family: monospace; margin-bottom: 0.4rem; }}
    .art-prompt {{ font-size: 0.75rem; color: var(--muted); font-style: italic; line-height: 1.4; }}
    .art-status-done {{ color: #22c55e; font-size: 0.7rem; font-weight: 600; }}
    .art-status-pending {{ color: #f59e0b; font-size: 0.7rem; font-weight: 600; }}
    /* Upload affordance (activated by JS when served) */
    .uploadable {{ cursor: default; }}
    .uploadable[data-slug] {{ transition: opacity 0.15s, outline 0.15s; }}
    .on-server .uploadable {{ cursor: pointer; }}
    .on-server .uploadable:hover {{ opacity: 0.75; outline: 2px dashed #6366f1; outline-offset: 3px; border-radius: 0.4rem; }}
    #upload-hint {{ display: none; color: var(--muted); font-size: 0.78rem; margin-bottom: 1.5rem; }}
    #upload-hint code {{ background: var(--surface); padding: 0.1rem 0.4rem; border-radius: 0.3rem; color: #a5b4fc; }}
    footer {{ margin-top: 2.5rem; font-size: 0.75rem; color: var(--muted); text-align: center; }}
  </style>
</head>
<body>
  <h1>⚡ Conductor Workspace</h1>
  <p class="subtitle">Generated {now} · <code>python scripts/build_workspace.py</code></p>
  <p id="upload-hint">To replace images, run <code>python scripts/serve_workspace.py</code> and open http://localhost:8000/ — then click any image to upload.</p>

  <h2>Projects</h2>
  <div class="grid">
    {project_cards_html}
  </div>

  <h2>Art Prompts</h2>
  <p style="color:#94a3b8;font-size:0.8rem;margin-bottom:1rem">
    Three images per project:
    <strong style="color:#e2e8f0">icon</strong> (1:1, 256×256),
    <strong style="color:#e2e8f0">card</strong> (2:3, 512×768),
    <strong style="color:#e2e8f0">hero</strong> (16:9, 1280×720).
    Generate using ChatGPT image generation or the OpenAI Images API (<code style="color:#a5b4fc">gpt-image-1</code>)
    at the correct ratio, drop the .webp into the listed path,
    — or click any placeholder while running <code style="color:#a5b4fc">serve_workspace.py</code>.
  </p>
  <div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(380px, 1fr))">
    {art_section_html or '<p style="color:#64748b">No art prompts pending.</p>'}
  </div>

  <h2>Pitches Awaiting Vote</h2>
  <div class="grid">
    {pitch_cards_html or '<p style="color:#64748b">No pitches pending.</p>'}
  </div>

  <footer>Conductor · {now}</footer>
  {UPLOAD_JS}
</body>
</html>"""

    WORKSPACE_FILE.write_text(html)
    print("workspace.html written")


if __name__ == "__main__":
    build_workspace()
