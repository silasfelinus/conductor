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

## t-010 — Public launch and Silas's visual/story verdict

<!-- note:begin t-010 -->
Present final accessible preview, art coverage, combat/rules balance, endings checklist and gamebook tone for Silas's verdict. Do not expose publicly or assert production deployment until approval.
2026-10-10: Silas, verbatim: "cool, this is good enough for public facing, move the gamebook out of admin". Public-launch verdict given ahead of the t-009 QA pass; kind_robots#3413 drops the admin gate (page + Play tab requiredRole). Merged is not deployed: live once Alexandria's deploy picks up main. t-009 QA continues post-launch.
<!-- note:end t-010 -->
