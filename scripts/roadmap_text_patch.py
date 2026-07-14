#!/usr/bin/env python3
"""
roadmap_text_patch.py — multi-field, multiline-aware surgical roadmap edits.

Builds on set_task_field.py's single-field text patcher (find_task_block /
field_value_end / normalize_scalar) to support the two things it deliberately
doesn't: field *removal* (task.pop equivalents like clearing `owner` on a
status change) and *multiline* values that must keep their paragraph breaks
instead of being flattened to one line (task `note` fields).

This is the primitive conductor/challenge-center t-020 asks for: apply a batch
of field changes to one task in a roadmap file by editing only the affected
lines, so a one-task status change produces a status-sized diff instead of a
whole-file yaml.safe_dump rewrite (which reformats every task, escapes
Unicode, and turns literal/folded blocks into quoted one-liners).

Used by process_task_events.py (task-event driven transitions) and
resolve_deps.py (dependency-unblock status writes) so both authoritative
roadmap writers share one safe text-patch path instead of each rolling (or
skipping) their own.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import set_task_field as stf  # noqa: E402


def set_multiline_task_field_text(text: str, task_id: str, field: str, value: str) -> str:
    """Set a field to a value containing embedded newlines as a literal block scalar.

    set_task_field_text() flattens embedded newlines to spaces by design (it's a
    single-line CLI scalar setter). Task notes are multi-paragraph prose where that
    would destroy the paragraph breaks, so this renders `field: |-` instead and
    indents each line of `value` under it verbatim -- no escaping, no Unicode
    conversion, so em dashes/arrows/etc. stay literal instead of becoming \\uXXXX.
    """
    if field not in stf.ALLOWED_FIELDS:
        allowed = ", ".join(sorted(stf.ALLOWED_FIELDS))
        raise stf.TaskFieldError(f"Field {field!r} is not allowed. Allowed fields: {allowed}")

    lines = text.splitlines(keepends=True)
    if not lines:
        raise stf.TaskFieldError("Roadmap is empty")

    start, end, field_indent = stf.find_task_block(lines, task_id)
    body_indent = " " * (field_indent + 2)
    body = "".join(f"{body_indent}{line}\n" if line else "\n" for line in value.split("\n"))
    replacement = f"{' ' * field_indent}{field}: |-\n{body}"

    found_field_idx = None
    for idx in range(start + 1, end):
        match = stf.KEY_RE.match(lines[idx])
        if not match or len(match.group("indent")) != field_indent:
            continue
        if match.group("key") == field:
            found_field_idx = idx
            break

    if found_field_idx is not None:
        value_end = stf.field_value_end(lines, found_field_idx, end, field_indent)
        lines[found_field_idx:value_end] = [replacement]
    else:
        insert_at = end
        while insert_at > start + 1 and not lines[insert_at - 1].strip():
            insert_at -= 1
        if not lines[insert_at - 1].endswith("\n"):
            lines[insert_at - 1] += "\n"
        lines.insert(insert_at, replacement)

    return "".join(lines)


def unset_task_field_text(text: str, task_id: str, field: str) -> str:
    """Remove a field (key + its whole value block) from one task. No-op if absent."""
    lines = text.splitlines(keepends=True)
    if not lines:
        return text

    start, end, field_indent = stf.find_task_block(lines, task_id)
    found_field_idx = None
    for idx in range(start + 1, end):
        match = stf.KEY_RE.match(lines[idx])
        if not match or len(match.group("indent")) != field_indent:
            continue
        if match.group("key") == field:
            found_field_idx = idx
            break

    if found_field_idx is None:
        return text

    value_end = stf.field_value_end(lines, found_field_idx, end, field_indent)
    del lines[found_field_idx:value_end]
    return "".join(lines)


def apply_task_field_ops(text: str, task_id: str, ops: list[tuple[str, str, str | None]]) -> str:
    """Apply a sequence of ("set"|"unset", field, value) ops to one task, in order.

    Each op re-locates the task block fresh against the current text, so ops can
    freely add/remove/replace fields without the caller tracking line-index drift.
    """
    for action, field, value in ops:
        if action == "set":
            if isinstance(value, str) and "\n" in value:
                text = set_multiline_task_field_text(text, task_id, field, value)
            else:
                text = stf.set_task_field_text(text, task_id, field, "" if value is None else str(value))
        elif action == "unset":
            text = unset_task_field_text(text, task_id, field)
        else:
            raise ValueError(f"unknown op action {action!r}")
    return text
