# Container log triage — reading 50 containers so you don't have to

Silas, 2026-09-03: *"I'm not searching around the logs of 50-ish containers
regularly to find suboptimal problems. If something is erroring in the logs but
not actually breaking the container, I'm not aware of it."*

Netdata and the Unraid GUI already cover metrics and outright breakage. This
covers the thing neither does: the steady drip of errors from containers that
are still nominally healthy.

## What it does

`container_log_triage.py` runs on Alexandria daily, reads `docker logs` for
every running container, keeps only error-ish lines, and collapses them into
**signatures** — a line with its timestamps, IPs, UUIDs, paths, and numbers
replaced by placeholders, so 4,000 occurrences of one problem become one row.

It then diffs those against a stored baseline and reports only three things:

| bucket | meaning |
|---|---|
| `new` | a signature never seen before |
| `spiking` | a known signature whose rate jumped against its own history |
| `quiet` | a known signature that stopped — either you fixed it, or the job that logged it stopped running |

Everything else is counted and stored silently.

**The baseline is the point.** Without it you get the same 40 warnings every
day and stop reading within a week. With it, a stable homelab reports zero to
five items a day.

## Two rules this script is built around

**Redaction is mandatory, not polite.** AGENTS.md hard rule 15: any command
handed to a human must be *incapable* of printing a secret, because they will
paste its output back. This script prints log lines from 50 containers, so it is
exactly that hazard. Every retained line passes through `redact()` before it is
fingerprinted, stored, or displayed — PEM blocks, JWTs, bearer tokens,
`password=`-style pairs, URL userinfo and query params, emails, and a catch-all
for long high-entropy blobs — and samples are truncated to 200 characters on top
of that. Covered by `tests/test_container_log_triage.py`.

It is defense in depth, not a proof. If you spot a secret shape it misses, add a
pattern and a test. `--no-samples` drops sample lines entirely if you want to
ship skeletons only.

**State goes in appdata, never `/mnt/user/pc`.** AGENTS.md hard rule 14. Default
state dir is `/mnt/user/appdata/container-log-triage/`.

## Setup on Alexandria

### 1. Confirm python3

```bash
python3 --version
```

Stdlib only — no pip, no dependencies. If that command fails, nothing below works.

### 2. Put the script on the box

It is a single standalone file; it does not need the Conductor checkout.

```bash
mkdir -p /boot/config/plugins/user.scripts/scripts/container-log-triage
# copy container_log_triage.py to /mnt/user/appdata/container-log-triage/
chmod +x /mnt/user/appdata/container-log-triage/container_log_triage.py
```

### 3. Run the inventory first — before scheduling anything

```bash
/mnt/user/appdata/container-log-triage/container_log_triage.py --inventory
```

This ignores and does not write the baseline. It prints every distinct signature
across every container, grouped and ranked. **This is the highest-value run of
the whole project** — it is the thing you have never seen, and it is worth
reading properly before automating anything.

Two things to check in that first output:

- **`HIGH CARDINALITY` warnings.** A container producing hundreds of distinct
  signatures means normalization is not collapsing its log format — tune
  `SKELETON_STEPS` rather than accepting the noise.
- **`unreadable` containers.** Usually a template setting `--log-driver none`.
  Expected, listed, never fatal.

### 4. Schedule it in User Scripts

Create a script named `container-log-triage`, set to **Scheduled Daily**, with:

```bash
#!/bin/bash
/mnt/user/appdata/container-log-triage/container_log_triage.py \
  --state-dir /mnt/user/appdata/container-log-triage
```

Exit codes: `0` clean, `1` findings, `2` could not run. It writes
`digest.json` and `digest.txt` beside the baseline on every run.

The first scheduled run reports everything as `new` — that is the baseline being
built. Skim it, then acknowledge or mute the noise.

### 5. Quiet the known noise

```bash
# looked at it, it's fine — stays silent unless its rate spikes
container_log_triage.py --ack a1b2c3d4e5f6

# never report this again, even if it spikes
container_log_triage.py --mute a1b2c3d4e5f6 --note "known upstream bug"
```

Fingerprints are the `[a1b2c3d4e5f6]` values in the output. They are stable
across container recreation (keyed on container *name*, not id, so a Force
Update does not reset them).

## Useful flags

| flag | why |
|---|---|
| `--since 48h` | wider window; anything `docker logs --since` accepts |
| `--exclude netdata` | skip a chatty container (repeatable) |
| `--all` | include stopped containers |
| `--no-samples` | skeletons only, no sample lines |
| `--json` | digest JSON on stdout |
| `--timeout 120` | per-container read budget |

## The Conductor side

`scripts/check_container_log_drift.py` reads the digest and reports it like any
other `check_*` in this repo, so findings land in the session-start sweep rather
than in a file nobody opens.

```bash
python scripts/check_container_log_drift.py --digest <path-or-url>
```

It watches the clock as well as the contents: **a digest older than 48h is a
finding**, not a pass. This repo has already paid for that lesson —
`check_engine_heartbeat.py` exists because `healthcheck.ps1` stopped running at
2026-09-01 02:26:07 and never said so, its log simply ending ~37 hours before
anyone noticed. From the reading end, "nothing to report" and "not running" look
identical, so the age check is the only thing separating them.

A *missing* digest is exit 0 with a "not configured yet" note, so the sweep stays
quiet until the User Script is actually scheduled.

## Not yet wired: getting the digest off Alexandria

The digest currently lands on Alexandria's disk. Conductor sessions run in an
ephemeral cloud container that cannot reach the home LAN — no raw TCP, and
`192.168.x` / tailnet `100.x` addresses resolve to the cloud VPC, not the house
— so the digest has to be **pushed** out over HTTPS on 443.

At a few KB a day, any of these works:

1. **POST to Kind Robots** — reuses `relay_agent.py`'s existing outbound pattern
   and its bearer token; needs a small endpoint.
2. **Commit to a repo** — simplest, and gives free history and diffs.
3. **Cloudflare Tunnel** — worth it only if on-demand access to arbitrary logs
   is wanted later, not for shipping one small file.

Until one is chosen, run the checker against a local path and the sweep reports
"not configured yet".
