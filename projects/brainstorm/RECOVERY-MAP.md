# Brainstorm Recovery Map

date: 2026-08-10
project: brainstorm
task: t-002
session: 2026-08-10T084900Z-brainstorm-t-002-b7f2
status: archaeology-complete

## Executive conclusion

The Brainstorm product was not merely a 2023-2024 experiment that later disappeared. It had a
second, substantially more mature life in spring 2026 and was still mounted as the public
`/brainstorm` experience in June 2026.

The best last coherent behavioral snapshot is the standalone
`components/brainstorm/brainstorm-manager.vue` present immediately before the June 15 Pitch
model migration, with commit `5e6f81188fd1e07d3a6d45092a93d4c61db00b19` as a useful stable
reference point. That manager already embodied most of the interaction Silas remembers:
request a deliberate number of ideas, inspect candidates individually, keep or reject them,
give rejection feedback, resubmit the rejected set, edit accepted material, and save/reuse
survivors.

The exact public-surface regression is also identifiable. On June 15, 2026, a three-commit
Pitch-removal sequence deliberately migrated the old Pitch domain into Dream. During that
migration the dedicated Brainstorm components were removed, and commit
`e9e4928ca2665c746c1d548ce28acd7090c77af5` changed `content/brainstorm.md` from the
Brainstorm dashboard / `pitchCards` / `:brainstorm-manager` to the Dreams dashboard /
`dreamCards` / `:dream-manager`. The commit itself says it had "Finished removing pitch and
migrating to dream" and expected follow-up bug testing. The present Dream-gallery substitution
is therefore not the original Brainstorm design. It is a migration scar.

**Restoration rule:** recover Brainstorm's interaction contract, useful product identity, and
human/AI curation loop. Do not resurrect the deleted Pitch schema, old provider assumptions,
old prompt hacks, or historical generations. Historical generation output is an anti-benchmark
and should be embarrassed by the revived service, per `DESIGN-BRIEF.md`.

## Timeline

### 2023-2024: original product lineage

Repository history contains a long first-generation Brainstorm lineage, including:

- `19b37e0` (2023-09-25), `brainstorming page`;
- the August 2024 PitchType/remodel sequence (`0041e10`, `7ba1a20`, `d8cc25b`);
- the September 2024 SPA/Pitch-store sequence (`21af63c`, `ac57ba0`, `06251f6`,
  `a37569d`, `6633ff5`, `d50f86b`, `694d127`, `3e54006`);
- November 2024 view/selector/API work (`4434253`, `ef0779c`, `e6f39ed`, `4318321`,
  `508ed6c`).

A representative November 2024 `brainstorm-view.vue` composed a Brainstorm image,
Brainstorm selector, `add-pitch`, and a grid of newly generated Pitch cards. The selector let
users switch Pitch types and choose an existing Pitch. This establishes the early
pitch -> generate -> inspect/save family of behavior, but it is not the best code snapshot to
port now.

### April 25-28, 2026: Brainstorm rebuilt as a dedicated manager

Commit `8082dd8` (`brainstorm manager and footer`) introduced a consolidated
`brainstorm-manager.vue`; its own comments described it as synthesizing earlier Brainstorm
game/view/manager iterations. Commit `b82fc6e` continued that manager work.

By this point Brainstorm was much closer to a creative workbench than a gallery. It had a
single editable premise, examples, result-count controls, candidate state, rejection feedback,
resubmission, Prompt-store handoff, art hooks, and human/AI/hybrid provenance.

This 2026 branch of the lineage is more relevant to restoration than simply checking out a
November 2024 component.

### May-June 2026: the public route still mounted Brainstorm

The public content route continued to mount `:brainstorm-manager` through May and into June.
Examples include refs around May 17 and May 28, plus June 1, June 2, June 6, and June 9.
Navigation/frontmatter changed as the broader dashboard system evolved, but the product mount
itself remained Brainstorm.

By June 6-9, `content/brainstorm.md` used a dedicated Brainstorm dashboard with `pitchCards`
and mounted `:brainstorm-manager`.

### June 15, 2026: exact replacement point

The regression happened as part of a deliberate Pitch-to-Dream domain migration, not because
someone consciously redesigned Brainstorm into a Dream gallery.

