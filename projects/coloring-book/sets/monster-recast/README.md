# Monster Recast

- slug: `monster-recast`
- production order: book 1
- status: active production
- format: physical + digital coloring book
- content rating: progressive teen horror, approximately PG-13

## Concept

**Monster Recast** combines horror cinema lineages, gender recasting, body diversity,
and theatrical camp. Familiar monster ingredients are rebuilt as original characters
and scenes rather than copied costumes or franchise likenesses.

This is not a collection of thin models wearing gender-coded monster costumes.
Women may remain huge, muscled, burned, scarred, gaunt, old, ugly, ferocious, or
barely conventionally feminine. Men may be decorative, vulnerable, beautiful,
monstrous, or trans. Nonbinary characters and drag performers belong naturally.
Gender is part of the idea, not a costume preset.

The set is queer-positive, sex-positive, and horror-forward while remaining suitable
for progressive teenage and adult coloring audiences. Implied nudity, lingerie,
swimwear, fishnets, scars, decay, and body horror may appear; explicit anatomy,
sexualized minors, sexual violence, and graphic gore may not.

## Fixed book shape

The canonical production contract lives in `../../PRODUCTION-MODEL.md`.

Monster Recast tracks exactly **36 interior illustration proposals** in
`proposals.yaml`. The cover is separate. Every proposal aims to finish as a matched
pair:

1. a confirmed final color master
2. a faithful confirmed final black-and-white coloring-page master

The legacy creative pool remains useful:

- `homage-concepts.yaml` contains 34 solo/scene lineage concepts
- `mr-035`, The Ticking Captain, is tracked directly in `proposals.yaml`
- slot 36 currently promotes the Monster Matinee group-page seed
- the remaining group-page seeds remain alternates and inspirations unless promoted
  into a numbered production slot

## Proposal authority

`proposals.yaml` is the production source of truth. Each slot records:

- working title and proposed prompt or prompt reference
- inspirations and exploratory candidates
- accepted color and BW working files
- confirmed final-draft color and BW files
- provenance, aliases, duplicates, and unresolved review notes

Accepted and final are different. A discovered file is not automatically accepted,
and an accepted working base is not automatically print-ready.

The older `approved/manifest.yaml`, `homage-concepts.yaml`, scene request files, and
job queues remain useful inputs. They do not override the proposal ledger when they
disagree about production state.

## Required preflight

Before generation, curation, counterpart work, or final confirmation, run:

```bash
python scripts/coloring_approved_status.py --check
python scripts/coloring_proposal_status.py --check
```

The first command scans physical approved assets. The second validates the three-book
ledger contract and reports the next incomplete action.

The July 12 migration snapshot reported 27 approved WebP files, 18 represented
concepts, 9 working pairs, 8 BW-only bases, and 1 color-only base. Reconcile those
files into `proposals.yaml`; do not guess missing filenames or silently rename art.

## Production loop

Roadmap task `t-022` owns Monster Recast production. It advances small batches rather
than waiting for every exploratory render:

1. reconcile discovered files
2. fill missing titles/prompts
3. attach inspiration or generate candidates
4. record accepted working color/BW files
5. create a faithful missing counterpart
6. revise and confirm final drafts
7. stop recurring at 36 final pairs
8. hand packaging to `t-025`

Approved compositions should evolve, not restart. Preserve pose, anatomy, body type,
age, scars, creature structure, perspective, contact points, and the visual hook.

## Rendering standard

The paired master system uses:

- a high-detail color illustration with thick clean black contours, bounded flat
  color, strong perspective, and many enclosed shapes
- a BW conversion that looks like the uncolored ink stage of the same composition

Use `STYLE-GUIDE.md` for the detailed production standard:

- serious theatrical camp rather than novelty slapstick
- clean thick outlines; no gradients or painterly haze
- dense but organized detail for teen/adult coloring
- coherent anatomy, contact points, props, and spatial perspective
- one independent file per image; never a collage or contact sheet
- no text, captions, labels, grids, or panels

## Originality guardrails

Internal briefs may name source films or archetypes so the cinematic idea is not lost.
Sellable art must replace protected expression with original identity and mythology.

Do not reproduce actor likenesses, studio logos, exact masks, exact makeup, exact
costumes, signature weapons, quoted text, or copied poster layouts. Change multiple
major anchors: silhouette, face, anatomy, wardrobe, era, color language, setting,
prop, origin, movement, and mythology.

Public-domain and folkloric monsters allow closer archetypal treatment than modern
franchise-specific slashers, dolls, aliens, and masks. A rough study may remain useful
inspiration while failing final originality review.

## Character data

`characters.yaml` remains a seed bank for original recurring figures. Private Kind
Robots Character creation is a follow-up after stable final art and must not block
book production. Public Character release remains human-gated.

## Files

- `proposals.yaml` — canonical 36-slot production ledger
- `STAGE-TWO.md` / `stage-two-handoff.yaml` — issue #414 migration and inventory handoff
- `CREATIVE-DIRECTION.md` — tone, rating, body diversity, and framing
- `STYLE-GUIDE.md` — rendering, anatomy, detail, and pair-conversion standard
- `homage-concepts.yaml` — legacy 34-concept creative pool and group seeds
- `characters.yaml` — original-character seed bank
- `approved/manifest.yaml` / `approved/*.webp` — legacy approvals and physical working assets
- `art-modeler-request.yaml` / `unapproved-art-jobs.yaml` — legacy generation inputs
