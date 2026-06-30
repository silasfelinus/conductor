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
KIND_ROBOTS_ROOT = REPO_ROOT.parent / "kind_robots"

ART_VARIANTS = ("icon", "card", "hero")
ALLOWED_IMAGE_EXTS = (".webp", ".png", ".jpg", ".jpeg")

ART_PROMPTS_HEADER = """# art-prompts.yaml — Image queue for Conductor project assets and Kind Robots missing-image requests
#
# Project assets use `images:` and are pruned automatically when matching files
# exist in this repo's projects/images/ folder.
#
# Inspiration images use `inspirations:`. Pruned automatically when matching files
# exist in the kind_robots repo at ../kind_robots/public/images/artcollections/.
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
# Prompt standard:
#   Write for modern OpenAI image generation, not legacy flat placeholders.
#   Kind Robots represents a consortium of projects aimed at multi-genre,
#   cross-dimensional experiences. When a scene includes people, characters,
#   teams, families, players, operators, or companions, represent a diverse array
#   across genders, races, ages, body sizes, body shapes, presentation styles,
#   and species. Mix humans, robots, animal-like beings, fantasy creatures, and
#   original nonhuman companions when it fits the asset.
#   Do this naturally and respectfully, without tokenism or stereotypes.
#   Icons should read instantly at small sizes: premium app-icon polish, strong silhouette.
#   Cards should feel like professional portrait key art for a polished product.
#   Heroes should feel like studio-quality game/product illustration with cinematic depth.
#   Always avoid readable text, logos, watermarks, contact sheets, and collages.
#
# Workflow:
#   1. Copy the generator prompt from ART-PROMPTS.md into ChatGPT.
#   2. Paste one batch of up to ten entries from this file.
#   3. Generate exactly one unique image per entry with the listed aspect ratio.
#   4. Export as .webp at the minimum size listed.
#   5. Save to the image_path listed below.
#   6. Run `python scripts/build_workspace.py` to refresh the workspace.
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


def inspiration_is_complete(image_path):
    """True if the inspiration image file exists in the kind_robots repo."""
    return (KIND_ROBOTS_ROOT / image_path).exists()


def pending_inspiration_entries(data):
    """Return inspiration entries whose image files are not yet in kind_robots."""
    pending = []
    for project in data.get("inspirations") or []:
        if not isinstance(project, dict):
            continue
        remaining_images = [
            img for img in (project.get("images") or [])
            if isinstance(img, dict) and not inspiration_is_complete(img.get("image_path", ""))
        ]
        if remaining_images:
            entry = {k: v for k, v in project.items() if k != "images"}
            entry["images"] = remaining_images
            pending.append(entry)
    return pending


def write_art_prompts(image_entries, inspiration_entries, request_entries):
    sections = {"images": image_entries, "requests": request_entries}
    if inspiration_entries:
        sections["inspirations"] = inspiration_entries
    body = yaml.safe_dump(
        sections,
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
    inspiration_entries = pending_inspiration_entries(data)
    request_entries = normalize_art_requests(data)

    if (
        (data.get("images") or []) != image_entries
        or (data.get("inspirations") or []) != inspiration_entries
        or (data.get("requests") or []) != request_entries
    ):
        write_art_prompts(image_entries, inspiration_entries, request_entries)

    return {entry["project"]: entry for entry in image_entries}, request_entries
