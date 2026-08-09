# Daily Dream pipeline

This is the canonical end-to-end contract for the daily dream. There is one object-creation path.

## The path

```text
agent-authored draft
    ↓
committed six-asset proposal in projects/dream-cycle/backlog/
    ↓ after one Pacific steering day
Hourly Conductor
    ↓
scripts/build_conductor_summary.py
    ↓ exactly once
scripts/build_dream_records.py
    ↓
kind_robots rows + built-data ledger + six unique art requests
    ↓
scripts/apply_daily_dream_facets.py
    ↓
art rendering / attachment passes
    ↓
daily digest reads committed proposal, built-data, Facets, and art state
```

## 1. Draft and steering

A sweeping agent checks whether the current Pacific date has a proposal with:

```bash
python scripts/build_dream_proposal.py --check --fetch
```

When one is missing, the agent reads `--brief`, authors one coherent JSON bundle, and writes it with `--from-json`. The proposal contract is exactly six assets:

- one dream vibe
- one dream location
- one Character
- one ITEM Reward
- one SKILL Reward
- one Scenario, authored from the completed preceding elements

The committed proposal is the human steering surface. It creates no database objects. Silas may add notes, park it, or veto it during its proposal day.

## 2. Object creation

`scripts/build_dream_records.py` is the **sole object writer** for daily-dream objects.

The Hourly Conductor calls `build_dream_records.ensure_records()` once through `scripts/build_conductor_summary.py`. The builder selects one eligible proposal, creates the complete bundle transactionally, records every resulting ID in `built-data`, queues exactly six unique art requests, and pins a retry marker when a write fails. Partial attempts are rolled back rather than continued by hand.

No agent manually reproduces the builder's REST calls. No playbook creates Characters, Rewards, Scenarios, relations, or PitchSheets stage by stage. A proposal moves from unbuilt to built through this builder only.

Immediately afterward, the hourly workflow runs `scripts/apply_daily_dream_facets.py`. Facet attachment is a sidecar to the same completed bundle, not a second creator.

## 3. Art completion

The builder owns the six request definitions and their stable IDs. The shared art pipeline renders them, and later attachment passes update each real model when its public asset exists. Repeated hourly runs are idempotent: they attach or report existing work, not create another bundle.

## 4. Digest reporting

The daily digest is read-only with respect to kind_robots content. Its workflow:

1. builds repository-backed digest JSON,
2. enriches the daily-dream cards with committed metadata and art state,
3. validates the payload,
4. renders the email payload,
5. optionally sends it.

6. authors the day's next proposal if one does not exist yet, and commits it.

The digest workflow receives no `KR_API_TOKEN` and never imports or calls the object builder or Facet writer. A missing, retrying, built, rendered, or attached asset must be reported honestly from committed evidence.

Step 6 is the only thing the digest writes, it writes it to THIS repo, and it does
not weaken the read-only rule above. `scripts/author_dream_proposal.py` produces a
proposal markdown file — it creates no kind_robots object, attaches no Facet, and
needs no token (the Facet catalog read is a public unauthenticated GET). The single
object writer is still `build_dream_records.py`, still reached only through Hourly
Conductor.

It exists because authoring used to live only in CLAUDE.md's session-startup
checklist, so a proposal appeared when a session happened to run and happened to
notice one was missing — and on a quiet day there was no dream at all (Silas,
2026-08-09: *"I'm not sure why the next dreams aren't written the turn the digest is
sent, or a step later if there isn't enough process."*). It runs after the email so
a failure cannot cost the digest, is `continue-on-error` for the same reason, and is
idempotent: on a day a session already authored one it prints "already exists" and
exits 0. The session checklist remains as a backstop for the days it fails.

Because this job now pushes a commit to `main`, it shares Hourly Conductor's
`conductor-main-writers` concurrency group rather than racing it.

## Legacy staged builds

The former eight-stage `type: dream` playbook was retired on 2026-08-02. It was a second object writer and had already left Lantern Post partially created. Legacy non-proposal dream outlines remain useful as idea inventory, but they are never resumed with direct API calls. To use one, an agent adapts its concept into the next canonical six-asset proposal.

Existing rows from a partial legacy build are retained as historical production content unless a separately scoped cleanup explicitly reconciles them. They must not be silently completed or duplicated.

## Continuous health check

Run:

```bash
python scripts/check_daily_dream_pipeline.py
```

CI enforces that:

- Hourly Conductor reaches the builder through one canonical call,
- Daily Digest has no object-writing capability,
- the active dream specs identify `build_dream_records.py` as the sole writer,
- retired direct-REST stage instructions do not return.
