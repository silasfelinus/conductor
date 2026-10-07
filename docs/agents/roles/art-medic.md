# Playbook: art-medic

Read AGENTS.md (core) first; this playbook adds only what this role needs.

### If you're fixing a failed art queue

`select_role.py` recommended `art-medic`: `ops/art-queue-health.yaml` lists art
queue failures an agent can fix. Auto Art Generate writes that file at the end of
every run (`scripts/art_queue_health.py record`) from its own step logs. The
workflow's green check means nothing here: both consume steps are
`continue-on-error`, and on 2026-10-07 the job was green while all 28 submissions
were prompt-contract 422s and twelve projects' art sat `pending` for days. Silas,
2026-10-07: Conductor agents should work on fixing failed ArtJob queues.

`python scripts/art_queue_health.py check` lists what is actionable. Each entry
has a `source` (`project-art` = `images:` in `projects/art-prompts.yaml`,
`requests` = its `requests:`, `kr-failed-jobs` = a FAILED Kind Robots ArtJob), a
`target`, a `kind`, and the date it was `first_seen`. Fix by kind:

- **`contract-rejected`** (kind_robots' prompt contract refused the prompt: 422 at
  enqueue). The `rules` field names the rule; the server's own wording is in
  `detail`. A rejected prompt never heals on its own.
  1. Rewrite the prompt in `projects/art-prompts.yaml`. For negation rules
     (`text-exclusion-pile`, `people-negation`, layout exclusions) start from
     `repair()` in `scripts/repair_negation_art_prompts.py`, then read the result:
     it can garble a sentence or add an "unpeopled" clause to a picture that has a
     hand in it. State the wanted result, never the unwanted noun ("every surface
     bare and unmarked", "one continuous scene"). `format-vocabulary` ("comic
     page", "poster", "trading card") needs a hand rewrite that describes the
     subject and the aspect ratio. Change only the `prompt` field. Edit the text in
     place, because a `yaml.safe_dump` round trip reformats the whole file.
  2. **Fix the producer, not just the row.** Find what wrote the prompt
     (`git log -S` on a distinctive phrase; `source:` on a request) and fix it so
     the next one is clean. On 2026-10-07 every project from
     `scripts/intake.py` was rejected because its templates ended in "no text";
     fixing the 24 rows without the template would have re-broken the next intake.
     If the producer is in kind_robots (`server/utils/artPromptContract.ts`,
     the missing-image reporter, `artAssetSuggest.ts`), open the PR there.
  3. Add a test that the producer's output passes `violations()` from
     `scripts/repair_negation_art_prompts.py`. That function mirrors only the negation rules. The
     server stays the authority, so do not copy its regexes into this repo.
- **`adopt-failed`** (the request's `last_art_job_id` points at a DONE ArtJob
  whose ArtImage has no data and 404s). Every run re-fails the same adoption and
  never resubmits. Delete that request's `last_art_job_id` line so the next run
  renders it again. Fix the prompt first if it is also contract-rejected.
- **`kr-job-failed`** (a FAILED Kind Robots ArtJob that
  `repair_failed_kindrobots_artjobs.py` has no known repair for). Read its `detail`.
  - **Contract rule:** fix the stored prompt the job came from, then requeue. Use the
    entity's art prompt through the API, as `repair_negation_art_prompts.py --apply`
    does. Fix its producer too, usually in kind_robots.
  - **Render-host fault:** use `scripts/drain_failed_art_backlog.py`, which
    canaries before it drains.
  - **Recurring class:** a whole class of payload faults the repair script should
    always handle goes into `repair_failed_kindrobots_artjobs.py` as a new repair
    reason.
- **`timeout` / `error`** become actionable only after persisting
  `--persist-days` (default 2). A single timeout is a busy render box. A persisting
  one usually means the box is down (`ops/home-server/RENDER-BOX-STATUS`,
  `render-box-watchdog.yml`) or the job is wedged (`scripts/recheck_render_queue.py`).
  Box hardware or credentials are Silas's to fix. Record that as `needs-human`
  with the evidence rather than retrying.

Verify before you call it done. Do not hand-edit `ops/art-queue-health.yaml`.
After your fix merges, dispatch Auto Art Generate (`workflow_dispatch`) or wait
for its next run, then confirm the entries are gone from the file it commits
and the images actually landed (status `done`, or `ADOPTED`/`DONE` in the run
log). An entry that comes back means the fix did not reach the real cause.

Batch the work: one PR may fix every entry that shares a cause. Merge it when
green, per CLAUDE.md. If a cause is outside this repo and you cannot fix it
from this session, open or update a roadmap task in the owning project (a
kind_robots ArtJob producer goes under `projects/kind-robots/`) with the
failing targets and rule, so the next session starts from your diagnosis.
