# Shifting Desks: Design Brief

date: 2026-10-12 PT
status: authorized new project; design phase; first slice building now (scope gate t-002 is soft)
owner: Conductor project `shifting-desks`; Kind Robots runtime, admin preview `/admin/shifting-desks`; public `/play/shifting-desks` is a separate hard human gate
direction menu: [PITCHES.md](PITCHES.md) (Silas picks the spine; the engine below serves every option)

## Promise

A **darkly comic, illustrated card adventure through a paranoid office hellscape.** You flip a beautifully illustrated encounter card. You read a short, sharp scene, then choose among two to four options, and every one of them costs something. You roll the dice, and the result is funny, awful, or both. Your employee file fills with flags, demerits, forms and dead predecessors. Five departments later you face the Board, or the ducts, or the Roach Union. There is no right answer. There is only the answer you can live with, until your Successor arrives.

Silas, 2026-10-12 PT: *"a darkly comic image card based experiential game system, where the user must navigate a complicated paranoid office hellscape ... the output layout [uses] the shifting sands format, the user will be given a series of morally questionable choices with no right answer, forced to impossibly difficult sacrifices, and unexpected moments of comedy. Giant cockroaches, deathtraps, weird psychological tests, nuclear bomb capable children's toys, mutant powers, secret organizations, and callbacks to classic works optional but appreciated."*