1. `dba7711` — `removed pitches`
2. `34c7386` — `removing pitches. part 1 of a few`
   - removes `components/brainstorm/brainstorm-manager.vue` and other Pitch/Brainstorm UI.
3. `e9e4928` — `Finished removing pitch and migrating to dream. Phew! This will almost
   certainly fail to build, still need to bug test`
   - changes `content/brainstorm.md` from:
     - `dashboardKey: brainstorm`
     - `dashboardTab: overview`
     - `cards: pitchCards`
     - `:brainstorm-manager`
   - to:
     - `dashboardKey: dreams`
     - `dashboardTab: brainstorm`
     - `cards: dreamCards`
     - `:dream-manager`

That substitution survived into the current site.

### Later Dream Brainstorm work is a different feature

`components/dreams/dream-brainstorm.vue` later became a Dream-specific source/ideas interface
and was migrated to the current `kr-panes` layout primitive in August 2026. It is useful
adjacent work, especially for future Dream-aware Brainstorm context, but it is not the general
Brainstorm product. Recent repository history explicitly describes Dream Brainstorm as tabled
pending a rebuild.

Likewise, legacy `DreamType.BRAINSTORM` / random-list semantics are a separate historical use
of the word "brainstorm". They must not define the revived product's storage contract by
accident.

## Last coherent product behavior worth recovering

The June 9-era standalone manager provides the strongest behavioral donor. Preserve the ideas,
not the implementation verbatim.

### Premise and context

- editable title / premise identity;
- a core pitch/request;
- optional generator instructions;
- editable examples/sample lines;
- explicit requested result count;
- creation-source provenance (`HUMAN`, `AI`, `HYBRID`, etc.).

The revived product should simplify the default composer compared with this old form. Title,
PitchType, max tokens, temperature, public/mature toggles, and provider-oriented settings are
not all appropriate as first-class default controls. What matters is that a human can state a
premise, ask for a chosen number of ideas, and add constraints or examples when useful.

### Candidate curation

The old manager already modeled candidates individually:

```ts
type CandidateStatus = 'pending' | 'accepted' | 'rejected'

type BrainstormCandidate = {
  id: string
  text: string
  status: CandidateStatus
  feedback: string
}
```

Useful behaviors to preserve and improve:

- stable identity per candidate;
- Keep / Reject on one candidate without affecting the rest;
- accept/reject pending candidates in bulk;
- freeform rejection feedback;
- resubmit rejected material for replacements;
- accepted generated lines become editable human material rather than a frozen model answer;
- a candidate can be handed to another prompt workflow;
- editing AI material changes provenance toward hybrid/human work.

Modern Brainstorm should extend this with inline editing, replacement of one slot,
non-destructive revision lineage, branching / "more like this", and stronger batch-level
semantic diversity.

### Persistence and handoff

The old manager saved a durable Pitch and could reopen/edit Pitch material. That persistence
semantics disappeared because the Pitch model itself was intentionally removed.

The product requirement survives even though the old table does not: a user should eventually
be able to save/reopen a Brainstorm session and selected candidates. The current data model
must be audited before choosing where that state belongs.

### Personality

The historical page identity remains useful evidence: Brainstorm as an eccentric brain-in-a-
jar host, with a taste for absurd and darker comedy. The persona may inform the revived surface
and system guidance, but should not become a hard dependency on one bot record.

## What must NOT be restored

### 1. The deleted Pitch schema as product architecture

The old manager was deeply coupled to `Pitch`, `PitchType`, `usePitchStore()`, Pitch CRUD, and
Pitch relationships. That domain was intentionally removed/migrated in June 2026. Recreating it
just to make an old component compile would reverse a later architectural decision without
justification.

Brainstorm needs its own modern session/candidate semantics or a genuinely compatible existing
model discovered by the current-state audit.

### 2. Historical generations or examples as positive quality targets

Silas consistently disliked the old generated responses. Old prompts, examples, saved
responses, and provider workarounds are archaeological evidence and negative fixtures only.
They must never become positive few-shot examples or acceptance criteria.

The revived generator should materially beat them on relevance, conceptual diversity,
specificity, surprise, constraint-following, editability, and actual comic/creative premise.
"Safe" must not be implemented as "bland".

### 3. Prose-line parsing as the data contract

