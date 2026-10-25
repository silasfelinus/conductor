# Comet City Academy: Final Exam
**Status:** new, active, high-priority original playbook. **Title:** provisional.
**Requested:** 2026-10-25 PT. **Master scope:** https://github.com/silasfelinus/kind_robots/issues/4181

## Core experience
A superhero-school game about graduating without allowing the world to be destroyed at prom. The player picks an initial **power family**, not a hero/villain alignment. Hero, villain, reformer, outcast and complicated independent trajectories emerge from actions, secrets, allegiances and consequences, not a morality toggle. A lovable ensemble at an eccentric but serious academy makes every decision personal.

Play **21 school days in three seven-day acts**: orientation and rivalries, compromised training and faculty secrets, then graduation/prom as a crisis finale. Allow selective fast-forwarding once daily content is resolved. Never pad the term with chores.

Each day: **(1) morning classes, NPC interactions and rumors; (2) a Dispatch-inspired training simulation board with 2–4 incidents, each assignable to 1–3 volunteer classmates or staff; (3) a school or Comet City location encounter card; (4) debriefs, consequences, injuries, promises, crisis countdown and saving.** Training-simulation events and real-world emergencies have different stakes and are clearly labeled. The academy assesses problem-solving, teamwork, ethics and collateral. Multiple responders improve some cases and create conflict or scarcity in others; a responder cannot be simultaneously assigned to incompatible missions. Show odds and constraints without revealing secret traits. Failures, refusal and neglect get interesting paths.

### Powers that materially reshape solutions
Six original initial families with distinct capabilities and costs:
- **Kinetic:** rescue, structural support, combat; collateral.
- **Technopathy:** diagnostics, construction, infiltration; surveillance and technological dependence.
- **Illusion/Empathy:** disguise, negotiation, de-escalation; trust/consent.
- **Elemental:** control terrain/weather/temperature; uncontrolled spread.
- **Spatial:** teleportation, barriers, evacuation; anchoring/range.
- **Morph/Biotech:** adaptation, healing, infiltration; exhaustion and identity complications.

Every act requires **at least two unique useful paths per family**. Universal negotiation, recruitment and investigation options prevent an unlucky build from becoming unwinnable. Pass, mixed, fail and decline all receive written outcomes, and every power has something it is genuinely bad at.

### Relationship and mystery spine
At least **16 full classmates/staff** with individual motives, voices, unique dispatch ability, agenda, wound/fatigue states, alliances and arcs. Include an ambitious student-council negotiator, a scholarship student frustrated by tokenism, an uneasy rescue instructor, a stage-tech engineer whose training scenarios predict real events, a masked serial-transfer rival and a prom organizer holding inconvenient evidence. These are *provisional seeds*, not canon names. Mix comedy, romance where earned, betrayals, sincere friendships and ideological disagreement. A rival should occasionally be correct.

At least **12 locations** with evolving local card decks: admissions hall, power lab, rescue arena, dorm, archive/library, rooftop garden, infirmary, dining hall, theater, city monorail, Comet waterfront and civic emergency hall. The campus and city must feel explorable, not be mere navigation buttons.

Foreshadow the prom catastrophe through school exercises, artifacts, missing records and NPC knowledge; the final crisis might involve a faculty coverup or students attempting a dangerous rescue, with causal branches set by earlier evidence. No single perfect romance, power or lucky skill roll guarantees the best resolution. Every early failure should leave a hard but recoverable route.

### Content, systems and visuals
Initial production floor: **6 powers, 16 NPCs, 12 locations, 36 meaningful encounter cards, 24 patrol/training cases, 12 distinct ending routes**. Each case/card has meaningful options, fully authored outcome tiers, distinct state flags and character callbacks. Maintain a machine-readable choice/ending graph and separate authored/reachable/illustrated coverage counts.

Seeded deterministic offline-at-play-time rules: day/act, powers/unlocks, classes, simulation grades, reputation (public and covert separately), trust/relationships, roster availability, injury/fatigue, resources, evidence, promises, crisis escalation, case results, save/load/version migration. Don't rely on LLM during a game. No irreversible production data changes.

**One-screen console presentation, not a web dashboard:** cinematic title/portrait/power creator, academy map, incident assignment desk, location illustration and encounter card, NPC scenes, prom/ending and yearbook galleries. Controller/touch/keyboard, accessibility, font readability and phone/tablet/desktop screenshots. First implementation PR ships a polished title and *playable full-day loop*, not a placeholder.

Art direction: original vivid superhero-coming-of-age comic illustration with clear painterly silhouettes, distinct powers and colorful inclusive cast that avoids stereotyping. Request and actually deliver project key art, cast expressions, locations, cases, success/mixed/failure and each ending; include prompt, art model, asset URL, scene ID and ArtJob identifiers. Pending prompts are not completed art.

### Adversarial acceptance
From-new-game, seeded action traces for **every ending**; hero/villain/independent, each power, deliberate failures, neglected missions, absent/injured volunteers, depleted resources, low trust, skipped clues and strange action orders. Verify no impossible roster combination, softlock, unearned ending or boring best strategy. Independent editors must read complete path transcripts; repair tone/pacing/consequences. Final subjective design review only **after** all agent-owned writing, art, QA and front-end work; public release separately authorized.

## Coordination
Conductor: `projects/comet-city-academy/roadmap.yaml`. Target: an internal Kind Robots Admin preview initially. Use tested playbook patterns from Emperor of Dust, Ecotone, Shifting Desks/Lands and Terrors on Crystal Street without coupling their saves. Keep master issue updated with shared findings and links, not routine repetitive task chatter.
