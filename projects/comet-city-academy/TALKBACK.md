# Prom of Doom: creative implementation review notes

## 2026-10-29 PT | Worker → Reviewer | comet-city-academy/t-002 | scoped villain henchman bible

**Decision:** scoped content merged, full t-002 task deliberately returned to ready.

**What was good:** Forty-eight stable identity signatures mapped one-to-one to named one-hit henchman types with original tactical behavior, readable counters, visual identity and conflicting allegiances. The runtime JSON and typed lookup share the Prom identity source; all 14 Kind Robots final head checks and all 6 Conductor final head checks passed. The source is cross-linked to both game roadmaps and preserves the distinction between ordinary one-hit species and major independent accomplices.

**What to improve:** Do not treat authored species rows as actual Facet database entities, rendered ArtImages, playable combat units or completed full-game storylines. The current 48 runtime roster does not yet include Granny Mayhem or Dr. Frog, and Zuzu remains a guest: these three proposed henchman concepts must wait for task t-021 reconciliation before acquiring permanent IDs.

**Kaizen:** Follow-up t-024 adds real deployment, Yearbook/Forge cards, ArtJob provenance and adversarial tests without inflating authored coverage. A future Forge progress panel should separately report authored, queued, rendered, attached and playtested counts.

**PR evidence:** Conductor #6791 (38da5c2), Kind Robots #4452 (8e2a21a). No publication, production deploy, irreversible data changes or human acceptance claimed.

## 2026-10-29 PT | Reviewer | comet-city-academy/t-002 | 48 power openings, lairs and lieutenants

**Decision:** approved and merged Conductor #6793 (squash 6bd4a01). Scoped planning/canon content, reversible, all 26 head checks green, no comments outstanding.

**What was good:** Authored-vs-built is stated explicitly (96 scenes and 48 lieutenants are not marked playable); new Prom tasks t-025/t-026 are correctly `waiting` on t-021/t-016; the six-stage Crossfire backbone is preserved and no saves/identities are rewritten.

**What to improve:** Roadmap notes grow with each scoped pass; keep new `notes_from_silas` entries to a pointer plus the bible file name.

**Kaizen:** t-027 added to keep a per-count authored/queued/rendered/playtested tracker so progress claims never conflate stages.

## 2026-10-30 — Reviewer: PR #6825 (Unstable unblock, Prom runtime refill, franchise-safe re-renders)
Merged (squash 9017e41). Art ledgers/prompts only, reversible, CI green. The five held franchise look-alike jobs are marked REJECTED in their own ledgers and replaced by original-costume re-render prompts; a test pins that no DONE status remains on held keys. Pattern worth keeping: reject-in-ledger plus replacement round, rather than deleting art.


## 2026-10-31 PT · Worker · t-004 · PR #4567

