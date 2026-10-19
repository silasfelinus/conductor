# ECOTONE: four value fault lines, companions and opening-state lenses

**2026-10-19 PT · design exploration prompted by Silas, not yet finalized game rules.** The story and its 32-ending registry remain canonical as already defined in [ECOTONE-32-ENDINGS.md](ECOTONE-32-ENDINGS.md). This document defines **four independent story tensions**, not a political quiz, drugs-as-politics classifier, binary good/bad moral meter or universal value prescription. No UI build, art generation or publishing authority.

## Four ideological/ecological/philosophical fault lines

| Story axis | Pole A | Pole B | Actual dramatic question |
| --- | --- | --- | --- |
| **Autonomy ↔ Solidarity** | Personal independence, privacy, self-determination | Mutual obligations, cooperation, institutions | How much agency belongs to an individual, and what do we owe neighbors? |
| **Continuity ↔ Reinvention** | Tradition, memory, existing ways of living | Progress, innovation, making something new | What must endure even when Humboldt changes? |
| **Ecology ↔ Engineering** | Nature, conservation, regeneration | Technology, infrastructure, human intervention | Is the future sustained by ecosystems, technology or difficult combinations? |
| **Agency ↔ Fate** | Free will, uncertainty, alterable outcomes | Determinism, prediction, unavoidable consequences | When futures seem readable, can choices actually change them? |

**The fourth is philosophical/metaphysical, not a conventional partisan political ideology.** It bridges the supernatural mystery and the player's ability to affect the county's future. If we ever add a fifth *governance* tension, a useful one to explore is **local/shared control ↔ outside/centralized control**, especially for a data center, but neither make this fifth track required nor assume all external investment harms the county.

**Explicit avoidances:** "Tradition" is neither synonymous with logging nor with Indigenous identity. "Community" is not equivalent to state coercion. "Technology" is not the corporate villain and "nature" not an automatic paradise. "Fate" does not mean losing the game. Local tribal nations have actual sovereignty, not a position on a toy slider. A rights or consent violation cannot be made acceptable through opposing-axis points.

## Companions: tensions, not predetermined compass positions

| Lead | Especially active tensions | Character's live contradiction |
| --- | --- | --- |
| **Juniper** | Ecology ↔ Engineering; Autonomy ↔ Solidarity | Forest nymph who protects living forest but must decide what shared stewardship and human livelihoods mean; humans cannot simply be excluded as invaders |
| **Kit** | Continuity ↔ Reinvention; Autonomy ↔ Solidarity | As a Hmong American contemporary artist, creative reinvention without reductive cultural branding; artist's independence versus collaborators' fair access and payment. Humboldt's 1885 Chinese expulsion is a separate historical episode, not Kit's family |
| **Mara** (working name) | Autonomy ↔ Solidarity; Continuity ↔ Reinvention | Independent tattoo artist sustaining her real creative ownership while voluntarily growing mentorship, new practices and economic security; Indigenous identity is neither her axis nor a mystical shortcut |
| **Cedar** (working name) | Continuity ↔ Reinvention; Ecology ↔ Engineering; Agency ↔ Fate | Rural son of a logging family and a growing family, both parents still together, enthusiastic about a locally accountable technoutopia. His radio offers apparently certain futures; he learns to verify the transmission and work to change what it predicts |

**Every companion must be able to argue from both poles of the axes that involve them.** Cedar can value local tradition while building broadband; Juniper may use technology to protect habitat; Kit can honor fixed history and innovate; Mara can be both fiercely independent and generous with apprentices. Avoid ethnicity, profession, temperament or drug-state stereotypes.

## Opening sobriety/perception as a narrative question lens

**These are *fictional authoring prompts*, NOT real pharmacological claims, personality diagnoses, alignments, partisan beliefs or permanent stats.** The four voluntary adult opening states define the **perspective and kinds of follow-up choices the scene foregrounds**, not the player's moral leanings or a free bonus to an axis.

| Opening state | The story camera foregrounds | Related question |
| --- | --- | --- |
| **Sober** (`sober`) | Documentary evidence, material timelines, inherited institutions, contracts | Which accounts of the past hold up, and what deserves preservation or reform? (Continuity ↔ Reinvention) |
| **Tipsy** (`tipsy`) | Conversations, social loyalties, improvisational negotiation | Who is at the table, who is excluded, and what responsibility does belonging carry? (Autonomy ↔ Solidarity) |
| **Stoned** (`stoned`) | Interdependence, patterns in habitats and economic networks | Which interventions actually coexist with a living ecosystem? (Ecology ↔ Engineering) |
| **Tripping Balls** (`tripping_balls`) | Conflicting possible realities, symbolic forecasts, corroboration of impossibilities | Does seeing a future make it inevitable? (Agency ↔ Fate) |