The old manager tried to recover candidates by splitting text responses, stripping bullets,
removing conversational preambles, unwrapping object-like output, and otherwise guessing what
the model meant. Those parsing hacks are evidence of an obsolete provider contract.

The modern endpoint should request and validate structured candidate output, with stable IDs
owned by the application. Structured transport must not force formulaic content.

### 4. Provider knobs as the default creative UX

The old sidebar exposed `maxTokens` and `temperature`. These were reasonable debugging tools in
an earlier LLM era, but users should now primarily control creative intent in human language:
result count, constraints, stranger/more practical, another angle, shorter, darker/funnier
where allowed, etc. Provider parameters can stay internal or advanced-only if still useful.

### 5. Old direct image-generation behavior

The old manager's image-generation path predates the current durable ArtJob infrastructure.
Do not restore it. Brainstorm art remains phase two and selected candidates must eventually use
the normal ArtJob enqueue/delivery pipeline with current Krea2 defaults.

### 6. A visible server-control panel as required product chrome

Older managers exposed server selection/management as part of Brainstorm. Current Kind Robots
has centralized server/provider configuration. Brainstorm should use the active/default text
service unless the current architecture provides a compelling, user-facing reason for an
advanced selector.

### 7. Public/mature controls copied mechanically from the old Pitch form

Maturity/privacy rules should come from current Kind Robots conventions and the semantics of a
saved Brainstorm session. Do not duplicate stale toggles merely because the old Pitch record had
them.

## Historical file -> modern interpretation map

| Historical evidence | Historical role | Current state / likely equivalent | Restoration decision |
| --- | --- | --- | --- |
| `components/content/prompts/brainstorm-view.vue` (2024) | Compose image + selector + add-pitch + generated Pitch cards | Deleted/obsolete component family | Behavioral evidence only |
| `components/content/prompts/brainstorm-selector.vue` (2024) | Select/filter Pitch types and current Pitch | Deleted Pitch UI | Do not port; modern saved-session browser can recover the useful intent later |
| `components/content/prompts/brainstorm-image.vue` (2024) | Brainstorm visual/persona | Historical assets/persona may still survive | Audit/reuse identity, not layout |
| `components/prompts/brainstorm-manager.vue` (Apr 2026) | Consolidated Brainstorm workbench | Superseded by later `components/brainstorm/brainstorm-manager.vue` | Useful intermediate archaeology |
| `components/brainstorm/brainstorm-manager.vue` (Jun 2026) | Best standalone premise -> candidates -> curate/save workbench | Deleted June 15 | Primary behavioral donor; do not blindly checkout |
| `content/brainstorm.md` | Public `/brainstorm` mount and presentation | Still exists but mounts `:dream-manager` | Restore to a dedicated Brainstorm implementation |
| `stores/pitchStore.ts` + Prisma `Pitch` | CRUD + generation settings + selected premise | Pitch domain intentionally removed | Do not resurrect solely for Brainstorm |
| `/api/botcafe/brainstorm` historical endpoint | LLM generation path | Path appears to survive and needs current audit | Reuse only if it fits current provider/auth/error contracts |
| `stores/promptStore.ts` | Prompt fragments / candidate handoff | Current store appears to survive; audit semantics | Possible reusable handoff, not Brainstorm persistence by assumption |
| direct historical art call | Generate a vibe image from Pitch artPrompt | Current durable ArtJobs | Replace later with explicit ArtJob flow |
| `components/dreams/dream-brainstorm.vue` | Dream-specific ideation/source UI | Current adjacent feature | Future Dream source adapter/consumer, not canonical `/brainstorm` |

## Old data-model assumptions to retire or revalidate

The historical manager assumed all of these; none should cross into the new implementation
without current evidence:

- a durable `Pitch` record is the root object;
- `PitchType` controls general Brainstorm behavior;
- accepted generated lines belong in the Pitch's `examples` field;
- title has special generator semantics;
- one selected Pitch is global store state;
- generation returns prose that can be split safely into lines;
- user-facing temperature/max-token controls are useful product concepts;
- generated art can be requested directly from the manager;
- Brainstorm persistence and broader site idea taxonomy are the same problem.

## Provider/API assumptions to retire or revalidate

Historical code reflects the capabilities and failure modes of earlier models:

