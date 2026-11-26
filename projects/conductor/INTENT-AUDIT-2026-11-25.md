# Portfolio Intent Audit — 2026-11-25 PT

A scheduled Conductor agent ran this review two days before the 11-27 deadline, after `select_role.py` assigned `roadmap-intent-auditor` (upcoming). It used no paid model API and did no device testing.

Sources read:
- `OVERSIGHT-AGENT.md` and the 2026-11-24 audit.
- Lifecycle and priority sources. `git log` shows no change to `CONTROL.md`, `priority.yaml` or `project-overrides.yaml` since the 11-24 audit; the only commit in that window is an ArtJob ledger record.
- Output of `session_sweep.py`, `project_triage.py` and `check_pr_merged_drift.py`.
- The open-task lists for rainbow-bullet-hell-space-princess, save-the-plumber and hopeful-hues. The note tails for rainbow t-012, t-013, t-022, t-030 and t-044, and for comet-city-academy t-002, t-016 and t-034.
- The open PRs in conductor and kind_robots, conductor#8037 (open) and kind_robots#5856 (merged).

## Verified

- **Direction is unchanged since 11-24.** No new human lifecycle or priority decision has landed. Rainbow and Save the Plumber still lead `priority.yaml` as the remaining `active` games in the 2026-10-21 focus tier.
- **Rainbow is at Tier A** (60/67 done) and its main-game standard shows real delivered work:
  - t-044 has shipped work for every row of STANDARD-AUDIT-2026-11-12 (kind_robots#5679, #5670, #5628, #5547).
  - t-012 has its critic fixes in #5709.
  - t-013 has the scripted persona matrix in #5709, which found and fixed the Delphion stalemate.
  - What remains is art and animation that is still rendering (t-022 and t-030, per ART/ANIM-BACKLOG-2026-11-24) and Silas's t-014 verdict. That matches the Tier-A guidance: move art and close reviews, with no extra polish sessions.
  - The 11-24 stale claim on rainbow t-011 was resolved. The task is now `done`.
- **Save the Plumber is moving on its Gen-2 engine.** t-020 is claimed with an open PR, kind_robots#5861 (independent camera for sealed pipe chambers). Its world tasks (t-021 to t-023) correctly wait on it.
- **Hopeful Hues reached a playtest handoff within two days of Silas's 11-23 direction.**
  - kind_robots#5856 merged with 13 green checks. It adds the conveyor, portal and buddy-dispenser mechanics, a 390/768/1440 browser playthrough harness, and a bot run that wins 495/495 levels. The PR says all 118 painted art slots are live.
  - conductor#8037 (open, from that session) moves the project to `playtest`/`normal`. See Still questionable.

## Corrected (this cycle)

- **The projection payload was at 82.7% of its 4 MB limit, and kr-arcade's roadmap was over its size limit again (170,253 bytes).** I ran `archive_done_task_notes.py --all`, a byte-for-byte verified move under the AGENTS.md archival carve-out. It archived 21 done-task notes across 9 projects and saved 54,344 bytes.
  - kr-arcade is now 149,005 bytes, under the 150,000 threshold.
  - Rainbow freed 19,869 bytes, mostly from the closed t-011.
  - `--verify-only` reports that all 100 archive pointers resolve.
  - The projection payload is now at 81.3% (746 KB headroom).
- **Three comet-city-academy tasks were stuck in `review` with expired claims, although their own notes say to return to `ready` after merge.** I queued `ready` task events. The scope is unchanged, and no matching PR or `worker/comet-city-academy-t-0*` branch exists in kind_robots.
  - **t-002**: kind_robots#4492 merged 10-30. Claimed since 11-21. The note says "return to ready after merge".
  - **t-016**: kind_robots#4842 merged 11-06. Claimed since 11-21. The note says "task stays ready for the remaining slices".
  - **t-034**: conductor#7793 merged 11-22. Claimed since 11-22. The note says "Partial; umbrella back to ready".

## Still questionable

1. **The Hopeful Hues done claims overreach on two tasks.** This is advisory for the reviewer of conductor#8037. I left the PR alone because its own session is live.
   - **t-013** is titled "...painted tile set trial...". The PR's own correction says the painted tile atlas "was never actually trialled". Either that part of the scope was dropped on purpose, in which case the note should say it was waived and why, or t-013 is not done.
   - **t-003** asks for "each far region" to get a signature mechanic. #5856 rotates three shared mechanics across the regions. That is good variety, but it is not one signature mechanic per region.
   - The `playtest` contract requires the finite roadmap to be genuinely complete. **Recommendation:** merge the lifecycle change only after t-013 records an explicit waiver or is split into a `playtest_iteration` follow-up, and after t-003's note states the rotation decision. No human gate is needed unless the reviewer disagrees.
2. **Hopeful Hues claimed five tasks at once.** Session `sbjq3s` claimed t-002, t-003, t-005, t-009 and t-013 at 11-25 23:50Z. That breaks hard rule 4 (one active claim). The result was one coherent PR, but the pattern should not spread. This is a process note for the reviewer, not a decision for Silas.
3. **Using `review` for partial work in progress is still systemic** (carried from 11-24). `check_pr_merged_drift.py` finds 35 tasks at `claimed`/`review` whose implementation PR already merged: comet-city-academy 9 (3 fixed above), every-villain-tactics 8, kr-arcade 8, rainbow 5 and deepheart 5. Some go back to 10-30. Reviewers releasing these partial tasks one at a time (every-villain-tactics on 11-25) helps, but it is not keeping pace.
   - **Recommendation:** have `process_task_events.py` (or the hourly writer) automatically return a `review` task to `ready` when its claim has expired, its `implementation_pr` is merged, and the latest note contains "return to ready" or "partial". This needs its own task. Rainbow t-012 is a related case: its note moves all remaining scope to t-030 and t-066, so a reviewer could close it.
4. **Projection headroom is structural** (carried). Even after this archive pass, open-task notes keep growing. The t-104 per-task HISTORY split is still the real fix. kr-arcade t-164, at 5.4 KB, is the largest open note there.
5. **The CONTROL "Priority order this week" line** is still stale (carried; Silas's choice; it does not affect task selection).

## Next review

2026-11-28 PT (three days).
