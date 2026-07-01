# Art Generator Connect — URL-to-Project Image Mapping

Generated: 2026-07-01
Task: art-generator-connect/t-003

---

## Purpose

Define exactly how generated image URLs map back to Conductor projects so that Workers,
scripts, and handoff notes all reference images the same way — and so that no binary files
are committed to conductor unless they are the three approved project art types.

---

## 1. Canonical URL Pattern for kind_robots Generated Images

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

ArtCollection inspiration images follow their own convention in kind_robots:

```
https://kindrobots.org/images/artcollections/<slug>/<slug>-inspiration-0N.webp
```

The `public/` directory root is omitted in all public URLs. The `imagePath` field in an
ArtImage DB record always stores the path without the hostname, relative to the kind_robots
public directory.

---

## 2. Project Art Flow: ART-PROMPTS.md → Generation → projects/images/ Commit

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

Agents MUST NOT commit any other image binaries to conductor without explicit approval from
Silas.

---

## 3. General Generated Image Flow: URL Reference Only, No Binary Commit

For all generated images that are NOT project icon/card/hero files:

- The generation produces an ArtImage record in the kind_robots DB with an `imagePath`.
- The Worker or script constructs the full public URL (see Section 1).
- The URL is recorded in the appropriate place (handoff note, roadmap task note, PR body).
- The binary file is NEVER committed to conductor.

This covers:
- Inspiration images (stored in kind_robots at `public/images/artcollections/<slug>/`)
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

## 4. When Images Are Committed to Conductor

Images are committed to conductor under exactly these conditions:

| Condition | Allowed |
|---|---|
| Project icon (`{slug}-icon.webp`) approved by Silas | YES |
| Project card (`{slug}-card.webp`) approved by Silas | YES |
| Project hero (`{slug}-hero.webp`) approved by Silas | YES |
| Inspiration images (kind_robots artcollections) | NO — stays in kind_robots repo |
| One-off generated images | NO — URL reference only |
| Any image during an automated agent run | NO — Workers must not commit binaries autonomously |

Agents MUST get explicit human approval before committing any binary image file, even for
the three approved project art types. The workflow in Section 2 requires Silas to confirm
the generated file is acceptable before it is committed.

---

## 5. Slug-to-Filename Convention

The established mapping for project art files committed to conductor:

```
{slug}-icon.webp   →   projects/images/{slug}-icon.webp
{slug}-card.webp   →   projects/images/{slug}-card.webp
{slug}-hero.webp   →   projects/images/{slug}-hero.webp
```

For ArtCollection inspiration images in kind_robots:

```
{slug}-inspiration-01.webp   →   public/images/artcollections/{slug}/{slug}-inspiration-01.webp
{slug}-inspiration-02.webp   →   public/images/artcollections/{slug}/{slug}-inspiration-02.webp
{slug}-inspiration-03.webp   →   public/images/artcollections/{slug}/{slug}-inspiration-03.webp
```

The slug matches the project directory name in `projects/` and the `projectSlug` field on
the ArtImage DB record.

Workers should use the slug from the roadmap task or roadmap.yaml `project:` field. Slugs
are always lowercase with hyphens (e.g. `art-generator-connect`, not `artGeneratorConnect`).

---

## 6. How Conductor Agents Should Reference Generated Images

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
| Project icon/card/hero | External (human-triggered) | projects/images/ | YES (human-approved only) | Git-tracked file |
| ArtCollection inspirations | kind_robots API | kind_robots public/images/artcollections/ | NO | Full public URL |
| One-off generated images | kind_robots API | kind_robots public/images/generated/ | NO | Full public URL + ArtImage id |

No agent should autonomously commit binary images. All binary commits require a human
approval step either in the PR review or via explicit instruction from Silas.
