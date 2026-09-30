# Playbook: worker

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

Read AGENTS.md (core) first; this playbook adds only what this role needs.

### If you're working
- **Step 0 — Todos**: run `python scripts/fetch_todos.py`. Handle the top OPEN todo if
  any exist (see "Todos" section). Call `complete_todo.py <id>` when done.
- **Step 1 — Resolve deps**: run `python scripts/resolve_deps.py`.
- **Step 2 — Claim**: run `python scripts/claim_task.py <project> <task-id> --owner worker
  --session <id>` (see "Rotation collisions" below). It checks `origin/main` fresh,
  refuses if another session already claimed the task, and otherwise pushes the
  `status: claimed`/`owner: worker`/`updated` commit straight to `main` for you. On
  `ALREADY_CLAIMED`, do not implement this task — pick the next `ready` task instead.
- Branch `worker/<project>-<task-id>`. Do ONLY that task.
- **Rebase onto `origin/main` immediately before opening the PR** (all kinds): run
  `git fetch origin main && git rebase origin/main` (or merge) right before `gh pr
  create`, so the PR opens conflict-free against the current tip instead of drifting
  stale while it waits for review. `STATUS.md` / `workspace.html` / `ROADMAP-AUDIT.*`
  are regenerated on every push to `main`, so a branch whose merge-base is even one
  `chore: refresh STATUS.md …` auto-commit behind will conflict on these files 100%
  of the time — resolve any such conflict by taking main's copy per hard rule 9
  (they're auto-generated). This keeps trivial auto-gen conflicts off the Reviewer's
  plate (kaizen from PR #550, conductor/t-045).
- **software:** open a PR into `main`, fill the handoff template (including "Flags for
  Reviewer"), set task `status: review`, verify it, resolve conflicts if present, and **merge
  it** — reversible/scoped/verified software work is merged, not parked at an open PR. After a
  successful safe merge, **before hand-writing `status: done`**, check `task-events/` for an
  already-queued event naming this same project/task (a "PR merged" auto-queue mechanism can
  race a manual close-out — both derive staleness from the same monotonically increasing
  `updated` timestamp, and whichever writes last makes the other look stale, silently
  discarding its `learning`/`note` payload with no trace; see conductor/t-085, TALKBACK.md
  2026-07-26). If a matching event exists, either let it apply on its own next processor run
  (don't also hand-write the transition) or explicitly consume it first — apply its
  `learning`/`note` payload, then delete the file — rather than racing it blind. Only once
  that's clear, close the task out with `python scripts/close_task.py <project> <task-id>
  done --session <id>` (the branch is auto-removed on merge) — **never** a plain
  `set_task_field.py` edit followed by a direct `git commit && git push` to `main`.
  `close_task.py` pushes the `status: done` edit to its own small branch (checked fresh
  against `origin/main`, same collision-resistant git plumbing as `claim_task.py`); open a
  tiny PR from that branch into `main` and merge it, exactly like any other software
  change. Hard safety rule 1 ("PRs only into `main`, except the Worker's atomic claim
  commit") does not carve out a second exception for close-out bookkeeping — a direct push
  here is exactly the gap conductor/t-091 self-flagged from the coloring-book/t-036
  close-out (2026-07-28): every prior close-out commit in this repo's history carries a
  `(#PR)` suffix, meaning a small follow-up PR was always the actual convention, just not
  the tooling default. Several close-outs from the same PR/session can share one
  `close_task.py` branch (call it once per task with the same `--branch`) so one PR closes
  a whole batch.
- **content:** write the draft file, open a PR, set `status: needs-human`.
- **proposal:** write `pitches/<date>-<slug>.md` using the pitch template, open a PR, set
  `status: needs-human`.
- **Every run ends with a clean `main` and no leftover branch.** The required terminal state
  for reversible, scoped, verified, non-gated work is **merged into `main`** — not an open PR
  left for a human to merge. Do not "park" safe work at an open PR because no one told you to
  merge: merging safe work is the default, not a request. Only work that is genuinely unsafe,
  human-gated, outward-facing, irreversible, or blocked ends unmerged — and it ends at
  `status: needs-human` with its PR open (so it isn't lost), never as a silent stranded branch.
  Merged branches are removed automatically (the repo's delete-on-merge setting + the
  `branch-janitor` workflow); never leave a no-PR branch behind. Work one task in flight at a
  time — you may complete several tasks in a single run, but finish each (merged, or parked at
  `needs-human` with a PR) before claiming the next. Never hold two active claims at once.
- **On closing a task at `done`** (e.g. after a safe self-merge): append the outcome record
  to `LEARNING.yaml`.
- **Merge conflicts:** resolve them intelligently. Keep both sides when they are independent,
  follow CONTROL.md and Silas notes when they conflict, and for `STATUS.md` / `workspace.html`
  accept the latest generated/main version. Re-check relevant verification after fixing conflicts.
- **After a Reviewer rejection:** read the Reviewer's feedback AND the task's
  `retry_context:` carefully before re-claiming — never retry blind. If you agree,
  fix and resubmit, saying in "Flags for Reviewer" how the retry addressed the
  retry_context. If you disagree, write your case to the project's `TALKBACK.md` and
  set `status: challenged` — do not silently retry a disputed decision.

**Recurring tasks** (`recurring: true`, e.g. brainstorm/t-001): these never reach `done`.
After doing the work and opening/merging the PR, set the task's `status` back to `ready`
(not `review`/`needs-human`) so it re-arms for a future cycle. The pitches it produces are the
output that goes to Silas — the task itself just keeps cycling. A recurring task that
produced nothing this cycle (e.g. pitch queue full) still re-arms to `ready`; note "no-op"
in the PR. Recurring tasks don't count toward milestone progress.

**No-op re-arms rest; gated re-arms don't re-arm at all** (2026-09-30). Every hourly pickup
of a recurring task is a whole agent session. coloring-book/t-022 was claimed 40 times in
48h while each cycle concluded "next step is FOR SILAS", and model-builder/t-029 ran 122
"no model-builder commits, re-arming" cycles. So:
- A cycle that found nothing to do re-arms with `close_task.py <project> <task> ready --noop
  --session <id> --append-note "..."`. That records `noop_streak` and `rest_until`, and every
  picker skips the task for 2h, 6h, 12h, 24h, then 48h as the streak grows (`max_rest_hours` on
  the task lowers the cap). The first re-arm without `--noop`, after a cycle that did real work,
  resets the backoff. (Not for `daily_commitment` tasks; the daily gate already covers them.)
- A task carrying `min_rest_hours` is capped: after ANY re-arm it rests at least that long, even when
  the cycle did real work (interface-vision/t-104 and t-105 are capped at 24h, Silas 2026-09-30).
  Don't remove or lower a cap without Silas.
- A cycle whose only next step is Silas's decision/approval goes to `needs-human` with the
  question stated, NOT back to `ready`. Re-arming a gated task just re-asks the question hourly.
- A task whose every cycle is a mechanical check (did files X change? did job Y finish?) is a
  script, not an agent task. File a kaizen task to make it one, and until then re-arm it with `--noop`.
- Keep the note short: append one short paragraph per cycle, never extend the first paragraph (six
  live notes had grown to 33-50KB, mostly by agents appending to one giant first line). Past
  20KB, archive: `archive_recurring_task_note.py <project> <task> --keep-head 3000 --keep-tail 3500`
  moves the note verbatim to `<TASK-ID>-HISTORY.md` (as a new round if one exists) and keeps the
  spec, the latest cycles and every signal daily_gate/select_role read.
`check_recurring_churn.py` (in the startup sweep) flags any task re-armed 8+ times in 7 days
without the backoff, and any live note over 20KB.

**Daily commitments** are the stricter recurring subset marked `daily_commitment: true`.
They maintain two machine-readable Pacific-calendar dates on the task: set
`daily_last_checked` after every completed daily attempt, including a legitimate no-op, and
set `daily_last_completed` only when the promised creative output actually shipped. Do not
advance `daily_last_completed` to make the selector green. For animation-manager/t-007,
"a creation shipped" means the new Screen FX component merged, is registered in the catalog,
and is tryable. If no buildable pitch can safely ship, record the reason, advance only
`daily_last_checked`, re-arm, and let the digest's release-age signal remain visibly stale.


### Rotation collisions (moved from AGENTS.md "Picking what to work on")

Picking a task from `priority.yaml`/`next_ready_task.py` only reads roadmap state — it
does not reserve anything. Two sessions triggered close together (e.g. concurrent
hourly burst-mode runs) can both read the same stale `ready` state, both fully
implement the same project/task, and only discover the collision when one of them
pushes. This happened for real on 2026-07-14 (`animation-manager/t-008` built twice —
see `TALKBACK.md` and `conductor/t-040`). Step 6 above (`claim_task.py`) exists
specifically to close this gap: it re-checks `origin/main` immediately before writing
the claim and retries under a push race, so a losing session fails fast into
`ALREADY_CLAIMED` instead of duplicating work. If a claiming session crashes before
finishing, the claim self-expires after `CLAIM_TTL_MINUTES` (90 minutes, see
`scripts/roadmap_claims.py`) so the task doesn't stay locked forever — `next_ready_task.py`
surfaces a stale-claimed task as pickable again automatically.

**Same-session post-compaction collisions** are the identical failure mode with a
different trigger: a session's context gets compacted mid-run and loses memory of
work it already completed earlier in the same scheduled window. Resuming from stale
in-memory state, it can find its own now-outdated `status: claimed` snapshot,
correctly avoid re-implementing (an open-PR check usually catches that part), but
then still draft an inaccurate wrap-up commit (roadmap/TALKBACK note) describing a
"nothing to do" or "releasing the claim" outcome that a real merge has since made
false. Hit twice the same day (2026-07-22): model-builder/t-029 and
storymaker/t-010, both in root/project `TALKBACK.md`. The fix is the same as the
concurrent-session case, just applied to the wrap-up step too, not only the
implementation step: **before writing any wrap-up commit for a claim this session
doesn't fully remember taking, `git fetch origin main` and diff the task's current
state** — a newer merge under the same or a related session id is the signal that
the "resume" is actually stale, and the wrap-up should defer to `origin/main`'s
version (via rebase, keeping the newer content) rather than push over it.

**Concurrent PR-conflict-resolution races** are a third variant: two independent
sessions both notice the *same* open PR has gone stale against `main` (e.g. because a
third PR just merged and moved the base) and both fix it themselves, unaware of each
other. Observed 2026-07-27: PR #1195 (ai-art-academy/t-010) and PR #1197
(music-mentor/t-007 close-out) both touched `music-mentor/roadmap.yaml` and
`LEARNING.yaml`. A Reviewer session merged #1197 first, then found #1195 conflicted
and fixed it by hand (dropping #1195's now-redundant duplicate music-mentor bundle,
keeping only its actual ai-art-academy scope) — but a *second*, independent session
had, in the meantime, pushed its own conflict-resolution commit to the same PR #1195
branch that took the opposite, wrong approach: it re-merged `main` but kept #1195's
stale, less-complete version of the music-mentor content instead of deferring to
what #1197 had already landed, which would have silently downgraded/reverted the
already-merged canonical entry had it been pushed on its own. The Reviewer session's
own second push caught this the normal way — `git push` (no force) failed with a
plain non-fast-forward rejection because the remote branch had moved — which is
exactly the safety net this depends on: **never force-push to resolve a PR conflict.**
The correct recovery is the same shape as the two collisions above: `git fetch` the
branch's actual current remote tip, `git merge` it in (not overwrite it), re-resolve
favoring whichever side matches `origin/main`'s already-merged canonical content for
any file both sides touched, verify the resulting diff against `origin/main` is
exactly the intended scope (`git diff origin/main --stat` should show only files the
PR is actually supposed to touch), and push normally. If a plain push is rejected,
that rejection is doing its job — fetch-merge-reresolve, don't force past it.
