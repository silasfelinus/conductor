# Art Generator Connect — URL-to-Project Image Mapping

Generated: 2026-07-01 (t-003) · Revised: 2026-07-05 per Silas's placement directive
Task: art-generator-connect/t-003, revised under m5

---

## Purpose

Define exactly how generated image URLs map back to Conductor projects so that Workers,
scripts, and handoff notes all reference images the same way — and so that no binary files
are committed to conductor unless they are the three approved project art types.

---

## 1. Canonical Image Placement in kind_robots (Silas, 2026-07-05)

The ideal location for any image landing in kind_robots `public/images/` is:

```
public/images/{most_relevant_schema_or_project}/{slug}/{slug}-{utility}-{n}.webp
```

- **`{most_relevant_schema_or_project}`** — the KR schema the image serves
  (`dreams`, `bots`, `characters`, `scenarios`, `rewards`, `milestones`, …) or the
  project/collection grouping it belongs to. There is almost always a relevant one —
  figure it out rather than defaulting to a dump folder.
- **`{slug}`** — the specific entity's slug (project slug, dream slug, character
  slug…). Lowercase-hyphenated, always. A slug folder's contents ARE that slug's art
  collection (per Silas 2026-07-04), tracked by its `gallery.json` manifest.
- **`{slug}-{utility}-{n}`** — filename states the slug, the image's utility
  (`inspiration`, `icon`, `card`, `hero`, `avatar`, `sheet`, …), and the **next
  available iterated number**. Numbering never overwrites: a new icon candidate for a
  slug that already has `slug-icon-1.webp` becomes `slug-icon-2.webp`.

**`artcollections/` is a fallback, not a home.** The whole `public/images/` tree is
made of art collections mapped 1-1 by folder name and slug — so a folder literally
named `artcollections` means "unsorted." Use it only when no relevant schema or
project can be determined, and treat anything in it as awaiting re-filing.

### Current vs. target state

Existing folders are one level deep (`public/images/{slug}/`, e.g. `flower/`,
`avatars/`), written by `scripts/distribute_images.py`, and served by
`GET /api/art/collection/folder/{slug}`. That flat form stays **valid** — it is the
degenerate case where the slug is its own best context. The two-level form is
preferred for new placements once tooling supports it (roadmap t-013 aligns
`distribute_images.py`, the folder endpoint, and `gallery.json` handling; existing
folders migrate opportunistically, never by bulk move).

Resolution order for readers (endpoint, scripts):

1. `public/images/{context}/{slug}/` (target form)
2. `public/images/{slug}/` (current flat form)
3. `public/images/artcollections/{slug}/` (legacy/unsorted)

## 2. Canonical URL Pattern for kind_robots Generated Images

When the kind_robots art API returns a generated image, it uses a relative path:

```
imagePath: "/images/generated/uuid.webp"
```

The absolute public URL is formed by prepending the kind_robots base hostname:

```
https://kindrobots.org/images/generated/uuid.webp
```

For ComfyUI Flux images the path prefix differs:

```
https://kindrobots.org/images/comfy/output_00001_.png
```

`generated/` and `comfy/` are engine landing zones, not final homes — an image that
turns out to matter gets re-filed per Section 1 (that re-filing is what
`distribute_images.py` and the t-012 consumer do).

The `public/` directory root is omitted in all public URLs. The `imagePath` field in an
ArtImage DB record always stores the path without the hostname, relative to the kind_robots
public directory.

---

## 3. Project Art Flow: ART-PROMPTS.md → Generation → projects/images/ Commit

This is the **only** flow where binary image files are committed to conductor.

```
ART-PROMPTS.md (images: section)
  └─ Silas reviews and approves the prompt
       └─ Image generated externally (ChatGPT, A1111, Flux, or other tool)
            └─ File saved to projects/process/<slug>-<variant>.webp locally
                 └─ scripts/distribute_images.py moves file to projects/images/<slug>-<variant>.webp
                      └─ Committed to conductor on a named branch
                           └─ PR opened for Silas review
```

Only three file variants per project slug are ever committed:

| Variant | Filename pattern | Dimensions |
|---|---|---|
| icon | `{slug}-icon.webp` | square (512×512 or 1024×1024) |
| card | `{slug}-card.webp` | portrait 2:3 |
| hero | `{slug}-hero.webp` | landscape 16:9 |

Files land at: `projects/images/{slug}-{variant}.webp` in `silasfelinus/conductor`.
(The conductor copy is the *active* asset and keeps its un-numbered name; superseded
versions are preserved on the kind_robots side under the slug's collection folder
with iterated numbering, which `distribute_images.py` already does.)

Agents MUST NOT commit any other image binaries to conductor without explicit approval from
Silas.

---

## 4. General Generated Image Flow: URL Reference Only, No Binary Commit

For all generated images that are NOT project icon/card/hero files:

