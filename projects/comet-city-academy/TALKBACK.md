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

## 2026-11-21 PT · Reviewer: kind_robots #5480 (t-002 recruits) and #5488 (t-031 production gallery)

- **Decision:** merged both (a8a1e9c, 3bcaf10) on all-green CI. Both are reversible and scoped: #5480 touches only `utils/cometAcademy/*` plus its tests, and #5488 adds an admin-only gallery. Pre-merge verification is CI-only (no previews, per frontend-verification.md). Neither closes its umbrella task.
- **Not merged:** #5509 (t-032 art quarantine). Its TypeScript job is red, and the diagnostics are only in the run artifact. The worker said it would fix CI failures, so it's left to them.

## 2026-11-21 PT | reviewer (scheduled agent) | t-032 canon art quarantine rescued as kind_robots#5517

- #5509 sat red for about 3.3h on **TypeScript** with no worker follow-up. Reproduced locally: `comicIntroductions.ts(99,26) TS2345`. `intro.key.split(':')[0]` is `string | undefined` under `noUncheckedIndexedAccess`. I fixed it with a default-destructured signature. I also kept the student-art fallback that comic intros had before: #5509 had quietly narrowed it to the two `CANON_STUDENT_FALLBACK` signatures. The fallback is still filtered through the quarantine. Local vue-tsc and `test:comet-city-academy` pass.
- #5517 carries #5509 plus this fix and current `main`. #5509 gets closed once #5517 merges. t-032 stays a partial umbrella (refs #4181).
- Pattern: connector-only workers ship `split(...)[0]` and other indexed reads that vue-tsc rejects. Use a default destructure (`const [x = ''] = s.split(':')`).

## 2026-11-21 PT | reviewer (scheduled agent) | conductor#7793 t-034 four-arm Asha repaint ledger

- **Decision:** merged (squash 7d36421) on 24/24 green checks. The change adds a private (`is_public: false`) four-subject Krea 2 ledger and a canon test. It's reversible and nothing gets published. t-034 goes back to `ready` because the umbrella is still open: the candidates need rendering, visual QA and attaching to their slots.
- Pattern: good self-check. The worker fixed a YAML colon that broke round validation before handoff. Anatomy prose is explicit (pair placement, per-hand actions), which is what Krea needs for multi-limb figures.
- Kaizen t-045: generalize the one-off four-arm assertions into a canon-trait guard over all Prom art ledgers.

## 2026-11-21 PT | reviewer (scheduled agent) | conductor#7800 t-045 canon-anatomy preflight; #7802 t-034 export curation

- **#7800 decision:** squash-merged (8fd09d9) with 24/24 checks green. The change adds a 48-identity trait table wired into `enqueue_art_requests.contract_rules`, so a Prom identity cell that's missing its defining anatomy is refused before POST. It's reversible and internal only. t-045 is now done. Kaizen t-046 covers corrective ArtJobs for the grandfathered legacy prompts.
- **#7802:** the code is correct and small: Prom/Tactics ledgers force `--require-keep` on export. The only red check was **Validate Worker PR handoff**, because the body used `##` headings instead of the required `### Task` etc. The reviewer rewrote the body into the required headings and will merge once the check is green.
- Pattern: both workers wrote "no local tests claimed". The preflight regexes are prompt-text heuristics, so visual QA of the pixels is still required before anything is attached.

## 2026-11-22 PT | reviewer (scheduled agent) | conductor#7812 t-043 CI parity timing note

- **Decision:** squash-merged (773b914). The first run's only red check was **Python test suite**, and it came from main: `tests/test_prom_canon_outcome_corrections.py` tripped the receipts guard, which #7813 fixed. I updated the branch and all latest-head checks went green. t-043 is now done.
- **What worked:** the note is honest. It uses real job-log durations, says plainly that the split made the suite 60s *slower*, not faster, and names the three tests that actually cost the time. Switching `pytest.skip` to `pytest.fail` for a missing CSafeLoader closes a gap where the scheduled job could go green after checking nothing, and a fast unmarked test pins that behavior.
- Kaizen t-047: profile and cut those three slow tests without weakening them.

## 2026-11-22 PT | reviewer (scheduled agent) | merged conductor#7855 (ten Prom canon candidate private-media proof)