Touchstones: **Paranoia** (Silas's first RPG and the emotional center), Infocom's **Bureaucracy** and **Hitchhiker's Guide**, **Brazil**, **Office Space**, **Papers, Please**, Fallout's **vault experiments**, **Portal**.

## Best of both parents

This project is modeled on **Zuzu: Shifting Lands** (the board) and **Zuzu Gamebook** (the depth). It takes the strongest proven idea from each and is set in an original, non-Zuzu world.

| From Shifting Lands | From the Gamebook |
| --- | --- |
| Board laid out as **5 lands × 3 locations + a boss gate per land**, shown as a growing illustrated card grid | **Authored prose quality**: 120–250 words max per scene, and every outcome leads somewhere written |
| **Fully authored encounter cards per location pool** (4 per location), chosen by a seeded weighted draw, never assembled from random parts | **Character sheet one tap away**: skills, meters, conditions, inventory, flags, last roll |
| Readable, persistent **card flip**, custom card backs, existing Kind Robots card components | **Natural 12 / natural 2** edges and complications, authored rather than silent instant death |
| **Map mutation with a written reason.** History never silently rewrites itself | **Powers with explicit costs and windows** (here: the Mutation card) |
| Choice cards show **intent, risk hint, skill and target** before you commit | **Long-term drift**: repeated choices nudge skills and unlock or close routes |
| **Journal** of every draw, roll, effect and reason | **Disabled choices explain themselves** ("Requires Clearance 3") instead of vanishing |
| **Seed persisted; no free reroll by refreshing** | **10+ distinct endings**, including hopeful ones, and ending ledger across runs |
| Contract tests + schema in Conductor, runtime in Kind Robots | **Pacing: welcome before threat.** The Company is lovely before it is horrifying |

The new idea that is neither parent's: **every choice costs something** (below). The project lives or dies on that rule.

## The core rule: no clean wins

Every choice card has a **cost** paid up front, a gamble on the dice, or both. The schema contract enforces this: for every choice, the cost plus the *success* outcome must contain **at least one harmful effect**. Even winning hurts. Good choices are the ones whose price you'd rather pay.

Harm and benefit are spread across five meters, so a "safe" choice in one meter is always a sacrifice in another:

| Meter | Start | Harmful direction | At the limit |
| --- | --- | --- | --- |
| **Composure** (your blood pressure; homage to Bureaucracy's meter) | 6 | down | 0 → nervous breakdown; lose one Successor |
| **Clearance** (badge level; opens sealed locations and options) | 1 | down | 0 → escorted to Orientation again |
| **Suspicion** (how much PAL/HR is watching you) | 0 | up | 10 → "a short, friendly conversation" (a disciplinary boss card) |
| **Successors** (Employee #4471-A, with B–F on file) | 5 | down | 0 → *Position Eliminated* ending |
| **Forms** (signed, stamped permission; the economy) | 3 | down | 0 → you cannot spend Forms to bypass or boost |

Sacrifices are often **other people**: a coworker companion, a society contact, the Roach Union, the intern. Those are flags and companion-trust values, not meters, and the journal remembers them.

## Rules v1: "File, Stamp, Survive" (prototype defaults for playtest)

- **Skills (0–3):** **Compliance** (procedure, quoting policy, forms), **Initiative** (bold action, running, climbing ducts), **Discretion** (stealth, lying, not being noticed), **Rapport** (charm, office politics, bribery), **Tinkering** (machines, toys, printers, traps), **Vigilance** (spotting traps, traitors and cameras).
- **Job Title card** (character select, like the Gamebook's sheet): *Intern*, *Temp*, *Middle Manager*, *Night Janitor*, *Internal Auditor*. Each sets a starting skill spread (6 points) and one perk.
- **Check:** roll **2d6 + skill + modifiers** against **7** (routine), **9** (risky) or **11** (dire). Ties succeed. **Spend 1 Form for +2** before rolling. A natural 12 earns an authored **Commendation**; a natural 2 triggers an authored **Incident Report**. Both are comic, and neither is an instant death.
- **Successors:** when Composure or a deathtrap ends you, the next Successor arrives with a new comic orientation line. They keep your flags and Clearance, carry Suspicion at half (rounded up), reset Composure, and lose your carried items. The death goes into the journal as a short card ("#4471-B: crushed by a falling org chart").
- **Secret Society card** (dealt face-down at run start): a hidden objective, one favor, and a betrayal condition. Societies: *Stapler Liberation Front*, *Friends of the Old Coffee Machine*, *Society for Accurate Minutes*, *Fourth Floor Irregulars*, *The Recyclers*, *Concerned Parents of the Toy Division*.
- **Mutation card** (dealt at run start): one powerful ability per department (examples: *Four-Second Precognition*, *Printer Whisperer*, *Paperclip Telekinesis*, *Fluorescent Camouflage*, *Perfect Signature Mimicry*). If a Witnessed tag is on the scene, using it costs +2 Suspicion.
- **Clearance gates:** some choices and locations need Clearance N. The UI shows the requirement and explains it.
- **Map mutation ("Restructuring"):** clearing a department triggers a memo that can merge, eliminate or add unvisited locations, always with a written reason. Visited history stays pinned.
- **Boss "reviews":** each department ends with an authored boss card that offers at least three routes (comply, subvert, flee or expose), each with real costs. None is a mandatory HP grind.
- **No LLM at play time.** Content is authored, the dice and state are deterministic, and the seed is persisted. Optional future atmospheric text may only re-word an already-decided fact packet, the same rule as Shifting Lands t-014.

## Recommended world (default unless Silas redirects; see PITCHES.md)

**Consolidated Wellness & Defense, Inc.** ("Making Tomorrow Safer, Today"). This is a vast campus that **restructures itself overnight**. It is supervised by **PAL** (Personnel Administration Liaison: "PAL is your pal!"), a relentlessly cheerful facility voice who loves you and is concerned about your numbers. You are new. Everyone, you included, is secretly a traitor.

| # | Department | Locations (first draft) | Boss card |
| --- | --- | --- | --- |
| 1 | **Orientation** | Security Desk & Badge Photo · Orientation Theater (psych intake) · Supply Closet B | *Your 90-Day Review, Today at 3* |
| 2 | **Records & Forms** | Pneumatic Tube Exchange · The Sub-Archive · Window 9 (Papers, Please-style desk shift) | *The Form That Requires Itself* |
| 3 | **Product Safety: Toy Division** | Concept Lab · Focus Group Room · Proving Grounds | *Snuggle Sentinel's Launch Party* (the plush bear with a warhead) |
| 4 | **Wellness & Testing** | Nutrition Studies · Cognitive Testing Chamber · the Mutation Suite | *The Final Wellness Exam* |
| 5 | **The Executive Floor** | The Boardroom Antechamber · The Founder's Office · Server Room Zero | *The Board* (and the hidden route to the **Training Simulation** true ending) |

**Recurring cast (original):** PAL; **Dale from Compliance** (your friend? your informant?); **Marguerite**, the night janitor who knows every duct; **Gus**, a seven-foot cockroach and shop steward of the **Roach Union**; **Intern Pip**, who is always about to be sacrificed; the **Founder**, whose head is kept in a jar on the Executive Floor and still chairs meetings.

**Endings (target ≥ 10):** *Employee of the Month* (complicit) · *Promoted to Management* (you became the problem) · *Position Eliminated* · *Escape Through the Ducts* · *Roach Union General Strike* · *Society Coup* · *Whistleblower* (exposed, doomed) · *Early Retirement* (the island is not an island) · *Department of Posthumous Affairs* (secret) · ***The Kind Rewrite*** (true ending: you gain admin access and rewrite PAL to remember people).

## Card format

Encounter packs live in `projects/shifting-desks/encounters/` and follow [ENCOUNTER-PACK.schema.json](encounters/ENCOUNTER-PACK.schema.json). It is a deliberate fork of Shifting Lands' v1 schema with these changes: office skills, five meters instead of HP/provisions, an up-front `cost` on each choice, an optional `roll` (a sacrifice can be certain), `requires` gates, a `tone` tag, and a `callback` field for homage cards. The validator `encounters/validate_pack.py` (run in CI by `tests/test_shifting_desks_encounters.py`) enforces the shape and the **no-clean-wins** rule.

First pack: [ORIENTATION-12.json](encounters/ORIENTATION-12.json). It has 3 locations × 4 cards, 4 good, 4 bad and 4 mixed, and every choice costs something.

## Art direction

**Mid-century corporate safety-poster illustration meets retro-futurist beige office.** It looks like screen-printed gouache with halftone grain. The limited palette is manila, carbon-paper blue, safety orange, fluorescent-tube green and oxblood. Cheerful mascot-poster compositions carry dread in the details. The world is full of pneumatic tubes, endless cubicle horizons, Brazil-like ducts, beige terminals with green phosphor, and wood-paneled executive gloom.

- **Card faces:** a single readable scene per card in 2:3 portrait, with a strong silhouette and a comic detail you notice on the second look.
- **Card backs:** a manila folder with a coffee ring, a security-stamp silhouette and a paperclip, with no lettering. Boss/review cards get an oxblood folder with a wax seal.
- **Prompts** are positive-only (Kind Robots art-prompt contract: no negations). End each one with "every surface bare and unmarked" so the renders carry no garbled text. In-game text lives in the UI, never in the art.
- **Original designs only:** no Vault Boy, Aperture, Paranoia or Brazil likenesses (see the IP guardrails).
- Generated internal art is pre-approved (AGENTS.md, 2026-07-06). Keep the prompt, model, seed, ArtJob ID and ArtImage ID for every card face in `art/` ledgers. Never list art as delivered before its URL has loaded.

## Tone guardrails

- **Darkly comic, PG-13**, the register of Paranoia, Portal or Hitchhiker's. Silas's kids are 11 and 14, and this should be a game they would laugh at.
- Deaths are **slapstick or offscreen** (crushed by a falling org chart, reassigned to the moon). There is no gore spectacle.
- **Punch up at systems**: procedure, surveillance, optimization, corporate euphemism. Don't punch down at coworkers' identities. The cast is diverse and queer-positive as a matter of course, never as a punchline.
- "Termination" and "reassignment" are the comic death register. **No suicide or self-harm jokes**: never phrase anything as "voluntary termination" of the self.
- The nuclear toys **never detonate on a child**. The stakes stay implied and the comedy comes from the corporate cheer around them.
- No real companies, products or living people.

## IP guardrails: homage, not copying

Callbacks are welcome as **short original allusions**, such as a jammed printer, a red stapler on a desk, a form numbered 27-something, plans on display in a locked filing cabinet in a disused lavatory, refreshments promised after testing, a towel, or a blood-pressure gauge. Each callback card sets `callback` so the ledger can collect them.

**Never use:** Paranoia's text, its computer's name or catchphrases, its clearance-color ladder, its secret-society names, or "Troubleshooters"/"Alpha Complex". Also avoid Aperture/GLaDOS names or lines, Vault-Tec/Vault Boy, Brazil's characters or dialogue, Douglas Adams or Infocom prose, Papers, Please's country or UI, Office Space quotes beyond a two-word nod, and any copied rules text. The rules above are our own.

## Implementation shape (Kind Robots)

- Admin preview first: `/admin/shifting-desks` with `requiredRole: ADMIN` and a discoverable Admin nav tab. Public `/play/shifting-desks` and any Arcade or menu listing are a **hard publish gate** that needs Silas's explicit approval.
- `utils/shiftingDesks/` holds a pure, tested reducer (seeded draw, meters, Successors, Suspicion, Clearance gates, Restructuring, save versioning). `stores/shiftingDesksStore.ts` is a thin Pinia 3 wrapper.
- **Reuse, don't fork,** Shifting Lands' stateless pieces (seeded RNG, 2d6 dice/result utility, the `kr-card-flip` reader and its board grid) and the Gamebook's dice tray where it fits. Do **not** mount either game's page or share their state owners.
- Content is a versioned snapshot of `projects/shifting-desks/encounters/*.json`, imported with provenance. Saves are browser-local, schema-versioned and migratable. No backend writes during play for v1.
- Accessibility: keyboard and screen reader, reduced-motion flip, the roll result announced immediately, and no hover-only actions. Device checks at 375 / 768 / 1440.

## MVP (first playable slice)

**Department 1 only:** the 12 Orientation cards plus the *90-Day Review* boss, Job Title select, the Society and Mutation cards, all five meters, Successors, a journal, save/resume, and at least 3 distinct department outcomes. It runs at the admin route with placeholder-labeled art and then with real card faces.

## Gates

- **Soft (parallel, blocks nothing):** t-002, choosing the spine, title and v1 party-mode scope from PITCHES.md.
- **Hard:** public `/play` release, any external publishing or sharing, spend, production deploy beyond the normal Kind Robots flow, and Silas's final visual and fun verdict.

## Open questions (tracked in t-002)

1. Spine: the recommended A+C+F+B+D+G synthesis, or another pitch?
2. Title: *Shifting Desks* or one of the alternates?
3. Is party mode ("Accusation Meeting") v1 or post-v1?
