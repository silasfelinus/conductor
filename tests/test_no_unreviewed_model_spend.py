"""Guard: no scheduled workflow may quietly start spending API credits.

2026-08-01. Four Opus vision passes had accumulated around the art pipeline,
grading generated art against written rubrics. The most expensive of them ran
hourly with `limit=0` -- no cap at all -- and was 278 requests behind its own
queue by the time anyone looked. Nobody decided to spend that money; each pass
was added reasonably, and together they became the largest line on the bill.

Art quality is a human call (see the ArtJob trainer panel), so those passes are
gone. This test exists so they cannot quietly come back: any workflow that hands
a job `ANTHROPIC_API_KEY` must be listed here on purpose.

Adding a workflow to ALLOWED is a deliberate act, not a formality. Before you
do, be able to answer:

  1. Is this a judgement a human should be making instead?
  2. Is the call volume bounded? A `--limit` with no value, or a queue drain
     with no cap, is how the last one got away.
  3. Does it run on a schedule? Scheduled spend compounds silently; manual
     spend does not.
"""

from __future__ import annotations

import pathlib
import unittest

WORKFLOWS = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows"

# Workflow filename -> why it is allowed to spend.
ALLOWED = {
    "hourly-conductor.yml": (
        "Haiku 4.5 status summary, max_tokens=400, one call per run "
        "(~$0.01/day). Falls back to rule-based output when the key is absent."
    ),
}


class NoUnreviewedModelSpend(unittest.TestCase):
    def test_only_allowlisted_workflows_receive_an_api_key(self):
        granted = {
            path.name
            for path in sorted(WORKFLOWS.glob("*.yml"))
            if "ANTHROPIC_API_KEY" in path.read_text(encoding="utf-8")
        }

        unexpected = granted - set(ALLOWED)
        self.assertFalse(
            unexpected,
            "These workflows grant ANTHROPIC_API_KEY but are not in the "
            f"allowlist: {sorted(unexpected)}.\n"
            "If the spend is intended, add the workflow to ALLOWED in this file "
            "with a one-line justification covering call volume and cadence. "
            "Read this module's docstring first -- it explains what went wrong "
            "the last time this was left unguarded.",
        )

        stale = set(ALLOWED) - granted
        self.assertFalse(
            stale,
            f"These workflows are allowlisted but no longer use the key: "
            f"{sorted(stale)}. Drop them from ALLOWED so the list keeps meaning "
            "something.",
        )

    def test_art_pipeline_has_no_vision_gate(self):
        """The removed curator modules must not reappear under any name."""

        scripts = pathlib.Path(__file__).resolve().parents[1] / "scripts"
        for gone in ("curate_art.py", "curate_art_jobs.py", "semantic_art_quality.py"):
            self.assertFalse(
                (scripts / gone).exists(),
                f"scripts/{gone} is back. Art quality is judged by a human in "
                "the ArtJob trainer panel, not by a model.",
            )


if __name__ == "__main__":
    unittest.main()