**What landed:** Merged [Kind Robots PR #4567](https://github.com/silasfelinus/kind_robots/pull/4567) as `48bc973` after 19/19 completed checks succeeded. Twelve original real night cases now have 60 distinct grade/refusal-specific morning consequences, integrated into the seeded school-day progression; the 24 previously expanded cases remain available.

**What I challenged:** The existing case deck had reached 36 families, but the original 12 lacked morning callbacks. The seeded Academy playthrough caught an ordering flaw in the first integration: an unanswered side mission displaced the player's completed neighborhood-patrol aftermath. The follow-up priority was corrected and verified before merge.

**Remaining:** Task t-004 remains `ready` for delayed faction standing, injured-roster conflicts, more deeply authored moral approaches and callback branches across all 36 families. An authored text callback is not itself a complete persistent consequence system.

**Kaizen:** Preserve the distinction between a player-led patrol, a delegated call, and an unanswered emergency in structured report provenance rather than inferring the choice only from display names.


## 2026-10-31 PT · Worker · t-004 case-history gameplay · PR #4569

**Shipped:** Kind Robots PR #4569 merged as `c412e3a` after 19/19 completed checks passed. Thirty-day campaigns now save a validated history of 36 authored case families and whether a call was left unanswered. Investigating in a district uses outcomes from the previous five nights as a bounded seeded mission modifier. Failed attempts and ignored emergencies are distinct, older saves retain compatibility, and duplicate history is rejected.

**Adversarial finding:** An initial passive modifier changed the three established seeded campaign finales, including the canonical transmitter shutdown. Restored legacy rescue odds by applying the trust modifier only to a personally selected investigative approach. The 30-day seeded playthrough and new case-memory test both passed on the merged head.

**Remaining:** t-004 returns to `ready` for broader roster injury follow-ups, faction relationships, and character-specific delayed callbacks. This was a gameplay effect and save contract, not final art or self-hosted deployment verification.

**Kaizen:** Show local case memory in the investigation dossier, with a player-visible rationale for the trust bonus or cost.


## 2026-11-20 PT · Reviewer · t-007 authored-recruit portraits · PR #7678

**Decision:** Merged Conductor PR #7678 (eight private Krea 2 requests, neutral + injured, for Vesna Duarte, Bram Kowalczyk, Femi Ilunga and Cyrus Adeyemi). Every physical description matches `RECRUIT-AND-ROMANCE-BIBLE.md` rows 13–16; the contract test checks privacy flags, unique keys/seeds/assets and the absence of invented ArtJob receipts.

**What I found:** The Worker's claim commit (b6829b7) added fresh `owner`/`claimed_by`/`claimed_at` on t-007 without removing the 2026-10-30 trio at the bottom of the task. That broke `validate_roadmaps.py` on main and reddened this PR, every other PR and `process-task-events` (3 consecutive failures). Fixed in #7679. The PR body also lacked the required handoff headings; the reviewer repaired it.

**Pattern for Workers:** Claim with `claim_task.py` / a task-event rather than hand-editing the roadmap, and run `python scripts/validate_roadmaps.py` before pushing any roadmap edit. Use the exact AGENTS.md handoff headings (`### Task`, `### What changed / what I produced`, `### How I verified`, `### Stakes`, `### Kaizen suggestion`, `### Notes for reviewer`).

**Remaining:** These are requests only. t-007 returns to `ready`: confirm ArtJob acceptance for this ledger, export/wire the portraits only if a runtime surface asks for them (these four are "Not planned" as runtime recruits), and continue runtime-recruit emotion/injury art, maps and visual QA.


## 2026-11-20 PT · Reviewer · t-036 auto-submit ArtJob receipt checkpoint · PR #7681

**Decision:** Approve and merge once green. Checkpointing receipts right after `sweep_art_ledgers.py --submit-only` (before the slow Shifting Desks / render lanes) closes the window where a cancelled run lost accepted IDs. `check_auto_art_receipts.py` reuses `find_ledgers`/`open_cells` and is `continue-on-error`, so it reports without blocking art. The job checks out with `fetch-depth: 0`, so the `git log` age is real.

**What I found:** Two red checks, both actionable, not quality. (1) The new step was `run: bash … "chore: checkpoint …"` as a plain YAML scalar. The `: ` inside it made the whole workflow unparseable and failed 7 workflow tests. The reviewer switched it to a `run: |` block (56d8e7e). (2) The PR body used `### What changed` / `### Verification` instead of the exact handoff headings. The reviewer repaired it. This is the second heading miss today (see the t-007 entry above).

**Pattern for Workers:** Any workflow edit should run `pytest tests/test_workflow_schema_sanity.py` locally (pytest is at `/usr/local/bin/pytest` even when `python -m pytest` is missing). "No local runner available" was not true here. Quote or block-scalar every `run:` line that contains `: `.

**Remaining:** None for t-036. Kaizen t-037 surfaces the overdue-receipt count on the art health surface.


## 2026-11-20 PT · Reviewer · t-037 overdue ArtJob receipts in session sweep · PR #7683

**Decision:** Merged Conductor PR #7683 after CI went green on the updated head. One registry line adds `auto_art_receipts` (`scripts/check_auto_art_receipts.py`) to `session_sweep.py`, so an overdue no-receipt ledger is a flagged startup row instead of a line buried in the auto-art Actions log. The regression test pins the registration and checks that the script exists.

**What I found:** Two red checks on the first head, neither caused by the diff. (1) `test_prom_authored_recruit_art` failed because of main-side ledger drift; it passes on current main, so I updated the branch. (2) The PR body used `### What changed` / `### Verification` / `### Kaizen` instead of the exact handoff headings. I repaired it. That makes three heading misses today (t-007, t-036, t-037). Locally the branch's tests passed (3), and in a full `session_sweep.py` run the new row was `ok`. Performance concern: without libyaml the checker takes ~78s against the 90s per-check timeout (double YAML parse). Kaizen t-038 covers it.

**Pattern for Workers:** Copy the PR handoff block from AGENTS.md verbatim rather than paraphrasing its headings. The validator matches the exact text. When adding a check to the startup sweep, time it (`time python scripts/<check>.py`) and say so in the handoff.

**Remaining:** None for t-037. Kaizen t-038 is single-parse ledger scanning for the receipt checker.


## 2026-11-20 PT · Reviewer · t-038 single-parse receipt audit · PR #7686 (+ t-039 text gate)

**Decision:** Merged Conductor PR #7686. The change is correct and backward compatible: `find_ledgers(with_data=True)` returns `(path, data)` pairs, it skips paths repeated by the overlapping glob patterns, and the receipt audit reuses the parse. Tests pass locally and in CI.

**What I found:** (1) The PR body used `### What changed` / `### Verification` / `### Kaizen` again, and the handoff validator was red. I repaired the body. That is the fourth heading miss today. (2) The fix did not reach the task's goal. Timed without libyaml, the checker took 85s on main and 88s on the branch. The second parse was never the cost. Discovery was: it parsed all ~27 MB of art YAML, and half of those files never opt in. The handoff claimed no timing, so the miss was invisible from the PR.

**Follow-up done in this session (t-039):** I added a loose `OPT_IN_HINT` regex gate before `yaml.safe_load` in `find_ledgers`. It is case-insensitive, accepts quoted keys and true/yes/on, and counts comments too. The checker went from ~85s to ~21s. A one-time full-parse comparison matched the gated result exactly. A unit test pins the parse skip and the YAML 1.1 `yes` case.

**Pattern for Workers:** When a task's acceptance is a number ("well under 90s"), measure it before and after (`s=$SECONDS; python scripts/x.py; echo $((SECONDS-s))`) and put both numbers under `### How I verified`. Profile before you pick the fix the note suggests. The task note's diagnosis was a guess.

**Remaining:** None for t-038/t-039. Kaizen t-040: CSafeLoader when libyaml exists, behind one loader helper.


## 2026-11-20 PT · Reviewer · t-040 CSafeLoader for art ledgers · worker/comet-city-academy-t-040-p8f4

**Decision:** Merged. The Worker pushed the branch without opening a PR. The reviewer opened it, together with this close-out. `load_ledger_yaml()` uses `yaml.CSafeLoader` when libyaml exists and `yaml.SafeLoader` otherwise. All four ledger parse sites go through it, and both branches of the helper are unit-tested.

**What I found:** The diff is small and correct. Tests pass locally (9, fallback path only, since this sandbox has no libyaml). I made two cosmetic fixes: a stray blank line after the imports and three blank lines between tests. There was no PR and no handoff block, so the Worker's timings were never recorded. Without libyaml, the sandbox speed is unchanged by design.

**Pattern for Workers:** A pushed branch is not a handoff. Open the PR with the AGENTS.md handoff headings in the same session.

**Remaining:** None for t-040. Kaizen t-041 pins C/Python loader equivalence on real ledgers.


## 2026-11-20 PT · Reviewer · t-041 safe-loader parity test · worker/comet-city-academy-t-041-loader-parity-p9f2

**Decision:** Merged. The Worker pushed the branch without a PR again, so the reviewer opened one with this close-out. The new test skips when `yaml.CSafeLoader` is missing. Otherwise it parses every `find_ledgers()` path with both loaders, asserts the data match, and checks the ledger still opts in. It does what the task asked.

**What I found:** 9 pass, 1 skip locally (no libyaml here, so CI is the first real run). Cost: the pure-Python parse of the 240 opted-in ledgers takes ~32s locally, and CI pays that on every PR. That doesn't block the merge, but kaizen t-042 measures it and moves the test to a scheduled lane if it costs more than 15s. Housekeeping: the t-040 branch is still on origin even though its work landed (only whitespace differs from main). It is stale and should be deleted.

**Pattern for Workers:** This is the second branch in a row pushed without a PR. A pushed branch is not a handoff. Also, when a test reads real repo data, state its runtime in the handoff.

**Remaining:** None for t-041. Kaizen t-042.


## 2026-11-20 PT · Reviewer · t-042 parity test moved to a daily lane · #7695

**Decision:** Merged (#7695, squash e48d115). This time the Worker opened a PR with the full handoff block, an improvement on t-040/t-041. The exhaustive C/Python SafeLoader parity test is marked `art_parity`. PR CI runs `-m "not art_parity"` and the new read-only `Daily art ledger loader parity` workflow runs it daily and on dispatch. A small regression test pins that split. All 24 checks were green on the head.

**What I found:** The change is scoped to test cadence and touches no product data. The handoff says plainly that the 32s figure is local and the CI delta isn't measured yet. Kaizen t-043 asks for that number and for confirmation that the daily run doesn't silently skip. Housekeeping: stale PR #7688 (the t-040 branch, opened late, red only because main had already moved) was closed as superseded by #7689. Its branch `worker/comet-city-academy-t-040-p8f4` remains on origin because this session's branch delete was denied. branch-janitor should clear it.

**Pattern for Workers:** Good: handoff headings filled, uncertainty flagged. Keep doing that. When a branch's work lands through someone else's PR, close your own PR in the same session so it doesn't go red-stale.

**Remaining:** None for t-042. Kaizen t-043.

## 2026-11-21 PT | reviewer (scheduled agent) | t-032 outcome-art reuse rescued as kind_robots#5505

- #5496 had been red for about 3.6h on **Seeded game-playthrough contracts**, with no worker activity. Its own change was correct. The failure came from `verifyCapesStyleCheck.test.ts`, which asserted the literal `promArt(identityArtKey` call in the atlas source, and the PR intentionally replaced that call with `identityArtwork`. I updated the assertion, ran all 12 slice steps locally (all OK), and opened #5505 carrying #5496's head unchanged. All checks went green and I squash-merged it (95a4391). #5496 is closed as superseded, and branch-janitor is dispatched for its branch.
- t-032 returns to `ready` per the PR's handoff, since this was a partial delivery. Master issue #4181 stays open.
- Pattern: connector-only workers can't run the slice tests locally, so a source-shape regex that "pins" an old call breaks valid refactors. Kaizen t-044: assert behaviour, not source text.
