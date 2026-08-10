#!/usr/bin/env python3
"""Apply small task-event files to authoritative conductor roadmaps.

The GitHub connector can reliably create tiny files but may truncate large roadmap
reads. This processor runs inside the repository checkout, applies task mutations
against the complete YAML file, validates the result, resolves dependencies, and
removes successfully consumed events.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bump_continuous_improvement import (  # noqa: E402
    LANE_COUNT as CI_LANE_COUNT,
    PR_RE as CI_PR_RE,
    bump_continuous_improvement_text,
)
from roadmap_claims import parse_timestamp  # noqa: E402
from roadmap_text_patch import apply_task_field_ops  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "task-events"
PROJECT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TASK_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ALLOWED_OPERATIONS = {
    "claim",
    "done",
    "ready",
    "review",
    "needs-human",
    "blocked",
    "rearm",
}
CLOSED_OPERATIONS = {"done", "blocked"}


class TaskEventCollision(Exception):
    """A claim (or later transition) that lost a race to another session.

    Raised so process() can *consume* the losing event -- delete it, mutate no
    roadmap state -- as a benign ALREADY_CLAIMED/collision result, instead of
    leaving it queued as a poison event that fails every future processor run for
    every unrelated PR (the same failure shape conductor/t-067 hit with malformed
    files). Restores the atomic ALREADY_CLAIMED invariant claim_task.py provides.
    """


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def event_files() -> list[Path]:
    if not EVENT_DIR.exists():
        return []
    return sorted(
        path
        for path in EVENT_DIR.glob("*.yaml")
        if path.name not in {"example.yaml"}
    )


def require_string(event: dict[str, Any], key: str, pattern: re.Pattern[str] | None = None) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"event field {key!r} must be a non-empty string")
    value = value.strip()
    if pattern and not pattern.fullmatch(value):
        raise ValueError(f"event field {key!r} contains unsupported characters")
    return value


def continuous_improvement_fields(event: dict[str, Any]) -> tuple[int, str] | None:
    """Return `(lane, pr_ref)` if the event carries both `continuous_improvement_lane`
    and `continuous_improvement_pr`, or `None` if neither is present.

    Fixes conductor/t-103: `rearm`/`ready`/`done` events previously only ever wrote
    a task's top-level `status`/`note` fields, never a `t-010`-style nested
    `continuous_improvement` mapping (`last_lane`/`next_lane`/`last_run`/`last_pr`),
    so the counter froze at its pre-cycle value on every close-out that went
    through the task-events path instead of a session hand-editing the roadmap.
    A closing session now sets these two fields explicitly on the event file and
    the processor applies them via `bump_continuous_improvement_text` (the same
    pure update function `scripts/bump_continuous_improvement.py`'s CLI already
    uses for the manual catch-up path) alongside the normal status transition.

    Both fields must be supplied together -- a lane number with no PR reference
    (or vice versa) is a malformed event, not a partial update, so this raises
    rather than silently applying half the pair.
    """
    lane = event.get("continuous_improvement_lane")
    pr_ref = event.get("continuous_improvement_pr")
    if lane is None and pr_ref is None:
        return None
    if lane is None or pr_ref is None:
        raise ValueError(
            "continuous_improvement_lane and continuous_improvement_pr must be "
            "supplied together"
        )
    if not isinstance(lane, int) or isinstance(lane, bool) or not 1 <= lane <= CI_LANE_COUNT:
        raise ValueError(
            f"continuous_improvement_lane must be an integer 1-{CI_LANE_COUNT}, "
            f"got {lane!r}"
        )
    if not isinstance(pr_ref, str) or not CI_PR_RE.match(pr_ref.strip()):
        raise ValueError(
            f"continuous_improvement_pr must look like owner/repo#number, got {pr_ref!r}"
        )
    return lane, pr_ref.strip()


# conductor/t-112: a `done` event's note can *claim* a PR merged without the
# merge having actually happened yet (brainstorm/t-010, 2026-08-10 -- a
# scheduled task-events run applied `done` six minutes before kind_robots#1718
# actually merged, because nothing checked GitHub). `verify_pr` is the
# reliable, structured way for an event writer to say "don't apply this until
# GitHub confirms owner/repo#N is merged"; the note-text scan below is a
# best-effort safety net for the shorthand `kind_robots#1718` / `conductor#42`
# cross-reference form, not a substitute for it -- prose like "PR #1718" with
# no repo prefix is deliberately NOT matched, since guessing the repo from
# free text risks false positives on unrelated numbers.
VERIFY_PR_RE = re.compile(r"^[\w.-]+/[\w.-]+#\d+$")
NOTE_PR_REF_RE = re.compile(r"\b(conductor|kind[_-]robots)#(\d+)\b", re.IGNORECASE)
REPO_ALIASES = {
    "conductor": "silasfelinus/conductor",
    "kind_robots": "silasfelinus/kind_robots",
}


def extract_pr_references(event: dict[str, Any]) -> list[tuple[str, int]]:
    """Return the `[(owner/repo, number), ...]` PR references a `done` event wants
    verified before it's allowed to close a task, deduplicated in the order found.

    Pure and network-free -- reads only the event's own fields -- so it's safe to
    call from the PR-time validator as well as the processor. Raises ValueError on
    a malformed `verify_pr` field (validation, not a network concern).
    """
    refs: list[tuple[str, int]] = []

    structured = event.get("verify_pr")
    if structured is not None:
        if not isinstance(structured, str) or not VERIFY_PR_RE.match(structured.strip()):
            raise ValueError(f"verify_pr must look like owner/repo#number, got {structured!r}")
        owner_repo, number = structured.strip().rsplit("#", 1)
        refs.append((owner_repo, int(number)))

    note = event.get("note")
    if isinstance(note, str):
        for alias, number in NOTE_PR_REF_RE.findall(note):
            repo = REPO_ALIASES[alias.lower().replace("-", "_")]
            ref = (repo, int(number))
            if ref not in refs:
                refs.append(ref)

    return refs


def check_pr_merged(repo: str, number: int) -> bool:
    """Return True if `repo`'s PR `number` is merged, False if it exists but isn't.

    Raises on any network/API failure (missing token, rate limit, unreachable
    host, non-200 response) -- callers must NOT treat "couldn't check" as either
    outcome; leaving the event queued for a later run is the safe default. A
    thin wrapper around one GET call so tests can monkeypatch it directly
    instead of mocking urllib.
    """
    url = f"https://api.github.com/repos/{repo}/pulls/{number}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "conductor-process-task-events",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise RuntimeError(
                f"verify_pr references {repo}#{number}, but GitHub returned 404; "
                "the PR or repository does not exist or is not visible to this token"
            ) from error
        raise RuntimeError(f"could not reach GitHub API for {repo}#{number}: {error}") from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(f"could not reach GitHub API for {repo}#{number}: {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"malformed GitHub API response for {repo}#{number}: {error}") from error
    if not isinstance(payload, dict) or "merged" not in payload:
        raise RuntimeError(f"unexpected GitHub API response for {repo}#{number}: {payload!r}")
    return bool(payload["merged"])


def find_task(roadmap: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = roadmap.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("roadmap tasks must be a list")
    matches = [task for task in tasks if isinstance(task, dict) and task.get("id") == task_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one task {task_id!r}; found {len(matches)}")
    return matches[0]


def stale_reason(task: dict[str, Any], event: dict[str, Any]) -> str | None:
    """Return a human-readable reason if `task`'s live state has already moved past
    what `event` knew about, or None if the event is still current.

    A queued event can sit unapplied for a while (e.g. stuck behind a malformed
    sibling file -- see conductor/t-067). If the task gets claimed or otherwise
    updated again in the meantime, blindly applying the old event once it finally
    parses would silently revert that newer state. Compare the event's own
    `updated` timestamp against the task's live `claimed_at`/`updated`: if the task
    has moved on since the event was generated, the event is stale.
    """
    event_updated = parse_timestamp(event.get("updated"))
    if event_updated is None:
        return None  # no reference timestamp on the event; nothing to compare against

    for field in ("claimed_at", "updated"):
        task_ts = parse_timestamp(task.get(field))
        if task_ts is not None and task_ts > event_updated:
            return (
                f"task.{field}={task_ts.isoformat()} is newer than event.updated="
                f"{event_updated.isoformat()} -- task moved on after this event was queued"
            )
    return None


def verify_event_ownership(task: dict[str, Any], event: dict[str, Any], operation: str) -> None:
    """For a non-claim transition that names a `session`, refuse to mutate a task a
    *different* session currently owns.

    Opt-in and backward compatible: an event with no `session` (the legacy path)
    is unaffected, so existing sessionless review/done events keep working. When a
    session IS named and it does not match the task's live `claimed_by`, raise
    TaskEventCollision so process() consumes the losing event rather than letting a
    session that lost the claim later flip the winner's task to review/done/etc.
    A `force: true` event bypasses this check (explicit override).
    """
    if event.get("force") or event.get("session") is None:
        return
    session = require_string(event, "session")
    claimed_by = task.get("claimed_by")
    if claimed_by is not None and claimed_by != session:
        raise TaskEventCollision(
            f"ALREADY_CLAIMED: {operation} not permitted -- task claimed_by="
            f"{claimed_by!r} but event session={session!r} (not this session's claim)"
        )


def compute_transition_ops(
    task: dict[str, Any], event: dict[str, Any], operation: str
) -> list[tuple[str, str, Any]]:
    """Decide which fields change for this event, without mutating `task` or
    touching any file. Returns a list of ("set"|"unset", field, value) ops in
    application order; an empty list means the event is a true no-op (e.g. a
    repeat claim by the same owner *and* session).

    Raises TaskEventCollision when a claim (or session-tagged later transition)
    loses a race to a different session -- callers consume that as an
    ALREADY_CLAIMED result, not a hard error."""
    current = task.get("status")
    force = bool(event.get("force", False))
    ops: list[tuple[str, str, Any]] = []

    timestamp = event.get("updated")
    if timestamp is None:
        timestamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    if operation == "claim":
        # Every claim must name the session that owns it, so a later collision or
        # ownership check has something concrete to compare (owner alone collapses
        # two concurrent Worker sessions into one owner-level no-op).
        session = require_string(event, "session")
        owner = event.get("owner", "worker")
        if current == "claimed" and not force:
            # A repeat claim is a true no-op ONLY when the same owner AND the same
            # session already hold it (idempotent replay). A different session on
            # an already-claimed task lost the race -- surface it as a collision so
            # the losing event is consumed, preserving the atomic ALREADY_CLAIMED
            # invariant instead of silently no-op'ing two rival claims into one.
            if task.get("owner") == owner and task.get("claimed_by") == session:
                return []
            raise TaskEventCollision(
                f"ALREADY_CLAIMED: task claimed_by={task.get('claimed_by')!r} "
                f"(owner={task.get('owner')!r}); losing claim session={session!r}"
            )
        if current != "ready" and not force:
            raise ValueError(f"claim requires status ready, found {current!r}")
        ops.append(("set", "status", "claimed"))
        ops.append(("set", "owner", owner))
        ops.append(("set", "claimed_by", session))
        ops.append(("set", "claimed_at", timestamp))
    elif operation == "rearm":
        if not task.get("recurring") and not force:
            raise ValueError("rearm requires recurring: true")
        ops.append(("set", "status", "ready"))
        ops.append(("unset", "owner", None))
        ops.append(("unset", "claimed_by", None))
        ops.append(("unset", "claimed_at", None))
    else:
        verify_event_ownership(task, event, operation)
        target = operation
        if not (operation in CLOSED_OPERATIONS and current == target):
            ops.append(("set", "status", target))
        if target not in {"claimed", "review"}:
            ops.append(("unset", "owner", None))

    if operation == "needs-human":
        ops.append(("set", "soft_gate", "true" if event.get("soft_gate") else "false"))
    elif operation in {"ready", "claim", "done", "blocked", "rearm"}:
        ops.append(("unset", "soft_gate", None))

    if "approved_by_human" in event:
        approved_by_human = event["approved_by_human"]
        if not isinstance(approved_by_human, bool):
            raise ValueError("approved_by_human must be a boolean when supplied")
        ops.append(
            (
                "set",
                "approved_by_human",
                "true" if approved_by_human else "false",
            )
        )

    ops.append(("set", "updated", timestamp))

    note = event.get("note")
    if note is not None:
        if not isinstance(note, str) or not note.strip():
            raise ValueError("note must be a non-empty string when supplied")
        existing = task.get("note")
        new_note = f"{existing}\n\n{note.strip()}" if existing else note.strip()
        ops.append(("set", "note", new_note))

    return ops


def prepare_learning(
    event: dict[str, Any],
    project: str,
    task_id: str,
    operation: str,
    task: dict[str, Any] | None = None,
    roadmap: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Validate the event's optional `learning` payload and return the record to
    append, or None if there's nothing to append (absent, or already recorded).

    Pure/read-only: raises on invalid payloads but never writes, so callers can
    validate learning data BEFORE mutating the roadmap -- a bad learning payload
    must not leave an already-applied, now-unrepeatable transition stuck with its
    event file undeleted (see process()'s ordering)."""
    learning = event.get("learning")
    if learning is None:
        return None
    if operation not in CLOSED_OPERATIONS:
        raise ValueError("learning may only accompany done or blocked events")

    if isinstance(learning, str):
        # conductor/t-097: a bare string `learning:` (task-events/README.md's
        # documented direct-push-to-main path never runs the PR-time
        # validate_task_events.py gate) recurred at least 5 times in one week
        # and each time silently red-flagged the shared "process" check for
        # every unrelated PR until a session stumbled onto it. Coerce it into
        # the required mapping instead of hard-failing the whole run, inferring
        # kind/stakes from the task's own roadmap entry when possible.
        #
        # kindrobots-unraid/t-006 (2026-08-09) surfaced the gap in the original
        # version of this coercion: an invalid roadmap `kind` (`infrastructure`,
        # not one of the three learning-ledger kinds) and an invalid task
        # `stakes` (`high`, not one of the three valid stakes) both fell through
        # to `None`, which is schema-valid to *write* (the required-fields check
        # below only checks key presence) but violates
        # `test_committed_ledger_schema_conformance`'s stricter "kind/stakes are
        # always one of the enum values" invariant, redding the Python test
        # suite on `main` for every subsequent PR. `backfill_learning.py`
        # already solved this exact problem for its own (roadmap-scan) path --
        # see its `test_invalid_kind_stakes_fall_back` -- by defaulting an
        # invalid kind to "software" and invalid stakes to "reversible" rather
        # than nulling them out. Mirror that convention here so both learning-
        # ledger writers agree on the same fallback and neither can produce a
        # schema-violating record again.
        lesson = learning.strip()
        if not lesson:
            raise ValueError("learning must be a non-empty string when supplied as a string")
        kind = roadmap.get("kind") if isinstance(roadmap, dict) else None
        if kind not in {"software", "content", "proposal"}:
            kind = "software"
        stakes = task.get("stakes") if isinstance(task, dict) else None
        if stakes not in {"reversible", "outward-facing", "irreversible"}:
            stakes = "reversible"
        learning = {"kind": kind, "stakes": stakes, "lesson": lesson}

    if not isinstance(learning, dict):
        raise ValueError("learning must be a mapping or a plain string lesson")

    required = {"kind", "stakes", "lesson"}
    missing = sorted(required - learning.keys())
    if missing:
        raise ValueError(f"learning is missing required fields: {', '.join(missing)}")

    path = ROOT / "LEARNING.yaml"
    ledger = load_yaml(path) if path.is_file() else {"records": []}
    records = ledger.get("records") or []
    if not isinstance(records, list):
        raise ValueError("LEARNING.yaml records must be a list")
    if any(
        isinstance(record, dict)
        and record.get("project") == project
        and record.get("task") == task_id
        and record.get("outcome") == operation
        for record in records
    ):
        return None

    return {
        "date": learning.get("date", dt.date.today().isoformat()),
        "project": project,
        "task": task_id,
        "kind": learning["kind"],
        "stakes": learning["stakes"],
        "passes": int(learning.get("passes", 0)),
        "outcome": operation,
        "failure_category": learning.get("failure_category"),
        "lesson": learning["lesson"],
    }


