# EGRESS-BLOCKERS.md

Append-only ledger of sandbox egress-allowlist rechecks. Several roadmap tasks
(ai-art-academy/t-008, t-013; digital-storefront's Stripe task; art-generator-connect's
Civitai/HF task) had each independently accumulated their own "RECHECKED &lt;date&gt;: still
a fresh connect_rejected/403" prose paragraph for the same known-blocked hosts — easy to
skip, and impossible to grep "how many times has this been reconfirmed, and when" across
tasks in one place. This file is that one place (conductor/t-052).

**Never edit or delete a prior entry — append only, like `TALKBACK.md`.**

## How to use this

Run `python scripts/recheck_egress_blocks.py <host> [<host2> ...] [--task <project>/<task-id>]`
before leaving a task `ready` on a suspected egress block, or before re-blocking a task that
was already flagged. It probes each host directly (a real HTTP request through the sandbox's
agent proxy — connection-level failures like `connect_rejected`/refused/timeout/DNS failure
mean *blocked*; any actual HTTP response, even a 403 or 404 from the remote site, means
*reachable*, since the connection itself succeeded) and appends one timestamped entry per
host below. Link the recheck to the roadmap task it's unblocking via `--task` so both sides
are greppable from either direction.

A `blocked` result here does **not** by itself change any task's `status` — the agent that
ran the recheck still applies the normal Failure-triage rules (AGENTS.md) to the task.

## Log

