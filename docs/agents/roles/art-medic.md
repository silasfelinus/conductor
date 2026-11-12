# Playbook: art-medic

Read AGENTS.md (core) first; this playbook adds only what this role needs.

### Off-brief adult renders: mark mature, withdraw, move on

Silas, 2026-11-02 PT, on a nude off-brief bake-off render: *"it could have just been marked mature and been done
with it ... it didn't need to be deleted ... this shouldn't require this much hassle."* When a render is NSFW or
otherwise adult but off-brief for its project, set the ArtImage's `isMature` (`PATCH /api/art/image/<id>`) and
withdraw it from the ledger. Never delete it and never park it on Silas. Escalate only content that is illegal
or plausibly involves a minor; a reviewer's "reads young" alone is not that bar.

### Unrecorded art: record it, then link it

Silas, 2026-11-11 PT: *"we keep finding art that was requested and made but not linked ... it should
be both corrected and linked and be a part of the normal conductor agent task rotation to be
responsible for that sweep so it doesn't get lost because a thread agent was killed."*
`select_role.py` names this role when `python scripts/reconcile_unrecorded_art.py --check` (sweep
line `unrecorded_art`) lists work. The hourly **Reconcile Unrecorded Art** workflow already writes
lost job ids back on its own; what reaches you needs judgment:

- **Untriaged `projects/<slug>/art/RECOVERED-<date>.yaml`.** Each subject is a DONE render whose
  ArtJob and ArtImage ids appear nowhere in Conductor or kind_robots. Read the ArtImage
  (`/api/art/image/<id>`), find what asked for it (`git log -S` on a phrase of `prompt_prose`, the
  project's open art tasks, kind_robots content), and set `triage:` on the subject:
  - `adopted` — it is the render an existing ledger cell or request wanted. Write its job id and
    `art:` there (or `last_art_job_id` on the request) so that project's normal curation sees it.
  - `linked` — you wired it in yourself (manifest, entity image, shipped file). Put where in
    `linked_to:` (kind_robots PR or path).
  - `duplicate` — a second render of something already recorded; `duplicate_of:` the kept job id.
  - `rejected` — off-brief. Adult renders are marked mature, never deleted (rule above).
  One PR per project's batch; merge when green.
- **Report older than 6h.** The workflow stopped: open its last run, fix it (workflow-medic rules).
- **Lookup unavailable for 48h.** kind_robots#5031 (`POST /api/art/queue/lookup`) is not live.
  Check the deploy; until it is, run with `--backfill-days 3` by hand.
- **Ambiguous cells.** Two lanes of one ledger share a prompt, so the backfill cannot tell their
  jobs apart. Match them by lane checkpoint in the job payload and write the ids by hand.

Recover by hand at any time (a session that knows it was cut off, or a report from Silas):
`python scripts/reconcile_unrecorded_art.py --apply --report ops/unrecorded-art.yaml
--backfill-days 3 --strays-days 2`, then commit the touched ledgers, `projects/art-prompts.yaml` and
the report. Never re-submit a cell to "fix" a missing id: the render already exists.

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
     A project image that is already pending also has a copy in
     `projects/art-generate.yaml`, which the consumer actually submits and the queue
     refresh preserves verbatim: change that copy too, or the old prompt keeps 422ing
     (`tests/test_project_art_prompts_contract.py` fails until they match).
  2. **Fix the producer, not just the row.** Find what wrote the prompt
     (`git log -S` on a distinctive phrase; `source:` on a request) and fix it so
     the next one is clean. On 2026-10-07 every project from
     `scripts/intake.py` was rejected because its templates ended in "no text";
     fixing the 24 rows without the template would have re-broken the next intake.
     If the producer is in kind_robots (`server/utils/artPromptContract.ts`,
     the missing-image reporter, `artAssetSuggest.ts`), open the PR there.
  3. Before pushing, run `python scripts/check_art_prompts_live_contract.py` (needs a
     kind_robots checkout beside this repo). It runs the real `artPromptContract.ts` under
     Node over every active row, so it catches the non-negation rules (`frame-noun`,
     `art-direction-jargon`, `format-vocabulary`) the Python test cannot. Run it after
     authoring hand-written `requests:` rows, too.
  4. Add a test that the producer's output passes `violations()` from
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
  - **Already replaced:** a later round re-rendered the work. List the id in
    `ops/superseded-art-jobs.yaml` with the replacement, and clear it in Kind Robots
    (`POST /api/art/queue/cancel-failed` with `jobIds` and a `reason`). The yaml alone hides it
    from art-queue-health but leaves it FAILED on Silas's admin queue page.
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