- conversational wrappers around supposedly list-shaped output;
- brittle line splitting and regex cleanup;
- model-specific token/temperature controls;
- generation driven through `pitchStore` rather than a dedicated typed contract;
- rejection feedback concatenated into generator prose;
- no application-owned structured candidate schema.

The current-state audit must identify the site's present text-server/provider abstraction,
auth/mana requirements, error-response conventions, and best structured-output pattern. The
creative prompt should be designed for current models, not translated from the old endpoint.

## Smallest safe restoration slice

After t-003 completes the current-state audit, the first code restoration should be deliberately
smaller than the June 2026 manager while preserving its essential loop.

### Include

- `/brainstorm` renders a dedicated Brainstorm surface again;
- `/plan/brainstorm` resolves to the same implementation, not a fork;
- freeform premise/request composer;
- requested result count with sensible bounds;
- optional compact constraints/examples field;
- explicit Generate action through a typed store/API contract;
- independently identified candidate cards;
- Keep, inline Edit, Reject, and regenerate/replace one candidate;
- visible batch error/loading/empty states;
- responsive layout using current Kind Robots primitives;
- no dependence on the deleted Pitch model;
- anti-benchmark quality instructions appropriate to current model capability.

### Deliberately defer from the first slice

- schema migration / durable sessions until existing models are audited;
- generated art;
- entity-aware Character/Dream context;
- advanced branch/revision-history UI beyond what is necessary for safe non-destructive
  candidate replacement;
- Conductor proposal integration;
- provider/model cockpit controls;
- public publishing or social handoff.

The point of the first slice is to make Brainstorm unmistakably Brainstorm again and prove the
modern text-generation + curation loop before attaching every future capability.

## Current-state questions handed to t-003

These are repository questions, not human gates. Resolve them from current Kind Robots code:

1. What is the current canonical text-generation/provider abstraction, including structured
   output, auth, mana, and error handling?
2. Does `/api/botcafe/brainstorm` still fit that abstraction, or should it be replaced behind a
   dedicated Brainstorm endpoint?
3. What current store/model, if any, genuinely fits saved Brainstorm sessions and candidates?
   Confirm that Pitch is gone rather than recreating it.
4. Which pieces of `promptStore` remain appropriate for explicit candidate handoff?
5. What is the canonical current route/alias pattern for `/brainstorm` and
   `/plan/brainstorm`?
6. How should the general Brainstorm workbench coexist with `DreamType.BRAINSTORM`, legacy
   random-list semantics, and `components/dreams/dream-brainstorm.vue` without semantic
   collision?
7. Which current privacy/maturity conventions apply to ephemeral and saved brainstorming?
8. Which current shared layout primitives should shape the candidate workspace at phone,
   tablet, and desktop widths?

## Recovery verdict

Brainstorm is unusually recoverable because the repository contains both the original lineage
and a modernized 2026 iteration. The mistake would be to interpret "restore" as "recreate the
old database model" or "make the old answers again."

Restore the loop. Restore the strange little brain. Restore the human ability to keep, reject,
edit, redirect, and weaponize a good idea against a blank page.

Then make the old generations look embarrassing.

---

## Current architecture audit — 2026-08-10

task: t-003
session: 2026-08-10T091100Z-brainstorm-t-003-c4a1

The current repository has enough surviving infrastructure to rebuild Brainstorm cleanly
without reviving the Pitch model or creating a private AI stack. The most important finding is
that the current system already contains each major infrastructure primitive Brainstorm needs,
but they are split across the Dream workaround, generic Suggest service, server store, content
router, and Prompt/object-context utilities.

The implementation should compose those primitives behind a Brainstorm-owned store and API
contract rather than making Dreams continue to impersonate the product.

### Route and presentation map

#### `content/brainstorm.md`

Current canonical public content document for `/brainstorm`.

Useful current presentation metadata should survive the restoration:

- `channelKey: plan`
- `tabKey: brainstorm`
- `dashboardKey: brainstorm`
- current Brainstorm title/subtitle/persona copy;
- Stage 3 mobile/tablet/desktop backdrop routes.

The remaining migration scar is structural:

- `cards: dreamCards`
- body mounts `:dream-manager`

