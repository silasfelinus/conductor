"""Catch workflow YAML that parses locally but GitHub Actions rejects.

2026-08-01. Removing `ANTHROPIC_API_KEY` from a step in PR #1495 deleted the
only key under its `env:`, leaving:

    - name: ...
      env:
      run: |

PyYAML reads that as `env: None` and reports the file as valid, so local
validation passed. GitHub Actions requires `env` to be a mapping, rejected the
whole file, and refused to start the workflow at all -- which surfaces as a run
with **zero jobs**, titled with the file path instead of the workflow's `name`,
failing on every trigger. It failed roughly every 25 minutes for hours before
anyone connected it to the edit.

The generalisable trap: `yaml.safe_load()` succeeding is not the same as
Actions accepting the file. These assertions cover the null-valued-key shapes
that a careless line deletion produces.
"""

from __future__ import annotations

import pathlib
import unittest

import yaml

WORKFLOWS = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows"

# Keys whose value must be a non-empty mapping when the key is present at all.
# Deleting the last entry under one of these is the exact mistake above: the
# right fix is to remove the key too, not to leave it dangling.
MAPPING_KEYS = ("env", "with", "outputs", "defaults")


def workflow_files() -> list[pathlib.Path]:
    return sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))


class WorkflowSchemaSanity(unittest.TestCase):
    def test_there_are_workflows_to_check(self):
        self.assertTrue(workflow_files(), f"no workflows found under {WORKFLOWS}")

    def test_no_present_but_empty_mapping_keys(self):
        problems: list[str] = []

        def check(where: str, node: object) -> None:
            if not isinstance(node, dict):
                return
            for key in MAPPING_KEYS:
                if key in node and not isinstance(node[key], dict):
                    problems.append(
                        f"{where}: '{key}:' is present but is "
                        f"{node[key]!r}, not a mapping"
                    )

        for path in workflow_files():
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            check(path.name, doc)
            for job_name, job in (doc.get("jobs") or {}).items():
                check(f"{path.name}: job '{job_name}'", job)
                if not isinstance(job, dict):
                    continue
                for index, step in enumerate(job.get("steps") or []):
                    label = step.get("name", f"#{index}") if isinstance(step, dict) else f"#{index}"
                    check(f"{path.name}: job '{job_name}' step '{label}'", step)

        self.assertFalse(
            problems,
            "GitHub Actions rejects these files even though PyYAML parses them.\n"
            "A rejected workflow produces a run with zero jobs and fails on every "
            "trigger.\nRemove the dangling key entirely rather than leaving it "
            "empty:\n  - " + "\n  - ".join(problems),
        )

    def test_every_job_has_steps_and_every_step_does_something(self):
        problems: list[str] = []
        for path in workflow_files():
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            for job_name, job in (doc.get("jobs") or {}).items():
                if not isinstance(job, dict) or "uses" in job:
                    continue  # reusable-workflow call: no steps of its own
                steps = job.get("steps")
                if not steps:
                    problems.append(f"{path.name}: job '{job_name}' has no steps")
                    continue
                for index, step in enumerate(steps):
                    if not isinstance(step, dict):
                        problems.append(f"{path.name}: job '{job_name}' step #{index} is not a mapping")
                    elif "run" not in step and "uses" not in step:
                        label = step.get("name", f"#{index}")
                        problems.append(
                            f"{path.name}: job '{job_name}' step '{label}' has "
                            "neither 'run' nor 'uses'"
                        )
        self.assertFalse(problems, "Invalid job/step shapes:\n  - " + "\n  - ".join(problems))


if __name__ == "__main__":
    unittest.main()
