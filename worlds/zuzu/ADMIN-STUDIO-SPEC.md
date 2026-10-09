# Zuzu Worldbuilding Studio: admin UX and implementation outline

**Status:** proposed experience/specification, not a deployed UI.
**Surface:** an admin tab ("Worlds" or "Zuzu World") under the existing Admin channel, with a dedicated route `/admin/worlds/zuzu`. No new top-level channel. Build as a world-scoped shell for future worlds, without creating a separate Conductor `Project` for each world.
**Related implementation:** [Kind Robots #3388](https://github.com/silasfelinus/kind_robots/issues/3388) (studio), [#3390](https://github.com/silasfelinus/kind_robots/issues/3390) (real resource reconciliation).
**Canonical sources:** [Zuzu world registry](README.md), [catalog](catalog.json), [full art ledger inventory](assets/), [resource submissions](resource-submissions.json). The latest Book One, Cast Picks, Video Guardrails and human-directed revisions supersede early generated seed lore.

## Product promise

A worldbuilder opens one art-first admin workspace, searches a character/scene/prop, sees all associated media and production usages, edits its live Kind Robots entity or starts a canon proposal, requests a variant/animation/replacement, and follows the resulting ArtJob/agent work through review without losing the provenance chain.

The interface is a **world CMS + asset finder + production request desk**, not an alternative ArtImage/Character/Reward/Scenario/Resource/Project database and not another Conductor task engine.

### Distinct users and jobs

- **Silas (admin/editor):** browse/filter/search, create/edit/associate/retire, inspect revisions, approve source-of-truth decisions, assign or suggest images to projects, request art/video changes, approve suggestions.
- **Conductor agents:** consume accepted world identity and asset references; propose entries/edits, supply ArtJobs and outputs with provenance; never declare their own invented game details canonical.
- **Other users:** no access to the admin studio, even for URLs or API endpoints. A future public world encyclopaedia would be a separate publication decision.

## Site map: six work areas, not fifteen top-level tabs

1. **Overview (home).** Hero world art, world description, canonical status, quick search, latest accepted cast, recent changes, outstanding reviews, recent media, production links, and queue health. Show counts *with source/date*, e.g. "657 recorded ArtImage outputs in 22 committed ledgers" is not "657 accessible gallery images."
2. **Library (all entities and assets).** Unified art-first grid/table with faceted *type* selector: Characters, Creatures, Factions, Locations, Props/Items/Rewards, Scenarios/Encounters, Story Beats/Scenes, Illustrations/Concept Art, Character Sheets/Expressions, ArtImages/ArtJobs, Animation Clips/Video/Audio, LoRAs/Checkpoints/Resources, and source documents. These are result types, **not individual navigation tabs**.
3. **World & Lore.** Reference bible: premise, world rules and themes, timeline/story arcs, locations/factions and character relationships; canon vs alternate continuities; authoritative source links. Human-accepted canon change goes through Conductor's source review, never an instant overwrite of a markdown bible when someone changes a field.
4. **Productions.** Filterable project cards for comic/Book One, Zuzu music videos #5 and #12 (different build histories), animated comic-film, Zuzu's Lair, Showdown, gamebook, Ghost Trail. Each opens a project-scoped view of its scenes, assets, variants, associated Resources, jobs, completion/provenance, and links to its existing editor/roadmap.
5. **Requests & Review.** Unified work inbox: propose a lore correction/new character, request image edit/variation/animation, generate missing poses, submit a scene to production, offer an asset to a project, review agent suggestions, compare candidates, accept/reject, and track job delivery. This is a thin UI over existing ArtJob and Conductor task-event workflows.
6. **History & Integrity.** Change log, accepted/rejected revisions, deleted/retired associations, source-commit provenance, stale links, missing image files/Resources, old-versus-new identity collisions, job failures, lineage graph, and restore/retry actions.

Keep **search, current world, project filter, status filter, add button, and pending count** persistent across work areas; the filter should maintain context when switching areas and navigating back.

## Desktop composition / sketch

```text
┌─ ADMIN / WORLDS / ZUZU ────────────────────── [ + Add ] [ Reviews 8 ] ┐
│ ZUZU WORLD [world dropdown]    [ Search anything...             🔎 ] │
│ Projects [All ▾]   Type [All ▾]   Canon [Any ▾]   Status [Any ▾]    │
├──────────────────────────────────────────────────────────────────────┤
│ Overview | Library | World & Lore | Productions | Requests | History│
├──────────────────────────────────────────────┬───────────────────────┤
│  art-first large results grid / story board  │ INSPECTOR (selection) │
│                                              │ image/video preview   │
│  [locked] Zuzu   [draft] Storm Crow          │ identity and canon    │
│  [locked] Sister [historical] early sheets   │ owner/source/rights   │
│  [accepted] Book One   [queued] scene art    │ linked jobs/projects  │
│                                              │ history + variants    │
│  gallery / grid / dense list view toggle     │ Edit | Use | Request  │
├──────────────────────────────────────────────┴───────────────────────┤
│ Source sync: Conductor commit ... | live DB checked at ... | Jobs ...│
└──────────────────────────────────────────────────────────────────────┘
```

The inspector is a **right-side panel on desktop**, a **full-screen detail view on phone**, and a **drawer/split panel on tablet**. Deep-link into `?type=character&id=...` (or named child routes) so jobs/agents/reviews can point at a specific item. Desktop keyboard navigation, escape-to-close, and screen-reader labels are required. Avoid duplicating the host workspace title/header.

## Universal filters and project semantics

- Search across titles, aliases, short summaries, resource triggers, source keys and real numeric IDs (`ArtImage`, `ArtJob`, `Resource`, project slug); full-text search must honor privacy. **Never leak hidden-twist terms via public labels, search suggestions, snippets, cache keys or client preload**.
- **Project:** All World (default); shared/unassigned; Comic/Book One; music video #5; music video #12; Comic Film; Lair; Showdown; Gamebook; Ghost Trail. Multiple project selection optional. **Project membership is many-to-many**: the same locked Zuzu pose can appear under multiple projects without copying it.
- **Media/type:** art still, character sheet, expression, concept, storyboard, gameplay sprite/stage, clip, final video, audio, LoRA, checkpoint, Character, Reward, Scenario, location, faction, document.
- **Canon:** canonical Book One; locked/approved visual identity; proposed; alternate/game-only; historical/superseded; legacy LLM filler (explicitly **not canon**). "Selected for one production" is separate from "world canon."
- **Workflow:** draft, needs review, approved, queued, rendering, failed, delivered/URL verified, archived; never convert `ArtJob: DONE` into "delivered image" without checking asset URL/visibility.
- **Use:** used in N projects, never used, orphaned, replaced, duplicate candidate; owner/source; recency, created/updated; private/mature flags; checkpoint/LoRA.
- Filters apply coherently to counts and result sets. Counts for static ledger references, live Resource records, video exports and derived static sprite files are disambiguated; no inflated "total ArtImages" from counting linked copies.

## Library cards and entity inspector

Every card has an actual art preview (with deliberate fallback for missing images), readable title/type, canon/selection state, last activity, production association(s), and one-click "Open". Hover actions on desktop must have accessible mobile equivalents.

The detail inspector sections:

- **Identity:** title, slug/aliases, kind/species, short editable description, long lore/backstory/traits, narrative role, personal/organizational relationships, canonical status/scope, and confidence/source citation.
- **Media board:** main/reference image; full image gallery of source sheets, orientations, expressions, scenes, video/animations, failures and rejected renders; separate pinned "approved" set from historical candidates. Fullscreen zoom, flip/mirror indicator (mirrored training angles are not new originals), side-by-side visual compare, image inspect/download only if permitted.
- **Usage:** where used, e.g. Comic Studio cast slot, #12 scene 13 clip, Showdown fighter art, Gamebook section; deep links to specific scenes, projects, job and Resource record. When changing a shared canonical image, show downstream impact; keep per-project overrides.
- **Generation:** reference image ID, ArtJob ID, engine/checkpoint, LoRA Resource IDs/triggers, prompt/negative/seed, dimensions, source image and parent-child revision chain, result URL status, content classification. Keep secrets/sensitive prompts out of open metadata.
- **History:** original LLM filler vs human-approved revision, author/agent, change reason, date, Git commit or API row version, accepted/retired state, rollback where reversible.
- **Actions:** Edit entry; Add link to project; Suggest/use in scene; Make variation; Inpaint/edit; Outpaint/reframe; Animate; Generate missing angles/expressions; Compare/promote; Replace project reference; Archive/unlink; Open original resource/editor. Show only actions actually supported by the object's type and permissions.

Editing a real `Character`/`Scenario`/`Reward`/`Resource` uses its existing authenticated CRUD endpoint; don't maintain shadow copies of the object's prose. World-level associations/notes/selection history may need **minimal typed curation records** (not new parallel model tables). Edits to canon-bearing Conductor source files are **proposed patches/PRs**, reviewed and reflected back after merge. A world entry can also be draft/local-to-project without becoming canonical.

## Add / edit entry flow

A single **+ Add** action opens a searchable type palette, "From existing Kind Robots record", "New world concept", "From image/ArtJob", and "Import from proposal". Prefill source/project. For a new character, ask for identity, species, role, personality, appearance, cast references, canon scope, and optionally link existing images/LoRA/training sheet. For a location, offer description, time period, factions, key scenes, geography and environment references. For a prop/Reward, connect keeper, canonical appearances and suitable render refs.

Before Create, **match by slug, owner, aliases and existing model IDs**; suggest reuse/update to prevent duplicate Coyote/Sister/Abbess records. Preserve owner and existing image/relationship data on patches. Draft autosave is separate from explicit **Save to Kind Robots** or **Propose canon change**. Make a small inline "edited fields / old → new" diff with revert; don't silently mass-write the registry.

**Remove** is three different choices:
1. **Unlink from this world/project**: removes the association without deleting the source image/record.
2. **Archive/retire this entry**: hides it from active views, with reason and undo/restore; keeps provenance.
3. **Delete underlying object**: gated by ownership, dependency warnings and a second explicit confirmation; never cascade-delete referenced art or irreversible production data through a world-level button. Admin authorization alone does not imply human approval for destructive irreversible changes.

## Art, animation and production-request composer

A main action on any image: **Request change**. Pre-populate its source image, current world, active project and (if selected) target scene/character. Present:

- **Intent**: new variation, inpaint/masked correction, outpaint/reframe, pose/angle/expression, background replacement, cleanup, animate (LTX/WAN), regenerate as new image, set as candidate for a particular role, or ask an agent for a creative suggestion.
- **Request body**: natural-language direction, reference media, optional mask/region, target usage/scene, aspect, engine/lane/checkpoint, LoRAs, budget/priority (respect live caps), whether exact source must be preserved, expected final file type, visibility and maturity.
- **Example grounded request:** "Take locked sister pose, put her in the mission scene, preserve clothing and proportions, create s13 end frame with the dropped dagger, use this result only for Music Video #12." Support reference-image plus scene last-frame continuity; never mutate the locked original.
- **Output strategy**: create new derived asset with parent ArtImage, attach provenance/ArtJob, offer to target project for review. Changing a shared canonical image/asset is a **separate explicit promote decision**; never overwrite every consuming project merely because a new render exists.
- **Submit**: distinguish `Enqueue ArtJob` (uses existing queue/relay), `Send agent request` (Conductor task event/proposal), `Attach existing asset to a job`, and `Save draft`. Preview dependencies/cost; no automatic spending or publication.
- **Track**: status transitions `draft → submitted → queued → running → rendered → delivered/URL verified → awaiting review → accepted / rejected / needs revision`, plus failure/retry using original ArtJob where appropriate. Track a clip's actual keyframes and repaired/local-substitution caveats.

For a **"suggest for job"** action, show the precise target: pending scene, asset slot, desired character, aspect, style, task/ArtJob reference, current candidate, and match confidence. Offer `Add as candidate`, `Use for this one scene` and `Propose replace reference`, each with distinct effects. Never silently overwrite the approved image across productions.

## Requests & review inbox

Display cards for **incoming agent proposals and Silas requests** with: type, target, affected project(s), current baseline, candidate diff or before/after comparison, provenance, owner, current workflow stage, and explicit `Approve`/`Reject`/`Request changes`/`Assign` actions. Group by "Needs my decision", "Rendering", "Waiting on agent", "Ready to use", "Failed", "Archived". Approval changes a candidate's acceptance/association only; publishing to a public page remains separately gated.

Every request or agent suggestion must refer to *existing source IDs* when available. An unverified image or model is marked "missing/unverified", not offered as finished. Make reviews idempotent and audit who accepted which revision. Different projects can accept different derived assets without changing the shared canonical identity.

## World & Lore: knowledge that production can actually use

Editable sections must include: world pitch/tone, canon policy, character cast and relationships, factions, places/regions, props/signature objects, book/episode arcs, chronological beats, themes/style bible, art constraints and reference frames, and unanswered story questions. Structured links between entries make this a world index, not just a wiki.

Use an **evidence + continuity** overlay:
- Book One canonical story and current locked cast/visual rules = authoritative.
- Gamebook branches, Showdown matchups, Lair deaths, arcade action = project-specific alternatives.
- Earlier LLM-generated Dream/Character/Scenario/Reward filler = legacy only, editable/remappable but not canon.
- Historical concepts and rejected character sheets = still discoverable for provenance/idea mining.
- Pending suggestions = not accepted canon.

A small **timeline/relationships view** is an optional second-phase visualization; v1 must at least show typed crosslinks and chronology without duplicating story documents. Canon edits require a provenance-backed change request to the actual Conductor file. Keep confidential plot details confined to authenticated protected source content, not public search, descriptions or client bundles.

## Productions: project filter is a full workflow, not a tag

Entering a production applies its scoped view across **all sections** while preserving global world assets as reusable candidates. Production panel shows: pitch, continuity scope, owners, source project/Conductor slug, app route, story/scene board, asset usage map, pending revisions, rendered outputs, and status. Link back to the proper existing editor and GitHub roadmap. No duplicate media editor for Music Video, Comic Studio, animation manager or Showdown in the World Studio.

A project can **subscribe** to approved world references (e.g. a named "Zuzu front angle" selection) and explicitly pin a version for reproducible builds. Warnings show when a world reference is superseded, but the project keeps its pinned version until its owner approves an update.

## Source of truth / security / data boundaries

- **Conductor** owns canonical world markdown/catalogues, character/cast decision provenance, coordination, task states and approval history; an admin lore proposal becomes a PR/task event and is authoritative only once merged. The ConductorProjection database is **read-only coordination cache**.
- **Kind Robots** owns Characters, Rewards, Scenarios, Resources, Dreams, ArtImages, ArtJobs, MusicVideo documents, production app state, Project presentation and rendered URLs. Use existing APIs and authentication. Use `Project.conductorSlug` as join; don't invent another cross-repo project identifier.
- Add the smallest new persistent relation tables/typed overlay necessary for world membership, asset usages, canon status/selection, and review records. Keep underlying entities and binary media in their existing owners. World IDs/entry IDs should be stable, versioned and source-resolvable.
- Enforce admin/ownership/maturity/private access **at the server API**, not simply by hiding tabs or relying on client-side filtering. Avoid retrieving all private ArtImages and filtering in-browser. Age/maturity permissions still apply to an admin account as required by existing access rules.
- Supply committed Conductor snapshot SHA, live DB observation time, and delivery verification timestamp independently in the interface. Offline/static fallback visibly differs from live data.
- Every mutation has actor, time, entity ID, previous value or commit, reason and resulting reference. Optimistic concurrency; report conflicts and avoid overwriting independent project edits.
- Read-only interactions and proposed/queued actions are distinct from actual mutations. Soft deletion default. Do not publish externally or incur unapproved costs.

## Responsiveness and UX quality

- Desktop: 2–3-column gallery plus sticky contextual inspector. Keyboard search and arrow-through-cards; multi-select only for *safe non-destructive association/tag actions*.
- Tablet: two-column grid with overlay inspector and sticky action footer.
- Phone: single-column media list, collapsible filter sheet and full-screen item detail with single bottom action menu. Project scope is visible at all times.
- Image-first: meaningful aspect ratios, skeleton states, zoom, side-by-side comparison; no tiny unreadable media buttons.
- Performance: paginate / virtualize hundreds of image records, dedupe source IDs from multiple ledger/project memberships, lazy-load previews/video posters, debounce search, cancel stale requests.
- Empty/errors: explicit "No matching records", "Source reference has no reachable image", "No verified Resource for this LoRA yet", stale Conductor snapshot, queue failure; make recovery actions available.

## Phased implementation and acceptance

### Phase 1: genuinely useful index (not a static six-image mockup)
- Admin tab and `/admin/worlds/zuzu`, overview, project filter, unified Library, detail inspector, type/canon/status filters, seven production links; source provenance.
- Read all 657 ledger-recorded image output refs across 22 ledgers **without asserting that every URL is live**; index project #5/#12 animation builds, derived Git media and five character-sheet LoRA datasets; distinguish locked, rejected, historical, missing.
- Deep link each item to existing editor/ArtJob/Resource route where possible. Preserve private/mature boundaries; test at phone/tablet/desktop.
- Verify results with live DB authoritative IDs (including pending #3390 reconciliation), show "not synced" states for missing rows.

### Phase 2: editing and curation
- Add from existing, create, edit, project associations, merge duplicate identities (non-destructive), compare/promote, archive/restore, undo, audit log; server-authorized controls.
- Prepare/view nine Character, five Reward, five Scenario submissions; reconcile legacy filler safely instead of copying guesses into new rows. Distinct "Edit live entity" vs "Propose world canon patch."

### Phase 3: creation and requests
- "Request image change" from media board, "Use for this production slot", submit AI agent proposals and ArtJobs, track output with delivery checks, compare/select, review and pinned-version consumer updating.
- Reuse existing production editors/queues; verify no duplicates or unauthorized publish/spend.

### Phase 4: world intelligence
- Timeline and relationship map, style/rule consistency checks, missing pose/scene planner, stale project references, prompt-compatibility preflight, recurring agent content suggestions. None should silently rewrite canon.

**Definition of done for Studio MVP:** Silas can filter to Video #12, find the repaired s13 clip and its original/derived source lineage, inspect all approved fennec sister angles and expression datasets, see that Storm Crow belongs to Showdown continuity, open an existing Character editor and propose a resource correction, attach an existing image as a candidate for a Gamebook scene, and submit/track a new image-edit request without changing the shared canonical source. Every action is permissioned and its state is visibly honest. Publishing, permanent deletion and canon promotion remain explicit gates.