**Decision for t-004:** keep the current page metadata/backdrops and replace the Dream-specific
mount with the new dedicated Brainstorm manager. Brainstorm does not need a gallery card source
for the first restoration slice, so `cards: dreamCards` should be removed unless the current
content-host contract proves it is required for unrelated chrome.

#### `content/channels/plan/brainstorm.md`

This tab document is already aligned with the intended product. It routes to `/brainstorm` and
describes the correct loop: turn a pitch into useful creative riffs, keep promising ideas, and
save reusable seeds. Treat this as presentation truth, not the Dream-specific dashboard text.

#### `stores/helpers/dashboardHelper.ts`

The `brainstorm` dashboard is partly correct but its primary tab still says `Dream Brainstorm`
and routes to `/dreams`. Its narrative also says survivors become Dream seeds.

**Decision for t-004:** primary Brainstorm tab routes to `/brainstorm` and uses general
Brainstorm language. The existing Prompts tab may remain as an adjacent handoff/browser.

#### `utils/projectPlacements.ts`

Already maps conductor slug `brainstorm` to:

- channel `plan`
- tab `brainstorm`
- route `/brainstorm`

No placement change is needed.

#### `/plan/brainstorm` alias

There is no current `content/plan/brainstorm.md` and no repository reference to the literal
`/plan/brainstorm` route. The catch-all `pages/[...slug].vue` already implements a same-origin,
SSR-aware `redirect:` frontmatter contract and re-applies it during client navigation.

**Decision for t-004:** add a tiny content redirect document at `content/plan/brainstorm.md`
with `redirect: /brainstorm`, rather than duplicating the Brainstorm implementation. Direct
load and client navigation then share the existing redirect machinery.

### Current generation path

#### `server/api/botcafe/brainstorm.ts`

The surviving endpoint is more modern than the old UI around it:

- uses the OpenAI Responses API;
- requests strict JSON-schema output;
- requires exactly the requested number of `{ title, pitch }` ideas;
- normalizes/validates returned idea objects;
- uses `manaGate()` and `estimateTextCostUsd()`;
- returns the site's `{ success, message, data, mana }` shape.

Those are useful implementation donors.

However, it is not the right canonical endpoint for the revived general product because it:

- is hard-coded to `OPENAI_API_KEY` and direct OpenAI fetches;
- defaults to `OPENAI_TEXT_MODEL` / `gpt-4o-mini` instead of the user's active text server;
- explicitly asks for **Dream** brainstorm ideas;
- accepts old provider knobs and compatibility aliases;
- includes canned positive examples (`Haunted Fitness Tracker`, `Reverse Life Insurance`,
  `Misfortune Cookies`) that would anchor the revived creative voice to exactly the kind of
  old-output baseline the project is meant to beat.

**Decision for t-006:** use the endpoint's strict structured-output shape and mana accounting as
organ donors, but replace/refactor it behind a dedicated Brainstorm generation contract. Do not
make the revived workbench depend on `/api/botcafe/brainstorm` as a Dream-specific public
contract.

### Current provider abstraction

#### `server/utils/suggest/suggestProviders.ts`

This is the best current provider-selection donor. It already derives and calls:

- Anthropic;
- OpenAI;
- OpenAI-compatible custom servers;
- Ollama.

It resolves a model from the selected server and knows the different provider endpoints. Its
current return type is plain text, so it is not by itself sufficient for Brainstorm's strict
candidate contract.

#### `server/api/suggest.post.ts`

This route shows the modern server-side pattern Brainstorm should follow:

- derive provider/model from the supplied server snapshot;
- use `manaGate()` with the selected server id;
- estimate generation cost from the same completion budget;
- resolve private object context server-side when required;
- call provider through shared utility code;
- return success/data/mana consistently.

**Decision for t-006:** either extract/generalize the provider-call utility so Brainstorm can
request structured candidate data per provider, or add a Brainstorm-specific provider layer
that uses the same provider/server derivation. Avoid a second, unrelated provider registry.

For OpenAI, native strict JSON schema is already proven in the current Brainstorm endpoint. For
providers without equivalent native schema guarantees, normalize and validate a minimal
`{ ideas: [...] }` envelope server-side. Parsing tolerance belongs at this provider boundary,
not in Vue components or the Pinia store.

### Active text-server selection

#### `stores/serverStore.ts`

