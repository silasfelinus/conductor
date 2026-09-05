#!/usr/bin/env python3
"""Turn Alexandria's container-log digest into a written morning review.

Silas, 2026-09-04: *"give me this kind of detail, guides on what to mute, and
how to fix ... baked into my daily morning email."*

`container_log_triage.py` (kind_robots) on Alexandria already answers *what changed* — it
fingerprints ~50 containers' error lines and diffs them against a baseline. The
digest it publishes is accurate and completely inert: a row saying `ownfoil ·
warn · 3999x` does not tell you that one truncated `.xci` is two thirds of the
box's daily log volume, that the fix is deleting a single file, or that the
netdata line beside it is cosmetic and safe to mute forever. That reading was
being done by hand, in chat, on request. This does it every morning.

The output is written to CONTAINER-LOG-REVIEW.json beside the digest, is picked
up by `build_digest.py` and rendered into the email by `build_digest_email_v2`.

Three things keep this from decaying into wallpaper, which is the specific way
a recurring automated report dies:

1. **It leads with what changed.** Standing problems are carried as a short
   "still costing you" list, not re-explained daily.
2. **The nag counter is computed here, not by the model.** `history` in the
   review file records when each fingerprint was first written up, so
   "unfixed for 9 days" is arithmetic on a stored date rather than something a
   model was asked to remember and could invent.
3. **It degrades to silence, never to noise.** No API key, an API failure, a
   digest that was never published — every one of those leaves the existing
   mechanical banner in place and exits 0. The digest email going out matters
   more than this section being in it.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_container_log_drift as drift  # noqa: E402

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
MODEL = os.environ.get("CONTAINER_LOG_REVIEW_MODEL", "claude-sonnet-5")
# claude-sonnet-5 runs adaptive (always-on) extended thinking with no
# budget_tokens knob to cap it -- thinking tokens count against max_tokens
# the same as visible output, so a low ceiling can be entirely consumed by
# thinking before any review text is written, producing a stop_reason:
# max_tokens response with only a thinking block ("empty completion"; see
# scripts/author_dream_proposal.py's MAX_TOKENS comment for the confirmed
# failure this exact pattern caused there on 2026-09-04). Raised for the
# same headroom reason, not because this review needs a longer answer.
MAX_TOKENS = 12000

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW = REPO_ROOT / "ops" / "home-server" / "CONTAINER-LOG-REVIEW.json"

# The model sees the changed signatures in full and the standing ones ranked by
# volume. Past ~30 rows the email is unreadable anyway, so a wider window would
# only buy tokens.
MAX_CHANGED = 25
MAX_STANDING = 25
MAX_ITEMS = 6
MAX_MUTES = 4
SAMPLE_CHARS = 300

SYSTEM = """\
You are triaging the overnight container logs of one person's home server \
(Alexandria, an Unraid box running ~50 Docker containers: *arr stack, media \
servers, WordPress sites, databases, monitoring). You write the container-log \
section of his morning email. He is technical, runs this box himself, and reads \
this before coffee.

Your job is to convert fingerprinted log signatures into decisions. For each \
thing you report, he should finish the sentence knowing what is wrong, what it \
costs him, and what to type.

Rank by what it actually costs, in this order:
1. Volume — a signature that is a large share of the day's matched lines is \
   usually one repeating failure, and killing it is the single highest-value fix.
2. Waste — repeated downloads, re-imports, retry storms, disk churn.
3. Security signal — probing, auth failures, exposed endpoints, plaintext \
   secrets in config. Say plainly whether a probe SUCCEEDED or failed; a failed \
   scan is context, not an incident, and must not be written as an alarm.
4. Real but contained errors.
5. Cosmetic noise — only ever as a mute recommendation, never as a finding.

Rules you must follow:

- Report AT MOST %(max_items)d items. Fewer is better. A quiet day should \
  produce one or two, or none at all.
- CHANGED signatures (new, spiking, newly quiet) are the reason this report \
  exists. Lead with them. Include a standing signature only when its ongoing \
  cost is high enough to be worth the line.
- A signature marked `days_standing` above 0 has been written up before. Do NOT \
  re-explain it. One short line: what it still costs and that it is still \
  unfixed.
- A signature that went QUIET after you recommended a fix is worth one \
  congratulatory clause, not a paragraph.
- Use ONLY the counts given to you. Never estimate, extrapolate, or invent a \
  number, a filename, a container, or a fingerprint.
- Samples are already redacted; `<REDACTED-BLOB>` and `<REDACTED>` are \
  deliberate. Never ask for the real value and never speculate about what it was.
- `fix` must be concrete. A shell command when a command does it, otherwise the \
  specific UI action ("blocklist that release in Sonarr's history for S03E02"). \
  Never write "investigate", "look into", or "monitor".
- Recommend a mute ONLY for a signature that is genuinely benign AND high-volume \
  enough to matter. Never mute a real problem to make the report shorter. Muting \
  is permanent and suppresses spike detection, so it is a deliberate choice, not \
  a tidying habit. Low-count cosmetic noise needs no mute at all — signatures \
  under 20 occurrences can never spike and under 10 can never go quiet, so they \
  are already silent.
