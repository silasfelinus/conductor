# Session-startup sweep checks — rationale and history

<!-- Moved verbatim out of CLAUDE.md on 2026-09-30 (token essentialization): CLAUDE.md is
auto-loaded into every session, so rationale and incident history live here and are read
only when a check fires or the situation comes up. Same authority as if still inline. -->

`python scripts/session_sweep.py` runs every check below and prints one compact line per
check plus the output of any that did not exit 0. Read the matching entry here when a check
flags something and you need to know why it exists or how to fix it.

## Step 5 checks (CLAUDE.md startup)

   - `python scripts/check_pr_merged_drift.py`
   - `python scripts/audit_human_gates.py`
   - `python scripts/check_gate_legitimacy.py --live` — the other half of the gate audit: which
     `needs-human` gates are really agent work (Silas, 2026-09-30: *"can we get some sort of
     oversight so that we aren't allowing things to hang when its not really a human gate
     issue?"*). The first run found 15 of 51. It flags five cases: a hard gate with no basis
     (NO_GATE_BASIS), an approved decision left parked (APPROVED_PARKED), a dependency wait
     filed as a gate (SHOULD_BE_WAITING), a deploy prerequisite that has already shipped
     (DEPLOY_PREREQ_MET, `--live` only), and gates nobody has re-triaged (UNREVIEWED). Every
     finding is agent work (`select_role.py` role `gate-triage`, playbook
     `docs/agents/roles/gate-triage.md`). Never report a flagged gate to Silas as his to clear.
     Exit 1 means findings. `--live` degrades to offline checks when the network is unavailable.
   - `python scripts/check_project_scaffold_drift.py` — a Kind-Robots-authored project's ONLY path
     into Conductor is the scaffold Todo `createProjectWithScaffoldTodo` writes; a closed todo alone
     never proved the roadmap directory actually landed (conductor/t-125, filed 2026-08-24: Todo
     #1320 was marked DONE while `projects/cthulhuquarium/` never existed). This checks both
     directions — a Kind Robots `conductorSlug` with no matching `projects/<slug>/roadmap.yaml`
     (the reported bug, exit 1), and a Conductor project with no matching Kind Robots row at all
     (weaker/informational, exit 3). Needs `KR_API_TOKEN`; exits 2 (unresolved, not clean) without it.
   - `python scripts/check_live_facet_coverage.py` — asks Kind Robots what Facets each
     built daily-dream record ACTUALLY carries, rather than trusting what the pipeline
     recorded at apply time (dream-cycle/t-026, 2026-09-02: PUT /api/characters/:id/facets
     ignored `facetKeys`, so all 36 built bundles logged `status: "complete"` with
     `errors: []` over a Character holding no Facets — for six weeks, until Silas noticed
     from the digest end). The applier now verifies its own responses, so a fresh build
     cannot repeat that silently; this catches what a one-time record cannot — a link
     deleted later, a catalog row merged out from under a record, or a bundle never
     repaired. `--repair` re-applies each bundle's stored seed selection. Needs
     `KR_API_TOKEN`; exits 2 (unresolved, not clean) without it.
   - `python scripts/check_milestone_status_drift.py` — a milestone's `status:` field (not-started/
     in-progress/done) is only ever read, never cross-checked against its own project's task list, so
     it can sit stale for weeks (conductor/t-135, filed 2026-08-28 from cthulhuquarium/t-063: m3 stuck
     at `not-started` despite 25/31 tasks already done). Flags a milestone marked not-started/pending/
     waiting with any done task under it, or marked done/complete with any non-recurring task under it
     that isn't done. Advisory only — wrong milestone status doesn't block task selection or gate
     anything, it only skews the digest's portfolio-percentage math; exit 1 means "worth a look and an
     edit," not a genuine gate. No network/token needed.
   - `python scripts/check_container_log_drift.py` — reads the daily container-log triage digest
     that kind_robots' `scripts/container_log_triage.py` writes on Alexandria (Silas, 2026-09-03: *"I'm
     not searching around the logs of 50-ish containers regularly to find suboptimal problems. If
     something is erroring in the logs but not actually breaking the container, I'm not aware of
     it."*). Reports only signatures that are NEW, SPIKING against their own history, or newly
     QUIET — a stored baseline suppresses the steady-state noise, without which the report becomes
     wallpaper in a week. **A digest older than 48h is itself a finding**, because from the reading
     end "nothing to report" and "the User Script stopped running" are indistinguishable — the
     `check_engine_heartbeat.py` lesson (healthcheck.ps1 stopped at 2026-09-01 02:26:07 and never
     said so; its log just ends, ~37 hours before Silas noticed). A MISSING digest is exit 0 with a
     "not configured yet" note, so this stays quiet until the User Script is scheduled and the
     digest is published off the host. No network/token needed for a local digest path.
   - `python scripts/check_roadmap_note_size.py` — watches the one hard ceiling in this repo.
     `scripts/sync_kind_robots_projection.py` POSTs the raw text of every roadmap under
     `MAX_PAYLOAD_BYTES = 4_000_000`; crossing it fails `tests/test_sync_kind_robots_projection.py`
     and stops the Kind Robots board syncing. That happened on 2026-09-11 at 4,000,134 bytes with
     **no prior warning**, and three days later the payload was back to 93.4% — because t-151's fix
     only watched a *single* note over 50KB, while the real shape was 154 medium notes summing to
     411KB in one file (conductor/t-158, 2026-09-14). It now reports three things: oversized single
     notes, oversized roadmap *files*, and the actual projection headroom. **Report the headroom
     line every session** — `--payload-only` prints just that line. Exit 1 past any threshold or
     80% of the limit; advisory, never a gate. The fix is
     `python scripts/archive_done_task_notes.py --all`, which moves done-task notes into
     `projects/<slug>/HISTORY.md` verified byte-for-byte under AGENTS.md's archival carve-out. No
     network/token needed.
   - `python scripts/check_facet_prompt_subjects.py` — asks the one question
     `server/utils/artPromptContract.ts` structurally cannot: not whether a live Facet prompt
     breaks a rule, but whether it says anything to draw. The negation-repair pass closed with a
     clean CLIP-node audit — 0 violations across 4,442 prompts — while rendering a plush blob for
     "Octopus", a frog for "Axolotl" and walls of garbled lettering for the ALIGNMENT cards
     (Silas, 2026-09-20: *"The prompts make no sense and the images reflect that"*). 149 prompts
     were the Facet's description pasted whole with its own title nowhere in them, which no
     pattern in a contract can detect, because it is a property of what the prompt LACKS. Flags
     NO SUBJECT (a producer-generated prompt that never names its Facet), APP WRAPPER (product
     and builder labels Krea paints as card text), and CARD COPY (the Facet's description
     appearing verbatim inside its own prompt). Hand-authored concrete scenes that deliberately
     skip the title are correct and are never flagged. Advisory; exit 1 is a prompt to go look at
     the cards, and the answer is still a contact sheet, never the audit. **CARD COPY was
     unreachable until 2026-09-22** — it required the prompt to START with the description (every
     producer since v2 puts the title first) AND to carry a registered taxonomy clause (which the
     negation repair trims off), so the script reported "Every prompt names something to draw"
     over 1,541 live prompts while 595 embedded their own description and Facet 810 "Martian
     Colonization" was rendering its card copy as lettering. It is containment-based and blocking
     now; a non-zero exit here is expected until the queue is re-run. Needs `KR_API_TOKEN`; exits
     2 (unresolved, not clean) without it.
   - `python scripts/check_priority_queue_starvation.py` — `projects/priority.yaml` is the
     deterministic worker pickup order, but nothing else reports how deep a session had to walk
     it before finding a `status: ready` task (conductor/t-149, filed 2026-09-11: the first six
     entries all had zero ready tasks that day, and "I picked the top-ranked available task" and
     "I walked past six gate-blocked projects to get here" read identically from the session
     end). Names each skipped project's reason (gated at needs-human — with the blocking task
     id/title named, so this doubles as a priority-ordered version of `audit_human_gates.py` —
     all waiting-blocked, or all claimed) and where the queue actually landed. Advisory only;
     exit 1 only past a threshold depth (default 3) so ordinary one/two-project fall-through
     stays quiet, or if literally nothing in the whole order has claimable work. No network/token
     needed.
   - `python scripts/check_vendored_scanner_parity.py` — the home-server vendored LoRA/model
     scanners (`ops/home-server/lora-catalog/scan_loras.py`, `scan_models.py`,
     `import_catalog.py`) are supposed to be a straight byte-for-byte copy of their kind_robots
     originals at `scripts/lora-catalog/` (per that directory's `PROVENANCE.md`), but nothing
     checked that until now (lora-ingestion/t-013, 2026-09-22: the vendored `scan_loras.py` was
     missing the Civitai tag category classifier entirely, and the gap was only caught by a
     downstream symptom — garbled preview classification). Fetches each kind_robots original via
     the GitHub Contents API and diffs it against the local vendored copy. Exit 1 on any drift
     (with a diff snippet and the `PROVENANCE.md` re-sync command); the fix is always re-copying
     the file, never hand-editing the vendored side to match. Needs `GITHUB_TOKEN`/`GH_TOKEN`
     (kind_robots is private); exits 2 (unresolved, not clean) without it.
   - `python scripts/check_daily_commitment_staleness.py` — `select_role.py`'s `daily-creative`
     role surfaces a `daily_commitment: true` task the moment its `daily_last_checked` predates
     today's Pacific date, but nothing distinguished "checked today, honest no-op" from "a
     session claimed it and stalled" or "nobody ran the role in days" (conductor/t-194, kaizen
     from animation-manager/t-020, 2026-09-23). Flags STALE CHECK (`daily_last_checked` missing
     or 2+ days stale) and STALLED CLAIM (`status: claimed` past the normal 90-minute claim TTL).
     Advisory only; exit 1 when at least one daily_commitment task is flagged. No network/token
     needed.
   - `python scripts/check_recurring_claim_drift.py` — flags any task showing `status: claimed`
     with `claimed_by`/`claimed_at` already null, a combination that never occurs from a live
     claim (claim_task.py and process_task_events.py only ever write all three fields together).
     Root-caused for conductor/t-195 from model-builder/t-029 drifting into this state twice
     (2026-08-12, 2026-09-25) while its own recurring cycle note already said "re-arming to
     ready" — both times caught only incidentally by `check_pr_merged_drift.py` noticing a stale
     `implementation_pr`. Traced to a manual merge-conflict resolution on the close branch that
     kept `origin/main`'s stale copy of this task's status alongside another task's genuinely
     newer change in the same conflicted file, rather than resolving per-task. Advisory only;
     exit 1 when at least one task is flagged — the fix is a normal `close_task.py` re-close back
     to whatever the note's last paragraph says actually happened. No network/token needed.
   - `python scripts/check_recurring_churn.py` — counts `close: <project>/<task> -> status=ready`
     re-arm commits on `origin/main` per task over the last 7 days and flags any active task with 8+
     that is not currently resting under the no-op backoff (2026-09-30, token essentialization).
     Nothing reported pickup frequency before, so coloring-book/t-022 (40 claims in 48h, every
     cycle gated FOR SILAS) and model-builder/t-029 (122 "no model-builder commits, re-arming"
     cycles) each burned a full agent session per hour for weeks. Fix a flagged task by re-arming
     no-op cycles with `close_task.py ... ready --noop` (2h..48h backoff, `roadmap_claims.
     NOOP_REST_HOURS`), moving a task waiting on Silas to `needs-human`, or turning a pure watcher
     into a script. It also flags any non-done task in an active or continuous project whose note
     is over 20KB, because each claim re-reads the whole note (2026-09-30: six live notes held 259KB;
     archived to ~36KB with `archive_recurring_task_note.py --keep-head 3000 --keep-tail 3500`).
     Advisory; exit 1 when flagged, 2 when git history can't cover the window.

