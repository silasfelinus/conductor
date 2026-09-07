# Daily Dream creative seed contract

**Current contract:** deterministic `seed_facets` version 2
**Generator:** `scripts/build_dream_proposal.py --brief`

## Source of creative constraints

The author does not manually invent a separate `creative_seeds` block for a dated Daily Dream. The proposal helper deterministically selects and assigns live Facets for the Pacific date. The author must preserve the returned `seed_facets` unchanged when writing the proposal with `--from-json`.

The plan supplies:

- two umbrella GENRE Facets,
- one ANIMAL or SPECIES Facet,
- rotating flavour Facets drawn from OCCUPATION, PERSONALITY, ARCHETYPE, QUIRK, THEME, SETTING, BACKSTORY, ROLE, ALIGNMENT, or STYLE,
- one additional GENRE for each dependent asset,
- one MATERIAL Facet,
- two planned taxonomy gaps for newly invented Facets.

## Fusion rule

Facets are story constraints, not metadata pasted on afterward. Each assigned Facet must visibly affect the premise, work, conflict, bodies or senses, environment, reward behavior, or art direction. A concept that remains the same after removing its Facets needs revision.

Wild combinations are welcome. Random-word soup is not. The six assets should feel like one world that could only have grown from that date's plan.

A creature Facet is not automatically a setting Facet. An otter, manatee, shark, shrimp, or other aquatic creature should have meaningful anatomy, movement, senses, and physiological needs, but it does not by itself require the whole civilization to live on an ocean. Ocean-scale geography should come from an assigned genre or setting that actually asks for it, or from a premise whose other Facets genuinely make that choice distinctive.

## History-aware seed cooldowns

The daily seed is deterministic, but Daily Dream is a curated sequence rather than a row of independent dice rolls. `scripts/build_dream_proposal.py` therefore checks the preceding five authored proposals for demonstrated world-scale theme ruts before drawing the next plan.

When a recent bundle has saturated a guarded theme family, the planner temporarily prefers Facets outside that family. The filter is a **cooldown, not a ban**: if filtering would leave too few candidates to satisfy a required draw, the full pool is used instead. The deterministic date seed still controls the choice inside the eligible pool.

The first guarded semantic family is `aquatic-world`, added after the September 3–6, 2026 run produced four consecutive ocean-centered worlds. It cools down explicitly aquatic setting/genre Facets and water-associated creature seeds after an aquatic world has appeared recently. This prevents independent random draws from clustering into a repetitive daily sequence without making Oceanic Mythology, The Big Blue, or aquatic creatures permanently unavailable.

Cooldown state is intentionally not written into `seed_facets`; it is authoring context, not a creative Facet, and should not prime the language model toward the motif it is trying to avoid.

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

Avoid repeating recent genre combinations, species families, occupations, palettes, location types, character archetypes, or whole-world habitat choices. Do not default to another enchanted lighthouse, mystical bell tower, magical archive, cozy market, lantern-lit workshop, vaguely whimsical tower, or ocean civilization with renamed nouns.

Architecture and imagery should follow from the assigned Facets rather than serving as a generic starting shell.

## Rut families are enforced, not just advised

The variety guardrails above are checked, not left to good intentions.
`scripts/dream_creative_ruts.py` holds the shared vocabulary for five historical grooves —
bureaucracy/record-keeping, archives and libraries, cozy markets and workshops, towers and
lighthouses, and repeated occupational archetypes — plus the ornamental noun-surname
detector.

`scripts/dream_theme_diversity.py` covers world-scale semantic families that cannot be caught reliably by asset-name vocabulary alone. Its aquatic-world detector requires several independent setting signals, so one aquarium, rainstorm, water bowl, or shoreline reference is not enough to fail a proposal.

The live guards preserve intentional Facet fusion:

- a historical rut family is only a complaint when the day's **Facets did not ask for it**, so a Bureaucratic Fantasy Facet may still produce a permit office on purpose;
- outside bureaucracy, the older lexical families only complain when the motif reaches an **asset name**. A lighthouse in passing is scenery; *The Lighthouse of Small Regrets* is the rut;
- a semantic aquatic-world proposal is rejected only when its authored creative text contains several world-scale aquatic signals **and** no assigned genre or setting explicitly requests an aquatic world. An ANIMAL or SPECIES Facet alone is deliberately not that permission.

At catalog scale the audit is stricter than the live contract: a motif carried by ≥30% of
the built catalog counts against a bundle even when its Facets did request it. See
`specs/REMASTER.md`.

## Validation

`build_dream_proposal.py --from-json` validates the authored bundle. `scripts/author_dream_proposal.py` adds history-aware prose and semantic diversity checks before a generated proposal may be written. `scripts/check_dream_outlines.py` and Daily Dream Contract CI verify that every eligible unbuilt proposal carries the exact version-2 six-asset shape.

Non-proposal legacy Dream files are idea inventory. They may contain loose inspirations, but they are not eligible inputs to the object builder and do not need a second seed schema.
