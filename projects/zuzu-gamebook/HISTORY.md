# zuzu-gamebook — task history archive

Full `note:` prose for completed zuzu-gamebook tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Pure TypeScript gamebook reducer, dice/combat mechanics and contract tests

<!-- note:begin t-002 -->
Extend the first deterministic preview reducer from kind_robots#3355 in utils/zuzuGamebook/; no browser APIs, no Math.random inside the reducer. Challenge outcomes, victory/defeat, effects, inventory capacity, powers, flags, mutually exclusive conditions, dice roll logs, resource caps, valid transitions, save-version migrations. Add contract tests to CI for replay determinism and each combat interaction.
2026-10-12 reconciliation: built and live. utils/zuzuGamebook/adventure.ts is the pure reducer (no browser APIs or Math.random inside it; dice from the run's seed), and verifyZuzuGamebook.test.ts checks replay determinism, combat, saves, power costs and the 375-section graph; the book launched under t-010. The status stayed ready by oversight.
<!-- note:end t-002 -->

## t-003 — Build beautiful standalone /play/zuzu-gamebook reader and character sheet

<!-- note:begin t-003 -->
Evolve the private-preview route and layout started in kind_robots#3355: Projects tab registration and placement, image-dominant scene frame, readable story and two-to-four consequence-rich actions, HUD, expandable character sheet, combat choices, accessible reduced-motion 3D-like dice roller, inventory, health/resolve and save/restart. Respect AGENTS.md: components use a Pinia store for localStorage/state; no live LLM. An admin-preview tab until explicit public-launch verdict.
2026-10-12 reconciliation: built and live at /play/zuzu-gamebook (launched under t-010): illustrated reader with plate-above or portrait-right layouts, HUD, character sheet, dice roller with reduced-motion fallback, combat moves, inventory, health/resolve and save/restart through the Pinia store. Polished on 2026-10-11/12: italics for spoken words, keyboard play (1-9), focus and scroll reset on each new section. The status stayed ready by oversight.
<!-- note:end t-003 -->

## t-004 — Book One graph and all authored scenes (~400 numbered sections)

<!-- note:begin t-004 -->
PLAN 2026-10-10: build against BOOK-ONE-OUTLINE.md (nine acts with budgets, act entry/exit contracts, dilemma catalogue, Honor/Taint tallies, flag registry, 13 endings, art plan). PROGRESS 2026-10-10: Acts I-IV written to budget as act modules (kind_robots utils/zuzuGamebook/acts/act1-4.ts, 128 new sections, book at 196); Acts V-IX in progress (wave 2, same contracts; done the same day: 375 sections, 13 endings, kind_robots#3437). Engine: reroutes of checked choices via #success/#failure, maxTaint gate for the best ending. PROGRESS 2026-10-09: 68 sections / 8 endings across six acts that follow Book One's chapters (utils/zuzuGamebook/book.ts), the mission rewritten welcome-first, clues paying off as roll bonuses, flag-gated choices with disabled hints, scene effects, and a 6000-walk seeded exploration test. Next increments: deepen each act toward ~400 (side encounters per WORLD-GUIDE gazetteer, Dustwater, a novice ally route, more consequence plates), then the later acts' plates via t-006. Expand the initial 20-scene, six-ending preview from kind_robots#3355 to a full book. The Bell That Never Rang. Build original branching scenarios that echo watering hole, wounded coyote, Hollow Bell, fennec siblings, apples, missing-child posters and corrupted mission without rewriting BOOK-ONE.md. Write ~400 unique sections (Silas 2026-10-09: "we should have many more chapters"; Fighting Fantasy's standard is 400, the Sorcery! books 456-800), 10-14 endings with genuinely different outcomes and multiple routes through each main act. Grow it an act at a time, each act a shippable PR that keeps the graph and state tests green. Track routes, flags and alternate endings. No endless choice loops or unknowable fails. Pure static bundle. PACING (Silas 2026-10-09): the abbess must not open by attacking. The mission act starts as a welcome: she greets Zuzu and the children, offers food, beds and work, and the kindness is real-seeming for several sections (meals, chores, a night's rest, the other nuns, the cobwebbed playground). Suspicion builds from clues (posters, absent footprints, a locked door, a child who stops appearing) and Mercy or Sense checks before any confrontation. Fighting her is a late consequence of what Zuzu uncovers, and some routes never fight her at all. WORLD HUB (2026-10-09): name characters, items and places as the worlds/zuzu canonical profiles do (Coyote Vagrant, Fennec Sister and Toddler, the Abbess, River Croc; Apples for the Road, the Drifter's Bandage, the Sister's Dagger; kasa and katana are worn, not carried). No Showdown-only fighters, no Old Komodo, no legacy KR filler lore. A new named character or place meant to outlive this book is proposed to Book One / the registry first.
2026-10-12 reconciliation: done. Book One ships 375 sections and 13 endings across nine acts (utils/zuzuGamebook/book.ts and acts/), within the canon rules above; verifyZuzuGamebook.test.ts proves the graph acyclic, every ending reachable and no softlock. On 2026-10-11/12 the eight short original endings were rewritten to full length and duplicate section titles made unique. The status stayed ready by oversight.
<!-- note:end t-004 -->

## t-005 — Scene art inventory, cinematic layouts and repeatable ArtJob manifest

<!-- note:begin t-005 -->
2026-10-09: done for the 20-section preview (kind_robots#3389). Every section has its own Arthemy plate: 15 vetted intro music-video keyframes and seeds, plus 5 gamebook renders (art/ROUND-1.yaml, editorial verdicts inline). The manifest is kind_robots utils/zuzuGamebook/art.ts (ArtImage id, source, alt, fit). Only the poster wall is a stand-in; Arthemy draws the sketched subject rather than the wall twice over, so retry it as a Kontext edit of an existing street plate. Continuing art for new sections is t-006. History: the initial 10 vector scene plates in kind_robots#3355 were placeholders, not finished generated art. Read ART-DIRECTION.md and comic locked cast. Make section-level art prompts, portrait/splash/widescreen/aftermath plates and aspect ratios for every scene/outcome. Add provenance fields (prompt, model, lane, source, ArtJob, ArtImage, delivery URL, reviewed). Prefer proven comic reference images. Avoid placeholder artwork presented as generated/finished.
<!-- note:end t-005 -->

## t-006 — Independently enqueue and review gamebook illustrations in batches

<!-- note:begin t-006 -->
Art generation explicitly pre-authorized for internal project use. Use the durable /api/art/enqueue ArtJob pipeline with stable idempotency and canonical series/character settings; check DONE AND reachable delivered URLs, verify Zuzu costume and the banned-terms guardrails. Round 1 (art/ROUND-1.yaml) covered the preview's gaps; each new act from t-004 gets its plates the same way, reusing vetted comic/MV renders first (search the worlds/zuzu ledger inventory), prompting from the registry's locked cast ArtImages, and adding each new ledger to the registry's inventory (assets/ledger-part-05.json or a new part) plus any exported plate to assets/repository-media.json in the same PR; tests/test_zuzu_world_inventory.py enforces it. Lessons: "poster" is refused by the KR prompt contract; "smoking blade" draws a cigarette; empty scenes need "(no characters:1.4)" plus figure/person negatives. Begin with cover, hero, first ten scene plates, dice/character-sheet motifs and consequence plates, then continue in book-sized batches. Do not incur paid external spend. ROUNDS 2026-10-10: ROUND-4 (34 jobs, Acts I-IV plates) and ROUND-5 (30 jobs, Acts V-IX plates incl. one Kontext restaging of the locked Abbess front) queued; each plate has a stand-in key in kind_robots art.ts until its keeper is reviewed and exported. ONE PLATE PER SECTION (Silas 2026-10-10: "if we have 400 sections, we have 400 pieces of art"; "some are shown horizontally and some vertically, left right top bottom, for variety"): ROUND-6 queues 302 jobs (151 Act I-IV sections x 2 seeds, mixed wide/tall/square); keepers are keyed by section id in art.ts and the page lays tall plates beside the text, wide ones above or below. ROUND-7 queues the other 436 (Acts V-IX and the 12 endings without their own plate): every one of the 375 sections now has its own plate in the queue. REVIEW 2026-10-10: round 4 kept 8/17 plates, round 5 kept 8/15 (the 16 replace stand-ins); round 6's first 46 sections kept 21 (kind_robots utils/zuzuGamebook/sectionArt.ts, scenes/sections/). Lesson: the {ZUZU} token without 'solo' drew a second small koala beside or on Zuzu in most renders; the 268 still pending Zuzu jobs were edited in place to add '(only one koala:1.3)' and second-koala negatives. Rejected Zuzu sections get rerolls once round 7 drains. REVIEW 2 (12:50): round 6 batch two kept 45 of 77 sections (58%, up from 46%) - 66 per-section plates live. [...]
[Earlier history (15,002 chars) archived verbatim to projects/zuzu-gamebook/T006-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
Finish scene-fidelity round 16 delivery: verify completed private ArtImage URLs, make an authenticated review/export pipeline, and retire temporary assets only after approved final art exists.
Nine Round 16 ArtJobs and ArtImages are DONE in the durable ledger. Implement authenticated URL/media decode/size review for all nine; never auto-promote unreviewed candidates or commit private originals.
Round 16 ArtJobs 44243-44251 / ArtImages 252163-252171 all returned DONE, readable media URLs, valid formats/dimensions (verified by action 40025486936), but 0/9 visually matched the scene. Recorded all nine editorial reject reasons in Round 16 ledger. Merged Conductor PR #6548 (ephemeral authenticated editorial contact sheet) and #6549 (nine subject-focused Arthemy house rerolls in ROUND-17-SCENE-FIDELITY.yaml). Both green. Fresh Round 17 ArtJob IDs not yet persisted; Auto Art Generate run 40026323889 queued behind an existing earlier run. Next action: inspect Round 17 queue IDs, wait for actual DONE/render media, review new images, choose only story-faithful keepers, export WebPs via reviewed Kind Robots PR, update manifests and retire placeholder SVGs. The a2-gift raccoon-head plate and temporary bell/bloom SVGs remain unresolved on the published site; do not call this task done.
Human-directed two-stage internal art generation: submit Krea 2 compositions for three mismatched scenes, select by scene fidelity, then conservative Arthemy img2img; keep publication and unreviewed promotion gated.
Implement Krea 2 Round 18 (9 compositions, auto-submit), dormant Arthemy Round 19 (sdxl-img2img at 0.28/0.43), proof-of-delivery + visually scored gate and tests. New workflows with no public thumbnails.
Merged green Conductor PR #6555 (0eb74342bf0044a1693f3558c0257e734ddd5b7e) for Krea2 -> gated Arthemy img2img. Round 18 has 9 private auto-submit Krea compositions. Round 19 remains dormant until the real Krea images are DONE, visibly reviewed, score >=7/8 and all critical scene objects pass, and reviewed receipt SHA matches. The activated stage creates 6 Arthemy source-preserving img2img jobs with denoise .28/.43. A new post-sweep review workflow verifies delivery but never publishes private contact sheets to public GitHub artifacts. PR CI, security and handoff all succeeded. Auto Art Generate run 40036731336 launched after merge; confirm real new job IDs in ROUND-18 ledger before claiming submission accepted. Once Krea is reviewed, activate Round19 via another green PR and export only approved final WebPs in kind_robots. Temporary SVGs and wrong raccoon-head scene remain to replace. Task is NOT done.
2026-11-02 PT: ROUND-18 reviewed. a2-bell-view passes 8/8 (gb18-a2-bell-view-1, ArtImage 252193) and a4-bloom passes 7/8 (gb18-a4-bloom-3, 252199). a2-gift failed every seed (best 6/8: the mark read as a cartoon face; seed 2 is a modern zip pouch; seed 3 has a gallows-like frame). Its three rows are rerolled in place (the activator requires exactly 9 subjects), with the mark described as a carved bandit's domino mask on a single upright post. Round 19 activation waits on the gift re-review. Then fill ROUND-18-SELECTIONS.yaml from a fresh krea-receipt.json and run activate_zuzu_gamebook_stylepass.py --receipt.

Merged Conductor PR #7308 (b3647f4cddb8e05b0de26358b1e5813054f76055) with all four workflows green: ROUND-20 manifest defines 14 PRIVATE Arthemy candidates for seven newly authored/unpainted route and fairness scenes, plus a source-backed 35-gap scene art audit. Auto Art Generate workflow #43188873701 triggered from the main push, but actual ArtJob IDs, DONE render receipts, visual review and exported WebPs are NOT yet verified. Keep t-006 ready, not done, until delivery and existing Round-17/18 stage-two review are completed; do not call artwork generated or game playtest-ready merely because the ledger was submitted.

2026-11-14 PT: Round 20's 14 render candidates already have DONE ArtJobs 68674-68687, no duplicate submissions. New ROUND-21-PRIORITY-SCENE-FIDELITY.yaml queues 20 PRIVATE new candidates (10 high-value early-book unregistered sections x two compositions) at priority 1000; their actual ArtJob ids and visual keeper acceptance must be confirmed after merge. Keep task active for source-backed delivery/review, additional unregistered scenes, two-character LoRA corrections and final WebP integration.

2026-11-14 PT: Conductor #7387 merged at e22e260 after all 6 current-head workflows passed. Round 21 has 20 high-priority (1000), private, auto-submitted candidate cells for ten previously unregistered scene plates. Prior Round20 14 jobs (68674-68687) already DONE and were not duplicated. Auto Art Generate run 43595625564 was in progress at closeout; require actual new ArtJob IDs, DONE, visual review, accepted WebPs and exact section registration before closing t-006. A duplicate updated YAML key introduced by the connector claim was repaired in #7387; processor now reached review. Return t-006 ready for outstanding delivery/review and t-012 paired-cast fidelity.

2026-11-14 PT latest verified main: 385 authored Book One sections, 371 exact SECTION_PLATES bindings and 371 corresponding checked-in section WebPs (all present); 14 exact registration gaps are a1-ridge-retreat, a2-bell-view, a2-wax, a3-apples-reach, a4-bloom, a4-well-scatter, a4-well-slip, a5-wellhouse-reckoning, a8-behind-the-altar, a8-give-ground, a8-under-the-wall, a8-wounded-flight, apple-tree, ending-water. Round20 covers seven with 14 DONE images 270438-270451; Round17/18 has DONE candidate art for apple-tree, a2-wax, a3-apples-reach, a2-bell-view, a4-bloom; ending-water already purpose-painted legacy kasa-on-water. New Act V a5-wellhouse-reckoning lacked any art queue entry; Conductor PR #7409 MERGED after all four checks green, two private max-priority Arthemy candidates in ROUND-22-WELLHOUSE-RECKONING.yaml. Auto Art Generate run 43652630082 was queued; ArtJob IDs pending. The only remaining work for t-006 is authenticated actual-frame fidelity review, keeper selection, approved WebP export, exact section registration, and re-running source/render tests; do not claim DONE images imply visually accepted artwork. Keep t-012 two-character LoRA gate separate. No public release or playtest promotion yet.

2026-11-15 PT close-out: kind_robots #5192 merged (b01655b, 13/13 checks green). All 14
remaining plate gaps resolved after real-pixel review: six Round 20 keepers, Round 23
house-style passes 272618 (bell view) and 272620 (desert bloom) replacing both SVG
stand-ins, and six purpose-painted plates bound to their sections. 385/385 sections and
all 15 endings have an exact painted plate, enforced by contract. Per-image verdicts in
art/ROUND-20, ROUND-22, ROUND-23. Evidence: projects/zuzu-gamebook/PLAYTEST-
READINESS-2026-11-15.md.
<!-- note:end t-006 -->

## t-007 — Integrate authored story bundle, chapter pacing and illustration manifest

<!-- note:begin t-007 -->
Validate all node ids and choice targets, all required effects/flags/items, encounter termination, at least eight reachable endings, every ending reachable from the start, and no no-win progression trap. Render real hero/environment/aftermath images with meaningful alt text and fallbacks. Add a test that explores reachable state as well as node graph shape.
2026-11-04 PT (round 3, pacing): Measured chapter pacing over 4,000 seeded walks (per- act section counts, single-way page chains, act transitions). Shipped: - Two Act VIII bridge sections (a8-under-the-wall, a8-behind-the-altar) for the three Act V outcomes that cut straight to the altar set piece. These were mission/investigate#success, crypt- glimpse/confront and a5-crypt-wren/hide, and they skipped Dustwater and the night road with no time passing. - Arrival lines for the Hollow Bell, Dustwater and mission-at- night act openings. - An "Act N · NAME" banner above the title on the first section of each act (actOpening). Phones never showed the chapter before. - A graceful missing- plate fallback: sectionPlate no longer throws, and stage and trail images fall back once on a load error. - A pacing contract in verifyZuzuGamebook: no backward act edges; act- skipping jumps must land on bridges; per-act section bands; at most 5 single-way pages in a row. Goldens are unchanged, saves are intact and no art was added. Remaining: Act IV is the longest act (16–25 sections, decisions every 1–2 pages). Act V's gate "deliver" choice makes the central act 2 pages on about 40% of random walks; that needs an editorial call. The Night Road long way (5 single-way pages) is kept as a deliberate slog.  Merged as kind_robots #4799; back to ready for the remaining scope.

Scoped Act V delivery aftermath choice implemented on worker/zuzu-gamebook-t-007-delivery-aftermath-a8c1; existing art plate reused. CI and story contract verification pending; t-007 retains further scope.

2026-11-15 PT close-out: Act V deliver shortcut now carries a moral aftermath
(kind_robots #5176, merged). Act IV length and the five-page Night Road slog are kept as
deliberate pacing, pinned by the act-pacing contract. 385 sections and 15 reachable
endings pass on main. Evidence: projects/zuzu-gamebook/PLAYTEST-READINESS-2026-11-15.md.
<!-- note:end t-007 -->

## t-008 — Combat, powers, dice, inventory and save/resume UI polish

<!-- note:begin t-008 -->
Interactive combat log and enemy cards, visual hit feedback, distinct animated rolling dice with result readable without animation, keyboard and screen reader announcements, save portability, combat outcome illustrations, mobile character-sheet drawer and recovery paths.

Adversarial recovery and full-pack loot changes implemented on worker/zuzu-gamebook-t-008-loot-recovery-g6e8f4. Pending CI and scoped PR review.

2026-10-22 PT: Merged reversible fix PR silasfelinus/kind_robots#4029 (squash bb7e04953eff9a7a08ab0931d573739835b0333a) after all 16 current-head GitHub workflows passed. Inventory overflow now pauses for explicit replace-or-leave, with V1 save compatibility and regression tests; a recoverable previous journey survives restart, retaining the existing confirmation. No ArtJobs or external publishing in this scope. Re-arm t-008 for its uncompleted combat log/feedback, portable saves and responsive acceptance work. Priority triage: (1) full start-to-ending witness transcripts for all 15 endings including Wren's Lamp via t-011/t-009; (2) combat strategy win-rate calibration for Guard/Feint versus Quiet Draw; (3) eight shared-art fallbacks via t-006/t-012; (4) remaining UI polish and device testing. t-009 remains waiting on t-006, t-007, and t-008.

2026-11-04 PT: Round-5 slice of t-008 is ready to land as a reversible PR. It adds a
per-round combat log: each round shows the move, both dice and the modifier against the
target, damage both ways and HP on both sides. The battle panel lists the newest three
rounds, a "Fight won/lost" report with the full log stays on the next page until Zuzu
moves on, and the newest round goes to a screen-reader live region. Story and move cards
now quote the engine's real odds: "Sense 8+ · 58%" with knowledge bonuses counted, and
target -2 when the foe is open. Cards also show Resolve and item costs (uses vs needs),
healing and finds. The character sheet explains each pack item and when it is used up,
and the special arts list now matches what the book actually offers. A toolbar "Saved"
mark appears after each save, or "Not saved" when storage is blocked. The Ledger can
copy a portable ZUZU1 save code and load one back with no server; codes are validated,
and the replaced journey goes to the recovery slot. Old saves load, including mid-fight
ones, and all 15 golden fingerprints are unchanged. Remaining: device testing on real
phones and tablets, chip-wrap check on the narrowest cards, a mobile character-sheet
drawer (the sheet still swaps out the reading pane below lg), animated hit feedback and
combat outcome illustrations, combat win-rate calibration (Guard/Feint vs Quiet Draw),
and shorter save codes (compact the visited trail) if QR sharing is wanted.  Merged as
kind_robots #4826.

2026-11-06 PT: Round-6 slice of t-008 is ready as a reversible PR. Below lg the
character sheet no longer replaces the story. It is a modal drawer over a dimmed reading
pane: a bottom sheet on phones and a right drawer on tablets. It has dialog/aria-modal,
a "Back to the story" button, backdrop and Escape close, a Tab trap, focus moved in and
restored, and an inert pane. Desktop keeps the same side column. Check-card chips no
longer state the roll twice: noteBeyondRoll drops "(Sense · 9)" and a failure cost moves
to the card's bottom line. At 390px the worst chip went from 6 lines covering the hint
to 2–3. The shared hand wraps chips between their parts and moves the shortcut key
inline when a hint exists, which also fixes the key covering hints in all 11 games.
Combat rounds now flash and shake on a wound and pop and float on a landed blow; reduced
motion keeps only the colour flashes, and loading a mid-fight save replays nothing.
Saves and fingerprints are unchanged. Verified with Playwright at 390/768/1440 on a
local dev server. Remaining: tests on real phones and tablets, combat outcome
illustrations, combat win-rate calibration (Guard/Feint vs Quiet Draw), shorter save
codes if QR sharing is wanted, and the Ledger dialog may need the same under-header
placement on tablets. Merged as kind_robots#4864 (2026-11-06, with a capture-group guard
fix in terms.ts).

2026-11-15 PT close-out: combat calibration pinned by a seeded 400-seed test in
kind_robots #5192 (merged b01655b): Guard best vs the Abbess (66%), Quiet Draw best vs
crocodile (93%) and the jackal band (50%), Feint the best free answer to the band once
Resolve is spent, Strike never best. UI polish shipped earlier (#4826, #4864); every
fight-outcome section now has a painted plate. Shorter save codes remain optional
polish. The 2026-11-15 heal-before-hurt preview slice (#5191, latent bug) moved to
playtest_iteration t-018 with its claim intact. Evidence: projects/zuzu-
gamebook/PLAYTEST-READINESS-2026-11-15.md.
<!-- note:end t-008 -->

## t-009 — QA and editorial playtest of every route, ending and device

<!-- note:begin t-009 -->
Automated deterministic playthroughs, randomized seeds, fairness/softlock tests, inventory abuse checks, all images delivered, WCAG-conscious keyboard/touch/reduced motion, and screenshots at 375px/768px/desktop. Real preview inspection before marking ready; flag public publishing and Silas's creative acceptance as explicit human gates.
2026-11-15 PT QA close-out: npm run test:zuzu-gamebook passes on #5192 head (graph, reachability, acyclic, act pacing, stateful exploration, plates 385/385, items, dice, 15 golden witnesses, 1,500- and 12,000-walk fight batteries, wounded matrices, saves, power costs, title/settings/endings/scrapbook). Live device pass on kindrobots.org at 390/768/1024/1440/1280x600: no overflow, no page errors, plates load, keyboard reaches choices. Minor: phone card captions are small (about 9px), flagged as a playtest question. Evidence: projects/zuzu-gamebook/PLAYTEST-READINESS-2026-11-15.md.
<!-- note:end t-009 -->

## t-010 — Public launch and Silas's visual/story verdict

<!-- note:begin t-010 -->
Present final accessible preview, art coverage, combat/rules balance, endings checklist and gamebook tone for Silas's verdict. Do not expose publicly or assert production deployment until approval.
2026-10-10: Silas, verbatim: "cool, this is good enough for public facing, move the gamebook out of admin". Public-launch verdict given ahead of the t-009 QA pass; kind_robots#3413 drops the admin gate (page + Play tab requiredRole). Merged is not deployed: live once Alexandria's deploy picks up main. t-009 QA continues post-launch.
<!-- note:end t-010 -->

## t-012 — Two-character Zuzu plates: the LoRAs exist but don't stack (Zuzu fuses with a second LoRA; abbess LoRA paints human faces)

<!-- note:begin t-012 -->
Silas, 2026-10-10: "go ahead for workarounds. We can fix things later when we have the LoRAs built, that task got moved to later because we had too much art that was going to be made...ironically, since by this point it would have helped to have them." Waits on comic-creator/t-016 (character LoRAs for Zuzu and the fennec siblings). Round 9 recomposed every section that pairs characters around one figure, a detail or a place, because the Arthemy house lane fuses Zuzu with whoever shares the frame or leaks his costume onto them. When the LoRAs land, redraw those sections (ROUND-9.yaml subjects whose original act*.json entry had two or more figures) as the two-character scenes the text describes, in the house lane with the LoRAs.
2026-10-11 Silas: "Loras now exist. Time to do a pass, correct bad art, and give this an overall polish." (comic-creator/t-016 done: zuzukoala 4593, zkasister 4583, zkatoddler 4588, zkacoyote 4578, zkaabbess 4595.) ROUND-12 (ArtJobs 37005-37024) tested ten paired scenes with every present character's LoRA: the sister and the toddler together render cleanly (survivors and a3-shade kept), but Zuzu still fuses with any second LoRA (two koalas, his hat on the fennec, fennec ears on him) and the abbess beside anyone gets a human face. So paired Zuzu moments stay single-figure, now drawn on-model. A plate audit of all 365 live plates flagged 95: 79 of the 102 Zuzu plates off-model (bear or dog face, two swords, no hat or poncho) and 16 others (blood, a hanging, human faces, a modern pistol). ROUND-13 (170 jobs from 37025) redraws the 85 Zuzu-alone compositions with his LoRA; ROUND-14 recomposes the 17 Zuzu ensembles, the 16 other flags and the 4 stand-ins; ROUND-15 (94 jobs from 37195) redraws the 47 sister/toddler/coyote/abbess plates with their LoRAs, kept only where better. The t-006 dependency is dropped: t-006's last four stand-ins are now redrawn here (ROUND-14), so t-012 no longer waits on it. REVIEW 13-15 (12 Oct): every redraw judged against the live plate. ROUND-13 kept 77 of 85 Zuzu-alone redraws (the zuzukoala LoRA puts him on-model: koala face, kasa, zigzag poncho, one katana); ROUND-14 kept 29 of 37 recompositions, including the last four stand-ins (a1-two-shadows, a4-well-battle, a8-fire-cells, a8-fire-altar); ROUND-15 kept 1 of 47 (the abbess LoRA gives human faces even alone in a scene, and the sister/toddler pair swaps outfits, so those live plates stay). 107 plates replaced. Rejects: tails and high heels on Zuzu, a modern paved road, fusion with a second figure, drowned-body and urination reads. ROUND-16 takes the 18 still left (two stand-ins found by the sweep, a2-bell-view and a4-bloom, plus the live plates whose candidates all failed); the LoRA negative now carries tail, high heels and asphalt road.
2026-10-11: the character LoRAs exist (comic-creator/t-016 done). Any ledger with `series: zuzu-koala-assassin` (every art/ROUND-*.yaml here) now gets them by default from enqueue_art_requests.py: each subject carries the LoRAs of the characters its prompt names (projects/comic-creator/cast-loras/zuzu-koala-assassin.yaml). The coyote's v1 LoRA still draws his right hand (t-023); stump plates keep the masked bandage edit. Following ROUND-12 above, Zuzu and the abbess are `stacks: false` there: a subject naming either beside another character gets no default LoRAs, so the explicit per-subject `loras:` in ROUND-12..15 stay authoritative.
2026-11-02 PT retitle (Silas asked why it still says the LoRAs don't exist): they do, since 2026-10-11 (comic-creator/t-016). The old title was stale. What is left is the stacking problem above: Zuzu plus any second character LoRA fuses the two figures, and the abbess LoRA gives human faces even alone, so paired Zuzu moments ship as on-model single-figure plates. Real fix candidates: render each figure alone with its own LoRA and composite (Kontext reference-stitch, as enqueue_art_requests.py `reference_image_id` already supports), regional LoRA masks in ComfyUI, or a retrained abbess LoRA.
2026-11-15 PT close-out at the rendered-frame level: no fused or human-faced figure ships. Paired Zuzu moments ship as on-model single-figure, empty-scene or still-life plates, each checked against its section text (Rounds 13-16 replaced 107 plates; this pass rejected the human-faced nun, dog-for-Zuzu and human-figure candidates). Composite or regional-mask two-character art stays optional t-011 polish. kind_robots #5192. Evidence: projects/zuzu-gamebook/PLAYTEST-READINESS-2026-11-15.md.
<!-- note:end t-012 -->

## t-013 — Wounded-route risk signals and meaningful retreat paths

<!-- note:begin t-013 -->
PR #4037 documented a 6-encounter, 4-health, 3-Resolve, 4-strategy adversarial matrix. At 3 HP, none of the four benchmarked tactics won the crocodile, Abbess or Hollis's band battles in 90 deterministic seeds per setup. Not all losses are dead ends: some authored scenes restore HP and continue, which must be preserved. Audit actual player routes for avoidable and forced encounters; identify when a wounded player is funnelled into near-certain defeat without fair foreshadowing or a meaningful alternative. Add concise one-screen risk cues or narrative retreat options where earned, not blanket stat buffs or free escapes. Preserve Honor/Taint, replay the 15 frozen ending fixtures, and extend adversarial route tests across injured-entry cases. Require current-head TypeScript, contract tests, and any relevant responsive preview checks.
First wounded-route slice: sister-free flag unlocks a costly alternative to the Abbess battle after the wound. New scene and low-HP/Resolve route regression assertions; awaiting PR CI. Other encounters remain for the wider t-013 audit.
2026-10-25 PT: Merged silasfelinus/kind_robots#4200 (squash 3cfe24528406f7eb77b34c10e1b1a2109fe07b31) after all 13 exact-head workflows passed, including all four contract shards, TypeScript, formatting and 15 golden replay witnesses. Added sister-free-gated retreat after wounded Abbess bargain: rescue both children and leave the breach unresolved, or turn back to fight. Tests cover 1/3/6/12 HP, 0/4 Resolve, locked sister condition, moral flags and preserved positional choice indices. No ArtJobs or production deploy. Remaining t-013: Croc/Hollis low-HP route fairness, real seeded wounded-entry witnesses and broader player risk-cue audit; new scene currently shares sister-dagger art pending its own keeper.
Hollis wounded-route slice: earned sister-trust and bandage retreat after failed parley; adds explicit failure risk cues, preserves existing choice indices, and tests low-health and exhausted routes. Kind Robots implementation PR to follow; t-013 remains open for Croc and complete seeded-route audit.
2026-10-26 PT: Merged kind_robots PR #4205 (squash 899887e371b6e4257edaf0a8c0576fba56f494a4). Hollis failed-parley now offers an earned sister-trust + bandage escape through a new scene, at a cost of 1 Resolve and the 2-HP dry detour. Shadow/Mercy checks warn of failure. 1/3/6/12 HP x 0/4 Resolve, lock, no-heal, Honor/Taint and positional-choice regressions added. [...]
[Earlier history (2,607 chars) archived verbatim to projects/zuzu-gamebook/T013-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
Scoped Abbess trust/risk-cue regression ready for PR: retired the nod rescue after later sister estrangement, warned of the exact three-HP wound on two risky choices, and added seed-48 precondition plus reducer guard tests. Full from-new-game Abbess wounded journeys and dedicated art remain open.
2026-10-26 PT: Merged Kind Robots PR #4234 (squash dbf5d25ca91ef73433d8b922efc8886ec8bafac8) after 13/13 exact-head workflows passed, including TypeScript, formatting, four contract shards and 15 golden endings. Abbess knifepoint sister rescue now retires after sister-wary despite prior sister-trust; two failed rolls explicitly warn of three-HP wound. Seed 48's legitimate trusted/estranged preconditions plus isolated Abbess reducer tests verify locks and positional choices. No ArtJobs or deployment. Remaining: full from-start wounded Abbess traces, other encounter fairness, stale sister-trust bonus audit and dedicated art. Evidence kind_robots#4139 comment 6419414000. Keep active, not For Human Gate.
Scoped fix prepared: remove stale sister-trust dice bonuses after sister-wary at Abbess standoff and sister's knife, with deterministic seeded regression. Implementation branch worker/zuzu-gamebook-t-013-trust-bonus-x7r4; PR and CI pending.
2026-10-26 PT: Merged kind_robots PR #4239 (squash 1ead308f4ec25d8220b2b2891ab83afd394ef0e6). Removed stale +2 sister-trust dice bonuses after sister-wary at Abbess standoff and sister's knife, preserving choice IDs and saves. Seed 28 regression verifies both outcomes at 3 HP/zero Resolve. All 13 exact-head workflows passed on a947285bc, including TypeScript, Prettier and four contract shards (run 40382492082). No ArtJobs or deployment. Remaining: full seeded wounded Abbess witnesses, wider fairness/risk cues, dedicated art, complete game QA. Evidence kind_robots#4139 comment 6424867166. Keep t-013 ready and game active; no human gate.
Testing a legitimate fresh-game wounded Abbess route through the freed-sister rescue, retreat, and return-to-fight branches. Kind Robots worker/zuzu-gamebook-t-013-wounded-witness-k4n9; PR and exact-head CI pending.
2026-10-26 PT: Merged Kind Robots PR #4244 (squash d81e2e899a7e4e8cfc75ef0a9e30624a9a639fd6). Real startRun seed 1, 43 legal moves, 7 HP reaches the freed-sister wounded Abbess route; escape and return-to-fight branches, replay and save validated. All 12 exact-head workflows passed at 9e8b74a87, including four contract shards, TypeScript and formatting. Evidence: kind_robots#4139 comment 6427595903. No ArtJobs or deploy. Remains: naturally lower-HP combat witnesses, forced-fight risk audit and dedicated scene illustration. Keep active, not For Human Gate.
2026-11-04 PT: Forced-fight audit slice. All 36 choices that lead into the 6 battles were audited, and none warned of a fight or said whether a loss is final. In 20k seeded walks, 1498 ended with an Abbess loss at ending-altar, often entered at 1 HP. Added pure fightAhead/fightCue in adventure.ts. They follow single-exit scenes, project sister-free and other flags, and flag deadly vs survivable losses and wounded entries within two blows. Choice cards in zuzu-gamebook.vue now show a Fight chip, a "Wounded, N HP: losing ends the journey" line and the foe/stakes caption, so cellar cut vs charge now visibly differs. Tests pin every fight-entering choice, the cellar/Hask/croc/Abbess cues, the real wounded-Abbess witness, and a 1500-walk seeded battery: 1548 fights announced, 174 wounded entries flagged, 224 final and 231 survivable losses matched their cue. Goldens unchanged. Kind Robots PR #4770 from a patch on base 050b23eb. Full vue-tsc was OOM locally, so CI decides. No art or deploy. Remaining: whether the no-sister wounded Abbess refusal (a8-voice-wound, Taint<2) needs an earned narrative alternative, and a responsive check of the cue at 390/768/1440.
2026-11-04 PT: forced-fight cue slice merged as kind_robots #4770 (squash 1107d7d). Back to ready for the rest of t-013: an earned narrative alternative at a8-voice-wound for a wounded no-sister journal, and a responsive check of the cue at 390/768/1440.
2026-11-04 PT: Silas: 'zuzu, who is male, should probably not have an unwinnable fight.' kind_robots #4780 gives each of ten scenes that could force a 0%-win fight (a8-voice- wound, stabbed, a8-word-broken, abbess-strikes, a8-word-kept, a8-standoff, a8-standoff- break, cellar, a4-well-toll, a4-well-grab) a costly non-fight way on (give ground and bind with the bandage, run with the freed children, carry word, or drop goods and run). 12,000-walk battery: no forced hopeless fight; fixtures and fingerprints unchanged.

kind_robots #4780 merged (no forced unwinnable fights). Remaining: earned narrative alternative at a8-voice-wound for wounded no-sister journal; responsive check of fight cue at 390/768/1440.

2026-11-04 PT clarification: #4780 already ships the earned alternative at a8-voice-
wound for a wounded no-sister journal: give ground to a8-give-ground, bind with the
bandage (+2 HP) and return, or climb out and carry word. Only the responsive check of
the fight cue at 390/768/1440 remains.

Waterhole crocodile fight-risk cues and route assertions submitted in Kind Robots PR #5166 at f0dbf960; exact-head CI pending. This is a partial t-013 slice; retain remaining wounded-entry fairness work.

2026-11-15 PT close-out: crocodile risk cues merged (#5166); earned wounded retreats
(#4780). Responsive check of the fight cue on live kindrobots.org at 390x844, 768x1024,
1024x768, 1440x900 and 1280x600: FIGHT chip and 'Wounded, 1 HP: losing ends the journey'
render on the wounded-Abbess choice beside the earned give-ground exit; no overflow, no
page errors. Screenshots in projects/zuzu-gamebook/playtest-evidence-2026-11-15/.
Evidence: projects/zuzu-gamebook/PLAYTEST-READINESS-2026-11-15.md.
<!-- note:end t-013 -->

## t-015 — Main-game standard: audit and close the gaps for Zuzu Gamebook

<!-- note:begin t-015 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

AUDIT DONE 2026-11-12: projects/zuzu-gamebook/STANDARD-AUDIT-2026-11-12.md holds the Met/Partial/Missing table, a proposed achievement list with award points, character-fit notes and the three smallest next PRs. Start there.

Start with the audit table from docs/agents/main-game-standard.md (title screen; settings menu; save/load and persistent progress; 12+ achievements; scrapbook; multiple endings with painted plates; customizable characters; 3+ replay hooks), marking each Met / Partial / Missing with evidence (file, route, live record). Put the table in this note and the first PR. Then close each gap in small CI-tested PRs; queue any needed ending, scrapbook or portrait art in an auto_submit ledger.

Character customization is EXCEPTED for this game: Zuzu stays the fixed protagonist (Silas 2026-11-11). Every other item applies.

Achievements are tracked by their own task; this one covers everything else.

Scoped implementation PR prepared: Zuzu's art-led title screen, four reading controls, painted endings, and persistent per-journey scrapbook with regression coverage. Main-game-standard acceptance remains open for account sync, complete art and human final QA.

Merged Kind Robots PR #5070 at commit 37eafdd60de28e26fa4a2eb09237f96486a0743a after all ten current-head workflows completed green: illustrated entry screen, real text/font/contrast/motion settings, painted 15-ending catalogue, versioned local journey scrapbook and tests. Also merged Conductor PR #7307 for no duplicate master task and a true deferred final human gate. Main-game standard remains READY, not done: add cast discovery scrapbook, reconcile account-backed saves and full device testing with existing story/art tasks. Do not promote project to playtest, and keep GitHub master issue #4139 open.

Scoped save-load corruption isolation fix submitted in Kind Robots branch worker/zuzu-t015-save-recovery-b7e9; broader account sync, art and device QA remain open. Do not mark t-015 done.

2026-11-14 PT reconciliation: Kind Robots #5154 is MERGED and preserves independently valid browser saves when adjacent slots contain corrupt JSON. This is a completed slice, not the whole t-015 acceptance task. Return t-015 to ready for its remaining account-backed Continue and persistent cast-discovery scrapbook; don't redo the shipped title, 17 achievements or endings catalogue. Final phone/tablet QA is t-009 after art delivery.

2026-11-14 PT: A scoped Kind Robots branch implements seven-character cast discoveries earned from newly visited story scenes/flags, persisted separately from the current run, migrated from local story progress, excluded from foreign save-code imports, and rendered as a locked-silhouette/portrait gallery in the Bell Ledger. Regression contract added. Pending CI and merge. Account-backed Continue and full device/art QA remain open; do not mark t-015 done or game playtest-ready.

2026-11-14 PT: Kind Robots cast scrapbook PR #5158 merged, with all workflow runs green. Seven-character discovery and persistence shipped. Re-arm t-015 for still-missing signed-in account-backed Continue and safe local fallback, without replaying cast/achievement awards from imported saves. No playtest promotion yet.

2026-11-14 PT account-backed Continue Kind Robots #5179 is MERGED at 1d366b4 after 16/16 workflows green: private account-owned revision-safe save, source validation, local fallback and explicit two-device conflict resolution. Cast scrapbook PR #5158 and 17 achievements previously merged. Main-game standard additionally needs a confirmed full-progress reset distinct from New Journey; Kind Robots PR #5185 is OPEN with code/tests and GitHub Prettier autofix, latest source commit 11cc94a; final exact-head CI is queued, do not merge unless all green. Scoped task has substantive code, not a claim-only event. Keep this task in review, not DONE, pending #5185 merge and documented standard closeout; final live account/device testing belongs to t-009 and actual human acceptance to t-017. No project playtest flip or master issue closure yet.

2026-11-15 PT close-out: confirmed full-progress reset #5185 merged after account-backed
Continue #5179, cast scrapbook #5158, corrupt-slot isolation #5154,
title/settings/endings #5070 and 17 achievements #5059. Every main-game-standard item is
Met or Exempt (fixed protagonist). Evidence: projects/zuzu-gamebook/PLAYTEST-
READINESS-2026-11-15.md.
<!-- note:end t-015 -->

## t-016 — Zuzu Gamebook achievement upgrade: 12 or more live achievements

<!-- note:begin t-016 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 3 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5059 (641e448), all checks green: 14 new + 3 kept = 17; importCode never awards; ending-count achievements use a played-endings record that only real play grows. Catalog seed succeeded.
<!-- note:end t-016 -->

## t-018 — Playtest polish: fight-preview HP applies heal before hurt, matching the reducer

<!-- note:begin t-018 -->
Split out of t-008 on 2026-11-15 PT at the playtest handoff so the slice keeps its owner without blocking the handoff. Kind Robots PR #5191 (opened by the t-008 claim above) makes fightFrom() heal before hurting, matching enter/applyEffects. The bug is latent: no Book One scene carries both heal and hurt today (checked on main b01655b), so it is defensive polish, not a playtest blocker. At handoff its TypeScript check was failing; the new test assigns to a BOOK scene's effects, which the scene type likely makes readonly. The owner should fix the typing, get CI green and merge, then mark this done.
2026-11-15 PT: Silas confirmed nobody else is working on this project, so the claim was taken over as stale. kind_robots #5195 merged (f6a2e37, 14/14 checks green); it carries the #5191 heal-before-hurt fix plus the missing probe Choice label that failed TypeScript. #5191 closed as superseded.
<!-- note:end t-018 -->
