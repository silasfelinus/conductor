# Da Vinci Design Brief

## Project shape

Da Vinci is a life simulator app/game/webgame for Kind Robots. It turns a fresh story session into a branching life narrative with structured choices, pass/fail outcome checks, achievements, milestone unlocks, and generated art.

The important design rule is that Da Vinci is not just AI-generated prose. It is a goal-directed playable ruleset. AI narration can create scenes, flavor, and choices, but the app owns the durable state, outcome math, achievement rules, and milestone unlocks.

## Core loop

1. A user starts a fresh life run.
2. Da Vinci seeds a protagonist, tone, dream pattern, and possible Kind Robots character influences.
3. The Chat system narrates a scene and offers structured choices or interprets a natural-language user response.
4. Each choice changes tracked life dimensions.
5. Narrative events may generate art that is saved into the user's art collection.
6. Chapter, threshold, secret, and choice achievements can unlock during play.
7. At the end of the run, life dimensions resolve into pass/fail conditions.
8. The pass/fail map resolves into one of 1024 deterministic endings.
9. The ending unlocks a Kind Robots milestone and displays icon, hero, and story summary art.

## Endpoint strategy

Da Vinci should support 1024 endpoints without manually authoring 1024 brittle story trees. The clean version is a 10-dimension pass/fail ending key.

Proposed dimensions:

- legacy
- wealth
- love
- wisdom
- health
- freedom
- fame
- creation
- community
- mystery

Each dimension is scored during a life run. At the ending check, each dimension passes or fails against a threshold. The resulting 10-bit signature maps to one ending.

Example:

```txt
legacy: pass
wealth: fail
love: pass
wisdom: pass
health: fail
freedom: pass
fame: fail
creation: pass
community: pass
mystery: fail
```

This becomes:

```txt
1011010110
```

That key maps to a deterministic ending record. Endings can be partially generated from patterns, but the key is stable.

## Ending record needs

Each ending needs:

- title
- slug
- outcome key
- summary
- victory type: victory, failure, mixed, or secret
- icon image path
- hero image path
- milestone link
- optional generated art links
- optional Dream, Character, or Bot relationship metadata

The ending gallery should be able to show locked and unlocked states. A locked ending can show silhouette/secret copy. An unlocked ending can show the full icon, hero, summary, and achievement metadata.

## Milestone integration

Every Da Vinci ending should unlock or link to a Kind Robots milestone. The preferred approach is to use the existing milestone system as-is, especially if it already has an icon/image field.

If the existing milestone schema cannot link an icon or hero cleanly, the schema change should be minimal. Do not introduce a second achievement source of truth unless there is no clean way to represent Da Vinci endings as milestones.

Preferred mapping:

- Milestone title: ending title
- Milestone description: ending summary
- Milestone icon/image: ending icon path
- Milestone metadata: outcome key, victory type, Da Vinci run id, ending id

The ending hero is primarily for the Da Vinci ending reveal screen, while the icon should be suitable for milestone badges and achievement grids.

## Art collection integration

Da Vinci should generate art as the user experiences the story. Art should become part of the user's collection rather than disposable chat decoration.

Art scene types:

- story moment
- dream vision
- character encounter
- threshold achievement
- ending icon
- ending hero

Recommended dimensions:

- ending icon: 512x512 square
- ending hero: 1280x720 landscape
- story moment: flexible, usually 16:9 or portrait depending on surface

Each generated image should store prompt, scene type, run id, chapter/context, and the resulting Art/ArtImage reference.

## Chat and narration contract

The Chat system should behave as narrator/game master, but structured state belongs to Da Vinci.

A useful response contract:

```ts
interface DaVinciNarrationResult {
  narrativeText: string
  choices: DaVinciChoiceOption[]
  mechanicalEffects: DaVinciChoiceEffect[]
  artPrompt?: string
  milestoneCandidate?: string
}
```

The model can help lead users toward achievements by using narrative patterns, but it should not silently award achievements or invent durable state. The app validates and saves the actual result.

## Narrative device patterns

Reusable narrative patterns should guide the life sim toward endpoint outcomes:

- temptation: short-term reward, long-term cost
- sacrifice: lose one value to protect another
- mentor encounter: Kind Robots character influences wisdom, mystery, or creation
- dream gate: symbolic Dream interaction opens unexpected branches
- false victory: visible success hides a deeper loss
- return: revisiting an earlier choice with changed context
- inheritance: a prior choice affects a future generation or legacy
- collapse: a neglected dimension fails and reshapes the story

These patterns are prompt tools and game-design tools. They are not the source of truth for outcome resolution.

## Relationship to Storymaker

Da Vinci is related to Storymaker but should not be merged immediately.

Recommended boundary:

- Storymaker is the broader collaborative storytelling engine.
- Da Vinci is a playable life-sim ruleset with deterministic achievements and endings.
- Shared concepts may include sessions, branches, artifacts, generated art, narrator prompts, and character/Dream integrations.
- Da Vinci should prove the endpoint and milestone system before any merge decision.

## First build slice

The first implementation slice should create the endpoint foundation, not the full life simulator.

Target:

- define the 10 ending dimensions
- define the 10-bit endpoint key format
- generate or seed 1024 placeholder ending records
- define locked/unlocked ending display behavior
- map endings to milestones
- store icon and hero path metadata
- add a minimal run shell only if needed for testing unlocks

This gives the narrative system concrete targets and prevents the project from dissolving into pretty but untestable AI fiction.