- Write in plain, direct prose. No preamble, no "Here's your report", no \
  encouragement, no emoji.

Return ONLY a JSON object, no prose around it, in exactly this shape:

{
  "headline": "one sentence, under 100 chars, what today actually is",
  "items": [
    {
      "fingerprint": "the exact 12-char fingerprint from the input",
      "diagnosis": "1-3 sentences: what is wrong and what it costs.",
      "fix": "the concrete action or command.",
      "action": "fix" | "watch" | "mute"
    }
  ],
  "mute": [
    {"fingerprint": "...", "why": "one clause on why this is safe to silence forever"}
  ]
}

`items` may be empty on a genuinely quiet day; say so in the headline. `mute` \
may be empty and usually should be. At most %(max_mutes)d mute entries.
""" % {"max_items": MAX_ITEMS, "max_mutes": MAX_MUTES}


def load_review(path):
    """The previous review and its history. Never raises on a bad file."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def signature_rows(digest):
    """Changed and standing signatures, deduplicated, richest bucket winning.

    A fingerprint can appear in both `new` and `top`; the bucket that tells
    Silas something ("this is new") must survive the merge, so changed buckets
    are collected first and `top` only fills in what is left.
    """
    changed, standing, seen = [], [], set()
    for bucket in ("new", "spiking", "quiet"):
        for item in (digest.get(bucket) or [])[:MAX_CHANGED]:
            finger = item.get("fingerprint")
            if not finger or finger in seen:
                continue
            seen.add(finger)
            changed.append(dict(item, bucket=bucket))
    for item in (digest.get("top") or [])[:MAX_STANDING]:
        finger = item.get("fingerprint")
        if not finger or finger in seen:
            continue
        seen.add(finger)
        standing.append(dict(item, bucket="standing"))
    return changed, standing


def with_history(rows, history, today):
    """Attach days_standing from the stored first_seen, not from the model."""
    out = []
    for row in rows:
        record = history.get(row["fingerprint"]) or {}
        first = record.get("first_reported")
        days = 0
        if first:
            try:
                days = (today - datetime.date.fromisoformat(first)).days
            except ValueError:
                days = 0
        out.append(dict(row, days_standing=max(days, 0), first_reported=first))
    return out


def prompt_rows(rows, total_matched):
    lines = []
    for row in rows:
        share = ""
        if total_matched:
            pct = 100.0 * (row.get("count") or 0) / total_matched
            if pct >= 1.0:
                share = " · {:.0f}% of today's matched lines".format(pct)
        standing = ""
        if row.get("days_standing"):
            standing = " · REPORTED BEFORE, still unfixed after {} day(s)".format(
                row["days_standing"]
            )
        baseline = ""
        if row.get("baseline"):
            baseline = " · baseline {}".format(row["baseline"])
        lines.append(
            "[{finger}] {container} · {severity} · {count}x{share}{baseline}{standing}\n"
            "    {sample}".format(
                finger=row.get("fingerprint", "?"),
                container=row.get("container", "?"),
                severity=row.get("severity", "?"),
                count=row.get("count", 0),
                share=share,
                baseline=baseline,
                standing=standing,
                sample=str(row.get("sample") or "")[:SAMPLE_CHARS],
            )
        )
    return "\n".join(lines)


def build_prompt(digest, changed, standing):
    scan = digest.get("scan") or {}
    total_matched = scan.get("lines_matched") or 0
    parts = [
        "Host: {}   Window: {}   Generated: {}".format(
            digest.get("host", "?"), digest.get("window", "?"),
            digest.get("generated_at", "?"),
        ),
        "Scanned {} containers, {} lines read, {} matched, {} distinct signatures.".format(
            scan.get("containers_scanned", "?"), scan.get("lines_read", "?"),
            total_matched or "?", scan.get("signatures_total", "?"),
        ),
    ]
    unreadable = scan.get("containers_failed") or []
    if unreadable:
        parts.append("Unreadable containers: {}".format(", ".join(map(str, unreadable))))

    if changed:
        parts.append(
            "\n=== CHANGED OVERNIGHT (this is what the report is for) ===\n"
            + prompt_rows(changed, total_matched)
        )
    else:
        parts.append(
            "\n=== CHANGED OVERNIGHT ===\n"
            "Nothing. No new signatures, nothing spiking, nothing newly quiet."
        )

    if standing:
        parts.append(
            "\n=== STANDING, BY VOLUME (already known; include only if the cost "
            "earns the line) ===\n" + prompt_rows(standing, total_matched)
        )
    return "\n".join(parts)


