# Space Couch
**Canonical display title:** **Space Couch**. **Stable Conductor slug:** `game-of-captains`. **Stable route during migration:** `/play/game-of-captains` (public-facing labels, project title, homepage highlight and Play tab should say Space Couch; preserve deep links and save keys). Previous working title **Game of Captains** remains the description of the *genre*, not the game's final display name.

**Creative direction:** Silas, updated 2026-10-26 PT. High-priority original Kind Robots illustrated comic science-fiction captain/crew playbook. Master issue [kind_robots #4182](https://github.com/silasfelinus/kind_robots/issues/4182), Conductor task ledger `projects/game-of-captains/roadmap.yaml`. First Play slice currently proposed in [kind_robots PR #4185](https://github.com/silasfelinus/kind_robots/pull/4185); reconcile the name on that live surface in a follow-up scoped code PR or before its safe merge if coordinated.

## 0. Canonical couch-shaped starship (supersedes old bridge design)

**The spaceship is literally a long, scarlet upholstered couch.** Four people can travel seated on it through the vacuum. An invisible protective force shield maintains atmosphere, pressure and survivability around the couch. The couch must remain visually recognizable in ship images, character deployments, cutscenes and dashboard art; a normal starship exterior, conventional cockpit or separate ship bridge would violate the premise.

**Room-folding miniaturization:** Temporary modular spaces unfold *behind* the backrest while the couch remains foreground: holodeck, war room, infirmary, science laboratory, spare bedroom as a rare story beat. Spatial expansion is not a license to replace the couch with an ordinary ship. Pocket rooms are intentionally scarce tactical choices, can fail in interesting ways, and cost resources. The couch force bubble is life-safe even in backup mode. In the first slice, room specialty matches grant +10% mission odds for one supply, launching expends one main shield charge, depleted main charge means -10% operational odds but safe emergency atmosphere, and one supply recharges one shield charge. Mission preview and actual result must agree; reload preserves state.

**Visual art:** Krea2 literal framing first, Arthemy painterly style second. Commission an iconic couch-in-space title/hero, portrait card and icon, three distinct room expansion images, shield variants, all travel/away and story consequences. The original hand-authored SVG `/game-of-captains/space-couch-stage.svg` is *temporary concept art* only. Record real ArtJob IDs and rendered image evidence before treating any art as complete.

**Migration:** Preserve internal Conductor/DB join key `game-of-captains`, Play route `/play/game-of-captains`, and save key `game-of-captains-voyage-v1`. Update presentation-only `Project.title` via Kind Robots API (not Conductor projection), Kit/Forge entries, social previews and Prom of Doom guest attribution. Existing Vox, Serendipity and Fluke narrator canon continues unchanged; the couch is this game's transport and does not retroactively rewrite Captain Fluke's distinct Improbability Starcruiser in original Dream #49.

## 1. Title, premise and dramatic question

**Space Couch**: **the captain is responsible for the orders**, even when the ship's navigation is powered by questionable arithmetic and somebody has replaced the diplomatic interpreter with a sandwich toaster. Choose your captain and core crew, chart an original starship's route through a mutable galaxy, run space and away-team missions, manage growing interpersonal tension, and repeatedly confront whether an advanced civilization should intervene when other cultures treat one another unjustly. A mission can end in a punchline and still require a memorial. The tension between command, loyalty, competence and duty is the heart of the game.

The comedic DNA of Space Quest, Red Dwarf, Hitchhiker's Guide, Star Wars, Star Trek, Lower Decks, Barbarella and The Orville informs **pace and tonal range**, not borrowed lore, outfits, dialogue or copyrighted characters. Tone: wry, sardonic, occasionally gleefully ridiculous, affectionate to competent misfits, capable of earnest loss. Avoid a string of unrelated gag encounters without an accumulative emotional or political spine.

An **unpredictable, seed-selected alien adversary** has a specific agenda, methods, allies, weaknesses, and several potential relations to the captain (destroyed, redeemed, recruited, revealed as misunderstood, exploited, or victorious). It disrupts travel, crew morale, faction diplomacy and mission results throughout all **three acts**, rather than merely changing the sprite at the final destination. Each destination must matter to whether a given ending is possible.

## 2. Systems and voyage structure

**Run opening:** choose among **six distinct captain backgrounds/personas**, select initial senior crew from **at least sixteen authored recruitable crew**, set ship identity and relationships. Choices affect opening resources, authority, how a captain's log interprets events, skills and which contacts trust them. **Captain Fluke** can be a playably adapted persona provided the canonical seeded NARRATOR identity remains unchanged and the adaptation is explicit. Crew are not stat tokens: named interpersonal debts, objections, skills, fears, romances where authored, injuries, loyalties, departures and grudges.

**Chapter cycle:** (1) captain's log and shipboard scene, (2) view star chart, distress signals and political/ship hazards, (3) choose mission/destination, (4) assign onboard posts and a **0–3-member away team** when permitted while maintaining a viable bridge watch, (5) resolve a sci-fi encounter with capability-specific paths and a serious ethical intervention dilemma, (6) antagonist complication or counterproposal, (7) debrief: ship resources, allies, injuries, faction standing, promises, responsibility and destinations, (8) save and move to a subsequent chapter. Sometimes an empty away team or risky lone captain is valid with real costs; staffing must not deadlock the game.

**Intervention doctrine** tracks informed local consent, autonomy, imminent harm, asymmetry of capability, treaty obligations, publicity/secrecy, crew dissent and whether a solution is reversible. Choices include rescue by invitation, open intervention, covert aid, negotiated compromise, refusing to interfere, sabotage and opportunistic involvement; **restraint must not always be automatically morally superior**, and technological advancement is not a measure of anyone's human worth. Follow up with the people affected, not only faction-score changes.

**Game state:** stable seed and antagonist, captain, roster, crew roles and morale, available ships/systems, treaties and intervention ledger, repairs/fuel/cargo/communications, faction trust, unresolved promises, scanned clues, missing crew, ship-vs-away location, per-crew injuries/romances, scene flags, action transcript, versioned save/load and local gallery unlocks. All major choices have authored great/success/mixed/fail/refused outcomes with delayed callback text. No playtime LLM dependency; mission and antagonist randomization are reproducible.

**Three acts:** **Act I, First Voyage** introduces bridge chemistry, the star routes and a first dilemma at the Serendipity neutral hub. **Act II, Unwelcome Responsibility** escalates encounters, reveals antagonist methods and makes crew doctrine fractures unavoidable. **Act III, The Last Command** sends the crew toward destination-dependent consequences, bargaining with or confronting the antagonist, and finales accounting for people helped, promises kept, planets changed and who remains on the bridge.

## 3. Full-screen navigation and presentation

**AAA aspiration, slice-by-slice execution:** every route is a true game stage within the available shell height, not a conventional application dashboard. All major views have strong full-screen artwork, context-specific compact controls, consistent gamepad/keyboard/touch focus and readable action hierarchy. A single integrated header icon/dock leads to these functional screens:
1. **Title / Captain Select**: painted ship/crew introduction, choice of persona and preview of potential first officers.
2. **Couch / Main Hub**: expansive open-space red couch and force-bubble painting, captain's log, one clear next order, live ship condition and NPC banter.
3. **Starmap / Navigation**: visually coherent star systems, charted jumps, ports, hazards, ship position, attainable destinations and deliberately discoverable routes.
4. **Mission / Away Team**: large scene plate and crew presence, onboard-vs-away assignments, unique mission actions and a real result.
5. **Crew Dossiers / Relationships**: portrait-forward roster with ability, trust, exhaustion, injury and incompatible loyalties.
6. **Captain Page**: background, duty, reputation, doctrine, gear, ship upgrades and personal timeline.
7. **Captain's Log / Scrapbook**: encountered worlds, adversary clues, voiced/comic key moments, important dilemmas, discovered conclusions and voyage epilogues.
8. **Settings / Save Slots**: safe save/load/overwrite with versioning, audio, motion, caption/text-size/contrast, controls and optional card backs.
9. **Finale / Endings**: destination-specific cinematics and epilogue art that pay off both comic and ethical stakes.

At 390 / 768 / 1440 px, keep large scene artwork and primary input visible without page scrolling. Switch to overlay panels/console panes with individually bounded scroll; do not crowd controls with status or tutorial essays. Use the shared art pipeline when scenes have generated art; **vector concept art in the current PR is not final painted coverage**.

## 4. Established canon, cast and authored encounters

**VERIFIED canonical Kind Robots seed references:** `stores/seeds/narrators.ts` and `utils/sceneChoices.ts`:
- **Barkeep Vox**, warmly sardonic humanoid tardigrade narrator of spacers' bar stories. Reuse the recognized design/voice and explicitly adapt a *separate playable NPC representation* if needed, without modifying the seed's `NARRATOR` role.
- **Serendipity Space Bar**, Dream #44, is a **sentient space bar** whose lighting and gravity seem to feel emotions. The building and Vox are not the same speaker. Neutral territory, with a house rule of **no vaporizing paying guests**. Make its hospitality, visitors, secrets and changing condition central to more than one chapter.
- **Captain Fluke**, Dream #49, frames the **Improbability Starcruiser** through confident, demonstrably inaccurate captain's logs, countered by a precise ship computer. A playable adaptation or repeated encounter does not overwrite existing narrator canon. The borrowed *names belong to Kind Robots*, not to unrelated science-fiction properties.

**Cast and world breadth:** **six playable captain backgrounds, sixteen named crew with substantial personal quests/portraits, twelve geographically/systemically distinct ports and star systems, eight coherent principal antagonists, forty encounter cards, thirty significant missions and sixteen substantially different reachable finale routes**. All planets have culturally heterogeneous individuals and institutions, not monolithic species stereotypes; give opponents defensible aims without pretending harm and rights are interchangeable opinions. Side and main crew earn friendship, friction, duty and betrayal; don't manufacture romance as crew assignment payment.

**Encounter seeds:** *The Library Planet's Due Date* (a self-aware archive claims contractual veto over evacuation); *The Serendipity Tab* (Vox withholds who paid a refugee ship's debt, while the building manipulates gravity to shelter someone); *The Imperfect Rescue* (the ship can tow only one refugee vessel, while an away team can attempt a second); *The Courtesy War* (two civilizations request the same disaster-relief technology but explicitly forbid aid to their neighbors); *The Insult Compiler* (ship AI translates a peace treaty as a marriage proposal and the crew must take diplomatic responsibility). Each must contain multiple viable, materially different approaches and result tiers, not merely the premise.