The store already defines text-compatible servers and exposes `activeTextServer` with this
fallback order:

1. explicit active text server id;
2. user's preferred text server;
3. default text server;
4. official text server;
5. first available text server.

It supports OpenAI, Anthropic, Ollama, Custom, and text/chat-category servers. The store also
owns its browser persistence, matching Kind Robots' component/store boundary.

**Decision for t-005/t-006:** Brainstorm uses `activeTextServer` by default and passes only the
safe server snapshot fields required by the generation endpoint. Do not restore the old visible
server-management panel. An advanced server choice can be considered later if it provides
actual creative value.

### Authentication and mana

#### `server/utils/manaGate.ts`

`manaGate()` calls `requireApiUser()`. Therefore current paid/free generation semantics require
an authenticated API user. It also correctly supports free generation for admin/server-key,
FAMILY role, user-owned resources, and public non-official servers, while charging normal
hosted generation atomically through the mana ledger.

**Decision:** do not punch a Brainstorm-specific hole through the economy/auth boundary.
Anonymous visitors may eventually use an ephemeral composer or inspect sample/local state, but
model generation must obey the current authenticated mana contract unless a separate product
policy explicitly changes it.

The store/UI must surface 401/402 and provider failures as normal Brainstorm states rather than
silently failing or inventing fake candidates.

### Current Dream workaround and semantic collisions

#### `stores/helpers/dreamHelper.ts`

`DreamType.BRAINSTORM` is not a clean Brainstorm-session model. The migration compatibility map
folds legacy `RANDOMLIST` and `TITLE` values into `BRAINSTORM`, and the helper still includes
pipe-delimited `buildBrainstormPrompt`, `buildTitleStormPrompt`, `extractExamples`, and
normalization utilities from that era.

This is legacy Dream taxonomy, not evidence that a general creative-ideation session belongs in
a Dream row.

#### `stores/dreamStore.ts`

The store still carries migrated Pitch-era Brainstorm state in localStorage:

- `numberOfRequests`;
- `temperature`;
- `maxTokens`;
- `exampleString`;
- `apiResponse`;
- legacy Pitch storage hydration.

`fetchBrainstormDreams()` builds a delimiter-era Dream prompt, calls
`/api/botcafe/brainstorm`, then normalizes the structured endpoint result back into a string.
This throws away structure only for the component to reconstruct it later.

#### `components/dreams/dream-brainstorm.vue`

This is a useful UX donor, not the canonical product. It contains candidate cards, acceptance,
rejection feedback, examples, resubmission, source-Dream selection, and current `kr-panes`
layout. But it is Dream-specific and currently:

- parses returned text with regex/delimiters into candidates;
- exposes max tokens and temperature;
- couples generation to `dreamStore`;
- saves lists as `DreamType.BRAINSTORM`;
- saves accepted candidates directly as Dreams;
- offers Dream-specific source/update actions.

**Decision:** preserve its good interaction ideas and responsive primitives. Do not make the
general `/brainstorm` surface a wrapper around this component. Later, Dream Brainstorm should
become a source-object entry point/consumer of the general Brainstorm workbench.

### Brainstorm store boundary

There is no current `useBrainstormStore` / `brainstormStore` in the repository.

**Decision for t-005:** create `stores/brainstormStore.ts` as the owner of:

- current premise/request;
- result count;
- user-facing constraints/examples;
- source-object reference metadata;
- generation/loading/error state;
- candidate collection and stable application-owned ids;
- keep/reject/edit state;
- single-candidate regeneration/branch requests;
- session-local revision history;
- browser persistence for ephemeral work, if retained.

Components may bind to/refine store state, but they do not call `/api/brainstorm/*` or
`localStorage` directly.

Do not move Dream gallery/query state, Prompt gallery state, or server management into the
Brainstorm store.

### Persistence model audit

No audited current model is a clean substitute for the deleted Pitch root.

#### `Prompt`

The Prisma model describes a Prompt as an art or text prompt to an AI that generates new media.
`promptStore` provides mature CRUD, ownership/visibility behavior, creation-source provenance,
and browser caching.

**Use it for:** an explicit handoff such as “save this selected candidate as a Prompt” or later
art-prompt workflows.