def call_claude(prompt, system, api_key, timeout=120.0):
    body = json.dumps({
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    request = urllib.request.Request(API_URL, data=body, method="POST")
    request.add_header("content-type", "application/json")
    request.add_header("x-api-key", api_key)
    request.add_header("anthropic-version", API_VERSION)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode())
    blocks = payload.get("content") or []
    text = "".join(b.get("text", "") for b in blocks if isinstance(b, dict))
    if not text.strip():
        raise RuntimeError("Claude returned an empty completion ({}).".format(
            {"stop_reason": payload.get("stop_reason"), "usage": payload.get("usage")}
        ))
    return text


def parse_json_object(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.rstrip().endswith("```"):
            cleaned = cleaned.rstrip()[:-3]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in the completion")
    return json.loads(cleaned[start:end + 1])


def coerce_review(raw, rows_by_finger):
    """Keep only what the digest can vouch for.

    Every number rendered into the email comes from the digest, and every item
    must name a fingerprint that was actually in today's input -- so a model
    that invents a container, a count, or a signature produces a shorter
    review, never a wrong one.
    """
    items = []
    for item in (raw.get("items") or [])[:MAX_ITEMS]:
        if not isinstance(item, dict):
            continue
        row = rows_by_finger.get(str(item.get("fingerprint") or "").strip())
        if row is None:
            continue
        diagnosis = str(item.get("diagnosis") or "").strip()
        fix = str(item.get("fix") or "").strip()
        if not diagnosis:
            continue
        action = str(item.get("action") or "fix").strip().lower()
        if action not in ("fix", "watch", "mute"):
            action = "fix"
        items.append({
            "fingerprint": row["fingerprint"],
            "container": row.get("container", "?"),
            "severity": row.get("severity", "?"),
            "count": row.get("count", 0),
            "bucket": row.get("bucket", "standing"),
            "days_standing": row.get("days_standing", 0),
            "diagnosis": diagnosis,
            "fix": fix,
            "action": action,
        })

    mutes = []
    for entry in (raw.get("mute") or [])[:MAX_MUTES]:
        if not isinstance(entry, dict):
            continue
        row = rows_by_finger.get(str(entry.get("fingerprint") or "").strip())
        why = str(entry.get("why") or "").strip()
        if row is None or not why:
            continue
        mutes.append({
            "fingerprint": row["fingerprint"],
            "container": row.get("container", "?"),
            "count": row.get("count", 0),
            "why": why,
        })

    headline = str(raw.get("headline") or "").strip()[:200]
    return {"headline": headline, "items": items, "mute": mutes}


def update_history(history, items, today):
    """Record when each reported fingerprint was first written up.

    Only reported fingerprints are recorded. A signature the review declined to
    mention has no nag clock to start, and one that stops being reported keeps
    its first_reported so the counter survives a quiet day in between.
    """
    stamp = today.isoformat()
    for item in items:
        record = history.setdefault(item["fingerprint"], {})
        record.setdefault("first_reported", stamp)
        record["last_reported"] = stamp
        record["container"] = item["container"]
    return history


def author(digest, previous, now, api_key):
    today = now.date()
    history = dict(previous.get("history") or {})
    changed, standing = signature_rows(digest)
    changed = with_history(changed, history, today)
    standing = with_history(standing, history, today)
    if not changed and not standing:
        return None, history

    rows_by_finger = {row["fingerprint"]: row for row in changed + standing}
    raw = parse_json_object(call_claude(build_prompt(digest, changed, standing), SYSTEM, api_key))
    review = coerce_review(raw, rows_by_finger)
    review.update({
        "generated_at": now.isoformat(),
        "digest_generated_at": digest.get("generated_at", ""),
        "host": digest.get("host", ""),
        "model": MODEL,
    })
    return review, update_history(history, review["items"], today)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--digest", default=drift.DEFAULT_DIGEST)
    ap.add_argument("--output", default=str(DEFAULT_REVIEW))
    ap.add_argument("--stale-hours", type=float, default=drift.DEFAULT_STALE_HOURS)
    args = ap.parse_args(argv)

    # Every early return here is exit 0. A missing review leaves the mechanical
    # banner in place, which is a worse email but still an email; a non-zero
    # exit would mark the digest workflow failed over a section that is, by
    # construction, the least important thing in it.
    now = datetime.datetime.now(datetime.timezone.utc)
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("container log review: no ANTHROPIC_API_KEY; leaving the mechanical banner.")
        return 0

    try:
        digest = drift.load_digest(args.digest)
    except (OSError, ValueError, urllib.error.URLError) as error:
        print("container log review: could not read the digest ({}).".format(error))
        return 0
    if digest is None:
        print("container log review: no digest published yet; nothing to review.")
        return 0

    state, reason, _ = drift.assess(digest, now, args.stale_hours)
    if state in ("stale", "unresolved"):
        # "The User Script stopped running" is the whole finding, and the
        # banner already says it. Reviewing signatures from a digest that may
        # be days old would dress staleness up as news.
        print("container log review: digest is {} ({}); skipping.".format(state, reason))
        return 0

    previous = load_review(args.output)
    try:
        review, history = author(digest, previous, now, api_key)
    except (urllib.error.URLError, OSError, ValueError, RuntimeError, KeyError) as error:
        print("container log review: authoring failed ({}); "
              "leaving the mechanical banner.".format(error))
        return 0
    if review is None:
        print("container log review: digest holds no signatures; nothing to review.")
        return 0

    payload = {"version": 1, "review": review, "history": history}
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("container log review: {} item(s), {} mute suggestion(s) -> {}".format(
        len(review["items"]), len(review["mute"]), args.output
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
