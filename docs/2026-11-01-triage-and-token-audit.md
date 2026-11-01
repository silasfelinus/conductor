# 2026-11-01 — Completion triage and token audit

Asked by Silas: which active projects are closest to done (only image generation and his
approval left), where tokens are wasted, and how to pitch information at the right level so
agents get pointed at one job.

Regenerate the triage any time with `python scripts/project_triage.py -v`. It reads the
roadmaps; don't redo this by hand.

## 1. Completion triage (19 active projects)

**Tier A: no writing or code left. Art, QA after art, and Silas's verdict only.**

| Project | Left |
| --- | --- |
| game-of-captains (Space Couch) | art t-008 and t-009; t-011 and t-020 in review (PRs in flight 2026-11-01); Silas t-012. **Watch:** kind_robots#4592 ("101 absurd alien species") is being imported as new scope. Decide whether it's v1 or post-launch. |

**Tier B: one or two build tasks away from Tier A.**

| Project | Build left | Then |
| --- | --- | --- |
| shifting-desks | t-025 (art-ledger evidence kaizen); t-021 is an optional expansion pitch, so defer it | art t-032 → t-041 → QA t-046 → Silas t-020. t-044/t-045 have sat in `review` since 10-27: confirm their PRs merged and close them. |
| crystal-street | t-016 first playable slice | art rounds 2–3 (t-004, t-005) → release gate t-011 |
| hybridizer | t-008 user-submitted images (security-sensitive) | art t-007 (4,000 hybrids) → QA t-009 → gates. **Cutting t-008 from launch scope makes this Tier A.** |
| rebel-button | t-001, t-004 (still early: 1/5 done) | not near completion despite the tier |

**Tier C: real writing or engineering still ahead.** Closest first: cthulhuquarium (4 build
tasks: t-084, t-085, t-092, t-094), ruler-hooked (4), zuzu-gamebook (4), emperor-of-dust (5 act
and story passes, plus 3 `review` tasks stale since 10-22 to 10-24). Furthest: memory-dungeon
(16 build, 14 in review), comet-city-academy (13), weird-humboldt (13), kr-arcade (76).

## 2. Where the tokens go (measured)

1. **Watching CI.** The last hourly "Conductor Agent" run (2026-11-01 11:43Z) took 21 turns.
   20 of them were wakes saying "N checks pending", and each one re-read about 80k tokens of
   cached context. That is about 40% of the run's cost, spent watching. → Fixed in AGENTS.md:
   enable auto-merge and end the run, or wait in one blocking call.
2. **The full startup ritual runs on every hourly run.** That means about 65KB of required
   reading (AGENTS.md, CLAUDE.md, state-reconciliation, SOURCE_OF_TRUTH, a role playbook), a
   90-second sweep with about 9KB of output, and a 13-section report that nobody reads. It
   happens 24 times a day. → Fixed in CLAUDE.md: unattended runs skip the report, run the sweep
   with `--max-lines 3`, and end with five lines at most.
3. **Spread.** 19 active projects plus 14 continuous ones, 15 of them marked `high`, and 130
   ready tasks. Each run lands in a different project and pays to load its context again, so
   no project builds momentum. 2,537 commits in the last 7 days, 270 of them claims.
4. **Heavy QA chains.** The master-completion imports gave several projects 5–6 separate
   whole-game audit, simulation and dossier tasks each, for example ruler-hooked t-046..t-051
   and cthulhuquarium t-091..t-096. Each one reads the entire game. One release-QA pass per
   project after its art lands would cover the same ground.
5. **Sweep noise that every session pays for:**
   - home-server container logs (komga, audiobookshelf) appear in every Conductor session;
   - `check_pr_merged_drift` comes back UNRESOLVED every time (20 tasks it can't look up, plus
     a 403 on PortOS), and its message tells agents to re-check them by hand;
   - `tzaddik_review` flags 938 suggestions every session.

   Each of these should route to one owning role, not to everyone.
6. **Limbo `review` tasks.** Tasks sitting in `review` with no open PR, some since 10-22, get
   re-evaluated by every session that scans the project.
7. **Unused connectors.** The hourly trigger carries Gmail, Calendar, Drive, Docs and
   visualize. Conductor work uses none of them.

## 3. Communicating at the right level

| Level | Audience | Carrier | Contains |
| --- | --- | --- | --- |
| Portfolio | Silas | daily digest + this triage | tiers, gates waiting on him, one decision per project at most |
| Steering | Conductor | `priority.yaml`, `project_triage.py` | focus set, decided once a day, not every run |
| Assignment | one agent | `select_role.py` output | one role, one project, one task id |
| Task | that agent | `show_task.py <id>` | brief, acceptance criteria, latest note paragraph |

An unattended agent should never need the portfolio view. If it does, steering failed upstream.

## 4. Decisions for Silas (not made here)

- **Hourly cadence.** 24 runs a day. Every 2–3 hours during waking hours would roughly halve
  the session count without losing much: art and CI are the bottlenecks, not agent turns.
- **Focus set.** Cap writing work at about five projects: finish Tier A and B first
  (game-of-captains, shifting-desks, crystal-street, hybridizer, cthulhuquarium) and mark the
  rest `normal` instead of `high`.
- **Scope cuts:** hybridizer t-008 to post-launch; shifting-desks t-021 deferred; Space Couch
  #4592 as v1 or post-launch.
- **Connectors.** Remove Gmail, Calendar, Drive, Docs and visualize from the "Conductor Agent"
  scheduled task. Agents can't edit a scheduled task's connectors; this has to be done in the
  claude.ai UI.
