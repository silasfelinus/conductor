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

## How a line is judged

**A line's own stated level wins.** Most of these containers say what they mean
— `[Info]`, `level=error`, `::INFO::`, `[php:warn]`, `"level":"error"`, `[WRN]`
— and the tool believes them in both directions: a stated warn/error/fatal is
kept, a stated info/debug/notice is dropped. Keyword matching is only the
fallback for lines that state nothing.

This is not a stylistic preference. From the first real inventory (2026-09-03),
scored by keywords alone:

| line | scored |
|---|---|
| `[Info] ... for Term: [Critical Role Vox Machina Origins]` | **fatal** |
| `[Info] DiskScanService: Scanning Panic (2021)` | **fatal** |
| `[Info] ... Skipping refresh of series: Trial & Error` | **error** |
| `[Info] DiskScanService: Scanning disk for Fail Safe` | kept |

Every one is an INFO line promoted by a word inside a *media title*. A library
containing Fail Safe, Panic, Trial & Error and Komi Can't Communicate is
adversarial input to a keyword classifier, and no keyword list survives it.

The trade: something logged at INFO that you did want — sabnzbd reports CRC
errors at INFO — is now dropped. `--include-info` turns the filter off.

**Paths may contain spaces.** The library is `/pc/movies/comedy/hot property
(2016)/...`, so a path rule that stops at the first space gives every filename
its own signature: bazarr showed 51 for about six real problems, radarr 43,
sonarr 33. Path matching now absorbs the spacey remainder, and any trailing
clause with it — `cannot update series <PATH> because of (IntegrityError)`
collapses to one row per root cause rather than one per title. The full reason
is still on the stored sample line.

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
  --state-dir /mnt/user/appdata/container-log-triage \
  --publish
```

Exit codes: `0` clean, `1` findings, `2` could not run or could not publish. It
writes `digest.json` and `digest.txt` beside the baseline on every run, and
commits the digest into Conductor — see **Publishing** below for the one-time
token setup. Drop `--publish` if you want to try it locally first.

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
| `--timeout 120` | per-container read budget |\n| `--include-info` | keep lines whose own level is info/debug/notice (default: drop) |
| `--publish` | commit the digest into Conductor in the same run |\n| `--secrets-dir` | where the publish token lives (default `/mnt/user/appdata/kind_robots/.secrets`) |

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

## Publishing: the digest commits itself into Conductor

The digest is committed to `ops/home-server/CONTAINER-LOG-DIGEST.json` on `main`,
beside the other home-server state files (`RENDER-BOX-STATUS`,
`ENGINE-HEARTBEAT-STATE.json`). Diffs are half the value — `git log -p` on that
one file is the history of what your containers have been complaining about.

**This happens inside the same daily run.** There is no second script, no
separate upload step, and nothing to add to pm2 — pm2 runs on ferngrotto and
supervises ComfyUI; it has no part in this. One User Script entry, one schedule.

It commits over the GitHub Contents API rather than cloning the repo onto the
array: nothing to keep in sync on Unraid, no git credential helper, no merge
race against the workflows that also commit to `main`, and no pack transfer for
a few KB of JSON. It still lands as an ordinary commit. Commits carry
`[skip ci]`, so a daily state file does not spend a full CI run.

### One-time: the publish token

Use a **fine-grained** personal access token, scoped to `silasfelinus/conductor`
only, with **Contents: write** and nothing else. That is the entire permission
this needs — it writes one file on one branch.

Create the file first, then paste into it, so the token never reaches your shell
history:

```bash
install -m 600 -D /dev/null /mnt/user/appdata/kind_robots/.secrets/conductor-publish-token
nano /mnt/user/appdata/kind_robots/.secrets/conductor-publish-token
```

The file may hold the bare token or a `CONDUCTOR_PUBLISH_TOKEN=...` line; quotes
are stripped either way. Hard rule 14 puts it under `.secrets/` and never on
`/mnt/user/pc`.

Verify presence without printing the value:

```bash
[ -s /mnt/user/appdata/kind_robots/.secrets/conductor-publish-token ] \
  && echo "token present" || echo "token MISSING"
stat -c '%a %n' /mnt/user/appdata/kind_robots/.secrets/conductor-publish-token
```

That should print `600`. If it prints anything else, fix it with `chmod 600`.

### The User Script

One entry, **Scheduled Daily**:

```bash
#!/bin/bash
/mnt/user/appdata/container-log-triage/container_log_triage.py \
  --state-dir /mnt/user/appdata/container-log-triage \
  --publish
```

Exit codes: `0` clean and published, `1` findings, `2` could not run **or could
not publish**. A digest nobody can read is not a clean run — without that, the
User Script would go green while the sweep quietly aged into a staleness warning
days later, which is the exact failure this whole pipeline exists to prevent,
reproduced one layer up.

To test publishing without waiting for the schedule, run it by hand once. It
prints the commit it made, and never the token.

### Where it shows up

Once it is publishing, three things read that file with no further setup:

| reader | what you see |
|---|---|
| `scripts/check_container_log_drift.py` | the session-start sweep reports new/spiking/quiet signatures |
| the daily digest email | one line: quiet, or what changed, or that the script stopped running |
| `git log -p ops/home-server/CONTAINER-LOG-DIGEST.json` | the whole history |

### Rotating or revoking

Replace the file's contents and the next run picks it up — nothing caches it.
Revoking the token in GitHub makes the next run exit 2 with an explicit
"GitHub rejected the token" message rather than failing silently.