## Step 7 — the dream docket (CLAUDE.md startup)

7. Run `python scripts/build_dream_proposal.py --check --fetch`. **Sessions own
   the docket** (changed 2026-09-04). The `daily-digest.yml` author step no
   longer receives `ANTHROPIC_API_KEY` on the schedule — the key is opt-in via
   the workflow's `spend_api_credits` dispatch input — because the hourly
   Conductor Agent Routine already runs on Silas's Max plan and the API step
   was doing the same work twice on credits (Silas, 2026-09-04: *"They are
   literally running as part of my normal Claude max account. I'm not spending
   $100 a month so it can then trigger the api."*). So: **when `--check`
   reports fewer than `TARGET_BUFFER_DAYS` (5) unbuilt proposals, author
   exactly ONE this session** using the `--brief` → `--from-json` recipe
   below, then move on. Never more than one per session; the hourly cadence
   fills the buffer within a day. The earlier intent still holds (Silas,
   2026-08-09: *"I'm not sure why the next dreams aren't written the turn the
   digest is sent ... that's very high on automated tasks."*) — it is simply
   done by sessions now, not by the API.

   **`--check` measures the docket, not the calendar** (changed 2026-08-31). It
   reports how many unbuilt proposals are queued and exits 0 whenever at least
   one is. A day with no proposal dated today is NORMAL and is not a failure:
   authoring pauses while the docket is `TARGET_BUFFER_DAYS` (5) deep, because
   Silas would rather spend that cycle elsewhere (2026-08-31: *"we don't need to
   spend effort writing new proposals if we have a backlog (though a 5 day or so
   buffer seems reasonable, just in case). It would be better spent to either
   take on a new task, or improve the current proposals in the docket."*). A
   shallow docket (1–4 queued) means author one this session, as above; a full
   one means leave it alone.

   Exit 1 means the docket is **empty**, which is the real alarm: nothing is
   queued for tomorrow. Author one yourself then: run `--brief` for the
   deterministic seed plan, then create exactly one dream vibe, one dream
   location, one Character, one ITEM Reward, one SKILL Reward, and one Scenario,
   with no narrator. Preserve the brief's `seed_facets` unchanged; the vibe is
   the umbrella, every dependent asset must follow its assigned Facets, and the
   Scenario is authored last and explicitly names the vibe, location, and
   Character. All user-facing card copy must be complete sentences that parse on
   their own — `scripts/dream_prose_quality.py` is the contract. Write it with
   `--from-json` and commit it with the session's log commits. An empty docket
   two days running means the hourly sessions have stopped doing step 7 —
   check the Conductor Agent Routine's recent runs and TALKBACK rather than
   papering over it by hand each session. (Manual API authoring is still
   possible: dispatch `daily-digest.yml` with `spend_api_credits: true`.)

   Builds drain the docket **oldest first, with no age cutoff**. A proposal that
   could not build on its day is picked up by the next run instead of being
   orphaned; the current creative contract is re-checked at build time, which is
   what actually keeps stale creativity out.

