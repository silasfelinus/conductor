import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "promote_stale_task_event_claims.py"
SPEC = importlib.util.spec_from_file_location("promote_stale_task_event_claims", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class PromoteStaleTaskEventClaimsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "task-events").mkdir()
        (self.root / "projects" / "demo").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_roadmap(self, claimed_at: str):
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(
                {
                    "project": "demo",
                    "tasks": [
                        {
                            "id": "t-001",
                            "status": "claimed",
                            "owner": "worker",
                            "claimed_by": "old-session",
                            "claimed_at": claimed_at,
                        }
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def write_claim(self):
        path = self.root / "task-events" / "claim.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "version": 1,
                    "project": "demo",
                    "task": "t-001",
                    "operation": "claim",
                    "owner": "worker",
                    "session": "new-session",
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def test_stale_claim_is_promoted_to_force(self):
        self.write_roadmap("2000-01-01T00:00:00Z")
        event = self.write_claim()

        changed = MODULE.promote_stale_claims(self.root)

        self.assertEqual(changed, [event])
        self.assertTrue(yaml.safe_load(event.read_text(encoding="utf-8"))["force"])

    def test_fresh_claim_keeps_collision_protection(self):
        from datetime import datetime, timezone

        self.write_roadmap(datetime.now(timezone.utc).isoformat())
        event = self.write_claim()
        before = event.read_text(encoding="utf-8")

        changed = MODULE.promote_stale_claims(self.root)

        self.assertEqual(changed, [])
        self.assertEqual(event.read_text(encoding="utf-8"), before)
        self.assertNotIn("force", yaml.safe_load(before))


if __name__ == "__main__":
    unittest.main()
