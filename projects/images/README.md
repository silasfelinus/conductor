# Project Card Images

Drop generated art here and the workspace updates automatically.

## How to add an image

1. Open `projects/art-prompts.yaml` — find the DALL-E prompt for your project.
2. Paste the prompt into ChatGPT (DALL-E 3 or GPT-4o image gen).
3. Download the result, export as `.webp` at 512×512px (1:1 ratio).
4. Save it here as `{project-slug}.webp` (e.g. `approval-portal.webp`).
5. Run `python scripts/build_workspace.py` from the repo root.

The project card immediately shows your image instead of the placeholder.

## Files

| File | Purpose |
|------|---------|
| `coming-soon.svg` | Placeholder shown while a project's real art is pending — do not delete |
| `{slug}.webp` | Real card art, replaces the placeholder for that project |
