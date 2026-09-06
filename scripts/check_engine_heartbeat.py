#!/usr/bin/env python3
"""check_engine_heartbeat.py — is the render engine actually alive, right now?

The dead-man's switch for the art pipeline. Every other health check in this
repo is either EDGE-TRIGGERED (a delta of failures per tick, a state
transition) or WORK-CONDITIONAL (it needs PENDING jobs or stale claims to have
an opinion). None of them ask the one question that matters when nothing is
happening: *when did we last hear from the engine?*

That gap cost 24 hours on 2026-09-02. ComfyUI crash-looped under pm2 (a custom
node's "\N{HIGH VOLTAGE SIGN}" hit a cp1252 stdout and killed the interpreter
before the Prompt Server bound 8188). Four separate checks stayed quiet:

  * healthcheck.ps1's liveness probe — the on-box watchdog had itself stopped
    running at 2026-09-01 02:26:07, ~37 hours before Silas noticed. Its log
    just ends. A watchdog cannot report its own absence, and this one was the
    only thing watching.
  * healthcheck.ps1's render-failure watchdog — measures NEW failures per tick,
    so it went quiet the moment the PENDING backlog finished draining. It needs
    work to fail.
  * check_render_box.py — with a drained queue it scored `None, "queue idle"`
    and main() prints "render box UP". ops/home-server/RENDER-BOX-STATUS still
    read `up` throughout.
  * the daily digest — carried nothing about render health at all.

Meanwhile the relay was posting `COMFY ok:false` to /api/server/heartbeat every
60 seconds — roughly 1,440 explicit "the engine is down" messages over the
outage — into a ServerHealthCheck table whose stated purpose is "so the ArtJob
dashboard can chart uptime". The signal was never missing. Nothing alarmed on it.

So: this runs OFF THE BOX (GitHub Actions), reads that same heartbeat series
through GET /api/server/uptime, and has an opinion when NOTHING is happening.
Two independent alarms, neither of which depends on queue depth:

  SILENT  no heartbeat at all within --stale-minutes. The relay is not running,
          the box is off, or it cannot reach Kind Robots. This is the state the
          on-box watchdog can never report, because it dies with the box.
  DOWN    heartbeats are arriving and saying ok:false for at least
          --down-minutes. The relay is alive and telling us the engine is not.
  DOZING  heartbeats are arriving, and healthy, but far too FAR APART. The
          relay's heartbeat thread sleeps 60s and can block at most 85s
          (a 10s engine probe plus a 15s post), so a gap past --doze-gap-minutes
          is not something it can produce: the process was not being scheduled.
          Repeatedly, that is a box suspending and resuming underneath a relay
          that never learns it happened.

DOZING exists because a box that sleeps looks HEALTHY from every angle. Each
beat it does send is fresh and ok:true, so neither alarm above fires, while the
machine spends most of an hour frozen. Observed 2026-09-06: one beat every ~7
minutes for 2h20m, either side of blackouts of 143 and 200 minutes.

An idle queue is not a broken box — that part of check_render_box.py's
reasoning was always right. But an idle queue with a silent or failing engine
heartbeat IS a broken box, and that distinction is the whole point of this file.

Exit codes: 0 healthy, 1 a problem worth an email, 2 unresolved (no token, API
unreachable, no COMFY server configured) — 2 is deliberately NOT 1, so a broken
credential cannot masquerade as a broken render box.

Env: KR_BASE_URL, KR_API_TOKEN (admin — /api/server/uptime is admin-only).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

# A heartbeat every 60s (relay HEARTBEAT_SECONDS) means 15 minutes is ~15
# missed beats -- comfortably past a deploy, a reboot, or a transient network
# blip, and still far inside the 24 hours this is built to prevent.
DEFAULT_STALE_MINUTES = 15
# A crash-looping engine reports ok:false continuously. A single restart
# reports it for a few beats. 10 minutes tells those apart.
DEFAULT_DOWN_MINUTES = 10
DEFAULT_WINDOW_HOURS = 6
# The relay's heartbeat thread sleeps 60s and its two HTTP calls time out at 10s
# and 15s, so 85s is the longest gap it can produce while running. 3 minutes is
# comfortably past that: a gap this size means the process was not scheduled,
# not that it was slow.
DEFAULT_DOZE_GAP_MINUTES = 3.0
# One such gap is a restart or a one-off stall. Three inside the lookback is a
# pattern, and a pattern is what distinguishes a dozing box from an event.
DEFAULT_DOZE_MIN_GAPS = 3
DEFAULT_DOZE_LOOKBACK_MINUTES = 60.0
# GET /api/server/uptime returns at most this many samples and downsamples to
# fit, which manufactures gaps that look exactly like dozing. Confirmed by
# asking for 5000 and getting 500. Never score dozing off a capped series.
SAMPLE_CAP = 500

OK = "ok"
SILENT = "silent"
DOWN = "down"
DOZING = "dozing"
UNRESOLVED = "unresolved"

EXIT_HEALTHY = 0
EXIT_PROBLEM = 1
EXIT_UNRESOLVED = 2


def parse_timestamp(value):
    """Parse an ISO-8601 timestamp from the API into an aware datetime, or None.

    Prisma serialises through JSON as e.g. "2026-09-02T15:20:37.123Z".
    fromisoformat on Python < 3.11 rejects the trailing "Z", and this script has
    to run on whatever the runner ships, so normalise it rather than assume.
    """
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def fetch_uptime(server_type="COMFY", window_hours=DEFAULT_WINDOW_HOURS, timeout=20.0):
    """The `data` block from GET /api/server/uptime. Raises RuntimeError."""
    if not KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN is required to read the engine heartbeat.")

    url = (
        f"{KR_BASE_URL}/api/server/uptime"
        f"?serverType={server_type}&window={int(window_hours)}&samples=500"
    )
    request = urllib.request.Request(url, method="GET")
    request.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    request.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            payload = json.loads(response.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"uptime returned HTTP {error.code}") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise RuntimeError(f"uptime unreachable: {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"uptime returned unreadable JSON: {error}") from error

    if status != 200 or not isinstance(payload, dict) or not payload.get("success"):
        raise RuntimeError(f"uptime returned an unsuccessful payload (HTTP {status})")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("uptime payload missing 'data'")
    return data


def latest_beat(server):
    """(when, ok) for the most recent heartbeat on `server`, or (None, None).

    Prefers the sample series (it carries per-beat `ok`) and falls back to the
    denormalised lastCheckedAt/lastStatus columns. `samples` arrives
    chronological -- the endpoint reverses a desc query for charting -- so the
    newest beat is the LAST element, not the first. Reading samples[0] here
    would pin the verdict to the oldest beat in the window and report a
    six-hour-old success as current, which is precisely the "stale completion
    counts as health" bug this file exists to avoid.
    """
    samples = server.get("samples")
    if isinstance(samples, list) and samples:
        for sample in reversed(samples):
            if not isinstance(sample, dict):
                continue
            when = parse_timestamp(sample.get("checkedAt"))
            if when:
                return when, bool(sample.get("ok"))

    when = parse_timestamp(server.get("lastCheckedAt"))
    if when:
        status = str(server.get("lastStatus") or "").strip().lower()
        return when, status in ("ok", "up", "online", "healthy", "true")
    return None, None


def newest_ok_beat(server):
    """When the engine last reported HEALTHY, or None. Used for the message.

    "down since" is the question a human actually asks, and the last ok beat
    answers it far better than "the oldest failing beat we still have", which
    is bounded by the query window rather than by the outage.
    """
    samples = server.get("samples")
    if not isinstance(samples, list):
        return None
    for sample in reversed(samples):
        if isinstance(sample, dict) and sample.get("ok"):
            when = parse_timestamp(sample.get("checkedAt"))
            if when:
                return when
    return None


def oldest_beat(server):
    """When the oldest retained heartbeat in the window arrived, or None.

    The lower bound on an outage whose start predates everything we can see.
    """
    samples = server.get("samples")
    if not isinstance(samples, list):
        return None
    for sample in samples:
        if isinstance(sample, dict):
            when = parse_timestamp(sample.get("checkedAt"))
            if when:
                return when
    return None


def minutes_since(when, now):
    return (now - when).total_seconds() / 60.0


def detect_dozing(
    server,
    now,
    gap_minutes=DEFAULT_DOZE_GAP_MINUTES,
    min_gaps=DEFAULT_DOZE_MIN_GAPS,
    lookback_minutes=DEFAULT_DOZE_LOOKBACK_MINUTES,
):
    """(is_dozing, detail) for a server whose latest beat is fresh and healthy.

    Reads the SPACING of the recent beats rather than their content. The relay
    cannot space its own beats past 85 seconds, so a cluster of far larger gaps
    is evidence about the machine, not about the relay or the engine.

    Returns (False, None) on a capped sample series: the endpoint downsamples to
    SAMPLE_CAP, and downsampling turns a perfectly healthy hour into a page of
    invented gaps. A false SLEEP alarm would be worse than the silence this is
    meant to end.
    """
    if min_gaps <= 0:
        return False, None

    samples = server.get("samples")
    if not isinstance(samples, list) or len(samples) >= SAMPLE_CAP:
        return False, None

    beats = sorted(
        when
        for when in (
            parse_timestamp(sample.get("checkedAt"))
            for sample in samples
            if isinstance(sample, dict)
        )
        if when is not None
    )
    # Bounded at BOTH ends. An unbounded upper end lets a beat newer than `now`
    # into the window, which drags a gap from outside the lookback into a
    # verdict that claims to describe only the last hour.
    recent = [
        when for when in beats if 0 <= minutes_since(when, now) <= lookback_minutes
    ]
    if len(recent) < 2:
        return False, None

    gaps = [
        (earlier, (later - earlier).total_seconds() / 60.0)
        for earlier, later in zip(recent, recent[1:])
        if (later - earlier).total_seconds() / 60.0 >= gap_minutes
    ]
    if len(gaps) < min_gaps:
        return False, None

    widest = max(gap for _, gap in gaps)
    return True, (
        f"{len(gaps)} gaps of {gap_minutes:.0f}+ minutes between heartbeats in "
        f"the last {lookback_minutes:.0f} minutes (widest {widest:.0f} min), "
        f"against a relay that cannot space them past ~1.5 minutes"
    )


def assess_server(
    server,
    now,
    stale_minutes=DEFAULT_STALE_MINUTES,
    down_minutes=DEFAULT_DOWN_MINUTES,
    doze_gap_minutes=DEFAULT_DOZE_GAP_MINUTES,
    doze_min_gaps=DEFAULT_DOZE_MIN_GAPS,
):
    """(state, reason) for one server report. Pure — all I/O is the caller's."""
    title = server.get("title") or f"server {server.get('serverId')}"
    when, ok = latest_beat(server)

    if when is None:
        return SILENT, (
            f"{title}: no heartbeat on record at all in the query window. "
            "The relay has never reported, or its history was cleared."
        )

    age = minutes_since(when, now)
    if age >= stale_minutes:
        return SILENT, (
            f"{title}: last heartbeat was {age:.0f} minutes ago "
            f"({when.isoformat()}), over the {stale_minutes}-minute limit. "
            "kr-relay is not reporting — the box is off, the relay is not "
            "running, or it cannot reach Kind Robots."
        )

    if not ok:
        last_ok = newest_ok_beat(server)
        if last_ok is not None:
            down_for = minutes_since(last_ok, now)
            since_text = f"since {last_ok.isoformat()}"
        else:
            # Not one healthy beat anywhere in the window. The outage is
            # therefore at least as old as the window, and this is the exact
            # shape of a sustained one -- 2026-09-02 had ~1,440 consecutive
            # ok:false beats. Dating it from the NEWEST beat instead (which is
            # seconds old, because they keep arriving) would score a day-long
            # outage as "down for 0 minutes" and return OK, silencing the one
            # case this file exists to catch.
            oldest = oldest_beat(server)
            down_for = minutes_since(oldest, now) if oldest else float("inf")
            since_text = "for the entire query window, with no healthy beat in it"

        if down_for >= down_minutes:
            return DOWN, (
                f"{title}: reporting ok:false {since_text} "
                f"({down_for:.0f} minutes). The relay is alive and telling us "
                "the engine is not — jobs will fail at POST /prompt."
            )
        return OK, (
            f"{title}: reporting ok:false but only for {down_for:.0f} minutes "
            f"(under the {down_minutes}-minute limit) — likely a restart."
        )

    # Fresh and healthy, so nothing above fires. Ask the one remaining question:
    # were the beats leading up to this one arriving on time?
    dozing, detail = detect_dozing(
        server, now, gap_minutes=doze_gap_minutes, min_gaps=doze_min_gaps
    )
    if dozing:
        return DOZING, (
            f"{title}: heartbeat is healthy right now, but {detail}. The box is "
            "being suspended and resumed underneath the relay — nothing renders "
            "while it is frozen, and SMB mappings and CUDA contexts do not "
            "reliably survive the cycle. Check 'powercfg /lastwake' and "
            "'powercfg /q SCHEME_CURRENT SUB_SLEEP' on the box."
        )

    return OK, f"{title}: heartbeat healthy {age:.1f} minutes ago."


