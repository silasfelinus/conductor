# Project art assets and the image intake pipeline

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read when creating a project or touching project icon/card/hero art.

## Project art

Every project has three visual assets displayed in the kind_robots Workspace panel:
- **icon** (`{slug}-icon.webp`, 256×256) — shown in the detail header
- **card** (`{slug}-card.webp`, 512×768) — shown on the project card
- **hero** (`{slug}-hero.webp`, 1280×720) — shown as a banner when a project is selected

Files live in `projects/images/`. The workspace derives URLs from the project slug; missing
files fall back to a placeholder automatically.

**Image intake pipeline** (`projects/process/` → `scripts/distribute_images.py`, run
automatically by the distribute-images workflow on pushes to main): each file routes by
art-generate.yaml / art-prompts.yaml entry, then filename convention. A file that matches a
known slug but has no specific resolution (e.g. `{slug}-inspiration.webp`, `{slug}-sketch.webp`)
becomes a new inspiration at kind_robots `public/images/{slug}/{slug}-inspiration-{n}.webp` —
a slug's folder there IS its art collection, tracked by a `gallery.json` manifest the script
maintains. If a distributed image would replace an existing file, the original is moved into
its slug's inspiration folder first and the new image takes its place. Files that match
nothing land in `projects/process/unmatched/` for Silas.

**Generated image approval rule:** Silas lifted the old approval block on 2026-07-06. Agents
may let the auto generator create images without asking first, and generated outputs may move
into canonical project images, ArtCollection inspirations, Dream images, Bot avatars, or Bot
emotion/action portraits when the task calls for it. This is intentionally low-stakes: generated
images are disposable and easy for Silas to delete, replace, or regenerate. Preserve prompt,
model, seed/source path, destination, and project slug metadata whenever practical so the image
can be traced or recreated. Do not use this rule to publish externally, spend money, modify
secrets/DNS/billing, or bypass any unrelated human gate.

**When creating or merging a new project**, append three image request entries to
`ART-PROMPTS.md` at the repo root using the template in that file. Remove each entry once
its image file is committed to `projects/images/`. Agents may also generate and commit those
assets directly through the auto art pipeline when a scoped task requests it; no separate
Silas approval is required for the image generation itself.
