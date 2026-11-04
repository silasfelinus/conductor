#!/usr/bin/env python3
"""Per-page render settings the Coloring Book Studio may set on a color render.

Silas, 2026-11-04 PT: "I should be able to ... change the checkpoint or select a
coloring book lora." The studio writes these into a `color-art-events/` request;
the event processor validates them here and the studio consumer persists them on
the page's `color-art-jobs.yaml` entry, where build_entries already reads
`engine`, `lora` and `lora_strength` (and now `checkpoint`) per concept.

Model names are ComfyUI-relative filenames chosen from the Kind Robots Resource
catalog by an admin. They are checked for shape here, and resolved against the
Resource registry at submission (a missing row warns, as resolve_model does).
"""

from __future__ import annotations

import json
import re
from typing import Any

ENGINES = ("krea2", "flux2-klein", "flux", "sdxl-checkpoint")
FIELDS = ("engine", "checkpoint", "lora", "lora_strength")
MODEL_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.,()+'\-/]{0,200}\.(?:safetensors|ckpt|pt)$")


def _model_name(value: Any, field: str) -> str | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"render_settings.{field} must be a string")
    clean = value.strip().replace("\\", "/")
    if not MODEL_NAME.match(clean) or ".." in clean.split("/") or "//" in clean:
        raise ValueError(f"render_settings.{field} is not a safe model filename")
    return clean


def normalize(raw: Any) -> dict[str, Any]:
    """Return a complete settings mapping (None clears a field) or raise."""
    if isinstance(raw, str):
        raw = json.loads(raw)
    if not isinstance(raw, dict):
        raise ValueError("render_settings must be a mapping")
    unknown = sorted(set(raw) - set(FIELDS))
    if unknown:
        raise ValueError(f"unsupported render_settings fields: {', '.join(unknown)}")

    engine = str(raw.get("engine") or "krea2").strip().lower()
    if engine not in ENGINES:
        raise ValueError(f"render_settings.engine must be one of: {', '.join(ENGINES)}")
    checkpoint = _model_name(raw.get("checkpoint"), "checkpoint")
    if engine == "sdxl-checkpoint" and not checkpoint:
        raise ValueError("render_settings.checkpoint is required for sdxl-checkpoint")
    if engine != "sdxl-checkpoint":
        checkpoint = None
    lora = _model_name(raw.get("lora"), "lora")
    strength_raw = raw.get("lora_strength")
    strength: float | None = None
    if lora:
        try:
            strength = float(1.0 if strength_raw in (None, "") else strength_raw)
        except (TypeError, ValueError) as error:
            raise ValueError("render_settings.lora_strength must be a number") from error
        if not 0 <= strength <= 2:
            raise ValueError("render_settings.lora_strength must be between 0 and 2")
    return {"engine": engine, "checkpoint": checkpoint, "lora": lora, "lora_strength": strength}


def apply(source: dict[str, Any], settings: dict[str, Any]) -> bool:
    """Write settings onto one queue entry; return whether anything changed."""
    changed = False
    for field in FIELDS:
        value = settings.get(field)
        if value is None:
            if field in source:
                source.pop(field)
                changed = True
        elif source.get(field) != value:
            source[field] = value
            changed = True
    return changed
