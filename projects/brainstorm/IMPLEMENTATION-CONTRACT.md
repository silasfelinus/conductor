# Brainstorm Implementation Contract

date: 2026-08-10
project: brainstorm
source: `DESIGN-BRIEF.md` + `RECOVERY-MAP.md`
status: implementation-ready

This is the short field manual for the restoration threads. The recovery map explains why;
this file pins the boundaries that downstream implementation should not casually rediscover or
re-litigate.

## Product invariant

Brainstorm is a human creative-divergence workbench:

**premise -> request X distinct ideas -> curate each candidate -> edit / keep / reject /
regenerate / branch -> save or hand off chosen material**

The historical interaction is evidence. Historical LLM output is an anti-benchmark. Modern
Brainstorm should embarrass it.

Do not confuse safe with bland. Allowed absurdity, sarcasm, gallows humor, cartoon peril, dark
comedy, strangeness, and genuine surprise are creative assets when the user's request calls for
them. Product safety/maturity rules still apply underneath the creative system.

## Ownership boundaries

### Brainstorm owns

- active premise/request;
- result count and creative constraints;
- user examples supplied for the current request;
- source-object reference/intent;
- candidates and their application-owned ids;
- keep/reject/edit state;
- candidate feedback;
- non-destructive regeneration/branch lineage;
- ephemeral session/browser state;
- later durable Brainstorm session persistence.

### Brainstorm does not own

- text-server inventory/preferences (`serverStore` owns these);
- Dream gallery/state (`dreamStore` owns these);
- Prompt gallery/state (`promptStore` owns these);
- provider credentials;
- mana accounting;
- ArtJob delivery state;
- Conductor project/task/pitch lifecycle;
- Character/Dream/Reward/etc. canonical model data.

## Canonical routes

- canonical product: `/brainstorm`
- alias: `/plan/brainstorm` -> `/brainstorm`

Use the existing Nuxt Content redirect contract for the alias. Never build a second workbench
under `/plan/brainstorm`.

Route-restoration files:

- `content/brainstorm.md`
- `content/plan/brainstorm.md`
- `components/brainstorm/brainstorm-manager.vue`
- `stores/helpers/dashboardHelper.ts`

Preserve current Brainstorm page persona/backdrop metadata. Remove Dream-gallery substitution.
`utils/projectPlacements.ts` already points `brainstorm` to `/brainstorm` and should not need a
change.

## Client/store contract

Create a dedicated Pinia store, expected path `stores/brainstormStore.ts`.

Components do not call APIs or `localStorage` directly.

Suggested core client types:

```ts
export type BrainstormCandidateStatus = 'pending' | 'kept' | 'rejected'

export type BrainstormSourceRef = {
  modelType: string
  id?: number
  slug?: string
  intent?: string
}

export type BrainstormCandidateRevision = {
  text: string
  title?: string
  createdAt: string
  reason: 'generated' | 'edited' | 'regenerated' | 'branched'
}

export type BrainstormCandidate = {
  id: string
  title: string
  text: string
  status: BrainstormCandidateStatus
  feedback: string
  edited: boolean
  parentId?: string | null
  revisions: BrainstormCandidateRevision[]
}

export type BrainstormGenerateRequest = {
  premise: string
  count: number
  constraints?: string
  examples?: string[]
  mode?: string
  source?: BrainstormSourceRef | null
  replaceCandidateId?: string | null
  parentCandidateId?: string | null
  feedback?: string
}
```

Provider-specific knobs such as `temperature`, `maxTokens`, provider name, or OpenAI model do
not belong in the public creative request shape. The active server may be supplied separately as
a safe server snapshot following current Suggest/serverStore conventions.

The store, not the model, assigns stable candidate ids. A generated candidate being replaced
must retain its previous text in revision history.

## Generation API contract

Preferred route:

`POST /api/brainstorm/generate`

Suggested normalized provider response:

```ts
export type BrainstormGeneratedCandidate = {
  title?: string
  text: string
}

export type BrainstormGenerateResponse = {
  candidates: BrainstormGeneratedCandidate[]
}
```

Successful API shape:

```ts
{
  success: true,
  message: string,
  data: {
    candidates: BrainstormGeneratedCandidate[]
  },
  mana: unknown
}
```

The endpoint must:

1. validate premise/count/constraints/examples;
2. derive the selected provider/model from the current text-server conventions;
3. preserve `manaGate()` auth/economy behavior;
4. resolve any source entity server-side with ownership/visibility checks;
5. use Brainstorm's modern creative-quality instructions;
6. request native structured output where available;
7. normalize every provider to the same small candidate envelope;
8. validate count/content and suppress obvious duplicates;
9. commit mana only after usable generation;
10. return structured candidates, never delimiter-formatted prose.

