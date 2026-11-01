# shifting-desks — task history archive

Full `note:` prose for completed shifting-desks tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Design brief, pitch menu and project scaffold

<!-- note:begin t-001 -->
Silas-directed session 2026-10-12 PT. Scaffolded via intake.py; wrote DESIGN-BRIEF.md (best-of-both table from Shifting Lands + Gamebook, no-clean-wins rule, five meters, Rules v1 "File, Stamp, Survive", Successors, Society and Mutation cards, recommended world Consolidated Wellness & Defense with PAL, five departments, ten endings, art direction, tone and IP guardrails) and PITCHES.md (seven directions A-G, six expansions, a recommended synthesis, title options).
<!-- note:end t-001 -->

## t-002 — Pick the spine, title and party-mode scope from PITCHES.md

<!-- note:begin t-002 -->
DECIDED by Silas in session, 2026-10-12 PT. Spine: "Combination of synthesis with vault test facility. I liked them best" (the restructuring campus + Paranoia social layer + Toy Division + window shifts + Kind Rewrite ending, fused with Pitch B: the campus is the surface of a sealed test vault, every department is a level deeper, PAL is HR and test proctor, and hidden Test Results grade the player). Party mode: "Not at all" (removed from the roadmap). Emphasis: "Secret societies & traitors" and "Paperwork & psych tests" (validator now requires at least half of each pack's cards to carry conspiracy, psych-test or paperwork tags). Title: CONFIRMED "Shifting Desks" (Silas, 2026-10-12 PT: "I confirmed shifting desks but it didn't get confirmed"; the question offered no keep-as-is option, so his pick did not register).
<!-- note:end t-002 -->

## t-003 — Encounter-pack contract, validator and Orientation department pack

<!-- note:begin t-003 -->
encounters/ENCOUNTER-PACK.schema.json (fork of Shifting Lands v1: five meters, cost per choice, optional roll, requires gates, tags, callback, boss review), validate_pack.py (CI authority; enforces shape, positive-only art prompts, flag and outcome reachability and NO CLEAN WINS), tests/test_shifting_desks_encounters.py (8 tests), and ORIENTATION-12.json: 3 locations x 4 cards (4 good / 4 bad / 4 mixed), 36 choices and the 5-route "Your 90-Day Review, Today at 3" boss with 6 department outcomes. All art is design-only.
<!-- note:end t-003 -->

## t-004 — World bible: the Company, PAL, departments, recurring cast, societies, mutations, callback ledger

<!-- note:begin t-004 -->
Write projects/shifting-desks/WORLD-BIBLE.md against the DECIDED world (t-002 and DESIGN-BRIEF "Decided world": the campus is the surface of a sealed test vault, each department one level deeper, PAL as HR and test proctor, hidden Test Results axes). Secret societies/traitors and paperwork/psych tests are the lead flavors, so give them the most depth. Cover Consolidated Wellness & Defense and its euphemism-speak; PAL's voice rules (cheerful, concerned, never cruel on purpose); all five departments with 3 locations each and a boss review sketch; the recurring cast (Dale, Pip, Marguerite, Gus and the Roach Union, Dr. Halvorsen, the Supervisor, the Founder, the Successor line); 6 Secret Society cards (objective, favor, betrayal condition); 8 Mutation cards (power, use window, witnessed cost); 5 Job Title cards (6-point skill spread + perk); a callback ledger listing every homage with its source and the "allusion, not quotation" boundary; and the ten endings with unlock conditions. Keep the IP and tone guardrails from DESIGN-BRIEF.md.
DONE 2026-10-12 PT: WORLD-BIBLE.md and encounters/DECKS.json (6 societies with flag- keyed objectives/betrayals, 8 mutations, 5 job titles), validated by validate_pack.py + tests/test_shifting_desks_encounters.py (12 pass). Unblocks t-008 and the department packs t-010..t-013.
<!-- note:end t-004 -->

## t-005 — Art direction sheet, card backs and three style-test card faces

<!-- note:begin t-005 -->
Write projects/shifting-desks/ART-DIRECTION.md (mid-century safety-poster x retro-futurist beige office, limited palette, halftone, positive-only prompts ending "every surface bare and unmarked"). Queue internal ArtJobs for: the encounter card back (manila folder, coffee ring, stamp silhouette), the boss/review card back (oxblood folder, wax seal), and three Orientation style-test faces (Gus Shop Steward, Something Ticking in the Toner, Trust Fall Over the Shredder). Record prompt, model, seed, ArtJob and ArtImage IDs in art/ROUND-1.yaml. Never list art as delivered before its URL loads. Generated internal art is pre-approved.
Art round 1 queued 2026-10-13 (session 2026-10-13T00:00:00Z-sd-art-q7k2): ART- DIRECTION.md written; five krea2 requests (shifting-desks-r1-*) added to projects/art- prompts.yaml requests and recorded in art/ROUND-1.yaml, all status requested. ArtJob and ArtImage ids arrive with the auto-art-generate run (watch each row's last_art_job_id); mark a subject delivered only after its media_url returns 200, then review the renders against ART-DIRECTION.md before setting art_ref on the cards.
DONE 2026-10-13 PT: all five round-1 renders answer 200 on media.acrocatranch.com and kindrobots.org (encounter back, review back, Gus, Something Ticking in the Toner, Trust Fall Over the Shredder). Reviewed against ART-DIRECTION.md: on palette, halftone, single readable scene, no lettering; verdict keep for all five (ROUND-1.yaml). Style test accepted internally, which unblocks t-015 (its faces are already queued in ROUND-2).
<!-- note:end t-005 -->

## t-006 — Public /play front page, Projects tab and card board shell

<!-- note:begin t-006 -->
kind_robots: public /play/shifting-desks (Silas, 2026-10-12 PT: "a real, front end, non admin front page") with a Projects channel tab. Do not mount the Shifting Lands or Gamebook pages or share their stores. Content is a provenance-stamped snapshot of ORIENTATION-12.json.
DONE 2026-10-12 PT in kind_robots#3620: public /play/shifting-desks (front page with PAL's welcome, three pillars and the five-level descent), Projects channel tab content/channels/projects/shifting-desks.md, original poster public/shifting-desks/ front-poster.svg, provenance-stamped content snapshot utils/shiftingDesks/orientation.json. Screenshots: projects/shifting-desks/screenshots/.
<!-- note:end t-006 -->

## t-007 — Seeded run reducer: meters, Successors, Suspicion, Clearance gates, save v1

<!-- note:begin t-007 -->
kind_robots utils/shiftingDesks/ pure reducer + stores/shiftingDesksStore.ts (Pinia 3 thin wrapper). Seeded weighted draw per location (persisted, no refresh reroll); choice resolution with cost, 2d6 + skill + Form boost vs 7/9/11, natural 12 Commendation / natural 2 Incident hooks; the five meters with limits from DESIGN-BRIEF; Successor arrival flow (keep flags and Clearance, halve Suspicion rounded up, reset Composure, drop carried items); Suspicion 10 triggers the disciplinary card; requires gates with explained disabled choices; boss department outcomes; Restructuring map effects with written reasons; browser-local versioned save. Unit tests for every rule plus a seeded replay test.
DONE 2026-10-12 PT in kind_robots#3620: utils/shiftingDesks/rules.ts (seeded draw, cost + 2d6 + skill + Form boost, natural 12/2, five clamped meters, Successor arrival with the Temp perk, Suspicion 10 conversation, requires gates with reasons, boss outcomes and reorientation re-deal, versioned save guard) and stores/shiftingDesksStore.ts. verifyShiftingDesks.test.ts simulates 3,000 seeded runs. Not yet built: Restructuring map effects between departments (moved to t-023; meaningful only once Department 2 exists) and carried items (none are authored yet).
<!-- note:end t-007 -->

## t-008 — Secret Society and Mutation decks in the engine (Job Titles shipped in t-007)

<!-- note:begin t-008 -->
Deal a face-down Society card and a Mutation card at run start; Job Title select sets the skill spread and perk. Society objectives and betrayal conditions evaluate against run flags; the Mutation is once per department, with +2 Suspicion on witnessed cards. Never reveal the player's Society to other cards. Tests for dealing, seeding, objective scoring and witnessed costs.
DONE 2026-10-12 PT in kind_robots#3622 (merged 98da421): every run deals a face-down society and mutation from a sealed envelope; per-department orders and betrayals keyed to flags; favors (force success, +3, ignore requirement, instant effects) and mutations (reroll, auto-success, +3, restore Composure) with +2 Suspicion when witnessed; v1/v2 saves upgrade. Verified by test:shifting-desks (3,000 seeded runs) and Playwright playthroughs at 390/768/1440.
<!-- note:end t-008 -->

## t-009 — Playable Orientation slice end to end at the public route

<!-- note:begin t-009 -->
MVP from DESIGN-BRIEF: Job Title select, the 12 Orientation cards drawn 3-per-run (one per location), choice cards showing intent, risk, skill and target, dice roll, success/failure prose and effects, journal, Successor deaths, the 90-Day Review with its 5 routes, and at least 3 reachable department outcomes. Placeholder art clearly labeled pending. Screenshots at 375/768/1440 in the PR.
DONE 2026-10-12 PT in kind_robots#3620, at the PUBLIC route per Silas's direction. Verified by a local nuxi dev + Playwright full playthrough at 390/768/1440 px: zero horizontal overflow, zero page errors, result screen reached at every width.
<!-- note:end t-009 -->

## t-010 — Department 2 pack: Records & Forms (Brazil / Bureaucracy)

<!-- note:begin t-010 -->
encounters/RECORDS-12.json: Pneumatic Tube Exchange, The Sub-Archive, Window 9 (Papers-Please-style applicant cards are a later engine feature, t-016; author this location as ordinary cards now). 3 x 4 cards, balanced polarity, boss "The Form That Requires Itself" with at least 3 routes. Must pass validate_pack.py. Pays off forged-dale, halvorsen-envelope and the Stapler Liberation Front contact from Orientation.
DONE 2026-10-13 PT: encounters/RECORDS-12.json ships Pneumatic Tube Exchange, The Sub-Archive and Window 9 with 4 authored cards each (12 cards, 4 good / 4 bad / 4 mixed, 11 of 12 tagged conspiracy, psych-test or paperwork, 3 ledger-bounded callbacks), and every choice pays a cost. Nine choices are gated on Orientation flags (forged-dale, halvorsen-envelope, stapler-front-contact, has-master-key, knows-the-ducts, roach-union-ally, roach-union-member, pip-trusts-you, wearing-a-dead-mans-badge). Boss "The Form That Requires Itself" has 5 routes and 5 department outcomes plus the refiled re-deal. validate_pack.py now lets requires.flag be granted by any pack with a lower department.order; DECKS.json gains records objectives and betrayals for all six societies; WORLD-BIBLE callback ledger updated. validate_pack.py OK for both packs and the decks; pytest tests/test_shifting_desks_encounters.py 17 passed. Wiring the pack into the kind_robots game is separate work.
<!-- note:end t-010 -->

## t-011 — Department 3 pack: Product Safety, Toy Division (Snuggle Sentinel)

<!-- note:begin t-011 -->
encounters/TOY-DIVISION-12.json: Concept Lab, Focus Group Room, Proving Grounds; boss "Snuggle Sentinel's Launch Party". Nuclear-capable toys are played for corporate cheer; nothing ever detonates near a child (tone guardrail). Pays off bear-imprinted, defused-mk0 and mailed-the-bear-upstairs. Must pass validate_pack.py.
DONE 2026-10-13 PT: pack conductor#6104 (TOY-DIVISION-12.json: Concept Lab, Focus Group Room, Proving Grounds, 12 graded cards, Launch Party boss with seven routes incl. Empathy 4 and Spite 4 gates, Restructuring memos for every Records outcome, society orders, art round 4 queued), wiring kind_robots#3629 (merged 8dc5530: third department registered, fallback, PAL memos). Three-department playthrough verified at 390 and 1440 with no errors or overflow; sim 2,666/3,000 complete.
<!-- note:end t-011 -->

## t-012 — Department 4 pack: Wellness & Testing (vault tests, psych tests, mutation suite)

<!-- note:begin t-012 -->
encounters/WELLNESS-12.json (Level -3, the Vault proper and the heart of the decided vault-test spine): Nutrition Studies, Cognitive Testing Chamber, the Mutation Suite; boss "The Final Wellness Exam" (the test is whether you will administer the test). Heaviest psych-test density in the game, and where hidden Test Results are partly revealed. Original facility, voice and framing, with no Aperture or Vault-Tec likeness. Must pass validate_pack.py.
DONE 2026-10-13 PT: pack conductor#6108 (WELLNESS-12.json: Nutrition Studies, Cognitive Testing Chamber, Mutation Suite; 11 of 12 cards psych tests; The Final Wellness Exam with seven routes incl. the Window 9 lab coat and Obedience 5 / Ingenuity 5 gates; Restructuring for every Toy Division outcome; society orders; art round 5), wiring kind_robots#3632 (merged 5a1c181). Four-floor playthrough verified on phone: the Vault reached and all four Test Results revealed at its review; no errors or overflow.
<!-- note:end t-012 -->

## t-013 — Department 5 pack: Sub-Level Zero, The Board and the Kind Rewrite true ending

<!-- note:begin t-013 -->
encounters/SUBLEVEL-ZERO-12.json (the executives live at the very bottom of the vault): Boardroom Antechamber, the Founder's Office, Server Room Zero; boss "The Board" with routes to Society Coup, Roach Union General Strike, Whistleblower, Promoted to Management and the hidden Kind Rewrite (gain admin access, rewrite PAL to remember people). Society objectives come due here. Must pass validate_pack.py.

Reviewer pass 1 failed (quality) on conductor#6110 head 758d8aa8aba1d524b629cf5c1854183dc7a623c9. Actual Kind Robots enqueue contract rejects The Founder's Desk corner-of-the-frame wording. See retry_context, project TALKBACK and PR comment 6142649623. Retain #6110 for original worker, re-claim before repair, correct all three prompt copies and validate all 17 actual krea2 requests. Consumer wiring and its CI are still required; no human gate, deployment or delivered-art claim is introduced.

DONE 2026-10-13 PT: pack conductor#6110 (SUBLEVEL-ZERO-12.json: Boardroom Antechamber,
the Founder's Office, Server Room Zero; PAL revealed; The Board, whose eight routes are
the endings incl. the hidden Kind Rewrite at admin-access plus Empathy 5; Restructuring
for every Wellness outcome; final society orders; art round 6), wiring kind_robots#3633
(all five departments playable; the Board's ending closes the Personnel File; low-staff
Successor thaw keeps seeded elimination near 17%). Five-floor playthrough verified on
phone and desktop with no errors or overflow.
<!-- note:end t-013 -->

## t-014 — Endings ledger and cross-department flag map

<!-- note:begin t-014 -->
encounters/ENDINGS.json + a validator extension: at least ten distinct endings with authored epilogue cards and unlock conditions; a static check that every ending is reachable from some seeded route and that every flag a later pack reads is granted by an earlier pack.
DONE 2026-10-13 PT: data conductor#6113 (ENDINGS.json with ten endings, epilogue cards and flag-keyed variants; FLAG-MAP.json for all 254 flags; validator coverage and staleness checks; art round 7), consumer kind_robots#3634 (merged 525a0f2: endingFor/endingLines, epilogue card in the Personnel File). Evidence per the #6113 review: all eight Board endings forced through their real routes on deterministic seeds and surviving save/reload, secret Posthumous Affairs outranks the default elimination, variant lines verified, and the seeded 3,000-run random sim reaches all ten endings.

Independent post-merge review session2026-10-13T112357Z-shifting-desks-closeout-r9k2 confirms consumer3634 merged525a0f278c21c5a23390b516cb7e7d380dadddd9 with32 completed green checks for exact headb81722f44eb67641449fd8f830a40ce119bfa160; coordinator6118 merged5713cffd6947408c2d001d410dd543c58c11de9f atfinalhead2e3832e9057e4b243c3bc13566faea6fc15dc173 with27 completed green/intentionalskip checks. Full consumer/coordination diffs inspected. Independent engine suite2475/3000 completed525 eliminated reachesall10 endings. Actual Vue/Pinia Personnel File and genuine natural saved states tested in native Chromium at390/768/1440:30 epilogue+real-localStorage-reload cases,15 variantchecks, no overflow/errors; scoped component fixture, not deployment. Secret elimination precedence verified. Currentmain preserves6119 art lifecycle test/ledger recovery. Clear residual owner from original close_task PR; historical claim provenance retained. t019 ready after dependencies; t026 ready browser-contract kaizen. No new render, email or publication.
<!-- note:end t-014 -->

## t-015 — Illustrate the 13 Orientation card faces (12 encounters + review)

<!-- note:begin t-015 -->
Queue internal ArtJobs from each card's art.brief once t-005's style test is accepted internally. Verify delivered URLs, then set art.status to approved-ArtImage and art_ref to the verified ArtImage id in ORIENTATION-12.json. Ledger in art/ROUND-2.yaml.
2026-10-13 PT: conductor #6127 (bc9b4b2) records delivery for every Shifting Desks station image: all 121 subjects across rounds 1-8 answered GET media_url with 200 image/webp, and Kind Robots serves /images from the media origin, so the art is live. Round 8 is reviewed (keep x5). Remaining for this task: Orientation cards' art.status approved-ArtImage and art_ref need ArtImage ids, which most ledger rows lack (a Kind Robots ArtImage lookup). Claim released.
2026-10-20 PT: closed by the art link pass on claude/shifting-desks-art-link. All 163 pack slots now map to the exact path kind_robots stationArt() serves; encounters/link_art.py links a slot (verified-repository-art, art_ref = public path) when its latest art ledger row is delivered and its visual verdict is keep. 143/163 linked and probed 200 image/webp. Every delivered render in rounds 2-12 (184) was reviewed: 159 keep, 25 sent back to ROUND-13 re-renders, tracked as t-032. ArtImage ids were not pursued: these images are files on the media host, not ArtImage records, so verified-repository-art is the accurate status.
<!-- note:end t-015 -->

## t-016 — Window shifts: the Papers-Please-style desk card type

<!-- note:begin t-016 -->
Pitch D as a recurring card type: inspect 3-5 applicant cards against the day's rule memo, stamp APPROVED/DENIED, with consequences written as flags that later cards read. Schema v2 extension + validator + reducer + UI. Original country-free office setting and original UI.
DONE 2026-10-13 PT. Data: conductor #6124 (17a71a7, RECORDS-12 window_shift, validator, schema, FLAG-MAP, art round 8) and #6125 (1d20d96, balance pass: two by-the-book denials cost a Form, approving your Successor costs 2 Suspicion for 2 composure). Engine and UI: kind_robots #3636 (8ddf03f). Window 9: The Tuesday Line deals four applicants before the Records review; you stamp APPROVED or DENIED against a three-rule memo; off-memo stamps draw PAL's audit and +1 Suspicion; a Restructuring that closes Window 9 skips the shift; mid-shift saves reload. Verified in CI and in local Chromium at 390/768/1440 (stamps, slam, audit, review follows, zero overflow and errors). t-019 balance thresholds hold (Schemer 44.5%). Art round 8 pending render.
<!-- note:end t-016 -->

## t-017 — Comic timing: memo ticker, stamp animation, Successor arrival and personnel file export

<!-- note:begin t-017 -->
Scrolling PA/memo crawl reacting to flags; stamp and flip animations with a reduced-motion path; Successor arrival card with an orientation line; an end-of-run Personnel File (cause of each termination, societies betrayed, forms filed) as a local printable/downloadable card. No external sharing, which is a publish gate.
DONE 2026-10-12 PT in kind_robots#3622: scrolling PAL memo ticker keyed to flags, APPROVED/DENIED stamp slam, Successor-thawed card, elevator interstitial with restructuring memo, and a printable Personnel File finale (both departments, society verdict, causes of termination, Print button). Reduced-motion paths for all of it.
<!-- note:end t-017 -->

## t-018 — Accessibility and device pass at 375 / 768 / 1440

<!-- note:begin t-018 -->
Keyboard and screen reader through a full department, roll results announced immediately, developer notes never spoken, disabled choices explained, focus return after flip, no hover-only actions, no horizontal overflow. Screenshots in the PR.
DONE 2026-10-13 PT: axe-core WCAG 2.1 A/AA audit through a full three-department run at 375, 768 and 1440 (front, hire, envelope, keyboard-opened choices, result, elevator, review, Personnel File): no overflow, no page errors. Fixed site-wide html lang, contrast on labels/chips/badges, focus return to the new card after Next and the elevator. Only remaining findings are two shared workspace-header elements at 1440 (outside the game; separate change). kind_robots#3630 merged e905484.
<!-- note:end t-018 -->

## t-019 — Seeded balance simulation across all five departments

<!-- note:begin t-019 -->
Simulate thousands of seeded runs with several policy bots (complier, rebel, coward, saint). Report the Successor death rate per department, ending distribution, meter-limit hits and dominant choices. Tune targets and costs so no policy wins clean and every ending appears. Commit the report and tuned packs.
DONE 2026-10-13 PT. Conductor #6122 (84b3f13): BALANCE-REPORT.md and the data-driven tuning (swap-the-file spends its Successor on success and is Risky 9; squeeze-the-duck is Risky 9; Humming Door and Spare Mustaches weight 3; thaw kept at 2). Kind Robots #3635 (68a0ed8): utils/shiftingDesks/balance.ts, five temperament bots plus a random baseline at 2,000 seeded runs each; verifyShiftingDesksBalance.test.ts runs in the gameplay CI (green, same numbers as the report). Elimination: complier 18.7%, rebel 35.8%, coward 0.1%, saint 19.9%, schemer 45.0% (was 54.0%), random 14.4%; every ending reached; no dominant or ungated dead choices. The Coward's near-total survival, paid for in Successors and with no payoff endings, is flagged for Silas's t-020 verdict.
<!-- note:end t-019 -->

## t-022 — Hidden Test Results: Obedience, Empathy, Ingenuity and Spite grading

<!-- note:begin t-022 -->
The vault-test half of the decided spine. Extend the pack schema/validator with an optional per-outcome grades object (obedience, empathy, ingenuity, spite; small integers), backfill ORIENTATION-12.json, and add reducer support. Grades stay hidden during play, are partly revealed at each department review ("PAL has prepared your interim results"), gate some boss routes, and set the ending's flavor text in the Personnel File. Tests for accumulation, gating and that no grade is shown early.
DONE 2026-10-13 PT: data half conductor#6100 (grades on all 82 choices, grade-gated review routes, DECKS test_results, validator checks), engine/UI kind_robots#3627 (save v4, interim results at each review revealing one more grade per level, Personnel File verdict). 3,000-run sim asserts every grade route is earned and four or more verdicts occur.
<!-- note:end t-022 -->

## t-023 — Restructuring: map changes between departments with written reasons

<!-- note:begin t-023 -->
Split from t-007 (2026-10-12 PT). When a department is cleared, a Restructuring memo may merge, eliminate or add unvisited locations in the next department, always with a written reason, and visited history stays pinned (DESIGN-BRIEF Rules v1). Needs Department 2 content (t-010) to mean anything. Reducer, journal entry, UI memo card and tests.
PARTIAL 2026-10-12 PT (kind_robots#3622): department progression shipped (descend, per-department outcomes, elevator with a PAL restructuring memo). Still open: memos that actually merge, eliminate or add unvisited locations in the next department, with the reason pinned in the journal.
DONE 2026-10-13 PT: data half conductor#6102 (RECORDS-12 restructurings keyed on every Orientation outcome plus knows-the-ducts; validator requires memos below the surface), engine/UI kind_robots#3628 (departmentBoard eliminate/merge/add/none, elevator notice and floor plan, restructured breadcrumb and card location, banner, journal pin, Personnel File line, save v5; re-deals never reopen a closed location). Sim asserts all four kinds occur in play.
<!-- note:end t-023 -->

## t-024 — Repair rejected Shifting Desks art prompts using the live enqueue contract

<!-- note:begin t-024 -->
Kaizen from conductor#6113 source review; next_free_task_id.py returned t-024. Actual Auto Art Generate run 38364751716 rejects Hungry Detector and Security Desk frame-noun prompts; actual TypeScript enqueue validation also rejects Founder's Desk. Replace inner frame with inner arch for requests shifting-desks-r2-the-hungry-detector and shifting-desks-r3-location-security-desk; replace corner of the frame with corner of the desk for shifting-desks-r6-the-founders-desk. Fix corresponding ROUND-2/3/6 ledgers and ORIENTATION-12/SUBLEVEL-ZERO-12 art briefs so every producer agrees. The Python negation detector is not the full server contract: validate changed/new requests with actual current Kind Robots checkArtPromptContract for krea2, cfg 1, steps 8. Read complete current files in explicit ranges, patch text in place, use current blob SHAs, preserve all pending durable ArtJobs, and coordinate with the active t-014 worker before shared root edits. Do not copy server regexes, weaken checks, overwrite queue state or mark requested art delivered. Verify the next generator adopts/renders the original targets and health clears without hand editing it. t-013's consumer is merged; these art defects remain independent unfinished work.

Recover the three independently verified frame-noun enqueue failures. Endings source and its review/kaizen handoff are merged in conductor#6113/#6114; t-014 remains with its original consumer worker. This claim reserves only the focused canonical prompt/ledger repair and generator verification.

Focused canonical prompt repair submitted from worker/shifting-desks-t024-art-prompts-j3p8. All nine changed request/ledger/source copies pass actual Kind Robots checkArtPromptContract (krea2 cfg1 steps8); originals reproduce frame-noun. 75 Python tests pass. Source merge and next generator adoption/rendering/health verification remain required; do not mark requested art delivered or close task from source changes alone.

Canonical source repair merged as conductor#6116 at 24cdb603f2634285af1ab7f8180ab8728a30f169 after all 23 exact-head checks completed success/intentional skip. Nine prompt copies pass actual current Kind Robots enqueue contract, all originals reproduce frame-noun; 75 focused Python tests and full pack/deck/ending validators pass. Job IDs/statuses/seeds/output paths retained. Task unfinished: inspect merge-triggered Auto Art Generate run on repaired main for original Hungry Detector, Security Desk and Founder Desk acceptance/adoption/rendered ArtImage and generated health clearance; do not close on source-only evidence or duplicate active jobs. Releases this session for sequential daily-delivery verification.

Resume own prior source repair: generator38386864668 completed successfully, original targets ArtJobs38506/38507/38508 DONE with ArtImages246648/246649/246650 and generated health failures empty. Recover the new producer consistency test's incorrect assumption that fulfilled requests remain forever: the generator legitimately prunes satisfied root rows, so verify live submissions against authoring ledgers without requiring retired history in the active queue. Preserve checks and add retirement/drift/duplicate regression coverage; record target delivery evidence and close only after exact-head green CI and live media verification.

Branch worker/shifting-desks-t024-queue-lifecycle-r9k2 fixes test assumptions about completed root requests legitimately pruned by build_workspace, preserving active request prompt/settings/uniqueness checks and adding eight lifecycle/drift/duplicate tests. 63 focused tests and all pack/deck/endings validators pass against drained current main. ROUND2/3/6 record actual ArtJobs38506/38507/38508 and ArtImages246648/246649/246650, rendered status with workflow successful2xxHEAD evidence; no invented exact200 or visual verdict. Auto Art Generate38386864668 succeeded and health failures empty. Await exact-head CI before merging/closing.

Prompt source repair6116 and lifecycle/evidence recovery6119 merged, latter df7a4da1eeb25bf1cbf43311d19925dcbc55e86e after all23 exact-head checks completed success/intentional skip. Original Hungry Detector, Security Desk and Founder Desk ArtJobs38506/38507/38508 DONE as ArtImages246648/246649/246650 in successful Auto Art Generate38386864668; .media-direct output requires successful2xx media HEAD in the runner, generated failures[] verified on main. Local proxy403 limits independent repeat, not the confirmed runner delivery. ROUND2/3/6 preserve durable IDs and rendered status with no invented exact200/visual verdict. 63 focused tests and all pack/deck/endings validators passed; live drift/duplicate assertions preserved and retirement regression covered. Source cause and original incident repaired without duplicate jobs. t025 ready tracks automated durable ledger synchronization.
<!-- note:end t-024 -->

## t-026 — Exercise epilogue cards and real save reload in the browser contract

<!-- note:begin t-026 -->
Kaizen from independent review of kind_robots#3634/conductor#6118. The shipped verifier checks Personnel File template text with a regex, which cannot establish mounted Vue/Pinia behavior or real localStorage reload. Independent native Chromium fixture of actual components/store/engine/scoped repository CSS passed30 cases: all10 naturally reached endings at390/768/1440,15 flag-variant checks, no overflow/runtime errors, persisted seed survives reload, art failure fallback remains visible. Add a focused reproducible equivalent to the app's permitted browser verification suite, retaining natural saved-state provenance and isolation from live APIs/deployment. Include secret-versus-default elimination and text-transform-safe DOM assertions; do not weaken engine gates or claim a fixture is a production deployment.
Done 2026-10-16 (overnight free rein): kind_robots#3761 (97b4465). utils/shiftingDesks/endingSaves.ts lets the balance policies reach every ending through the real engine and keeps each save's seed, job and policy as provenance; cypress/public/shifting-desks-endings.cy.ts loads each save through real localStorage at 390/768/1440 (epilogue title, flag variant lines, no other ending's card so secret and default elimination stay distinct, no overflow, gallery record), plus a real reload and an art 404 fallback, with textContent assertions. 33 passing against a local dev build. It runs read-only on demand (shifting-desks-gameplay.yml workflow_dispatch, default production); PR CI asserts a natural save exists for every ending. Not yet run against production: dispatch it after the next Alexandria deploy.
<!-- note:end t-026 -->

## t-027 — Daily Memo: one seeded Wellness Weekend a day, shareable result

<!-- note:begin t-027 -->
Silas, 2026-10-16: free rein overnight on levels, art and features. Built PITCHES.md expansion "Daily Memo" in kind_robots#3743 (merged 7572586): a Daily Memo button on the front desk deals the seed daily-YYYY-MM-DD on the Company's Pacific calendar, so every player gets the same files, society and mutation; the hire screen and heads-up floor tip name the memo; a daily Personnel File gets "Share today's memo" (native share sheet, else clipboard). No save-schema change. Tests cover the Pacific day boundary, identical daily runs, isRunState and the share text; Playwright fit verified at phone and both iPad orientations.
<!-- note:end t-027 -->

## t-028 — Toy Division Recall Desk: a second Papers, Please window shift

<!-- note:begin t-028 -->
Silas, 2026-10-16: free rein on levels to design/release and art to submit. TOY-DIVISION-12.json gains window_shift recall-desk-friday at the Proving Grounds: a Product Safety Memo (no payloads, drop-tested in writing, no toy that asks where it is shipped) and four applicants: Wendell's ticking rabbit (payload), Intern Pip's lunch-break bear (clean), the Supervisor's Snuggle Sentinel Mk 0 with a Defense-waived drop test, and Tinbert the wind-up robot who asks where it is going (recalling it by the book costs Empathy). Six ENDINGS variants remember the stamps. Balance: every bot stays under two Successor losses on Toy Division (Rebel 1.87, Saint 1.64, Schemer 1.87) and the Schemer is eliminated 47.6% (<50%); BALANCE-REPORT regenerated. Art round 9 (ROUND-9.yaml): five Classic Krea 2 requests plus Western Cartoon and Noir style rows (STYLE-CATALOG 126 subjects, 252 v2 requests); all ten Krea prompts pass the live checkArtPromptContract. Kind Robots snapshot merged in kind_robots#3749 (65cc968), with the window component showing each desk's own stamp words. Remaining: deliver round 9 art, then close.

2026-10-20 PT: art delivery verified on claude/shifting-desks-art-link. Every render
this task queued answers 200 image/webp on the media host in Classic, Western Cartoon
and Noir. Classic verdicts are recorded in its round ledger, and sent-back renders are
re-queued in ROUND-13 (t-032).
<!-- note:end t-028 -->

## t-029 — Wellness Consent Window: a third Papers, Please window shift

<!-- note:begin t-029 -->
Silas, 2026-10-16 free rein. WELLNESS-12.json gains window_shift consent-window-rounds at the Mutation Suite: an Informed Consent Memo (awake while signing; no test result may volunteer again) and three volunteers from the recurring cast: Kevin knocking from inside Tank Nine (already a result; keeping him in by the book costs Empathy), Doris from Accounting signing in her sleep, and Marguerite volunteering to map every duct (clean). Stamps read CONSENT / VOID. Three ENDINGS variants remember them. A four-applicant draft (Dale signing for Pip) pushed the Rebel to 52% eliminated through Suspicion, so the line is three; every policy now stays under 50% (Rebel 47.5%, Schemer 48%) and BALANCE-REPORT is regenerated. Art round 10 (ROUND-10.yaml): four Classic Krea 2 requests plus Western Cartoon and Noir rows (STYLE-CATALOG 130, 260 v2 rows); all eight Krea prompts pass the live checkArtPromptContract. Remaining: Kind Robots snapshot PR, art delivery.

2026-10-20 PT: art delivery verified on claude/shifting-desks-art-link. Every render
this task queued answers 200 image/webp on the media host in Classic, Western Cartoon
and Noir. Classic verdicts are recorded in its round ledger, and sent-back renders are
re-queued in ROUND-13 (t-032).
<!-- note:end t-029 -->

## t-030 — Sub-Level Zero Antechamber Sign-In: a fourth Papers, Please window shift

<!-- note:begin t-030 -->
Silas, 2026-10-16 free rein. SUBLEVEL-ZERO-12.json gains window_shift antechamber-sign-in at the Boardroom Antechamber: you mind the Board's sign-in ledger, stamped ADMIT / TURN AWAY, under the Board Visitor Protocol (attend alive and entirely attached; wear no one else's face, mustache or badge). Three visitors: the Founder's head on a tea cart (turning him away costs Empathy), Dale from Compliance in the Founder's 1962 mustache, and Delegate Six of the Roach Union, who booked ahead (clean). Five ENDINGS variants remember them (promoted-to-management, position-eliminated, society-coup, roach-union-general-strike, posthumous-affairs). Balance: the first draft put the Rebel at 57% and the Schemer at 52.5% eliminated through finale Suspicion; returning Dale's mustache now earns PAL's approval (-1 Suspicion, -1 composure) and the by-the-book stamps carry the Rebel's and Schemer's grades. Every threshold holds (Rebel 49.4%, Schemer 49.3%, both within a point of the ceiling, so the next finale content needs a margin pass) and BALANCE-REPORT is regenerated. Art round 11 (ROUND-11.yaml): four Classic Krea 2 requests plus Western Cartoon and Noir rows (STYLE-CATALOG 134, 268 v2 rows); all eight Krea prompts pass the live checkArtPromptContract. Kind Robots snapshot kind_robots#3762 merged (84e6734); the Sign-In fits at 390/768/820/1180/1440 with no scroll. Remaining: art round 11 delivery, then close.

2026-10-20 PT: art delivery verified on claude/shifting-desks-art-link. Every render
this task queued answers 200 image/webp on the media host in Classic, Western Cartoon
and Noir. Classic verdicts are recorded in its round ledger, and sent-back renders are
re-queued in ROUND-13 (t-032).
<!-- note:end t-030 -->

## t-031 — Double every encounter deck: 24 cards per department, 8 per location

<!-- note:begin t-031 -->
Silas, 2026-10-17: "I like the pacing of 3 encounters before boss. What I want to do is double the encounters, so we have a possible 24 per." A run still deals one card from each of a floor's three locations, so pacing is unchanged; every location's pool is now 8 deep instead of 4. 60 new encounters (12 per department, 4 per location, polarity 4/4/4 each, every card graded): Orientation (Refreshments Are Served, The Red Stapler, Fumigation Thursday...), Records (The Tube That Goes Up, The Founding Charter, Forty-Two Years Overdue...), Toy Division (My First Reactor, The Robot Panel, The Hug Test...), Wellness (The Taste Panel, The Graduates' Lounge, Form M: Declaration of Powers...), Sub-Level Zero (Item Four, The Fifth Jar, Kevin's Cabinet, Ticket Number Two...). 40 new choices pay off earlier-floor flags, and 15 new ENDINGS variants read the strongest new flags (42 variants total); FLAG-MAP regenerated. Balance: halving the old deathtraps' draw rate dropped the Coward below its two-Successor floor, so the classic deathtrap cards keep their old frequency through doubled weights (Orientation x4, Jam in Tube 14, Thursday Door and Successor Waiting Room to 6), free paperwork picks now cost composure, and the new cards' -2 Suspicion reliefs are -1. Every threshold holds with more margin than before (Rebel 47.1%, Schemer 44.0%, Saint 35.1%, Complier 21.6%). Art round 12 (ROUND-12.yaml): 60 Classic Krea 2 card faces plus Western Cartoon and Noir rows (STYLE-CATALOG 194 subjects, 388 style rows); all 180 prompts pass the live checkArtPromptContract. Kind Robots kind_robots#3793 merged (188b6ec): the 24-card snapshot plus a denser four-route desk (four-route cards one size down, locked routes fold into lock chips) so the longer new cards fit at 390/768/820/1180/1440. Remaining: art round 12 delivery, then close.

2026-10-20 PT: art delivery verified on claude/shifting-desks-art-link. Every render
this task queued answers 200 image/webp on the media host in Classic, Western Cartoon
and Noir. Classic verdicts are recorded in its round ledger, and sent-back renders are
re-queued in ROUND-13 (t-032).
<!-- note:end t-031 -->

## t-033 — Tone ladder: lower floors grow more Cronenbergian (rules and station art)

<!-- note:begin t-033 -->
Silas, 2026-10-20 PT: "In later levels, things might get more cronenbergian. I loved the giant cockroach appearance in the first act. Great tone." ART-DIRECTION.md now carries a per-floor tone ladder: one impossible thing treated as normal on the surface (Gus is the benchmark), toys a little too alive in Toy Division, the body starting to do paperwork in the Vault, and corporate biology in Sub-Level Zero. Its limits are no blood, wounds, exposed organs, pain, nudity or distress, and flesh that is always smooth and upholstered. DESIGN-BRIEF "Tone guardrails" points to it. Art round 14 (ROUND-14.yaml) queues nine forced Krea 2 renders, all passing the live checkArtPromptContract: the Wellness and Sub-Level Zero department arrivals, their six location card backs, and the Board grown into one long suit. The pack briefs take the new prompts, and the replaced prompts and seeds stay in ROUND-5/6 for a one-request revert. Delivery and review ride t-032; card text follows in t-034.
<!-- note:end t-033 -->

## t-034 — Tone ladder text pass: Wellness and Sub-Level Zero card flavor

<!-- note:begin t-034 -->
Carry the t-033 tone ladder into the words players actually read. The 48 Wellness and Sub-Level Zero encounter cards, both reviews and both window shifts should gain body-horror texture in their flavor_text and outcome text, in the ART-DIRECTION.md "Tone ladder" register: PAL's grilles that lean in, furniture that breathes, mutations reported cheerfully by HR, and the Board as one organism. Change no mechanics, ids, flags or grades, so BALANCE-REPORT and FLAG-MAP stay byte-identical, which proves it. Keep the brief's tone guardrails (no blood, wounds or self-harm). Mirror the text into the kind_robots utils/shiftingDesks/wellness.json and sub-level-zero.json snapshots (art_prompt too, so the nine t-033 station prompts and the Western Cartoon/Noir STYLE-CATALOG rows can follow), then check the desk at 390 and 1440.

Lower-floor prose pass on canonical Conductor and Kind Robots branches. The source changes cover 48 encounter introductions, every choice-result text, two bosses and window shifts; runtime additionally adopts current station art prompts. Mechanical JSON fields remain unchanged. Preparing scoped PRs and CI.

Shifting Desks lower-floor tone ladder is merged. Canonical Conductor PR https://github.com/silasfelinus/conductor/pull/6513 merged e29a4b59ec960baff5df2dfb41ff7b9e47527bae with all 23 checks completed green or intentionally skipped. Runtime Kind Robots PR https://github.com/silasfelinus/kind_robots/pull/4043 merged 055f442158a2fab69b9cbdcd2772b51d7ea3c134 with all 19 final-head checks completed green or intentionally skipped. All 48 Wellness and Sub-Level Zero encounter intros and every available choice outcome, both boss reviews, and two window shifts received distinct living-office details. Runtime prose matches canonical source and ten station art prompts match canonical briefs, with both runtime sourceSha fields stamped to Conductor merge e29a4b59ec960baff5df2dfb41ff7b9e47527bae. Structured before/after diff allowed only prose and art prompts; no flags, grades, costs, rolls or ending identifiers changed. t-032 art review and t-025 render evidence synchronization remain open, so playtest-only focus is not yet justified. No ArtJobs were submitted and no Alexandria deployment or browser screenshots were verified.
<!-- note:end t-034 -->

## t-035 — Narrative coherence audit of Shifting Desks encounters and endings

<!-- note:begin t-035 -->
Silas, 2026-10-21 PT: Approved a full-deck creative quality pass following
the four-office-supply identity fix. Evaluate all 120 cards, reviews, window
shifts, and ending variants for clear setup-to-choice relationships,
surprising but earned outcomes, character continuity and later callbacks.
Record an evidence-backed audit and make scoped narrative improvements with
canonical pack, runtime snapshot, flag-map and regression-test parity.
Avoid overlapping Wellness/Sub-Level tone-ladder work in t-034.

Audited all five department inventories and ending variants; Conductor PR and Kind Robots companion implementation add three conditional narrative callbacks, five setup/outcome repairs and six ending echoes. Complete first scoped pass; prioritize further remaining flags and t-034 integration separately.

First scoped narrative audit completed. Full 120-card inventory and prioritized follow-up ledger merged on conductor PR #6465 (864ef2f, Worker PR CI, Python suite and security all green); runtime stories, ending callbacks and regression checks merged on kind_robots PR #3993 (28754b7, all 14 CI workflows green). Fixed the chronology trap discovered by adversarial review. Remaining Records callbacks and deeper deck polish are tracked by kind_robots issue #3994; t-034 Wellness/Sub-Level tone work remains independently unclaimed here.
<!-- note:end t-035 -->

## t-036 — Shifting Desks quality pass II: Records consequences and reachable callbacks

<!-- note:begin t-036 -->
FROM GITHUB ISSUE silasfelinus/kind_robots#3994 (https://github.com/silasfelinus/kind_robots/issues/3994), opened by @silasfelinus on 2026-10-21. Imported by scripts/sync_github_issues.py. Reference the issue in the implementing PR (`Closes silasfelinus/kind_robots#3994`) so it closes on merge; the bridge closes it otherwise once this task is done.

Follow-up to Conductor #6465 / Kind Robots #3993 and the evidence in `projects/shifting-desks/NARRATIVE-AUDIT-2026-10-21.md`.

**Goal:** Continue Silas's approved full-deck narrative quality work rather than treating the first five-card pass as completion.

**Priority 1:** Inspect all Records & Forms cards for authored future promises; prioritize `the-tube-that-goes-up`, `the-suggestion-tube`, `pip-at-window-10`, and the earlier reported-on-Pip / permanent-record threads. Make at least one *reachable* downstream scene or ending echo per consequential major choice. Challenge outcomes should stay causally linked on both success and failure.

**Priority 2:** Review Toy Division's `the-robot-panel` dissent flags, Beverly's inspector callbacks, and the moral effect of product decisions. Ensure no answer is offered without setup and no callback requires a flag obtainable only later in a run.

**Hard checks:** 2-4 routes per card; same run seeded deterministic, no clean wins; accurate Risky/Routine/Dire target 9/7/11; validate canonical pack, generate exact FLAG-MAP, sync Kind Robots snapshots, typecheck, simulation, phone/desktop layout. Preserve all existing art and images. Avoid conflicting with shifting-desks t-034 Wellness/Sub-Level tone-ladder work. Keep user-facing publication within approved scope and report deploy separately.

This should be the next independently claimable task, not a duplicate of t-035.

Conductor PR #6467 has merged at c17ec700b4ca6d56a97b9872863cd20ec24d28a1, after Worker PR CI, security and 2933 Python tests passed. Companion kind_robots PR #3996 has all story snapshots stamped to this source and is under final CI. Repaired six earlier-choice continuities and added 26 ending paragraphs; final completion waits for app checks and merge.

Pass II complete: Conductor PR #6467 merged as c17ec700b4ca6d56a97b9872863cd20ec24d28a1 after 2933 Python tests, security and all Worker CI; Kind Robots PR #3996 merged as d943618bb6582fcfc2bbbef2e6b1f8ea65849926 after all 14 workflows completed green. The PR closes issue #3994. Shipped 25 Records prose improvements, six reachable Toy callbacks, 26 flag-aware epilogue passages, verified exact flag map; no ArtJobs, DB migrations or app visual layout edits. No Vercel preview found; Alexandria production deploy remains unverified.
<!-- note:end t-036 -->

## t-037 — Narrative pass III: reviews remember employee history and Board endings

<!-- note:begin t-037 -->
Silas, 2026-10-21 PT: "sounds great, keep it up" after passes I and II.
Improve Records and Toy Division mandatory reviews with gated choices that
recognize prior actions, then add final Board ending acknowledgements tied
to the actual choices. Preserve seeded engine behavior, validators and art.
Keep Wellness/Sub-Level Zero pack text free for independent t-034.
Source and runtime snapshots must stay synchronized and both PRs green.

Pass III merged on Conductor PR #6474 at f793d56caaf50cfd00376ef9baf44b967bde01ab (full Worker PR CI, security and handoff green) and Kind Robots PR #4006 at dfe5050368f012342049f69f7de1bf32690a79eb (all 17 applicable workflows green). Kept the seven-choice limit and added two-maximum deterministic case-file exhibits on Records and Toy review screens, plus 18 real flag-keyed Board ending passages. Canonical ending data is stamped in Kind Robots to the merged Conductor SHA. No new art jobs or database schema edits. Live Alexandria deployment and cross-device visual rendering were not verified.
<!-- note:end t-037 -->

## t-038 — Adversarial playtest follow-up: risk rewards, successor memory and gated-choice coverage

<!-- note:begin t-038 -->
Silas-directed follow-up 2026-10-22 PT after 2,000 adversarial seeded runs. Reward authored costly interventions, make safe outcomes feel consequential, make Successor terminations remembered in epilogues, and distinguish unreachable gated options from declined available ones in CI telemetry. Mirror canonical Conductor encounter changes into Kind Robots runtime; preserve no-clean-wins, source parity and all eleven endings.

Canonical source PR silasfelinus/conductor#6490 merged d88e1a1f2cb13124fb7976b739ad0fd74372c6c4 and runtime PR silasfelinus/kind_robots#4021 merged 14a1b7762b8e1f1558b52ab4cdb756e2cc45563f. Added four success-only risky Forms with visible hints, persistent successor and choice consequences, and split 26 unpicked routes into 9 never offered versus 17 offered but not picked. Tested 2,000 seeded runs, 0 engine violations, all 11 endings. Conductor 25/25 and Kind Robots 23/23 GitHub check runs completed successfully or intentionally skipped. No external promotion or production deployment performed.

Implemented and merged Conductor PR #6490 and Kind Robots PR #4021. All 25 Conductor and 23 application GitHub checks passed or were intentionally skipped. Canonical and runtime reward manifests are byte-identical on main. New risk awards and epilogue receipts shipped to main, with a green 2,000-run adversarial playtest (zero softlocks and all eleven endings observed). Browser rendering and Alexandria production deployment remain unverified. Wider public promotion stays gated by t-020.
<!-- note:end t-038 -->

## t-039 — Adversarial pass III: discoverable prerequisite chains and earned callbacks

<!-- note:begin t-039 -->
Silas, 2026-10-22 PT: approved follow-through on Shifting Desks adversarial playtest. Examine the nine never-offered conditional routes. Preserve original unlocks and no-clean-wins, but establish new earned alternate discovery paths with honest narrative cues and matching canonical/runtime source data. Add deterministic source-to-target gate tests and compare standard simulated choice coverage. No public promotion, deployment or art generation.

Conductor PR #6494 merged fd58fbd13efb7f30439e9e365b08956f273fffa8 after all 25 check runs passed or were intentionally skipped. Kind Robots PR #4025 merged 619f791a070773fbda7474c7a9aeea1a1bca3eec after all 23 check runs passed or were intentionally skipped. Nine earned alternate prereq story chains, visible hints, distinct ending callbacks and tests added with canonical and runtime data byte-identical. Standard 2000-run adversarial test reduced never-offered choices from nine to two, never-picked from 26 to 24, without engine violations, stalls or losing any of eleven endings. No production deployment or promotion verified.

Canonical Conductor PR #6494 and Kind Robots PR #4025 merged, 25 and 23 respective check runs green or intentionally skipped. Original hidden routes retained, nine alternative earned clue chains and nine epilogue callbacks tested. 2,000 standard seeded runs yielded zero engine violations, zero stalls, all eleven endings and two (formerly nine) never-offered options. No verified production deployment, browser render or promotion.
<!-- note:end t-039 -->

## t-040 — First-clear Personnel Archive: persistent illustrated milestones, endings and run dossiers

<!-- note:begin t-040 -->
P1, owner directive 2026-10-23 PT. A finished run must leave visible evidence of accomplishment, immediately and across browser reloads. First naturally reached ending unlocks an accessible one-screen Personnel Archive and clearly announces the unlock on the ending screen, with persistent navigation at the front desk and from the ending. Tabs: Milestones, Endings, Achievements, Runs (discoveries optional). Cards show art/badges, earned timestamp, progress, silhouette/redaction for locked, filled/partial for progress, distinct rare treatment without spoilers. Initial milestones: first completion, first ending, full five-department clear, first mutation, secret-society membership, successor use, Board approval, first test report, form thresholds; never award a milestone unearned. Persist bounded finished-run dossiers (end ID, job, society, mutation, floors, employee count, forms, grades, date, seed) idempotently on reload; migrate existing endingsFound/current finished save as fairly as evidence permits and never invent unseen run histories. Honor reduced motion and responsive internal gallery scroll. Existing ending-gallery collection must remain available and 11 ending IDs unchanged. Test first win, refresh, repeat win, no win, tampered saves, mobile widths.

First-clear archive and mixed test reports landed in merged silasfelinus/kind_robots#4066 on 2026-10-23 PT; its Shifting Desks gameplay contract, TypeScript typecheck, and other recorded CI workflows passed. This task's original implementation scope is complete. Ending hero/badge art, ceremony, print cabinet, full visual acceptance and real-device QA remain independent follow-ups (t-032, t-041, t-042, t-044 through t-046).
<!-- note:end t-040 -->

## t-042 — End-of-run reward ceremony: achievement unlock, milestone progress and clear run summary

<!-- note:begin t-042 -->
P1. On first win show unlocked archive call-to-action; on every finish show earned ending hero, at least one linked achievement or milestone image/card, newly earned awards without duplicate unlock spam, progress toward remaining milestones, levels and departments cleared, mutations, society, files, successors, key incidents and next-play motivation. Render rewards above fold in the one-screen end panel without stealing all story text; no fake rewards and no spoilers for unseen paths. Existing Kind Robots achievements must remain authoritative when an achievement code exists; local milestone gallery supplements rather than duplicating global account rewards. Adversarial reload/double-resolve checks.

Implemented an end-of-run reward ceremony on Kind Robots branch worker/shifting-desks-t-042-20261027T173845Z-gpt6-74a9. One-screen ending hero now shows earned and previously filed distinctions, authentic receipt stats and a non-spoiler milestone next target. Session-scoped award announcements are idempotent and do not retrigger on reload. Added pure tests for duplicate and phantom award suppression. PR and CI review in progress; no rendered art, public promotion or deployment claimed.

DONE: silasfelinus/kind_robots#4306 merged as 824302d29e22cb560c21bf137e68b20245c0b262. End-of-run Personnel File now presents larger ending art, icon-backed awarded distinction, honest departments/files/employees/forms totals, job/society/mutation and next milestone progress. Newly-earned notices are session-only and deduplicated across repeated endings/reloads. Canonical Kind Robots achievements are unchanged. Verified the full PR workflow set: Shifting Desks gameplay contract, TypeScript Type Check, Layout Contract, changed-file Prettier, art/icon safety, schema parity, all four Contract Tests shards and verifier completed successfully. No PR preview exists and this merge is not evidence of a production deploy or visual acceptance. Remaining artwork and achievement images belong to t-032/t-041, printable dossier t-044, cabinet t-045 and full QA t-046; final fun/promotion gate t-020 remains human-controlled.
<!-- note:end t-042 -->

## t-043 — Test Results: credible mixed evaluations, liabilities and sharper HR writing

<!-- note:begin t-043 -->
P1. The first human full run had Empathy 13, Ingenuity 8, Obedience 7, Spite 6, all tagged Exceptional: unfun. Keep raw grades, seed, skill gates, thresholds and engine balance unchanged. Presentation may award at most one Exceptional; others gain relative or corporate liability descriptors (e.g. Productive Liability, Admirably Compliant, Valuable in Limited Amounts), with score-dependent and rank-dependent observations, paradoxical counterbalances and different report verdicts on repeat builds. No invented stat penalties or downgrading hidden numeric rolls. Preserve level/bar accessibility. Add golden case with 13/8/7/6, all-low and tied scores, varied seeded playthrough reports and first-read humor review. Any gameplay tradeoff proposal must be separate and balance-tested before touching mechanics.

First-clear archive and mixed test reports landed in merged silasfelinus/kind_robots#4066 on 2026-10-23 PT; its Shifting Desks gameplay contract, TypeScript typecheck, and other recorded CI workflows passed. This task's original implementation scope is complete. Ending hero/badge art, ceremony, print cabinet, full visual acceptance and real-device QA remain independent follow-ups (t-032, t-041, t-042, t-044 through t-046).
<!-- note:end t-043 -->

## t-047 — Playbook Forge upgrade: write the missing 135th encounter

<!-- note:begin t-047 -->
Silas, 2026-10-27 PT: "Anything that is in playbook forge and has quests unwritten or art prompts unwritten should be upgraded. (Memory dungeon will take the longest and should be last). Space couch has a lot of fresh writing still in need and still looking to capture that right blend of space comedy and satire. All art prompts should be written for the appropriate engine, no metaphors for krea2." Shared bar: kind_robots PR #4308 (verifyPlaybookArtPrompts, artPromptsComplete). Forge 2026-10-27: encounters 134/135.
DONE 2026-10-27 PT: kind_robots #4326 merged as 68c89a0 after 20/20 checks. Encounters 134->135: a fourth Consent Window applicant, Nadia the night nurse, who starts her signature awake and finishes it asleep. Seeded balance holds: rebel 47.5% eliminated, coward just over 2 Successors lost. No rendered window art yet.
<!-- note:end t-047 -->