**Sober parity remains non-negotiable**: sober players can perceive and verify the supernatural, pursue every companion's happy path and reach an ethical technoutopia. Likewise every other opening has evidence and agency, and may avoid, refute or reverse its suggested thematic question. `opening_state` remains immutable for collectible ID `lead.opening.hope|dark`; `current_state` is mutable and does not establish ideology. An opening is **not** an axis offset.

## Scene tagging and playable state (proposed, not yet engine code)

Keep the current **Rizz, Burly, Wits, Local Lore, Psyche** stats and dice; four fault lines are **authoring metadata**, not replacement skills or morality points.

Every substantial stay/follow crossroad or side-encounter choice can carry:
- `tensions`: zero to two named axis IDs, each with **both values in genuine tension** (e.g. `autonomy-solidarity`).
- `stakes`: *which specific person, habitat, institution or future commitment is affected*, for example `worker_apprenticeship`, `forest_easement`, `community_fiber_ownership`.
- `decision_flags`: concrete persistent player actions (consulted residents, disclosed uncertainty, preserved evidence, cut corners).
- `evidence` and `consequences`: statements that establish actual verified facts and make dice failure, time costs and follow-up repairs visible.

Optionally track the player's repeated preferences in an **in-game Journal → Values** tab as qualitative "You've favored local independence", etc. The four axes are **not mandatory four sliders on the main board**; that would violate the single-screen minimalism. Do not derive a numeric ideology or an ending solely from a companion, chemical state, origin, or one roll. The ending resolver still returns one of **32** `lead.opening.hope|dark` IDs based on earned story conditions, not an ideological extreme; optimistic outcomes must be available to varied coherent values.

### Example: Cedar and the smart-forest network

A fictional consortium proposes to install radio repeaters, field sensors and compute infrastructure near a forest. They claim the project guarantees new skilled jobs.

**Real tradeoffs in one scene:** ecology vs engineering (where are sensors sited? what power and water do they draw?), autonomy vs solidarity (public safeguards vs landowner control), continuity vs reinvention (preserve timber/grower family knowledge in a modern technical training network), agency vs fate (a CB signal claims this build must fail). Choices:
1. Support the project *with enforceable local network ownership, ecologist/worker review and a relocation option*; tough coalition and evidence checks; potentially hopeful technoutopia.
2. Sign an exclusive private concession for promised jobs without independent verification; a possible dark network-control outcome, but a good-faith worker still deserves dignity.
3. Reject the build and organize a smaller co-op alternative, paying real time and financial costs; a different hopeful future is possible, with credible setbacks.
4. Investigate the CB's allegedly inevitable disaster, compare public records and dissenting expert testimony, then re-open the town debate; foresight does not dictate outcome.

**This allows** Cedar's `cedar.sober.hope` and `cedar.tripping.hope` to embrace technology for different dramatic reasons, while no path automatically maps "tech" to bad or "tripping" to predestination.

## Narrative and QA guidance

- Four tensions, each with two meaningful poles; every companion can meaningfully explore at least two. Across 16 lead×opening intersections, the thematic questions **cross**, not just repeat companion stereotypes.
- For all four openings × four chosen leads, author ≥1 meaningful scene presenting genuine two-sided tradeoffs and ≥1 scene in which an unexpected **hybrid position** can succeed or fail because of actions, not a hidden purity score.
- Verify the same opening can end `hope` or `dark` for the same lead via authored choices and fair rolls. This still yields exactly **32** collectible endings (16 hopeful / 16 dark), not 4×4×4×2 or axis-specific bonus endings.
- Never use ethnicity/tribal sovereignty or voluntary consumption as ideology or default alignment; civic/rights safeguards cannot be overridden by a value axis.
- Do not make `free will` a hidden privileged ideology or `determinism` automatically negative; let plausible predictions remain useful while allowing players to question them.
- The existing **single-screen phone/tablet/desktop** interface remains unchanged: optional journal tab/tooltip for value conflicts; only bounded internal scrolling.
- **No new artwork, ArtJobs, production deployment or public release.** This is a creative framework pending more character and scene writing.
