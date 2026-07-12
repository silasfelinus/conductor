# Kind Robots Model Builder

## Purpose

Model Builder is a resumable front-end production system for upgrading existing Kind Robots records or creating new related records through explicit human gates.

A **Marketing Deck is one recipe**, not the root abstraction. The root workflow is:

1. select a source model,
2. select a recipe and individual outputs,
3. review an idea pitch,
4. review proposed model fields, relationships, and generation prompts,
5. generate selected assets,
6. create or update the durable models and promote approved assets.

Supported source types:

- Project
- Character
- Bot
- Facet
- Dream
- Reward
- Scenario

The first reference runs are:

- Humboldt Scoop Solutions Project → Marketing Deck
- an existing Character or Bot → Character Deck
- an approved Dream → three new, fully gated Characters linked to that Dream

## Product correction

The previous Marketing Deck proposal remains valuable, but it becomes one recipe inside Model Builder. The reusable abstraction is not “marketing source → marketing deliverable.” It is:

**source model → recipe → build items → gated stages → artifacts → model writes and relationships**

This matters because the same front end should be able to:

- upgrade one existing Character’s art,
- create a full Character Deck,
- turn a Reward ITEM into card art plus an optional 3D model,
- generate three Characters that fit a Dream,
- add a Narrator Bot and starter scenarios to a Dream,
- produce a Marketing Deck for a Project,
- stop after producing pitches or prompts without creating anything.

## Core vocabulary

### Source Model

The existing record that provides identity, constraints, relationships, and inspiration. A run stores both its live reference and a source snapshot so it can detect later changes.

### Recipe

A versioned set of eligible outputs and defaults for a source type. Recipes are editable presets, never mandatory bundles.

Initial recipes:

- `marketing-deck`
- `character-deck`
- `reward-deck`
- `art-upgrade`
- `relationship-expansion`

### Build Run

A resumable user-owned orchestration record containing the selected source, recipe version, options, usage, status, and revision history.

### Build Item

One requested output or one prospective model. Examples:

- `hero-image` for an existing Character
- `expression:joyful` for a Bot
- `business-card` for a Project
- `character:create:1` in a three-character Dream expansion

Each Build Item advances independently through the gates and can fail or be retried without restarting the entire run.

### Build Artifact

A generated or assembled file plus provenance: prompt, workflow, provider, model/checkpoint, seed, dimensions, source asset, output path, and promotion state.

### Commit

The final API-backed create/update/link operation. Commit is separate from generation. Generating a pretty image does not silently rewrite a model or establish a relationship.

## Four explicit gates

Every Build Item uses the same stage vocabulary.

### 1. PITCH

Produces a compact concept pitch for the requested output or prospective model.

For a new Character this is the casting idea. For a hero image it is the scene direction. For a lawn sign it is the communication concept.

The user may edit, approve, reject, or rerun it.

### 2. FIELDS_AND_PROMPTS

Produces structured, editable drafts:

- target model fields,
- relationship proposal,
- art prompts,
- optional video prompt,
- optional 3D/reference prompt,
- expected asset paths and dimensions,
- factual or schema validation warnings.

No unreviewed prose should be smuggled into a final model from a hidden prompt.

### 3. GENERATE_ASSETS

Runs only the selected deterministic, image, video, or 3D workflows. Candidate assets remain drafts until promoted.

Text-only items may complete this stage through deterministic file generation rather than Comfy.

### 4. COMMIT

Shows a final before/after or create diff, then uses the existing model APIs to:

- create or update the target row,
- create/link ArtImage or ArtCollection records where appropriate,
- upsert ExpressionMedia,
- connect related models,
- promote selected canonical files,
- leave rejected candidates in the inspiration/revision set.

Commit must be idempotent. Replaying an approved commit must not duplicate rows, files, or relations.

## Progress and invalidation rules

The front end presents requested Build Items as rows and gates as columns. A checkbox requests or approves a stage; status is shown separately as queued, running, review, complete, stale, failed, or skipped.

Rules:

