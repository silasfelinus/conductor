"""Guard: no scheduled workflow may quietly start spending API credits.

2026-08-01. Four Opus vision passes had accumulated around the art pipeline,
grading generated art against written rubrics. The most expensive of them ran
hourly with `limit=0` -- no cap at all -- and was 278 requests behind its own
queue by the time anyone looked. Nobody decided to spend that money; each pass
was added reasonably, and together they became the largest line on the bill.

Art quality is a human call (see the ArtJob trainer panel), so those passes are
gone. This test exists so they cannot quietly come back: any workflow that hands
a job `ANTHROPIC_API_KEY` must be listed here on purpose.

2026-09-04. Silas: "They are literally running as part of my normal Claude Max
account. I'm not spending $100 a month so it can then trigger the API." The
hourly Conductor Agent Routine and the daily-digest author step were doing the
same work twice -- once on the Max plan, once on API credits. So a second rule
now applies on top of the allowlist: any workflow that runs on a `schedule:`
may hand out the key ONLY behind an explicit `workflow_dispatch` input named
`spend_api_credits`, so the scheduled run never spends and a human has to ask
for it by name. The secret itself stays -- the option is useful -- it just
never fires on its own.

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
import re
import unittest

WORKFLOWS = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows"

# Workflow filename -> why it is allowed to spend.
ALLOWED = {
    "hourly-conductor.yml": (
        "Haiku 4.5 status summary, max_tokens=400, one call per run. OPT-IN "
        "only (spend_api_credits on workflow_dispatch); every scheduled run "
        "takes the rule-based fallback because the hourly Conductor Agent "
        "Routine already does this assessment on the Max plan."
    ),
    "daily-digest.yml": (
        "Two model-authored steps, both OPT-IN only (spend_api_credits on "
        "workflow_dispatch): the Daily Dream proposal "
        "(scripts/author_dream_proposal.py, Sonnet 5, max_tokens=4000, "
        "MAX_ATTEMPTS=2, skips when the docket is at its buffer) and the "
        "container-log review (scripts/author_container_log_review.py, Sonnet "
        "5, max_tokens=4000, one call). On the schedule neither gets the key: "
        "the docket is topped up by agent sessions (CLAUDE.md startup step 7) "
        "and the digest falls back to its mechanical log banner. Silas "
        "2026-08-09 wanted proposals written the turn the digest goes out; "
        "2026-09-04 he wants that done by the Max-plan sessions, not the API."
    ),
    "daily-dream-prose-repair.yml": (
        "One-shot human-requested catalog prose repair, triggered only by an explicit "
        "request file on main and never by a schedule. It edits model-authored Daily "
        "Dream card copy rather than replacing human judgement. Calls are bounded to "
        "at most two attempts per built bundle that actually fails the prose contract; "
        "the current catalog is finite and the request is consumed after one successful run."
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

    def test_scheduled_workflows_only_spend_on_explicit_request(self):
        """A `schedule:`-triggered workflow may reference the key only on a
        line gated by the `spend_api_credits` dispatch input, so the cron
        never spends and a human has to opt in by name."""

        for path in sorted(WORKFLOWS.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            if "secrets.ANTHROPIC_API_KEY" not in text:
                continue
            if not re.search(r"^\s+schedule:\s*$", text, re.MULTILINE):
                continue  # manual/push-only workflows are a deliberate act already
            for lineno, line in enumerate(text.splitlines(), start=1):
                if "secrets.ANTHROPIC_API_KEY" not in line:
                    continue
                self.assertIn(
                    "inputs.spend_api_credits == true",
                    line,
                    f"{path.name}:{lineno} hands out ANTHROPIC_API_KEY on a "
                    "scheduled workflow without the spend_api_credits gate. "
                    "Use: ${{ inputs.spend_api_credits == true && "
                    "secrets.ANTHROPIC_API_KEY || '' }} and declare the "
                    "boolean workflow_dispatch input (default false).",
                )
            self.assertRegex(
                text,
                r"spend_api_credits:\s*\n(?:\s+\S.*\n)*?\s+type:\s*boolean",
                f"{path.name} must declare spend_api_credits as a boolean "
                "workflow_dispatch input (default false).",
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
