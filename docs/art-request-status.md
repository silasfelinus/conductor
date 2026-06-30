# Art Request Status

Generated: 2026-06-30
Source: ART-PROMPTS.md + projects/images/ + kind_robots/public/images/artcollections/

Legend: ✓ = file exists | ✗ = missing | — = no prompt written yet

---

## Project assets (icon / card / hero)

Files live in `silasfelinus/conductor` at `projects/images/{slug}-{type}.webp`.

| Slug | Prompt | Icon | Card | Hero | Status |
|---|---|---|---|---|---|
| alexa-integration | ✓ | ✓ | ✓ | ✓ | done |
| approval-portal | ✓ | ✓ | ✓ | ✓ | done |
| art-generator-connect | ✓ | ✓ | ✓ | ✓ | done |
| brainstorm | ✓ | ✓ | ✓ | ✓ | done |
| career-transition | ✓ | ✗ | ✗ | ✗ | **pending — generate 3 images** |
| coat-dance | ✓ | ✓ | ✓ | ✓ | done |
| conductor | ✓ | ✓ | ✓ | ✓ | done |
| conductor-app | ✓ | ✓ | ✓ | ✓ | done |
| digital-storefront | ✓ | ✓ | ✓ | ✓ | done |
| engagement | ✓ | ✓ | ✓ | ✓ | done |
| global-ui | ✓ | ✓ | ✓ | ✓ | done |
| humboldt-scoop | ✓ | ✓ | ✓ | ✓ | done |
| humboldt-scoop-cms | ✓ | ✓ | ✓ | ✓ | done |
| kind-robots | ✓ | ✓ | ✓ | ✓ | done |
| media-watchlist | ✓ | ✓ | ✓ | ✓ | done |
| mermaids-of-venice | ✓ | ✓ | ✓ | ✓ | done |
| pinball-hero | ✓ | ✗ | ✗ | ✗ | **pending — generate 3 images** |
| sketchy | ✓ | ✓ | ✓ | ✓ | done |
| storymaker | ✓ | ✓ | ✓ | ✓ | done |
| wishmaster | ✓ | ✓ | ✓ | ✓ | done |

**Pending project asset sets:** `career-transition` (3 images), `pinball-hero` (3 images). Prompts for both are in ART-PROMPTS.md backlog.

---

## Inspiration images (3 per project)

Files live in `silasfelinus/kind_robots` at `public/images/artcollections/{slug}/{slug}-inspiration-0N.webp`.

| Slug | Prompt | In ART-PROMPTS.md | Count on disk | Status |
|---|---|---|---|---|
| alexa-integration | ✓ | backlog | 3 | done |
| approval-portal | ✓ | backlog | 3 | done |
| art-generator-connect | ✓ | backlog | 3 | done |
| brainstorm | ✓ | backlog | 3 | done |
| career-transition | — | not yet | 0 | **missing prompt + images** |
| coat-dance | ✓ | backlog | 3 | done |
| conductor | ✓ | backlog | 3 | done |
| conductor-app | ✓ | backlog | 4 | done |
| digital-storefront | ✓ | backlog | 3 | done |
| engagement | ✓ | backlog | 4 | done |
| global-ui | — | not queued | 0 | not started |
| humboldt-scoop | ✓ | backlog | 3 | done |
| humboldt-scoop-cms | ✓ | backlog | 3 | done |
| kind-robots | ✓ | backlog | 4 | done |
| media-watchlist | ✓ | backlog | 4 | done |
| mermaids-of-venice | ✓ | backlog | 3 | done |
| pinball-hero | — | not yet | 0 | **missing prompt + images** |
| sketchy | ✓ | backlog | 3 | done |
| storymaker | ✓ | backlog | 4 | done |
| wishmaster | ✓ | backlog | 4 | done |

**Inspiration gaps:**
- `career-transition`: no prompt written; no artcollection dir. Write 3 prompts in ART-PROMPTS.md backlog, then generate.
- `pinball-hero`: no prompt written; no artcollection dir. Write 3 prompts in ART-PROMPTS.md backlog, then generate.
- `global-ui`: no artcollection dir and no prompt in the backlog. Low priority — global-ui is an interface system without a strong visual identity of its own. Add prompts when the project identity is clearer.

---

## Summary

| Category | Total | Done | Pending |
|---|---|---|---|
| Project assets (icon/card/hero sets) | 20 projects × 3 = 60 | 54 | **6 (career-transition + pinball-hero)** |
| Inspiration image sets | 20 projects × 3 = 60 | ~51 | **~9 (career-transition × 3, pinball-hero × 3, global-ui × 3)** |

**Immediate actions for Silas:**
1. Generate `career-transition-icon.webp`, `-card.webp`, `-hero.webp` from prompts in ART-PROMPTS.md, commit to `projects/images/` in conductor.
2. Generate `pinball-hero-icon.webp`, `-card.webp`, `-hero.webp` from prompts in ART-PROMPTS.md, commit to `projects/images/` in conductor.
3. Write 3 inspiration prompts for `career-transition` and `pinball-hero` in ART-PROMPTS.md backlog.
4. Generate those 6 inspiration images, save to `kind_robots/public/images/artcollections/{slug}/`.