**Do not use it for:** a Brainstorm session with premise, multiple candidates, rejection state,
revision lineage, and branch relationships. Encoding that graph into Prompt rows would overload
a model with different semantics.

#### `PitchSheet`

`PitchSheet` still exists, but it is a presentation/story pitch-sheet model tied to Dream or
Project with hook/highlight/detail/layout fields. It is unrelated to the deleted general
Brainstorm Pitch semantics.

**Decision:** do not commandeer `PitchSheet` for Brainstorm persistence.

#### `Dream`

Dream remains a valid **handoff/source** object and future Brainstorm adapter, but the
`DreamType.BRAINSTORM` compatibility taxonomy should not become the new session root.

#### Conductor pitches

Conductor pitch files remain coordination proposals and are out of bounds for ordinary user
Brainstorm persistence.

**Recommendation handed to t-010:** unless another genuinely generic draft/session model is
found during persistence implementation, prefer a small additive `BrainstormSession` /
`BrainstormCandidate` schema over semantic overloading. t-010 owns the final migration/design
decision; the text-first restoration does not need to block on it.

### Prompt handoff

`stores/promptStore.ts` remains a good explicit destination for selected candidate text. It
already tracks `CreationSource` including `HUMAN`, `AI`, and `HYBRID` and owns Prompt CRUD.

The Brainstorm store should not mutate Prompt state automatically during generation. Handoff is
an explicit user action after curation, so AI output stays draft material until the human
chooses what it becomes.

### Source-object context

`server/utils/suggest/artModelContext.ts` already demonstrates a strong reusable security and
serialization pattern:

- normalize a typed `entityRef`;
- resolve by id/slug server-side;
- enforce `isPublic || userId === viewer.userId` unless admin;
- expose only selected scalar fields;
- compact long strings;
- support Project, Bot, Character, Dream, Scenario, Reward, and Facet.

**Decision for t-012:** generalize/reuse this pattern rather than letting the browser dump raw
model objects into prompts. Character and Dream adapters can select Brainstorm-relevant fields
while retaining the same ownership boundary.

### Privacy and maturity

The current core models consistently expose owner/public/mature semantics, and Dream helpers
filter visibility using ownership, `isPublic`, `isActive`, and the user's mature-content
setting.

For the first text-only Brainstorm slice:

- ephemeral unsaved sessions are private application/browser state;
- generation input is sent only to the selected text provider required to satisfy the request;
- no Brainstorm output becomes public merely because it was generated;
- explicit handoffs inherit the destination model's current privacy/maturity contract.

For durable Brainstorm sessions, t-010 should default saved user sessions private unless there
is a clear product reason to publish them. Do not inherit the old Dream component's
`isPublic ?? true` behavior for a new session model.

### Responsive/layout primitives

`kr-panes`, `kr-pane`, `kr-pane-scroll`, and `kr-panel-flat` are current shared interface
primitives used across the site, including the Dream Brainstorm component. They are suitable
for desktop/tablet workbench structure, while mobile should collapse to a single-column
candidate stream rather than preserve a three-pane desktop layout at all costs.

The good donor from `components/dreams/dream-brainstorm.vue` is the interaction density and
current primitive vocabulary, not its Dream-specific left/right sidebars.

### Tutorial/help drift

`tutorialCards.ts` still teaches `Dream Brainstorm` inside the Dreams tutorial: start with an
idea, generate riffs, accept them, save Dream seeds.

This is another presentation remnant to update after the general workbench exists. It should
not block t-004, but later polish should teach the canonical Brainstorm product and treat Dream
brainstorming as one use case/source context rather than the definition.

## Recommended implementation sequence from the audit

### t-004 — route restoration

Exact likely Kind Robots files:

- `content/brainstorm.md`
  - preserve page/persona/backdrop metadata;
  - remove Dream gallery substitution;
  - mount dedicated `:brainstorm-manager`.
- `components/brainstorm/brainstorm-manager.vue`
  - create a current shell/workbench surface, not a checkout of June code;
  - no direct API/localStorage calls.
- `stores/helpers/dashboardHelper.ts`
  - primary Brainstorm tab -> `/brainstorm`;
  - remove Dream-only naming/narrative.
- `content/plan/brainstorm.md`
  - add redirect-only alias to `/brainstorm` using existing content redirect contract.

Do not touch schema or restore Pitch.