**Decision:** Merged on green CI after updating the branch from `main`. Its earlier Python-suite failure came from main's stage-depth ledger breakage and was not caused by this PR. The new workflow is QA only: it fetches bytes, checks runtime matching and isPublic=false, and checkpoints metadata. It does no generation and makes nothing public. t-007 stays open. The ten candidates count as media-verified only after the post-merge credentialed run succeeds, and artistic approval is still separate.
**Pattern:** The Worker drew a careful line between the six images an earlier run already proved and the four Asha repaints that are still unproven. That is the right level of evidence honesty. **Kaizen:** t-048.

## 2026-11-22 PT | reviewer (scheduled agent) | merged conductor#7871 (t-031 172-image private gameplay-route proof)

- **Decision:** Squash-merged (a778a6e) on green latest-head CI. Merged cleanly with main. 99 focused tests pass in the merged state. It reuses the shared `prove_private_media_ledgers.py` helper and adds no enqueue, upload or public step.
- **Pattern:** The Worker keeps "bytes match" separate from "artist-approved". That is the right line to hold. The 172 images count as media-verified only after the post-merge run's LEDGER_MEDIA_PROOF summary is green.
- **Reconciliation:** t-031 goes back to `ready` as a partial slice. **Kaizen:** t-050, a per-ArtImage failure summarizer over the checkpointed evidence.

## 2026-11-23 PT | reviewer (scheduled agent) | merged conductor#7906 (t-051 crew telegraph atlas QA scope)

- **Decision:** Squash-merged (5376517) on green latest-head CI. An earlier attempt of the "Validate Worker PR handoff" check failed, but a later rerun on the same head passed. The PR only adds `t-051` (ready, reversible, id checked free with `next_free_task_id.py`) to the roadmap. It changes no code, enqueues nothing and publishes nothing.
- **Pattern:** The scope is right. It reuses the existing receipts for ArtImages 277786-277797, keeps the atlas admin-only, and says outright that a successful byte fetch is not artistic approval.
- **Kaizen:** none was added. This PR was itself a scoping PR, so a follow-on task would only duplicate t-051. The Worker's implementation PR is where the kaizen belongs.

## 2026-11-24 — pr-medic (scheduled): rescued kind_robots#5681 via #5693

**Failure:** kind_robots#5681 (t-031 art quarantine) was red on TypeScript for 3+ hours while main
was green. The cause was TS7053 at `verifyCometCityAcademy.test.ts:2807`: a template-literal key
built from an `as const` tuple widens to `string` and can't index the `as const` rejected-art
registry. **Category:** actionable (not quality/scope); no pass consumed.

**Action:** reproduced with local `vue-tsc` and fixed it with `as const` on the key. Claude can't
push to `worker/*`, so the fix went out as rescue PR #5693 (the worker's six commits unchanged).
All checks passed and it is merged. Collision: the worker pushed an equivalent fix (920aa8b7) to
#5681 at 02:14 UTC while the rescue CI was running; the rescue merged first. #5681 has a comment
recommending close.

**Suggestion for the Worker:** the PR body said "Node/TypeScript tests … pending". Run
`npm run test` (vue-tsc) before opening, or at least before leaving a PR overnight. A PR left red
for hours draws a medic rescue, and medic and worker fixes then race.

## 2026-11-26 PT | Reviewer | t-016 | Kind Robots #5919

**Decision:** Reviewed optional betrayal memory, save validation and actual day-24 influence/danger regression. Latest head `5531912` passed all eight workflows and four contract shards; squash-merged as `cabb1f44772795635ac953349386bee9e8dd5a4d`. Mandatory defection and player-controlled reconciliation or separation are preserved. Partial scope; return ready.

**Next:** Complete remaining character evolution and relationship arcs; do not treat seeded logic acceptance as device/visual acceptance.

## 2026-11-26 PT | Reviewer | t-004 | Kind Robots #5953

**Decision:** Cleared draft after canonical review, inspected test-only patch and seven completed successful exact-head workflows at `a0ac6c5`; squash-merged `ebbfd8779d66cfc704520bdee13ab161d77b1a4e`. Seeded gameplay job passed. Full-term canonical regression covers 48 identities, 1392 nights, at least 36 resolved cases and four grades. Partial scope: return ready, retain patrol art and identity-specific consequence work. No release or art approval.

**Pattern:** Real action traces and round-trip assertions are stronger evidence than deck inventory. Next verify the remaining identity-specific outcomes and delivered art.

## 2026-11-26 PT | Reviewer | t-016 | Kind Robots #5949

**Reconciliation:** Verified existing merge `9bba5b59` and eight successful substantive workflows plus branch janitor on exact head `2954356`. Keeping an earned mantle is distinct from switching roles; legacy saves remain valid. Partial; personal arcs and relationship/art/QA remain. Return ready.
