# Asset coverage matrix

Static repository audit completed 2026-07-14 for every project directory under `projects/`
(excluding the non-project support directories `_template`, `images`, `curation`, `process`).
Covers icon/card/hero identity images, ArtCollection inspiration images, and mock-screenshot
need. Per `DESIGN-BRIEF.md`, "title image" and `hero` are the same asset — there is no separate
title-image slot to track.

This is a filesystem-verifiable audit only. Two things it deliberately does **not** attempt,
consistent with `FRONTEND-SURFACE-MAP.md`'s existing precedent of flagging DB-only fields
rather than guessing:

- **Project Dreams** (`dreamType: PROJECT` records) live in the Kind Robots database, not in
  any file this repo can read. Whether a project has a Dream, and what its `liveUrl` is, needs
  live-DB verification — not claimed here.
- **Bot avatar / emotion-action portraits** are covered by `t-004` (bot parity spec), not this
  matrix — a project's bot-image gap is a different asset family from its identity images.
- No image binaries were generated or reviewed for quality while producing this matrix, per
  `DESIGN-BRIEF.md`'s non-goals.

## Method

- **Icon/card/hero present**: `projects/images/<slug>-{icon,card,hero}.webp` exists in this
  repo (the canonical destination per `ART-PROMPTS.md`).
- **Queued**: an entry for that asset exists in `projects/art-prompts.yaml`'s `images:` list
  (`status: pending` prompt already written, just not generated/saved yet).
- **Missing & unqueued**: neither present nor queued — nothing in the pipeline will produce it
  without a new prompt being added.
- **Inspiration images**: count of `*inspiration*.webp` files in Kind Robots'
  `public/images/artcollections/<slug>/`. Target is at least 3 per `DESIGN-BRIEF.md`'s visual
  asset parity section.
- **Mock screenshot needed**: pulled from `FRONTEND-SURFACE-MAP.md`'s Class column where that
  project was audited (`A`/`D` = real or intended user-facing surface → screenshot concepts
  are useful; `B` = external bridge; `C` = internal/shared, no product surface to screenshot).
  Eleven projects below post-date or were out of scope for that audit and are marked
  **unclassified** rather than guessed.

## Matrix

| Project | Override status | Icon/card/hero | Missing & unqueued | Inspirations (of 3+) | Mock screenshot needed? |
| --- | --- | --- | --- | --- | --- |
| `ai-art-academy` | active | queued (icon,card,hero) | — | 0 | Yes (Class A) |
| `alexa-integration` | active | have | — | 3 | B — external bridge, low priority |
| `animation-manager` | active | **none** | icon, card, hero | 0 | Unclassified |
| `animation-studio` | active, no override (see `conductor/t-039`) | **none** | icon, card, hero | 0 | Unclassified — resolve t-039 first |
| `appmaker` | active | have | — | 0 | Yes (Class A/D) |
| `approval-portal` | retired | have | — | 3 | No — retired |
| `art-generator-connect` | active | have | — | 3 | No (Class C — internal integration) |
| `brainstorm` | active | have | — | 3 | Yes (Class A) |
| `career-transition` | retired | have | — | 0 | No — retired |
| `challenge-center` | active | have | — | 0 | Yes (Class D) |
| `coat-dance` | active | have | — | 3 | Yes (Class D) |
| `coloring-book` | active | queued (icon,card,hero) | — | 0 | Yes (Class A) |
| `conductor` | active | have | — | 3 | Yes (Class A) |
| `conductor-app` | active | have | — | 4 | B — external bridge, low priority |
| `davinci` | active | have (icon,card) | hero | 0 | Yes (Class D) |
| `digital-storefront` | active | have | — | 3 | No (Class A, complete surface) |
| `dream-cycle` | active | queued (icon,card,hero) | — | 0 | No (Class C — internal automation) |
| `ecosystem-map` | active | queued (icon,card,hero) | — | 0 | No (Class C — internal planning) |
| `engagement` | finished | have | — | 4 | No (Class C, finished) |
| `global-ui` | active | have | — | 4 | No (Class C — internal shared layer) |
| `humboldt-impropriety-calendar` | retired | have | — | 0 | No — retired |
| `humboldt-scoop` | active | have | — | 3 | B/D — external bridge |
| `humboldt-scoop-cms` | active | have | — | 3 | D — admin tool |
| `kind-robots` | active | have | — | 4 | No (Class C — the platform itself) |
| `kindrobots-unraid` | active | **none** | icon, card, hero | 0 | Unclassified — infra, likely No |
| `media-watchlist` | active | have | — | 4 | Yes (Class D) |
| `mermaids-of-venice` | active | have | — | 3 | Yes (Class D, first storefront product) |
| `model-builder` | active | **none** | icon, card, hero | 0 | Unclassified |
| `mural-design` | active | **none** | icon, card, hero | 0 | No — Class A but already shipped/complete surface |
| `newsfeed` | active | **none** | icon, card, hero | 0 | Unclassified |
| `packmaker` | active | have (icon) | card, hero (both queued) | 0 | Yes (Class D) |
| `pinball-hero` | retired | have | — | 0 | No — retired |
| `recipe-box` | retired | have | — | 0 | No — retired |
| `ruler-hooked` | active | queued (icon,card,hero) | — | 0 | Unclassified |
| `serendipity` | active | have | — | 0 | Yes (Class D) |
| `sketchy` | active | have | — | 3 | Yes (Class D) |
| `storymaker` | active | have | — | 4 | Yes (Class D) |
| `superkate-hairstyle-ai` | active | queued (icon,card,hero) | — | 0 | Yes (Class A, shares Superkate tab) |
| `superkate-services-calculator` | active | have | — | 0 | Yes (Class A, shares Superkate tab) |
| `wishmaster` | active | have | — | 4 | Yes (Class A/D) |

