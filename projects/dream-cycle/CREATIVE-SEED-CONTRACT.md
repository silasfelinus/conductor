# Daily Dream creative seed contract

**Current contract:** deterministic `seed_facets` version 2
**Generator:** `scripts/build_dream_proposal.py --brief`

## Source of creative constraints

The author does not manually invent a separate `creative_seeds` block for a dated Daily Dream. The proposal helper deterministically selects and assigns live Facets for the Pacific date. The author must preserve the returned `seed_facets` unchanged when writing the proposal with `--from-json`.

The plan supplies:

- two umbrella GENRE Facets,
- one ANIMAL or SPECIES Facet,
- one OCCUPATION Facet,
- one additional GENRE for each dependent asset,
- applicable MATERIAL and PERSONALITY Facets.

## Fusion rule

Facets are story constraints, not metadata pasted on afterward. Each assigned Facet must visibly affect the premise, work, conflict, bodies or senses, environment, reward behavior, or art direction. A concept that remains the same after removing its Facets needs revision.

Wild combinations are welcome. Random-word soup is not. The six assets should feel like one world that could only have grown from that date's plan.

## Six-asset authorship order

Author exactly:

1. the umbrella vibe,
2. one location,
3. one Character,
4. one ITEM Reward,
5. one SKILL Reward,
6. one Scenario, written last and explicitly grounded in the vibe, location, and Character.

Daily Dream proposals have no narrator.

## Writing the visual fields (`look`, `art_direction`)

Every `look` and `art_direction` you write is fed to **Krea 2** more or less
verbatim by `scripts/dream_art_prompts.py`. Krea 2 is a distilled diffusion
transformer, not an instruction-follower. It paints the concrete nouns it is
given and ignores conditionals, so these fields have to carry actual appearance:

- **Describe what is visible, not what the thing does.** Material, shape, scale,
  colour, wear, how light hits it. "A dented tin ladle the length of a forearm,
  bowl worn to mirror-bright, handle wrapped in salt-stiffened cord" is usable.
  "It surfaces the hidden fortune buried in a person or object" is not — that is
  the `grants` field's job.
- **A reward's `look` is an object or a visible effect, never a person.** For a
  SKILL, describe the signature the technique leaves in the air while it is
  being used.
- **Assume nothing carries over.** The builder supplies framing, lighting, house
  style, and the cast/no-cast decision; you supply the subject.

This is not a style preference. On 2026-08-08 twenty-four Rewards rendered as
crowds of strangers because their only visual input was a sentence about what
they did, and the house prompt tail — which then carried an unconditional
"cast characters naturally across many species, ages, body sizes..." clause —
was the most concrete thing in the prompt. `item-tidefortune-ladle` was a
picture of fifteen people and no ladle. `look` is a required field now for
exactly this reason.

## Variety guardrails

Avoid repeating recent genre combinations, species families, occupations, palettes, location types, or character archetypes. Do not default to another enchanted lighthouse, mystical bell tower, magical archive, cozy market, lantern-lit workshop, or vaguely whimsical tower with renamed nouns.

Architecture and imagery should follow from the assigned Facets rather than serving as a generic starting shell.

## Validation

`build_dream_proposal.py --from-json` validates the authored bundle. `scripts/check_dream_outlines.py` and Daily Dream Contract CI verify that every eligible unbuilt proposal carries the exact version-2 six-asset shape.

Non-proposal legacy Dream files are idea inventory. They may contain loose inspirations, but they are not eligible inputs to the object builder and do not need a second seed schema.
