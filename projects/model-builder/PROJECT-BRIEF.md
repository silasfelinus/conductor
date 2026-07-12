# Kind Robots Model Builder

## Purpose

Model Builder is a resumable, human-gated production system for upgrading existing Kind Robots records or creating new related records.

**Marketing Deck is a recipe, not the root product.** The reusable workflow is:

1. select a source model,
2. select a recipe and individual outputs,
3. review an idea pitch,
4. review proposed fields, relationships, and generation prompts,
5. generate selected assets,
6. review a final diff and create, update, link, or promote only approved work.

Supported source types:

- Project
- Character
- Bot
- Facet
- Dream
- Reward
- Scenario

Initial reference runs:

- Humboldt Scoop Solutions Project → Marketing Deck
- an approved Character or Bot → Character Deck
- an approved Dream → exactly three independently gated Characters linked to that Dream

## Core contract

### Source Model

The existing record supplying identity, constraints, canonical assets, relationships, ownership, maturity flags, and inspiration. Each run keeps both a live reference and a source snapshot so later changes can be detected.

### Recipe

A versioned, editable preset of eligible outputs. Defaults are conveniences, never mandatory bundles.

Initial recipes:

- `marketing-deck`
- `character-deck`
- `reward-deck`
- `art-upgrade`
- `relationship-expansion`

### Build Run

A resumable orchestration record containing the source, recipe version, selected options, usage, status, approvals, and revision history.

### Build Item

One requested output or prospective model, such as:

- `hero-image` for a Character
- `expression:joyful` for a Bot
- `business-card` for a Project
- `character:create:1` in a three-character Dream expansion

Each item advances independently and may be retried without restarting the run.

### Build Artifact

A generated or assembled file with prompt, workflow, provider, model or checkpoint, seed, dimensions, source asset, output path, ownership, and promotion state.

### Commit

The final API-backed create, update, link, or promotion operation. Generation never silently rewrites a durable model or establishes a relationship.

## Four explicit gates

Every Build Item uses the same stages:

1. `PITCH`
2. `FIELDS_AND_PROMPTS`
3. `GENERATE_ASSETS`
4. `COMMIT`

Users may edit, approve, reject, pause, resume, rerun, or stop after any stage.

Invalidation rules:

- Editing a pitch marks fields, prompts, assets, and commit stale.
- Editing fields or prompts marks assets and commit stale.
- Replacing an asset marks commit stale.
- Stale outputs remain as revisions until cleanup.
- A later stage cannot bypass an unapproved prerequisite.
- One failed child does not poison a quantity-based batch.

## Creation timing

### DEFERRED

No target row exists until final commit. Draft fields and assets remain attached to the Build Item.

### DRAFT_EARLY

After field approval, a private and inactive target row may be created when a durable ID is needed for assets or relationships. Final activation and canonical promotion remain separate approvals.

## Recipe matrix

| Source type | Suggested default | Additional choices |
| --- | --- | --- |
| Project | Marketing Deck | Manager Bot, Art Upgrade |
| Character | Character Deck | Art Upgrade, signature Rewards |
| Bot | Character Deck | expressions, transitions, Art Upgrade |
| Reward | Reward Deck | Art Upgrade, relationship pitches |
| Dream | Art Upgrade | Characters, Rewards, Scenarios, Narrator Bot |
| Scenario | Art Upgrade | cast Characters, Rewards |
| Facet | Art Upgrade | fitting Dreams, Characters, Rewards, Scenarios |

Users may remove all defaults and request a single output.

## Marketing Deck

Marketing Deck is primarily a Project recipe and may consume related Projects.

Selectable outputs include:

- business card
- existing-logo application sheet
- lawn sign
- banner
- flyer
- website mockup board
- app mockup board
- photo-shoot plan
- print and video shot lists
- static ad concepts and posters
- video commercial treatment
- storyboard
- optional Comfy execution package
- week-by-week launch plan

The Humboldt Scoop reference uses:

- `humboldt-scoop` as the parent business and site
- `humboldt-scoop-cms` as the related customer-management and route-planning product

Existing logos, approved copy, website direction, and real product screens remain authoritative. No unsolicited rebrand.

## Character Deck

Character Deck applies to Character and Bot sources and may also create one from a Dream, Facet, or Scenario.

Selectable outputs include identity pitch, schema-field proposal, canonical prompt, portrait candidates, promoted avatar, icon, card, hero action shots, transparent cutout or model-sheet reference, selected ExpressionMedia emotions and actions, custom expression keys, optional reaction clips, transitions, and 3D reference/model output.

