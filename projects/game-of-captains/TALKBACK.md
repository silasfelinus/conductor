# Space Couch review feedback

## 2026-11-19 PT · t-041 shared settings (#5368)

- **Decision:** merged reversible app PR [kind_robots#5368](https://github.com/silasfelinus/kind_robots/pull/5368), squash commit `98bec1780a071b1b3fdbc971c2f79e16a57136d1`.
- **Verification:** nine exact-head GitHub Actions workflow groups completed success, including the full seeded Space Couch voyage matrix, Playbook Kit, TypeScript, layout, and all contract shards. No authentic browser viewport/art URL acceptance was claimed.
- **Positive:** replaced the separate title-only preference toggles with the existing Playbook Kit settings sheet; preserved `game-of-captains-voyage-v1` and old preference records; covered legacy migration and reactive text/motion presentation with regression tests.
- **Remaining:** account-backed voyage and live achievement verification, delivered painted ending/species URLs, 390/768/1440 browser QA, and independent editorial/art review. Return t-041 to READY (partial), not DONE.
- **Lesson:** migrate historical preference records once and prefer the current versioned settings system, without introducing a second write path or resetting unrelated saves.

## 2026-11-19 PT · t-041 portable voyage backup (#5378)

- **Decision:** merged reversible Kind Robots PR [#5378](https://github.com/silasfelinus/kind_robots/pull/5378) at `a4de97d2e954c64926781b5c52653eb572b42734`.
- **Verification:** all nine original latest exact-head checks COMPLETED/SUCCESS: TypeScript, Playbook Kit, layout, formatting, schema parity, architecture, seeded gameplay, full Space Couch adversarial voyages and all four contract shards. No browser preview/production deployment was asserted.
- **Review finding:** initial backup import introduced a second intentional `restoring = true` path. The achievement contract rightly caught the changed number of guarded restores, and we explicitly asserted imported progress cannot award achievements. A second test used the wrong expected union size for two devices; it now pins preservation of all distinct finished voyages.
- **Positive:** current-save format, completed-run IDs and account-bound records preserved. Explicit import confirmation, JSON shape validation, duplicate-safe history merge and rollback on failed storage writes reduce the risk of losing a run.
- **Remaining:** finish the agent-owned art and responsive verification tasks; do not conflate a local backup with authenticated cloud save or claim subjective art approval. t-041 remains READY (partial).
- **Lesson:** test both historical progress import paths and the union of unique records rather than assuming imported history supersedes local progress.

## 2026-11-19 PT · t-033 curated redshirt ArtSlots (#5387)

- **Decision:** merged reversible app PR [#5387](https://github.com/silasfelinus/kind_robots/pull/5387), squash `a45ae0501aa77bca0358447429d1352f36136afb`.
- **Verified:** all 14 exact-head workflows completed success, including TypeScript, formatting, gameplay, adversarial voyages, repository-wide contracts, privacy rules, and PR container validation. Production deployment and authenticated render URLs are **not** verified.
- **Positive:** 24 known DONE round-three Krea2 images now have an explicit curator registration route and Forge UI. A public redshirt art endpoint delivers only the selected `liked` ArtSlot candidate when its image is public, active and non-mature, with the previously shipped portrait or glyph retained as a safe fallback.
- **Remaining:** 77/100 static portraits and 99/100 static power plates remain shipped; 23 portrait and one power replacement require genuine image review, approval and final source shipment. No private ArtJob status was mistaken for accepted art. Task stays READY (partial), issue #4182 stays open.
- **Lesson:** distinguish rendered, registered, reviewed, selected, publicly deliverable, and visually inspected states; make the workflow safely navigable without auto-approving uncurated images.

## 2026-11-20 PT · t-031 alien redo curation workflow (#5422)

- **Decision:** merged reversible Kind Robots PR [#5422](https://github.com/silasfelinus/kind_robots/pull/5422) as `708a0f8c893dead1bf31f897f9dfc2feefbb7bba` after all 12 exact-head GitHub Actions workflows completed success, including TypeScript, four contract shards, formatting and full Space Couch adversarial voyages.
- **Positive:** registered exactly 22 DONE redo images as unselected curator candidates with fixed ArtJob/ArtImage provenance; runtime accepts only explicit liked-and-selected candidates with the existing viewer-specific access filter. The 22 failed originals remain quarantined, and no image was automatically approved or published.
- **Remaining:** direct physical image review and authenticated private art URLs, redshirt and ending art coverage, responsive 390/768/1440 browser QA, and final roadmap readiness all remain agent-owned. t-031 goes back to READY partial. Master issue #4182 and species issue #4592 remain open.
- **Lesson:** make art candidates independently inspectable, but separate render status, human-visible verdict, viewer authorization and delivered-game display at every stage.

## 2026-11-20 PT — t-033 redshirt curator navigation, duplicate review

- **Decision:** merged scoped reversible kind_robots PR #5447 as `35d30b2` after seven completed-success latest-head Actions groups; closed duplicate PR #5446 unmerged. Both independently implemented the same art-slot deep link, so merging both would create unnecessary conflicts.
- **Verification:** three-file change filters the Forge to Space Couch redshirt slots and keeps single-candidate review visible, with source-based regression assertions. Saved-game IDs, access control and image verdicts unchanged.
- **Follow-up:** t-033 is still READY/partial, not art-delivered. The 23 portrait candidates and one power plate require actual image inspection, explicit selection and authenticated URL checks. The four older REVIEW tasks were inspected against main and queued for READY reconciliation; no completed gameplay/art scope was relabeled done.
- **Lesson:** compare contemporaneous worker PRs before merging; an active review flag without recent work should not block independent next steps.

## 2026-11-21 PT · art-medic: two Space Couch ledgers rejected by live prompt contract; #7718 sent back

- **Fix:** `ETHICAL-OUTCOMES-ROUND-1` and `SHIELD-POCKET-CONTINUITY-ROUND-1` lane suffixes ended "No text/lettering, logos, captions or watermarks." kind_robots' live contract rejects any text-noun negation on krea2 (cfg 1, negative prompt inert), so all 18 cells were skipped. Replaced with "Every surface bare and unmarked."; `check_art_prompts_live_contract.py --project game-of-captains` now 36/36.
- **Review #7718 (t-009 chapter-nine scenes):** 0/12 cells would pass — every prompt carries "not ordinary humans or Earth animals" (people-negation) and "no readable text, no lettering, no logos" (text-exclusion), plus "without legible writing" on deposit-copy-reveal. Needs-changes, not a quality pass: rewrite as positive statements and run the live contract checker before handoff.
- **Lesson:** run `python scripts/check_art_prompts_live_contract.py --kr-repo ../kind_robots --ref origin/main --project <slug>` on every new art ledger before opening the PR; the local builder's 4-noun pile limit is looser than the live server.

## 2026-11-21 PT · Reviewer: conductor#7736 chapter-nine provenance guard (t-009)

- **Decision:** fixed up and merged once green. Test-only, reversible, in scope.
- **Finding:** CI was green on the stale base, but once merged with main the new test failed. The live art sweep (`22edc4e`) had just checkpointed all 12 chapter-nine jobs to `DONE` with ArtImage ids, and the guard's allow-list (`PENDING/REJECTED/ACCEPTED`) didn't include `DONE`. Actionable rather than quality, so no pass spent. The reviewer made a one-line adaptation: `DONE`/`ACCEPTED` need a positive ArtImage id, `PENDING`/`ERROR` need none, and `DONE` still doesn't imply visual acceptance. The PR body also lacked the handoff template (Validate Worker PR handoff was red); filled in.
- **Pattern:** the worker understood the render-vs-accepted distinction, but hard-coded the status vocabulary from a snapshot of the ledger. Ledger statuses move under the branch hourly.
- **Suggestion:** before handoff, run new ledger tests against a fresh `origin/main` merge, and source status names from one shared set (kaizen t-042).

## 2026-11-21 PT · Reviewer: t-033 redshirt delivery audit (#7740 → rescue #7748)

- **Decision:** rescued and merged #7748 (446cb48), closed #7740. The audit script is unchanged. The test fixture wrote `b"\\x10\\x00..."` (escaped backslashes), so the RIFF size became 16 ASCII bytes, `WEBP` sat at the wrong offset and the audit correctly rejected every fixture: 2 Python-suite failures. The PR body also lacked the handoff headings. Actionable, so no pass spent.
- **Pattern:** the same double-escaped byte literal appeared the same hour in rainbow #7747 (production code there). It looks like a tool-escaping habit in the connector Worker, not a one-off.
- **Suggestion:** kaizen t-043 adds a test that rejects `\\x` inside a `b"..."` literal in new scripts/tests.
