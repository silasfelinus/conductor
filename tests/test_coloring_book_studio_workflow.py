import unittest
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "process-color-art-events.yml"
).read_text(encoding="utf-8")


class ColoringBookStudioWorkflowTests(unittest.TestCase):
    def test_preflight_needs_no_model_credential(self) -> None:
        """Art review is a human job -- this workflow must not want an API key."""
        self.assertIn("id: queue_preflight", WORKFLOW)
        self.assertNotIn("ANTHROPIC_API_KEY", WORKFLOW)
        self.assertIn(
            "if: ${{ steps.queue_preflight.outputs.process == 'true' }}",
            WORKFLOW,
        )

    def test_stale_queue_credential_errors_do_not_block_a_restored_key(self) -> None:
        self.assertNotIn("--require-no-render-gate-error", WORKFLOW)
        self.assertIn("python scripts/coloring_queue_status.py", WORKFLOW)
        self.assertIn('echo "process=true" >> "$GITHUB_OUTPUT"', WORKFLOW)

    def test_non_credential_preflight_errors_still_fail(self) -> None:
        self.assertIn('if [ "$status" -ne 0 ]; then', WORKFLOW)
        self.assertIn('exit "$status"', WORKFLOW)

    def test_skipped_submission_does_not_trigger_retry_failure(self) -> None:
        self.assertIn(
            "if: ${{ steps.queue_preflight.outputs.process == 'true' && steps.consume.outcome != 'success' }}",
            WORKFLOW,
        )


if __name__ == "__main__":
    unittest.main()