def write_learning_record(record: dict[str, Any]) -> None:
    """Append one record to LEARNING.yaml as new trailing text -- never touches
    the bytes of any existing record, so prior entries keep whatever quoting/
    escaping style they were originally written with."""
    path = ROOT / "LEARNING.yaml"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        ledger = yaml.safe_load(text) or {}
    else:
        text = "records: []\n"
        ledger = {"records": []}

    fragment = yaml.safe_dump(
        [record], sort_keys=False, default_flow_style=False, width=100, allow_unicode=True
    )

    if ledger.get("records"):
        if not text.endswith("\n"):
            text += "\n"
        path.write_text(text + fragment, encoding="utf-8")
    else:
        path.write_text("records:\n" + fragment, encoding="utf-8")


def process(path: Path, dry_run: bool) -> str:
    event = load_yaml(path)
    version = event.get("version", 1)
    if version != 1:
        raise ValueError(f"unsupported event version {version!r}")

    project = require_string(event, "project", PROJECT_RE)
    task_id = require_string(event, "task", TASK_RE)
    operation = require_string(event, "operation")
    if operation not in ALLOWED_OPERATIONS:
        raise ValueError(f"unsupported operation {operation!r}")

    roadmap_path = ROOT / "projects" / project / "roadmap.yaml"
    if not roadmap_path.is_file():
        raise ValueError(f"unknown project roadmap: {roadmap_path.relative_to(ROOT)}")

    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    roadmap = yaml.safe_load(roadmap_text)
    if not isinstance(roadmap, dict):
        raise ValueError(f"{roadmap_path}: expected a YAML mapping")
    task = find_task(roadmap, task_id)

    reason = stale_reason(task, event)
    if reason is not None:
        # The live task has moved on since this event was queued (conductor/t-067):
        # applying it now would silently revert whatever claimed/updated it more
        # recently. Drop the event rather than patch over newer state -- replaying
        # it again next cycle can never become non-stale, since roadmap timestamps
        # only move forward.
        if event.get("learning") or event.get("note"):
            # conductor/t-086: a stale event can carry a learning/note payload that
            # would otherwise vanish with no trace beyond this terse skip line (the
            # near-miss that motivated this task -- see TALKBACK.md 2026-07-26). Make
            # the loss impossible to miss instead of relying on a session noticing the
            # file in task-events/ by chance before this unlink() runs.
            print(
                f"WARNING {path.relative_to(ROOT)}: dropping STALE event for "
                f"{project}/{task_id} that carries a learning/note payload -- {reason}",
                file=sys.stderr,
            )
        if not dry_run:
            path.unlink()
        return f"{project}/{task_id}: STALE skip ({operation}) -- {reason}"

    # conductor/t-112: a `done` event can name a PR it claims is merged when
    # GitHub doesn't yet agree (brainstorm/t-010, 2026-08-10 -- applied 6 minutes
    # before the actual merge). Verify every referenced PR *before* computing any
    # transition; an unmerged reference redirects this event to `needs-human`
    # instead of `done` rather than closing the task on an unconfirmed claim. A
    # verification failure (network/API error -- "don't know") raises and leaves
    # the event queued for a later run, same as any other unresolvable event --
    # it must never be treated as either "merged" or "not merged".
    effective_operation = operation
    effective_event = event
    if operation == "done":
        unmerged = [
            f"{repo}#{number}"
            for repo, number in extract_pr_references(event)
            if not check_pr_merged(repo, number)
        ]
        if unmerged:
            mismatch = (
                "AUTO-PARKED by process_task_events.py (conductor/t-112): this event's "
                "operation was 'done' and named " + ", ".join(unmerged) + " as merged, "
                "but the GitHub API reports it is not merged yet. Re-queue a fresh "
                "'done' event once the PR actually merges."
            )
            original_note = event.get("note")
            note = (
                f"{original_note.strip()}\n\n{mismatch}"
                if isinstance(original_note, str) and original_note.strip()
                else mismatch
            )
            # `learning` describes an outcome that hasn't actually landed yet, so it
            # doesn't travel with the parked event; `compute_transition_ops` would
            # also reject a `needs-human` operation carrying an unrelated `learning`
            # payload as accompanying anything but done/blocked.
            effective_event = {key: value for key, value in event.items() if key != "learning"}
            effective_event["note"] = note
            effective_event["soft_gate"] = True
            effective_operation = "needs-human"

    # Compute everything (transition + learning validation) before writing anything,
    # so an invalid learning payload can't leave a half-applied, now-unrepeatable
    # transition behind with its event file stranded (atomicity requirement).
    try:
        ops = compute_transition_ops(task, effective_event, effective_operation)
    except TaskEventCollision as collision:
        # A claim (or session-tagged transition) that lost a race to another
        # session. Consume it with NO roadmap mutation -- the winning session's
        # claim stands untouched. Leaving it queued would poison every future
        # processor run for every unrelated PR, so this is a consumed result, not
        # an error (exit 0, event deleted), unlike a genuinely malformed event.
        if not dry_run:
            path.unlink()
        return f"{project}/{task_id}: {collision}"

    learning_record = prepare_learning(
        effective_event, project, task_id, effective_operation, task=task, roadmap=roadmap
    )
    ci_fields = continuous_improvement_fields(effective_event)

    if not dry_run:
        new_text = roadmap_text
        if ops:
            new_text = apply_task_field_ops(new_text, task_id, ops)
        if ci_fields is not None:
            lane, pr_ref = ci_fields
            run_value = effective_event.get("updated") or "now"
            new_text = bump_continuous_improvement_text(new_text, task_id, lane, pr_ref, run_value)
        if new_text != roadmap_text:
            yaml.safe_load(new_text)  # re-parse to confirm the edit produced valid YAML
            roadmap_path.write_text(new_text, encoding="utf-8")
        if learning_record is not None:
            write_learning_record(learning_record)
        path.unlink()

    if effective_operation != operation:
        return f"{project}/{task_id}: {effective_operation} (parked from {operation}: unmerged PR)"
    return f"{project}/{task_id}: {effective_operation}"


def run_resolver(dry_run: bool) -> None:
    command = [sys.executable, str(ROOT / "scripts" / "resolve_deps.py")]
    if dry_run:
        command.append("--dry-run")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files = event_files()
    if not files:
        print("No task events to process.")
        return 0

    had_error = False
    for path in files:
        try:
            print(process(path, args.dry_run))
        except Exception as error:
            had_error = True
            print(f"ERROR {path.relative_to(ROOT)}: {error}", file=sys.stderr)

    run_resolver(args.dry_run)
    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())