- A later gate cannot silently bypass an unapproved prerequisite.
- Editing a pitch marks fields/prompts, assets, and commit stale.
- Editing fields or prompts marks assets and commit stale.
- Replacing an asset marks only commit stale unless the new asset requires prompt changes.
- Stale outputs are retained as revisions; they are not immediately deleted.
- Users can pause, resume, cancel, rerun one stage, or retry one Build Item.
- Quantity expansions create independent Build Items so one failed child does not poison the batch.

## Creation timing

New related models need two supported modes.

### DEFERRED

No target row is created until COMMIT. Draft fields and assets belong to the Build Item. Best for simple generations and maximum caution.

### DRAFT_EARLY

After FIELDS_AND_PROMPTS approval, create a private, inactive target row when a durable ID is needed for attachment or relationship work. Assets may then reference that draft. COMMIT promotes approved fields/assets and activates the row.

Draft-early creation is not publication. It must remain private/inactive and traceable to the Build Run.

## Default recipe selection

| Source type | Suggested default | Additional choices |
| --- | --- | --- |
| Project | Marketing Deck | Manager Bot, art upgrade |
| Character | Character Deck | art upgrade, signature Rewards |
| Bot | Character Deck | expressions, transitions, threads, art upgrade |
| Reward | Reward Deck | art upgrade, optional Character owner or Scenario use |
| Dream | Art Upgrade | Characters, Rewards, Scenarios, Narrator Bot |
| Scenario | Art Upgrade | cast Characters, Rewards |
| Facet | Art Upgrade | fitting Dreams, Characters, Rewards, Scenarios |

Defaults are preselected conveniences. The user can remove every default and request a single output.

## Character Deck

Character Deck applies to Character and Bot sources, and can also be used when creating one from a Dream, Facet, or Scenario.

Selectable outputs:

- identity/concept pitch
- complete schema-field proposal
- canonical art prompt
- portrait/avatar inspiration candidates
- promoted canonical portrait/avatar
- icon
- card image
- hero action shots
- transparent/cutout image
- turnaround or model-sheet reference
- selected ExpressionMedia emotions
- selected ExpressionMedia actions
- custom expression/action keys
- optional looping reaction clips
- optional high-value transitions
- optional 3D reference and generated model

The current ExpressionMedia contract is authoritative:

- Bot XOR Character owner
- NEUTRAL as canonical generated avatar
- emotions change face/framing only
- actions may change pose/state
- art prompts retain identity/presentation language
- dry-run validation occurs before batch writes

The full 20-expression set is available, but the UI should permit subsets. A reference run should prove identity consistency on a small set before spending compute on all twenty.

## Reward Deck

Reward Deck adapts to `rewardType`.

All Rewards may request:

- pitch
- schema fields
- icon
- card image
- hero/use scene
- collection placement
- Dream/Character relationship suggestions

Type-aware 3D behavior:

- `ITEM`: offer 3D reference and printable-model workflow by default
- `PET`: optionally offer a figurine workflow
- `SKILL`, `POWER`, `MAGIC`, `FAVOR`: default to art-only

The user may override defaults, but the UI should not pretend every abstract concept naturally wants an STL.

### 3D terminology

The existing Hunyuan3D endpoint accepts an image and returns a generated model file. Its current implementation appears centered on GLB-style output. Therefore Model Builder distinguishes:

1. `threeDPrompt`
2. approved 3D reference image
3. generated source model file, such as GLB
4. mesh inspection/repair
5. optional verified STL conversion/export
6. print-readiness review: manifold geometry, scale, wall thickness, orientation, and supports

A file is not called STL or print-ready unless those stages actually happened.

## Marketing Deck

Marketing Deck applies primarily to Project and can include related Project sources.

Selectable outputs remain:

- business card
- existing-logo application sheet
- lawn sign
- banner
- flyer
- website mockup board
- app mockup board
- photo-shoot plan
- print and video shot lists
- static ad concepts/posters
- video commercial treatment
- storyboard
- optional Comfy execution package
- week-by-week launch plan

The Humboldt Scoop reference uses:

- `humboldt-scoop` as parent business/site
- `humboldt-scoop-cms` as related customer-management and route-planning product

