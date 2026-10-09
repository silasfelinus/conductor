# Zuzu: Koala Assassin — The Bell That Never Rang

> **Shared Zuzu world registry:** [worlds/zuzu](../../worlds/zuzu/README.md) has the cross-project canon, locked art references, model lookups and other production links. Read it before introducing shared lore or assets.

## Original illustrated branching gamebook RPG

**Owner:** `zuzu-gamebook` in Conductor. **Client:** `/play/zuzu-gamebook` in `kind_robots`.
**Genre:** Dark weird-west animal fable, cinematic interactive story, single-player.
**Related but separate:** `kr-adventures` is the shared preset choose-your-own-adventure reader; `zuzu-lair` is a timed animated QTE game; `zuzu-showdown` is a 2D fighter. This is the slower, deeper role-playing book of consequential decisions, not a toggle on either game.

### Player promise
Open to a full-bleed illustrated scene, not a questionnaire. Read one dense but brisk numbered section; weigh two to four meaningful choices. Choices branch by knowledge, injury, supplies, relationships, stealth or combat. Physical dice roll across the art and land with an unambiguous numerical result. Every success and every costly failure leads somewhere authored. The player can survive but fail someone, win at a terrible cost, or find the rare hard-won outcome. Replays expose alternate routes, secrets, tools and endings.

Inspired by the **decision density, agency, resource tension and rule-system depth** of Sorcery!, Lone Wolf, Grey Star and Fighting Fantasy. Invent our own attributes, dice probabilities, writing, artwork, encounter designs, spells and interface. Do not lift proprietary text, scene numbering, creatures, tables, signature system names or rules verbatim.

### Canon
Read in this order before authoring:
1. `projects/comic-creator/issues/zuzu-koala-assassin-01/BOOK-ONE.md` (latest story of record).
2. `.../CAST-PICKS.md` (locked image references; Zuzu R6 with later proportion fixes).
3. `.../VIDEO-GUARDRAILS.md` (costume, prohibited terms, art prompt gotchas).
4. `projects/zuzu-lair/DESIGN-BRIEF.md` and `projects/zuzu-showdown/DESIGN-BRIEF.md` for shared setting and mechanics vocabulary.
The gamebook is an **alternate trail** through the world, not a claim to supersede the comic's fixed chronology. Encounters may refract its watering hole, coyote, Hollow Bell, fennec siblings, apple tree, mission, posters, abbess and cosmic portal. The endings are what-ifs; the comic's three-on-the-road finale remains canon. Zuzu is short, stocky, serious, under a wide kasa; dusty rust-brown poncho, dark brown trousers, orange sash, katana diagonally **across his back**. No invented old Gallowsun/Stationmaster lore. Never disclose the comic's hidden twist in a section, title, image prompt, alt text or metadata.

### Rules v1: Road, Steel, and Quiet
- **Attributes:** Steel +2 (precision/grit), Sense +1 (observation/instinct), Shadow +1 (stealth/timing), Mercy +0 (people-reading/care). Long-term choices can shift a stat by at most +1/-1 between -2 and +4. Attributes are **not** a re-skinned classic SKILL score.
- **Dice:** roll **2d6 + attribute + situational item/power modifiers** against a **target** of 7 (steady), 9 (risky), 11 (demanding), 13 (desperate). Equality succeeds. Natural 12 brings an *edge* (bonus clue, resource or position) if scene-authored; natural 2 triggers a complication if authored, never silent instant death. The result always shows dice, modifiers, threshold and branch.
- **Health:** 12 hit points, floor 0. Resolve: 4 points spent on powers, rest grants recovery at an authored camp. No free healing by going backward. Wounds can impose conditions; never use permanent numeric degradation without a recovery opportunity.
- **Inventory:** 5 slots (stackable minor supplies with declared stack limit); initial poncho, kasa and sheathed katana are worn equipment and not slots. Items carry explicit tags for check modifiers, narrative prerequisites or combat effects. Starting pack: canteen (2 water), bandage (1), dry apple (1), flint (1). Story-gated keys/clues occupy a journal, not scarce item slots.
- **Special powers:** *Still Wind* (1 Resolve, add +2 to Sense/Shadow challenge before rolling); *Quiet Draw* (2 Resolve, add 3 to attack damage on one landed blow); *Last Kindness* (2 Resolve, prevent 3 damage or stabilize a companion in explicitly permitted scenes). Costs and use windows are explicit, powers never bypass critical narrative flags automatically.
- **Conditions:** e.g. bleeding, exhausted, marked, ally-coyote, sibling-trust, suspicion-of-abbess; store as named flags with meaningful onset and cure. Injury can raise a check target by 1 rather than stacking arbitrary stat penalties.
- **Persistent choices:** scene effects are transactional and recorded in a history log. Never grant an item twice by revisiting; never allow farming healing or Resolve by loops. Track visited nodes; avoid time loops in the first book.
- **Character sheet:** always one tap from HUD, with HP, Resolve, attributes, equipment, all inventory slots, wounds, powers, clues/journal, relationships, location, previous roll and ending records. Print/save export later.
- **Save:** browser-local with explicit schema version, validation and migration, resumable mid-fight; no account, no backend writes, no network during play. Autosave after every committed outcome, allow restart with confirmation. Branch history and discovered endings are separate from a reset run.