The current ExpressionMedia contract remains authoritative:

- Bot XOR Character owner
- NEUTRAL as canonical generated avatar
- emotions change face or framing rather than identity
- actions may change pose and state
- dry-run validation before batch writes
- identity consistency proven on a subset before generating the full expression set

## Reward Deck

All Rewards may request a pitch, schema fields, icon, card, hero or use scene, collection placement, and relationship suggestions.

Type-aware defaults:

- `ITEM`: offer a 3D reference and printable-model path
- `PET`: optionally offer a figurine path
- `SKILL`, `POWER`, `MAGIC`, `FAVOR`: default to art-only

Model Builder distinguishes:

1. `threeDPrompt`
2. approved reference image
3. generated source model such as GLB
4. mesh inspection and repair
5. optional verified STL conversion or export
6. print-readiness review for manifold geometry, scale, wall thickness, orientation, and supports

Nothing is labeled STL or print-ready unless those stages actually occurred.

## Art Upgrade

Art Upgrade exposes only valid assets for the source, such as primary image, icon, card, hero, profile or avatar, key scene, inspiration candidates, ArtCollection, and missing-asset repair.

Asset-only runs do not rewrite unrelated text.

Standard targets:

- icon: 256×256
- card: 512×768
- hero: 1280×720
- avatars and expression stills: square

## Relationship Expansion

Initial supported expansions:

- Dream → X Characters
- Dream → X Rewards
- Dream → X Scenarios
- Dream → optional Narrator Bot
- Project → optional Manager Bot
- Scenario → X cast Characters
- Scenario → X Rewards
- Facet → fitting Dreams, Characters, Rewards, or Scenarios
- Character → signature Rewards
- Reward → optional Character-owner or Scenario-use pitch

Each child is an independent Build Item with its own gates and final relationship diff.

## Infrastructure to reuse

Build on existing Kind Robots infrastructure rather than creating a parallel system:

- current model single and batch APIs
- existing LLM generation specifications
- ArtImage and ArtCollection provenance
- ExpressionMedia and ExpressionTransition
- expression batch dry-runs
- image generation workflows
- LTX image-to-video workflows
- `/api/comfy/hunyuan3d`
- generated-art paths and inspiration-folder promotion

An endpoint inventory is mandatory before implementation. Remembered route names are not a contract.

## Proposed orchestration records

### ModelBuildRun

Stores owner, source type and snapshot, recipe/version, selected options, status, usage, timestamps, and cancellation state.

### ModelBuildItem

Stores stable output key, action (`CREATE`, `UPDATE`, or `ASSET_ONLY`), target type/id, quantity index, pitch, field and relationship drafts, prompt bundle, stage statuses, approvals, stale reason, errors, and idempotency key.

### ModelBuildArtifact

Stores artifact kind, source/prompt/workflow provenance, provider/model/checkpoint/seed, dimensions, format, draft and promoted references, ownership, and review state.

### ModelBuildRevision

Stores item, stage, previous and next payload snapshots, actor, reason, and timestamp.

These records orchestrate work; they do not replace the canonical domain models.

## Front-end architecture

The Kind Robots UI follows existing patterns:

- components render state and dispatch store actions
- `modelBuilderStore` owns API calls, run state, resume hints, and optimistic updates
- server routes own provider credentials and generation
- components never call API routes directly
- source adapters normalize display data
- model-specific writers validate final payloads

Primary screens:

1. source type and record picker
2. recipe/output selector with quantities
3. row-by-stage progress matrix
4. pitch, field, relationship, and prompt editors
5. asset candidate review and promotion
6. final create/update/link diff
7. run history and resume

## Safety and ownership

- User-requested generations belong to the requesting user.
- System canon follows existing ownership rules.
- Mature flags are preserved and explicitly reviewed.
- Credentials remain server-side.
- Estimated and actual usage are visible around expensive stages.
- Generated assets do not imply permission to publish, deploy, print, fabricate, advertise, contact customers, create accounts, or spend.
- Existing canonical files are preserved as revisions or inspirations before replacement.
- Commercial generation follows `CONTROL.md` licensing rules.

## Definition of done

Model Builder is proven when all three reference runs use the same orchestration engine:

1. HSS Marketing Deck from a Project plus related Project
2. Character Deck for an existing Character or Bot
3. Dream expansion creating and linking exactly three Characters

Each run must demonstrate editable gates, selective reruns, persistence/resume, provenance, usage visibility, safe failure recovery, idempotent final commit, and no duplicate records or silent canonical replacement.