## Gaps found

### Missing & unqueued icon/card/hero (needs new `art-prompts.yaml` entries)

Six **active** projects have no identity images at all, and nothing queued to produce them:

- `animation-manager` — icon, card, hero
- `kindrobots-unraid` — icon, card, hero
- `model-builder` — icon, card, hero
- `mural-design` — icon, card, hero
- `newsfeed` — icon, card, hero
- `davinci` — hero only (icon/card already exist)

Plus `animation-studio`, whose own active/retired status is an open question
(`conductor/t-038`/`t-039`) — asset work there should wait on that resolution rather than
front-run it.

Per `DESIGN-BRIEF.md`'s image approval gate, closing this gap means **adding prompts to
`projects/art-prompts.yaml`**, not generating images directly — routed to whichever project
picks it up (art-generator-connect owns the generation pipeline itself; the identity images
are each project's own roadmap responsibility).

### Already queued, just needs a generation pass

Seven projects have `status: pending` icon/card/hero prompts already written in
`art-prompts.yaml` waiting to be picked off the queue: `ai-art-academy`, `coloring-book`,
`dream-cycle`, `ecosystem-map`, `ruler-hooked`, `superkate-hairstyle-ai` (all three types), and
`packmaker` (card + hero; icon already exists). No new prompt-writing needed — these just need
a generation cycle plus the human approval step `DESIGN-BRIEF.md` requires before promotion.

### Inspiration image gaps

23 of the 34 non-retired projects have **zero** inspiration images (target: 3+), including
several `active`, `priority: high` projects that already have full icon/card/hero coverage:
`appmaker`, `challenge-center`, `serendipity`, `superkate-services-calculator`. Inspiration
images establish visual vocabulary before a project's other assets get generated, so these are
good candidates for the next `art-prompts.yaml` `inspirations:`-style batch (see
`ART-PROMPTS.md`'s existing inspiration backlog for the prompt format).

### Mock screenshot concepts

Genuinely user-facing projects per `FRONTEND-SURFACE-MAP.md`'s Class A/D — `ai-art-academy`,
`coloring-book`, `conductor`, `brainstorm`, `challenge-center`, `coat-dance`, `davinci`,
`media-watchlist`, `mermaids-of-venice`, `packmaker`, `serendipity`, `sketchy`, `storymaker`,
both Superkate projects, `wishmaster`, `appmaker` — are reasonable mock-screenshot candidates.
Eleven newer or unaudited projects (`animation-manager`, `animation-studio`,
`kindrobots-unraid`, `model-builder`, `newsfeed`, `ruler-hooked`, and the four retired/finished
projects already marked No) fall outside `FRONTEND-SURFACE-MAP.md`'s 2026-07-10 audit scope —
classifying them belongs to a `FRONTEND-SURFACE-MAP.md` refresh, not a guess folded into this
matrix.

## Canonical destination paths (for reference)

- Icon/card/hero: `projects/images/<slug>-{icon,card,hero}.webp` in `silasfelinus/conductor`.
- Inspiration images: `public/images/artcollections/<slug>/<slug>-inspiration-0{n}.webp` in
  `silasfelinus/kind_robots`.
- Prompt source of truth: `projects/art-prompts.yaml` (`images:` for identity assets); active
  send-now queue: `projects/art-generate.yaml`.