def assess(
    data,
    now,
    stale_minutes=DEFAULT_STALE_MINUTES,
    down_minutes=DEFAULT_DOWN_MINUTES,
    doze_gap_minutes=DEFAULT_DOZE_GAP_MINUTES,
    doze_min_gaps=DEFAULT_DOZE_MIN_GAPS,
):
    """(state, reason) across every active server in the uptime payload.

    Worst state wins, and an inactive Server row is skipped: deactivating a
    server in the admin UI is a deliberate act, and paging about a box someone
    intentionally retired is how a watchdog trains its owner to ignore it.
    """
    servers = data.get("servers")
    if not isinstance(servers, list) or not servers:
        return UNRESOLVED, "no COMFY server rows returned — nothing to check."

    active = [s for s in servers if isinstance(s, dict) and s.get("isActive")]
    if not active:
        return UNRESOLVED, (
            f"all {len(servers)} COMFY server row(s) are marked inactive — "
            "nothing is expected to be rendering."
        )

    verdicts = [
        assess_server(
            server,
            now,
            stale_minutes,
            down_minutes,
            doze_gap_minutes,
            doze_min_gaps,
        )
        for server in active
    ]
    # DOZING sits last: a box that is frozen half the time is a real problem,
    # but a box that is answering ok:false right now is a worse one.
    for wanted in (SILENT, DOWN, DOZING):
        matching = [reason for state, reason in verdicts if state == wanted]
        if matching:
            return wanted, " | ".join(matching)
    return OK, " | ".join(reason for _, reason in verdicts)


