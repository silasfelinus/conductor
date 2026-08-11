# EGRESS-BLOCKERS.md

Append-only ledger of sandbox egress-allowlist rechecks. Several roadmap tasks
(ai-art-academy/t-008, t-013; digital-storefront's Stripe task; art-generator-connect's
Civitai/HF task) had each independently accumulated their own "RECHECKED <date>: still
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

## 2026-07-17T13:08:25Z | metmuseum.org | reachable | ai-art-academy/t-013
reachable (HTTP 429)

## 2026-07-17T13:08:27Z | upload.wikimedia.org | reachable | ai-art-academy/t-013
reachable (HTTP 200)

## 2026-07-17T13:08:28Z | www.metmuseum.org | reachable | ai-art-academy/t-013
reachable (HTTP 429)

## 2026-07-17T13:14:58Z | www.artic.edu | reachable | ai-art-academy/t-013
reachable (HTTP 403)

## 2026-07-17T13:14:59Z | api.artic.edu | reachable | ai-art-academy/t-013
reachable (HTTP 200)

## 2026-07-17T13:15Z | www.artic.edu/iiif/2/* (IMAGE HOST, not the domain) | manually-blocked | ai-art-academy/t-013
The automated recheck above logs www.artic.edu as "reachable (HTTP 403)" because
any HTTP response counts as reachable by this ledger's own rule (connection
succeeded). That masks a real, distinct problem: the 403 is a Cloudflare bot
challenge (`cf-mitigated: challenge` response header, JS-challenge HTML body),
not an ordinary 403 or rate limit — confirmed on both the full-size and
info.json IIIF paths, retried after a delay with no change. api.artic.edu (the
JSON metadata API, different host) is genuinely reachable and returns real data.
Net effect: artwork metadata + is_public_domain flags can be fetched from
api.artic.edu, but the actual image bytes at www.artic.edu/iiif/2/... cannot be
downloaded from this sandbox. Affects ai-art-academy/t-013's impressionism,
post-impressionism, and de-stijl examples (all correctly public-domain per the
API, just image-fetch-blocked) — left as ready follow-up work once this
resolves or a session runs with different egress.

## 2026-07-17T15:07:16Z | api.stripe.com | reachable | digital-storefront/t-013
reachable (HTTP 404)

## 2026-07-17T19:15:17Z | huggingface.co | reachable | ai-art-academy/t-021
reachable (HTTP 200)

## 2026-07-17T19:15:17Z | civitai.com | reachable | ai-art-academy/t-021
reachable (HTTP 200)

## 2026-07-18T11:17:11Z | kind-robots.vercel.app | reachable | ai-art-academy/t-004
reachable (HTTP 200)

## 2026-07-20T22:14:06Z | artic.edu | bot-challenged | ai-art-academy/t-010
bot-challenged (HTTP 403, cf-mitigated: challenge)

## 2026-07-20T22:14:24Z | huggingface.co | reachable | ai-art-academy/t-010
reachable (HTTP 200)

## 2026-07-20T22:14:25Z | civitai.com | reachable | ai-art-academy/t-010
reachable (HTTP 200)

## 2026-07-21T02:15:45Z | artic.edu | bot-challenged | ai-art-academy/t-010
bot-challenged (HTTP 403, cf-mitigated: challenge)

## 2026-07-21T02:15:46Z | www.artic.edu | bot-challenged | ai-art-academy/t-010
bot-challenged (HTTP 403, cf-mitigated: challenge)

## 2026-07-21T02:16:11Z | huggingface.co | reachable | ai-art-academy/t-010
reachable (HTTP 200)

## 2026-07-21T02:16:12Z | civitai.com | reachable | ai-art-academy/t-010
reachable (HTTP 200)

## 2026-07-22T16:08:12Z | commons.wikimedia.org | reachable | ai-art-academy/t-010
reachable (HTTP 200)

## 2026-07-26T02:05:00Z | kind-robots.vercel.app | reachable | ai-art-academy/t-004
reachable (HTTP 200)

## 2026-07-26T03:04:20Z | kind-robots.vercel.app | reachable | ai-art-academy/t-004
reachable (HTTP 200)

## 2026-07-26T05:05:45Z | kind-robots.vercel.app | reachable | coloring-book/t-022
reachable (HTTP 200)

## 2026-08-11T16:15:12Z | kind-robots.vercel.app | reachable | coloring-book/t-022
reachable (HTTP 200)
