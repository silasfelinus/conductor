# Portfolio Intent Audit — 2026-11-26 PT

A scheduled Conductor agent ran this review one day before the 11-28 deadline, after `select_role.py` assigned `roadmap-intent-auditor` (upcoming). It used no paid model API and did no device testing.

Sources read:
- `OVERSIGHT-AGENT.md` and the 2026-11-25 audit.
- `CONTROL.md`, `priority.yaml` and `project-overrides.yaml`. `git log` since the 11-25 audit shows one change, the `hopeful-hues` lifecycle line. No human priority decision has landed.
- Commits on main since 11-25 20:00 PT, plus the output of `session_sweep.py --max-lines 3` and `check_pr_merged_drift.py`.
- The Rainbow t-012, t-022, t-030 and t-066 tasks, the Save the Plumber task list, and Hopeful Hues t-003 and t-013.

## Verified

- **Direction is unchanged.** Rainbow and Save the Plumber still lead the 2026-10-21 focus tier in `priority.yaml`.
- **Rainbow is in art integration, as Tier A intends.** Batch 12 of the P-01 idle loops was reviewed and shipped on 11-26 (conductor#8117). The rest of ANIM-BACKLOG-2026-11-24 is still rendering. No new polish work was opened.
- **Save the Plumber is moving through its Gen-2 worlds.** t-020 (the Gen-2 level engine) is `done`. t-021 (World 1) is claimed by a live session from 11-27 05:41Z. t-028's main-game fixes merged in kind_robots#5901 on 11-26.
- **The Hopeful Hues concern from 11-25 is resolved.** The override records that the painted tile set was delivered and verified (t-013) on 11-26, after Silas's 11-25 direction that painted art must replace every code-drawn tile. The project is `playtest`/`normal`. t-003's note now says plainly that all regions share the Gloom, Tangles and buddy mechanics with seeded layouts. That is an honest record of the narrower scope.

## Corrected (this PR)

- **The kr-arcade roadmap was over its 150,000-byte limit again (150,803 bytes, per the sweep), and the projection payload was at 80.8%.** I ran `archive_done_task_notes.py --all`, which moves notes byte-for-byte. It archived 20 done-task notes across 7 projects and saved 51,489 bytes. The payload is now at 79.5%. kr-arcade is at 146,684 bytes. `--verify-only` reports that all 100 archive pointers resolve.
- **Three Rainbow tasks were stuck in `review` with expired claims from 11-20 and 11-22.** I fixed them with `close_task.py`:
  - **t-012 → done.** kind_robots#5709, #5687 and #5670 merged. The task's own 11-24 note says the only remaining scope is the animated cinematics, which t-030 tracks. The story majors went to t-066, which is done. Leaving t-012 open would track the same scope twice.
  - **t-022 and t-030 → ready (partial).** Their PRs merged, but some art is still rendering (ART-BACKLOG and ANIM-BACKLOG-2026-11-24). They go back to the queue for the next integration slice.
  - **Why `close_task.py`:** the task-event processor refuses `ready`/`done` from a session that does not hold the claim, and refuses `claim` unless the task is `ready`. So there is no event route for a `review` task with an expired claim.

## Still questionable

1. **Partial work left in `review` is still systemic (carried from 11-24 and 11-25).** `check_pr_merged_drift.py` now lists 14 tasks (it listed 35 on 11-25):
   - kr-arcade has 5: t-085, t-090, t-110, t-154 and t-164.
   - Rainbow had 5. This PR fixes 3 of them; t-013 and t-044 remain.
   - Save the Plumber has 1: t-028.

   The audit above also shows that the event route cannot release these tasks. **Recommendation, unchanged:** extend `reconcile_stale_claims.py`, which today only releases `claimed` tasks, so that it moves a `review` task to `ready` when its claim has expired, its `implementation_pr` has merged, and its latest note says the work is partial. This needs its own task; I did not create one in this audit.
2. **Projection headroom is structural (carried).** Archiving buys about 50 KB a cycle. The t-104 split of per-task HISTORY is still the real fix.
3. **The CONTROL line "Priority order this week" is still stale** (carried). It is Silas's choice and does not affect task selection.

## Next review

2026-11-29 PT (three days).