DEFAULT_REALERT_HOURS = 6.0

ALERT_NONE = "none"
ALERT_DOWN = "down"
ALERT_REMINDER = "reminder"
ALERT_RECOVERED = "recovered"


def load_state(path):
    """The prior run's record, or None. A corrupt file is treated as absent."""
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            record = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    return record if isinstance(record, dict) else None


def save_state(path, record):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")


def decide_alert(previous, state, now, realert_hours=DEFAULT_REALERT_HOURS):
    """(alert, record) — what to email, and the state to persist.

    The auto-art-generate render-box email fires only on the TRANSITION
    (`NOW=down && PREV!=down`), so a box down for a week emails once, on day
    one. Silence then means "still broken" and "fine" at the same time. Here a
    sustained problem re-alerts every `realert_hours` until it clears.

    UNRESOLVED is deliberately inert: it neither alerts nor overwrites the
    stored state. An expired KR_API_TOKEN must not manufacture a RECOVERED
    email for an engine that is still down, nor reset the outage clock so the
    next reminder never comes.
    """
    stamp = now.isoformat()
    bad_states = (SILENT, DOWN, DOZING)

    if state == UNRESOLVED:
        return ALERT_NONE, previous

    previous = previous if isinstance(previous, dict) else {}
    was_bad = previous.get("state") in bad_states

    if state in bad_states:
        if not was_bad:
            return ALERT_DOWN, {"state": state, "since": stamp, "last_alert_at": stamp}

        since = previous.get("since") or stamp
        last_alert = parse_timestamp(previous.get("last_alert_at"))
        due = last_alert is None or (now - last_alert).total_seconds() >= realert_hours * 3600
        if due:
            return ALERT_REMINDER, {
                "state": state,
                "since": since,
                "last_alert_at": stamp,
            }
        return ALERT_NONE, {
            "state": state,
            "since": since,
            "last_alert_at": previous.get("last_alert_at") or stamp,
        }

    if was_bad:
        return ALERT_RECOVERED, {"state": OK, "since": stamp, "last_alert_at": stamp}
    return ALERT_NONE, {
        "state": OK,
        "since": previous.get("since") or stamp,
        "last_alert_at": previous.get("last_alert_at"),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stale-minutes", type=float, default=DEFAULT_STALE_MINUTES)
    parser.add_argument("--down-minutes", type=float, default=DEFAULT_DOWN_MINUTES)
    parser.add_argument("--window-hours", type=float, default=DEFAULT_WINDOW_HOURS)
    parser.add_argument(
        "--doze-gap-minutes",
        type=float,
        default=DEFAULT_DOZE_GAP_MINUTES,
        help="a gap between heartbeats this wide is longer than the relay can "
        "produce while running (default: %(default)s)",
    )
    parser.add_argument(
        "--doze-min-gaps",
        type=int,
        default=DEFAULT_DOZE_MIN_GAPS,
        help="how many such gaps in the last hour count as a dozing box rather "
        "than a one-off stall (default: %(default)s); 0 disables the check",
    )
    parser.add_argument("--server-type", default="COMFY")
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the verdict as JSON on stdout (for a workflow step)",
    )
    parser.add_argument(
        "--state-file",
        help="persist state here so a sustained problem re-alerts instead of "
        "emailing once on the transition and then going quiet",
    )
    parser.add_argument("--realert-hours", type=float, default=DEFAULT_REALERT_HOURS)
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)

    try:
        data = fetch_uptime(args.server_type, args.window_hours)
    except RuntimeError as error:
        state, reason = UNRESOLVED, str(error)
    else:
        state, reason = assess(
            data,
            now,
            args.stale_minutes,
            args.down_minutes,
            args.doze_gap_minutes,
            args.doze_min_gaps,
        )

    alert = ALERT_NONE
    if args.state_file:
        previous = load_state(args.state_file)
        alert, record = decide_alert(previous, state, now, args.realert_hours)
        if record is not None and record != previous:
            save_state(args.state_file, record)

    if args.json:
        print(json.dumps({"state": state, "reason": reason, "alert": alert}))
    elif state == OK:
        print(f"engine heartbeat OK: {reason}")
    else:
        print(f"engine heartbeat {state.upper()}: {reason}", file=sys.stderr)

    if state == OK:
        return EXIT_HEALTHY
    if state == UNRESOLVED:
        return EXIT_UNRESOLVED
    return EXIT_PROBLEM


if __name__ == "__main__":
    sys.exit(main())