### Combat: risk rather than whack-a-mole
A foe has HP, Guard, Pressure, intent table and illustrated introduction/death/escape states. Each round:
1. Enemy telegraphs **intent** (aggressive blow, defend, rush, feint) before the player chooses.
2. Player chooses **Strike** (Steel check vs 7+enemy Guard; deal 2-4), **Guard** (Sense check to mitigate/return damage), **Feint** (Shadow check to break enemy Guard), **Use item**, **Power**, or **Withdraw** where scene permits. Enemies are distinctive, not damage sponges.
3. Resolve roll and apply both sides' outcomes and side effects once, using seeded dice. Enemy intent resolves even when player fails; every consequence is shown.
4. Victory, surrender, retreat or defeat follows a dedicated story node with an illustration. 0 HP sends the player to an authored ending or rescue branch, never a blank game-over.
Hard fight sample: the watering-hole crocodile is high-pressure but offers terrain and coyote-cooperation choices; the convent threat is an environmental puzzle with a combat component, not a giant HP bar. No combat against the fennec children.

### Story structure and quality gates
**Book One: The Bell That Never Rang.** 80-120 illustrated **numbered sections**, ~9 acts with multiple routes, at least 8 meaningfully distinct authored endings and 3 or more hopeful/survivor endings. Target 20-35k words across all routes, 120-250 words per ordinary scene, shorter during combat. Distinct major endings: walk away alone; survive with the siblings; save coyote and flee; sacrifice to close the portal; lose the mission; escape injured and hunted; expose the abbess but doom the mission; narrow survival with debt; best ending earned through resource planning and compassion. No cheap instant death from one untelegraphed dice roll. Reconcile who survives each route and where the canonical comic differs. Some ending flavor can depend on flags, but do not count trivial wording variants as separate endings.

**Graph contract:** a static, versioned JSON/TS bundle with section id, prose, art key + alt, choices with conditions/affordances and target, optional pre-roll challenge, explicit success/failure/edge branches, effects, encounter spec and optional ending id + ending tone. Stable IDs and migration aliases for published saves. Validator rejects missing targets, orphan sections, unresolvable reference names, runaway cycles, absent illustrations/alt text, contradictory state requirements and unreachable endings. Add tests that explore *stateful* routes, not only a graph DFS. Conditional choices have disabled explanations in the UI when knowledge/gear is missing, not vanishing buttons without clues.

**Authoring plan:** vertical slice ~12 scenes + two endings, with dice/powers/inventory/combat before scaling to 80+ and eight endings. Agents can develop authored scenes and art manifests in parallel with pure reducer and UI, with clear ownership paths. Never call the prototype a finished book.

### Presentation contract
Think **illustrated hardcover meets widescreen western**. Desktop: 60-70% scene art dominating top of viewport, numbered folio and typographic title; unobtrusive HP/Resolve/condition indicators overlay the image border, a parchment-ish text card partially overlapping bottom of art, art-led choices below. A brass/gunmetal dice tray slides in under choices; click/tap and keyboard work. Fixed nav to Character Sheet, Journal, Map/Chapter and Ending Ledger. Mobile: single column, image with focal crop and caption, readable type, thumb-safe actions; no horizontal overflow. Palette: dusty auburn, ink, storm teal, antique bone, restrained copper highlights. No default form stack, generic dashboard grids, or fully saturated fantasy purple.

Art dimensions: hero and setting 16:9 / 3:2, ending plates 4:5 and cinematic 16:9, portrait cards 3:4, badge/illustrated dice motifs 1:1. Each section includes alt text describing **actual image**. While art jobs await delivery, use an intentional illustrated placeholder/fallback with correct size and label, not a broken image or claim of a completed plate. Respect `prefers-reduced-motion`; roll outcome must be available to screen readers immediately and rerolls logged, not hidden behind animation. Device checks: 375, 768, 1440px.

### Autonomous contributor protocol
Tasks and scene writing live in Conductor, runtime in Kind Robots. Agents may claim, write, generate internal art and submit/merge scoped verified PRs independently per AGENTS.md; art generation is **explicitly approved** for this project. Create reproducible manifests, save exact prompt, seed, engine/checkpoint/LoRAs, ArtJob ID, ArtImage ID, license source and verified public URL. Use existing local generation infrastructure; no paid third-party spend. Never claim art exists until URL was loaded. Review changes with tests and screenshot(s) before merging. Public launch, explicit aesthetic acceptance, infrastructure/secret changes and production deployment remain human gates. After validated v1 release, set lifecycle to continuous with an explicitly recurring improvement task rather than starving higher-priority finite work.
