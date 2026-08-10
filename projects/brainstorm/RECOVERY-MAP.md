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
