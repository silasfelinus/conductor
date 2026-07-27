#!/usr/bin/env python3
"""Compare Kind Robots Resource paths with ComfyUI's authoritative LoRA list."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def normalize(value: str) -> str:
    return value.strip().replace("\\", "/").strip("/").casefold()


def basename(value: str) -> str:
    return normalize(value).rsplit("/", 1)[-1]


def extract_comfy_loras(payload: dict[str, Any]) -> list[str]:
    node = payload.get("LoraLoaderModelOnly")
    if not isinstance(node, dict):
        raise ValueError("object_info is missing LoraLoaderModelOnly")

    required = node.get("input", {}).get("required", {})
    lora_name = required.get("lora_name") if isinstance(required, dict) else None
    values = lora_name[0] if isinstance(lora_name, list) and lora_name else None
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise ValueError("LoraLoaderModelOnly.input.required.lora_name has an unexpected shape")

    return values


def extract_resource_paths(payload: Any) -> list[str]:
    rows = payload.get("data", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("resources JSON must be an array or an object with a data array")

    paths: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        local_path = row.get("localPath")
        if isinstance(local_path, str) and local_path.strip():
            paths.append(local_path)
    return paths


def compare(resource_paths: list[str], comfy_paths: list[str]) -> dict[str, Any]:
    exact = {normalize(path): path for path in comfy_paths}
    by_name: dict[str, list[str]] = {}
    for path in comfy_paths:
        by_name.setdefault(basename(path), []).append(path)

    matches: list[dict[str, str]] = []
    ambiguous: list[dict[str, Any]] = []
    missing: list[str] = []

    for resource_path in resource_paths:
        normalized = normalize(resource_path)
        if normalized in exact:
            matches.append(
                {
                    "resourcePath": resource_path,
                    "comfyPath": exact[normalized],
                    "match": "normalized-exact",
                }
            )
            continue

        candidates = by_name.get(basename(resource_path), [])
        if len(candidates) == 1:
            matches.append(
                {
                    "resourcePath": resource_path,
                    "comfyPath": candidates[0],
                    "match": "unique-basename",
                }
            )
        elif len(candidates) > 1:
            ambiguous.append(
                {"resourcePath": resource_path, "candidates": sorted(candidates)}
            )
        else:
            missing.append(resource_path)

    return {
        "summary": {
            "resources": len(resource_paths),
            "comfyLoras": len(comfy_paths),
            "matched": len(matches),
            "ambiguous": len(ambiguous),
            "missing": len(missing),
        },
        "matches": matches,
        "ambiguous": ambiguous,
        "missing": missing,
    }


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--object-info", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = compare(
        extract_resource_paths(load_json(args.resources)),
        extract_comfy_loras(load_json(args.object_info)),
    )
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