### t-005 — application contract/store

Create a dedicated `stores/brainstormStore.ts` plus shared Brainstorm types/helpers if they
become large enough to justify extraction.

Suggested minimal client types:

```ts
type BrainstormCandidateStatus = 'pending' | 'kept' | 'rejected'

type BrainstormCandidate = {
  id: string
  title: string
  text: string
  status: BrainstormCandidateStatus
  feedback: string
  edited: boolean
  parentId?: string | null
}

type BrainstormGenerateRequest = {
  premise: string
  count: number
  constraints?: string
  examples?: string[]
  mode?: string
  source?: BrainstormSourceRef | null
  replaceCandidateId?: string | null
  feedback?: string
}
```

The store owns candidate identity and should preserve previous text when regenerating one slot.
Provider-specific controls do not belong in this public request shape.

### t-006 — generation endpoint/provider contract

Prefer a dedicated route such as `POST /api/brainstorm/generate`.

The endpoint should:

1. read/validate the Brainstorm request;
2. resolve selected text server/provider using the existing server/suggest conventions;
3. call `manaGate()` before generation;
4. build Brainstorm's current creative-quality system/user prompts;
5. request structured candidates where the provider supports it natively;
6. normalize all providers into the same validated candidate envelope;
7. reject malformed/short/duplicate batches rather than shipping parser debris to the client;
8. commit mana only after usable provider output;
9. return `{ success, message, data: { candidates }, mana }`.

Do not seed the model with the current canned Brainstorm fallback examples. User-provided
examples may be passed as context because they describe the user's target, not a product-wide
creative ceiling.

A useful server-side candidate transport is intentionally small:

```ts
type BrainstormGeneratedCandidate = {
  title?: string
  text: string
}

type BrainstormGenerateResponse = {
  candidates: BrainstormGeneratedCandidate[]
}
```

Stable UI ids are application/store concerns and need not be trusted from the model.

### t-007 — workbench

Use the June manager and current Dream Brainstorm as UX donors:

- compact premise composer;
- visible result count;
- optional constraints/examples disclosure;
- candidate cards as visual center;
- Keep / Reject / Edit / Regenerate-this / More-like-this;
- rejection feedback only when useful;
- batch actions secondary to per-candidate control;
- no chat transcript;
- no provider cockpit;
- no Dream source browser until the general loop is excellent.

Phone: single-column curation stream.
Tablet: composer + candidate workspace without sidebars fighting for width.
Desktop: workbench can use pane structure, but candidate area remains dominant.

## T-003 answers

1. **Provider/auth/mana:** reuse serverStore + Suggest provider derivation/calls + `manaGate`;
   add Brainstorm-specific structured normalization.
2. **Old endpoint:** useful donor, not the revived canonical contract. It is OpenAI-only and
   Dream-specific.
3. **Persistence:** old Pitch is gone; Prompt, PitchSheet, Dream, and Conductor pitch semantics
   do not cleanly fit a Brainstorm session. t-010 may need an additive dedicated session model.
4. **PromptStore:** explicit selected-candidate/prompt handoff only, not session storage.
5. **Routes:** `/brainstorm` remains canonical content page; use the existing safe frontmatter
   redirect machinery for `/plan/brainstorm`.
6. **Dream overlap:** `DreamType.BRAINSTORM` is legacy taxonomy; Dream Brainstorm becomes a
   future source adapter/consumer, not the general product.
7. **Privacy/maturity:** unsaved work private; generation obeys authenticated mana/provider
   rules; saved sessions should default private and explicit handoffs inherit destination rules.
8. **Layout:** reuse current `kr-*` pane/panel primitives, but preserve candidate dominance and
   collapse cleanly by breakpoint.

## Audit verdict

No architectural blocker requires human input before restoration begins.

The old product was lost because a domain migration took its UI with it. The current site now
has cleaner routing, provider selection, economy controls, structured OpenAI output, object
visibility helpers, and better responsive primitives than Brainstorm had when it disappeared.

That means revival does not require nostalgia-driven rollback. It requires one small new owner
for Brainstorm state, one clean provider-aware generation contract, and a workbench that treats
the model as a prolific creative accomplice whose suggestions remain subject to human taste.

The infrastructure has caught up with the idea. The output now has to do the same.