Existing logo, approved copy, website direction, and real product screens remain authoritative.

## Art Upgrade

Art Upgrade is the general-purpose recipe. It exposes only assets valid for the selected source:

- primary image
- icon
- card
- hero
- profile/avatar
- key scene
- inspiration candidates
- ArtCollection
- repair/regeneration of missing canonical assets

Asset-only runs must not rewrite unrelated text fields.

Standard targets remain:

- icon: 256×256
- card: 512×768
- hero: 1280×720
- avatars and expression stills: square

## Relationship Expansion

Expansion creates new models using valid schema relationships rather than a universal free-for-all.

Initial options:

- Dream → X Characters
- Dream → X Rewards
- Dream → X Scenarios
- Dream → optional Narrator Bot
- Project → optional Manager Bot
- Scenario → X cast Characters
- Scenario → X Rewards
- Facet → fitting Dreams, Characters, Rewards, or Scenarios
- Character → signature Rewards
- Reward → optional Character owner pitch or Scenario-use pitch

Every child is its own Build Item with its own four gates and relationship diff.

## Existing infrastructure to reuse

The implementation should build on, not beside:

- current model single/batch APIs
- Character LLM generation endpoint
- Dream, Bot, Reward, and Scenario generation specs
- ArtImage and ArtCollection provenance
- ExpressionMedia and ExpressionTransition
- expression batch dry-run behavior
- existing image generation pipeline
- LTX image-to-video workflows
- `/api/comfy/hunyuan3d`
- existing generated-art file conventions and inspiration-folder promotion

An endpoint inventory is required before implementation because remembered route names are not a contract.

## Proposed orchestration records

Names may change after schema review, but boundaries should remain.

### ModelBuildRun

- user/owner
- source type, id, slug, and snapshot
- recipe key and version
- run status and current stage
- options and selected relationships
- estimated and actual usage
- timestamps and cancellation state

### ModelBuildItem

- run ID
- stable output key
- target model type
- action: CREATE, UPDATE, or ASSET_ONLY
- target ID/slug when known
- quantity/index
- pitch draft
- field draft
- relationship draft
- prompt bundle
- per-stage statuses and approvals
- stale reason and error state
- idempotency key

### ModelBuildArtifact

- item ID
- artifact kind
- source/prompt/workflow provenance
- provider/model/checkpoint/seed
- dimensions and format
- draft path/reference
- promoted path/reference
- review state

### ModelBuildRevision

- item/stage
- previous and next payload snapshots
- actor
- reason
- timestamp

These records orchestrate work. They do not replace Character, Bot, Dream, Reward, Scenario, Facet, Project, ArtImage, ArtCollection, or ExpressionMedia.

## Front-end architecture

The UI lives in Kind Robots and follows existing patterns:

- components render state and dispatch store actions
- `modelBuilderStore` owns API calls, run state, local resume hints, and optimistic updates
- server routes own provider credentials and generation calls
- no component calls API endpoints directly
- source adapters normalize display data
- model-specific writers own final payload validation

Primary screens:

1. source type and record picker
2. recipe/output selector with quantities
3. progress matrix
4. pitch/field/prompt editors
5. asset candidate review and promotion
6. final create/update/relationship diff
7. run history and resume

## Safety and ownership

- User-requested generations belong to the requesting user.
- System canon follows the existing generation ownership rules.
- Mature flags are preserved and explicitly reviewed.
- Credentials remain server-side.
- Usage is visible before and after expensive stages.
- Generated assets never imply permission to publish, deploy, print, fabricate, advertise, or spend.
- Existing canonical files are preserved in revision/inspiration storage before replacement.
- Commercial generation follows the licensing rules in `CONTROL.md`.

## Definition of done

Model Builder is proven when all three reference runs work through the same orchestration engine:

1. HSS Marketing Deck from a Project plus related Project
2. Character Deck for an existing Character or Bot
3. Dream expansion that creates and links exactly three Characters

Each run must demonstrate editable gates, selective reruns, persistence/resume, provenance, usage visibility, safe failure recovery, idempotent final commit, and no duplicate records or silent canonical replacement.