Provider parsing tolerance stays server-side. Vue and Pinia do not strip bullets, split pipe
delimiters, remove "Sure, here are...", or guess JSON wrappers.

## Provider reuse

Reuse or generalize:

- `server/utils/suggest/suggestProviders.ts`
- `server/api/suggest.post.ts` patterns
- `stores/serverStore.ts` active text-server selection
- `server/utils/manaGate.ts`

`server/api/botcafe/brainstorm.ts` is an implementation donor for OpenAI Responses strict JSON
schema and mana handling, **not** the canonical revived contract.

Do not preserve its Dream-specific prompt or canned product-wide examples.

## Creative-generation contract

The system prompt should optimize the batch, not merely each sentence.

A strong batch:

- attacks the actual premise;
- varies conceptual strategy rather than nouns/adjectives;
- contains materially distinct candidates;
- includes useful specificity;
- respects explicit constraints;
- leaves room for human development instead of over-polishing everything;
- can understand comic premise/escalation;
- permits dark/absurd/strange/serious/practical material when requested;
- contains at least some genuinely non-obvious angles.

Failures include:

- noun-swapped paraphrases;
- random weird nouns with no premise;
- corporate naming-list sludge;
- generic inspiration;
- fake profundity;
- repetitive rhetorical templates;
- verbose explanations that crowd out the ideas;
- safety language that sanitizes allowed material into cheerful mush.

User-provided examples are valid context. Historical Brainstorm outputs are negative fixtures,
not positive few-shot material.

## Persistence boundary

Do not resurrect Prisma `Pitch`.

Do not use these as Brainstorm-session storage merely because they exist:

- `DreamType.BRAINSTORM`
- `Prompt`
- `PitchSheet`
- Conductor `pitches/*.md`

They may be explicit source/handoff destinations where their existing semantics fit.

`t-010` owns the final durable persistence decision. Current audit recommendation is an
additive `BrainstormSession` / `BrainstormCandidate` model if no genuinely generic session model
proves suitable.

Unsaved Brainstorms are private draft/application state. A generated candidate does not become
public by existing.

## Object-context boundary

Future object-aware brainstorming should follow the existing server-side pattern in
`server/utils/suggest/artModelContext.ts`:

- typed entity reference from client;
- server resolves by id/slug;
- owner/public/admin visibility enforced server-side;
- selected canonical scalar fields only;
- compact long text;
- user can see/remove the source context.

Character and Dream are first adapters. Do not send arbitrary serialized Prisma objects from
the browser.

## Art boundary

Text first.

Brainstorming **art prompts** is text generation and may arrive before rendering.

Actual image rendering is explicit and later:

- selected candidates only;
- durable ArtJob pipeline only;
- current Krea2 defaults unless user deliberately selects another supported build;
- no implicit batch render because the user requested many text ideas;
- preserve source session/candidate/prompt/ArtJob/result traceability.

## Workbench contract

The candidate workspace is the visual center, not a Dream gallery and not a chat transcript.

Minimum useful candidate actions:

- Keep / unkeep
- Reject
- Edit inline
- Regenerate this candidate only
- More like this / branch

Generation controls:

- premise/request
- result count
- optional constraints/examples
- Generate

Provider controls remain invisible by default.

Responsive intent:

- phone: single-column curation stream, actions thumb-reachable;
- tablet: composer + dominant candidate workspace, no competing sidebars;
- desktop: panes are allowed, but candidates retain the majority of useful space.

Use current `kr-panes`, `kr-pane`, `kr-pane-scroll`, `kr-panel-flat` vocabulary where it fits.

## Error/auth states

First-class states include:

- no premise;
- generating;
- malformed/short provider response;
- provider unavailable;
- unauthenticated generation (401);
- insufficient mana (402);
- no active compatible text server;
- candidate-level regeneration failure without losing old text.

Never fabricate candidates as a silent error fallback.

## Deliberate first-slice exclusions

Do not block the first working text loop on:

- durable DB sessions;
- generated art;
- Character/Dream source adapters;
- Conductor proposal integration;
- social publishing;
- provider cockpit controls;
- full persona polish.

The first slice succeeds when `/brainstorm` is unmistakably Brainstorm again and the modern
premise -> candidates -> human curation loop has a clean technical home.

## Verification expectations

Every implementation slice follows Kind Robots' normal gates:

- relevant typecheck/tests;
- direct load and refresh;
- loading/empty/error/auth transitions;
- no component-owned API/localStorage calls;
- eventual PR-preview visual verification at phone, tablet, and desktop before the project can
  be considered finished.

When implementation behavior and historical code disagree, this contract plus the current
`DESIGN-BRIEF.md`, `RECOVERY-MAP.md`, and latest Silas direction win.