**Art production:** three project identity assets, six captain hero/mood sets, sixteen crew full-figure and emotion portraits, injury/absence variants, key bridge/starmap and twelve locations, primary and optional antagonists, mission plates, meaningful choice consequences and all finales. Record prompt, model/seed, run/scene key, rendered ArtJob/ArtImage ID, delivered URL and visual review. **Requested ≠ queued ≠ rendered ≠ delivered ≠ verified**.

## 5. First playable slice

**Current target:** [Kind Robots PR #4185](https://github.com/silasfelinus/kind_robots/pull/4185) opens a Play route with concept-painted/vector couch spacecraft, select captain/crew, three space missions, away-team assignments, one of several seeded aliens interfering, ethical decisions, debrief, a short end card, Pinia autosave, project placement and two home highlights. This is useful production scaffolding, **not** the completed 3-act game.

For an acceptable **Space Couch** slice:
- Title, Play tab, main home highlight and project display metadata use **Space Couch**, with stable `game-of-captains` slug/Play route/saves and old deep links retained.
- One fully playable mini-voyage with **captain selection, 3–4 person bridge complement, one ship mission, one away-party challenge (0–3), one deeply written ethical fork, a seeded antagonistic complication, return debrief and a verifiable ending**. The crew composition demonstrably changes options, costs and outcomes.
- Reuse Vox, sentient Serendipity and Fluke **without confusing their canonical narrator roles**. Seed-select at least two truly different villains in slice, revealing their individual motives in separate scenes.
- Deliver finished working **couch, star chart, mission, crew, log/ending and settings** navigation; app-like tab screens with no action are not accepted. Make an illustrated, responsive 390/768/1440 stage, then layer in painted ArtImages as generation completes.
- Test real choices under several captain/crew/antagonist seeds, with logs and a save-reload mission resume. No lost state, duplicate awards or unwinnable crews. Preserve a complete from-new-game replay trace and verify route/dashboard highlight direct navigation.

This first slice is intentionally less ambitious than the finished three-act/cast/story/art target. Finish the safe, reachable game route now; independently queue/deliver paint in later art tasks rather than pretending the vector canvas counts as final art.

## 6. Completion gates and coordination

Build out all cast, galaxy, antagonists, authored outcome branches and significant ship/away dilemmas; graph every ending to proof by **from-new-game seeded action trace without injected flags**. Run adversarial careers as rescue-first captain, cynical non-interventionist, treaty legalist, overreaching interventionist, opportunist, unreliable officer, missing specialists, hostile crew, absent/wounded teammate and careless commander. Review what each planet thought, not only whether the captain collected XP. Independent editorial reads whole transcripts for humor, nuanced ethics, continuity, original identity and earned loss; image audits check actual art and presentation at the relevant widths. Repair issues and rerun. **Do not rename the master issue “Awaiting human gate” until every agent-actionable gameplay, prose, art and quality task is complete**. Human design acceptance and separately requested outward publication remain distinct gates.

**Implementation:** Conductor roadmap `projects/game-of-captains/roadmap.yaml`. Existing Kind Robots `Project.conductorSlug`, Play URL, and save identities should be treated as migration-sensitive, even though public display branding changes to **Space Couch**. The next work in an open PR must not clobber another agent's edits; integrate at latest remote tip, run full checks and merge only green.