- The generation produces an ArtImage record in the kind_robots DB with an `imagePath`.
- The Worker or script constructs the full public URL (see Section 2).
- The URL is recorded in the appropriate place (handoff note, roadmap task note, PR body).
- The binary file is NEVER committed to conductor.

This covers:
- Inspiration images (stored in kind_robots per Section 1 placement)
- One-off generated images, proof-of-concept outputs, test generations
- Any image produced during a live generation call via POST /api/art/generate or
  POST /api/comfy/flux/generate

Example of correct handoff note format:

```
Generated art for {slug}:
- Icon candidate: https://kindrobots.org/images/generated/abc123.webp (ArtImage id: 1234)
- Prompt: "a glowing robot holding a paintbrush, clean app icon style"
- Next step: Silas approves → file saved to projects/images/{slug}-icon.webp → committed
```

---

## 5. When Images Are Committed to Conductor

Images are committed to conductor under exactly these conditions:

| Condition | Allowed |
|---|---|
| Project icon (`{slug}-icon.webp`) approved by Silas | YES |
| Project card (`{slug}-card.webp`) approved by Silas | YES |
| Project hero (`{slug}-hero.webp`) approved by Silas | YES |
| Inspiration images (kind_robots collections) | NO — stays in kind_robots repo |
| One-off generated images | NO — URL reference only |
| Any image during an automated agent run | NO — Workers must not commit binaries autonomously |

Agents MUST get explicit human approval before committing any binary image file, even for
the three approved project art types. The workflow in Section 3 requires Silas to confirm
the generated file is acceptable before it is committed.

---

## 6. Slug-to-Filename Convention

The established mapping for project art files committed to conductor:

```
{slug}-icon.webp   →   projects/images/{slug}-icon.webp
{slug}-card.webp   →   projects/images/{slug}-card.webp
{slug}-hero.webp   →   projects/images/{slug}-hero.webp
```

For collection images in kind_robots, per Section 1:

```
{slug}-inspiration-1.webp  →  public/images/{context}/{slug}/{slug}-inspiration-1.webp
{slug}-inspiration-2.webp  →  public/images/{context}/{slug}/{slug}-inspiration-2.webp
{slug}-icon-2.webp         →  public/images/{context}/{slug}/{slug}-icon-2.webp   (superseded/candidate icons)
```

(flat `public/images/{slug}/` remains valid until t-013 tooling lands; artcollections/
only as unsorted fallback)

The slug matches the project directory name in `projects/` and the `projectSlug` field on
the ArtImage DB record.

Workers should use the slug from the roadmap task or roadmap.yaml `project:` field. Slugs
are always lowercase with hyphens (e.g. `art-generator-connect`, not `artGeneratorConnect`).

---

## 7. How Conductor Agents Should Reference Generated Images

### In PR bodies and task notes

Always use the full public URL, not the raw `imagePath`:

```
# Correct
Generated: https://kindrobots.org/images/generated/abc123.webp
ArtImage id: 1234 (projectSlug: art-generator-connect)

# Wrong — path only, unresolvable outside kind_robots
Generated: /images/generated/abc123.webp
```

### In roadmap task notes

Include the ArtImage id and the full URL so that the image can be looked up or re-queued
if needed:

```yaml
note: >
  Generated icon candidate (ArtImage id: 1234).
  URL: https://kindrobots.org/images/generated/abc123.webp
  Awaiting Silas approval to commit as projects/images/art-generator-connect-icon.webp.
```

### In ART-PROMPTS.md entries

When adding a new project art request to the queue, include:

```
- `{slug}` — icon, card, hero → `projects/images/{slug}-{type}.webp` in `silasfelinus/conductor`
```

and write the prompt text in the backlog section of ART-PROMPTS.md following the existing
format.

### When queuing via the art request API

Use POST /api/conductor/art-request with the target `src` path as it will appear in
conductor after approval:

```json
{
  "src": "projects/images/{slug}-icon.webp",
  "label": "{ProjectLabel}",
  "variant": "icon",
  "prompt": "..."
}
```

This endpoint writes to the conductor YAML queue and does not trigger live generation.
Live generation (POST /api/art/generate or POST /api/comfy/flux/generate) requires human
approval and must be explicitly authorized by Silas for each run.

---

## Summary

| Image type | Generated where | Stored where | Committed to conductor | Reference format |
|---|---|---|---|---|
| Project icon/card/hero (active) | External or KR API | conductor projects/images/ | YES (human-approved only) | Git-tracked file |
| Collection/inspiration images | kind_robots API | kind_robots `public/images/{context}/{slug}/` (flat `{slug}/` ok; `artcollections/` = unsorted fallback) | NO | Full public URL |
| One-off generated images | kind_robots API | kind_robots public/images/generated/ (landing zone) | NO | Full public URL + ArtImage id |

No agent should autonomously commit binary images. All binary commits require a human
approval step either in the PR review or via explicit instruction from Silas.
