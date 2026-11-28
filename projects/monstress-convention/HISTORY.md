# monstress-convention — task history archive

Full `note:` prose for completed monstress-convention tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — MONSTRIQUE private opening screen and Playbook Kit scaffold with mature access

<!-- note:begin t-001 -->
Build the MONSTRIQUE Vignette spec and private title screen at /admin/monstrexx within the existing shell, plus an initial navigable hotel lobby scene. Verify admin AND viewerShowsMature on server; no guest/CHILD/mature-off rendering or leaking assets. Do not expose Play/nav/highlights until the separate release gate. Art briefs now, ArtJobs when available; painted images are not a code blocker. Test phone/tablet/desktop.
2026-11-06 PT: Done. Private title screen (New Game, Continue, Settings, Scrapbook) and Vignette kit spec shipped in kind_robots #4845/#4848; renamed MONSTRIQUE at /admin/monstrique with Chapter 1 rewrite, flirt/gratitude and favour puzzle in #4867. Server-checked admin + mature opt-in, no CHILD; public Play/nav still behind t-013. Visual check on main pending (gated route, no pre-deploy screenshots).
<!-- note:end t-001 -->

## t-002 — Soft creative scope review, continue development

<!-- note:begin t-002 -->
Present the premise, cast, first playable slice and tier-growth recommendation to Silas without halting reversible implementation or treating silence as publication approval. 2026-11-06 PT: STORY-BIBLE.md written from Silas's MONSTRIQUE brief. Recommendation awaiting Silas: culprit = Marta the night manager, secretly the band's invisible fifth member "Little Miss Nobody" (alternate: Draculina). Build Chapters 2-5 against it; lock it only in Chapter 6.
FOR SILAS (2026-11-06 PT): Premise, cast, Chapter 1 and growth plan are written up in STORY-BIBLE.md (with FRANCHISE-HISTORY.md as the authority) and playable at /admin/monstrique. Two decisions: (1) Culprit. RECOMMENDATION: Marta the night manager, secretly the band's invisible first erasure "Little Miss Nobody"; the alternate is Draculina. Chapter 1 already plants Marta's clues, and nothing locks until Chapter 6. (2) Mummy name: DESIGN-BRIEF says Celestine Veil, the ledger says Nefertari, and Chapter 1 shows Celestine at the convention. One character or two, and which name? Soft gate: Chapters 2-5 can be built meanwhile. Reversible, so the 2026-09-30 default- recommendation rule may adopt (1) after 7 days.
2026-11-07 PT: Done; Silas decided in session: "I like draculina for the villain. But in the last act. The mummy should be named Cleo Pappatra". Canon updated in STORY-BIBLE.md (case, endings, chapter plan) and across the project docs.
<!-- note:end t-002 -->

## t-016 — MONSTRIQUE achievement upgrade: 12 or more live achievements

<!-- note:begin t-016 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 0 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5066 (d3a33c8), all checks green: 16 live achievements from a shared achievementsFor(prev,next) in both case stores' commit(); no mature-only achievements; load, mode-load and forgetCase never award. Catalog seed run 43175067016 succeeded. Title-menu entry left for the standard task.
<!-- note:end t-016 -->

## t-017 — Chapter 1 delivered art in the game: painted rooms, cast figures, walk areas refit

<!-- note:begin t-017 -->
Replace the hand-coded SVG room paintings and vector cast with round CH1-CAST-AND-MOTEL-R1 (ArtImages 280896-280913, all DONE): seven painted backgrounds, stage figures cut out with transparent backgrounds, ghost expression sheets for dialogue portraits. Static general-safe files like the title splash; re-fit WALK_AREAS, hotspot coordinates and per-exit entry points to each painting; keep SVG only as a missing-art fallback. Main-game standard: no SVG art. Closes t-003's remainder.

kind_robots#6027 merged (squash 7afeb22) after all 12 checks were green, including TypeScript and the 4 contract shards. Seven Chapter 1 rooms (motel exterior, front office, ice alcove, balcony, Rooms 205/207/204) now render painted backgrounds (ArtImages 280905-280911) from public/monstress-convention/rooms. Hand-drawn SVG remains only as the missing-art fallback for city-map and convention-center. Marta, Dolores, Gavin and the Odette/Violet ghosts stand as cut-out figures (280900-280904): feet on marks, depth-scaled, ghost float, speaker bob, Marta clipped behind the counter. Painted dialogue portraits come from the ghost expression sheets and figure crops. A 1344x768 world layer letterboxes on desktop over blurred ambient art and pans with Iris on phones, so pips stay on their objects. Every hotspot, WALK_AREAS floor, per-room depth and per-door entry point is refit to the paintings (closes t-003's remainder). Data lives in utils/monstrique/stageArt.ts; the art-pipeline and navigation contract tests are extended. Visual QA used Playwright at 390x844 and 1440x900 for every painted room: no page errors, no overflow. The missing city-map and convention-center backgrounds are queued as round CH1-CITY-AND-CONVENTION-R1 (conductor#8150, merged). Iris, Norb and Cleo stay vector until t-018/t-020.
<!-- note:end t-017 -->
