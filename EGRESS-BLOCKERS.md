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

## 2026-07-17T03:05:31Z | metmuseum.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T03:05:32Z | upload.wikimedia.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T04:07:49Z | metmuseum.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T04:07:50Z | upload.wikimedia.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T06:07:05Z | metmuseum.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T06:07:06Z | upload.wikimedia.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T07:51:10Z | metmuseum.org | reachable | ai-art-academy/t-013
reachable (HTTP 429)

## 2026-07-17T07:51:11Z | upload.wikimedia.org | reachable | ai-art-academy/t-013
reachable (HTTP 200)

## 2026-07-17T07:51:11Z | api.stripe.com | reachable | digital-storefront/t-011
reachable (HTTP 404)

## 2026-07-17T07:51:28Z | metmuseum.org | reachable | ai-art-academy/t-008
reachable (HTTP 429)

## 2026-07-17T07:51:29Z | upload.wikimedia.org | reachable | ai-art-academy/t-008
reachable (HTTP 200)

## 2026-07-17T07:51:29Z | www.metmuseum.org | reachable | ai-art-academy/t-008
reachable (HTTP 429)

## 2026-07-17T09:07:31Z | metmuseum.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T09:07:31Z | upload.wikimedia.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T09:51:12Z | huggingface.co | blocked | ai-art-academy/t-021
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T09:51:12Z | civitai.com | blocked | ai-art-academy/t-021
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T09:54:30Z | api.stripe.com | blocked | digital-storefront/t-011
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T10:54:12Z | metmuseum.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T10:54:12Z | upload.wikimedia.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T10:55:37Z | kind-robots.vercel.app | blocked | coloring-book/t-006
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T10:55:38Z | huggingface.co | blocked | ai-art-academy/t-021
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T10:55:38Z | civitai.com | blocked | ai-art-academy/t-021
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T11:07:51Z | metmuseum.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T11:07:52Z | upload.wikimedia.org | blocked | ai-art-academy/t-008
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T11:08:30Z | api.stripe.com | blocked | digital-storefront/t-013
blocked (URLError: <urlopen error Tunnel connection failed: 403 Forbidden>)

## 2026-07-17T11:50:07Z | metmuseum.org | reachable | ai-art-academy/t-008
reachable (HTTP 429)

## 2026-07-17T11:50:08Z | upload.wikimedia.org | reachable | ai-art-academy/t-008
reachable (HTTP 200)

## 2026-07-17T11:52:00Z | artic.edu | reachable | ai-art-academy/t-008
reachable (HTTP 403)

## 2026-07-17T11:52:01Z | api.artic.edu | reachable | ai-art-academy/t-008
reachable (HTTP 200)

## 2026-07-17T11:52:02Z | clevelandart.org | reachable | ai-art-academy/t-008
reachable (HTTP 200)

## 2026-07-17T11:52:03Z | nga.gov | reachable | ai-art-academy/t-008
reachable (HTTP 403)

## 2026-07-17T11:52:06Z | rijksmuseum.nl | reachable | ai-art-academy/t-008
reachable (HTTP 200)

## 2026-07-17T11:52:07Z | commons.wikimedia.org | reachable | ai-art-academy/t-008
reachable (HTTP 200)
