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
- the character's embodiment: one GENDER, one AGE, one BUILD, one HAIR and **two** ORIGIN Facets,
- a `body` of `humanoid` or `creature`,
- two planned taxonomy gaps for newly invented Facets.

## Embodiment — the character's body is seeded

Added 2026-09-15. Silas: *"there are lots of factors that could be switched. Hair color, style, age, gender presentation, body shape, size, racial background, default emotional state ... It would be great if we could utilize something so there is more diversity automatically roled when creating characters without such guidance."*

The catalog was deep on what a character IS and empty on what a character LOOKS like, so `look` was authored under no constraint at all — and unconstrained authoring converges. Measured across all 98 characters this pipeline had produced up to that date:

| axis | coverage |
| --- | --- |
| saturated hair colour | 0.0% |
| long hair | 0.0% |
| hair mentioned at all | 23.5% |
| explicit age | 14.3% |
| human skin tone | 9.2% |
| any stated affect | 14.3% |
| she/her vs he/him | 39.8% vs 9.2% (they/them 3.1%) |

Every axis the plan rolled came out varied. Every axis it did not roll collapsed to a single value: *"a wiry woman in a patched coat with close-cropped grey hair and a scar."* Diversity was never a prompting problem; it was a missing seed.

**All five axes draw every day.** They are deliberately not rotated the way flavour taxonomies are: each measured at or near zero, so a rotation would leave most days still unrolled on most axes.

### `body` is rolled, not assumed

Whether the protagonist is a person or an animal used to be an unstated authoring choice that the creature Facet merely nudged — some days the otter was the lead, some days it sat on a human's shoulder, with nothing deciding which. It is now drawn. When `body` is `humanoid`, the creature Facet is someone or something else in the character's world. When it is `creature`, the creature Facet is what the character IS.

### ORIGIN is culture, never phenotype

This is what makes heritage safe to roll on a catalog where most characters are not human. Silas: *"we should figure out how to deal with non-humans so we don't get 'southeast asian/canadian walrus'."*

A walrus raised in a Lisbon-facing trade quarter wears that quarter's oilcloth and swears by its saints. It does not have its people's cheekbones. Humanoid complexion is **derived from ORIGIN by the author**, which is why there is deliberately no COMPLEXION or ETHNICITY taxonomy — a standalone phenotype table read per character is precisely the shape that tokenizes. Two ORIGIN Facets draw rather than one, because a blend reads as a person where a single label reads as a label; this mirrors Silas's own practice: *"I usually choose a blend of 1-2 countries of origin with an ethnicity wildcard ... it works to provide diversity."*

**The anti-stereotype rule.** An ORIGIN may shape **material specifics only** — a textile, a dish, a craft, a tool, a script, a naming convention, how something is worn or mended. It may **never** shape temperament, morality, competence, or personality. Those came from PERSONALITY and ALIGNMENT, which are rolled separately precisely so that origin does not predict them. Any proposal where the origin explains the character's disposition has broken this contract and needs revision.

### Anatomy scope

Every embodiment Facet declares a scope of `any`, `humanoid`, or `creature`, and the planner draws only what fits the day's `body`. Box braids need hands and head hair; a brindled coat needs fur. ORIGIN is `any` throughout, by definition — culture attaches to any body.

### These axes are never auto-invented

GENDER and ORIGIN are excluded from `INVENTABLE_TAXONOMIES` because a nightly script inventing an ethnicity or a gender, unreviewed, and then seeding it into every future dream is this feature's worst failure mode. AGE, BUILD and HAIR are excluded for a quieter reason: an invented body descriptor is overwhelmingly likely to be a near-synonym of an existing one, and a catalog of near-duplicate body words re-narrows exactly the axis this was built to widen. New entries are hand-added to kind_robots' `utils/seeds/facetEmbodimentValues.ts`.

### The body must reach `look`

A Facet linked to the record but absent from `look` changes no pixel. That is the mirror image of dream-cycle/t-026, where Facets were recorded as applied over a Character that held none: both read as "complete" from the pipeline end, and neither changes a rendered image. The brief therefore requires every embodiment seed to be visible in `look`, **expressed rather than listed** — `look` must read as one observed person, not a character sheet — and requires a visible default expression derived from the PERSONALITY Facet, since only 14.3% of characters stated any affect at all.

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
- an aquatic-world proposal is rejected as a repetition only when its authored creative text contains several world-scale aquatic signals, one of the preceding five authored proposals was already aquatic-world shaped, **and** no assigned non-creature genre or setting explicitly requests an aquatic world. ANIMAL and SPECIES Facets never grant that exemption, even when a creature's own name contains words such as `ocean` or `marine`.

At catalog scale the audit is stricter than the live contract: a motif carried by ≥30% of
the built catalog counts against a bundle even when its Facets did request it. See
`specs/REMASTER.md`.

## Validation

`build_dream_proposal.py --from-json` validates the authored bundle. `scripts/author_dream_proposal.py` adds history-aware prose and semantic diversity checks before a generated proposal may be written. `scripts/check_dream_outlines.py` and Daily Dream Contract CI verify that every eligible unbuilt proposal carries the exact version-2 six-asset shape.

Non-proposal legacy Dream files are idea inventory. They may contain loose inspirations, but they are not eligible inputs to the object builder and do not need a second seed schema.
