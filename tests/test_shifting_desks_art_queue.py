"""Round ledgers must preserve the prompts and render settings actually submitted."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from repair_negation_art_prompts import violations  # noqa: E402


def test_shifting_desks_rounds_match_submission_queue():
    requests = yaml.safe_load((ROOT / "projects/art-prompts.yaml").read_text())["requests"]
    for ledger in sorted((ROOT / "projects/shifting-desks/art").glob("ROUND-*.yaml")):
        for subject in yaml.safe_load(ledger.read_text())["subjects"]:
            matches = [row for row in requests if row.get("id") == subject["request_id"]]
            assert len(matches) == 1, (ledger.name, subject["request_id"], len(matches))
            request = matches[0]
            assert " ".join(subject["prompt"].split()) == " ".join(request["prompt"].split()), subject["request_id"]
            for field in ("engine", "size", "seed"):
                assert subject[field] == request[field], (subject["request_id"], field)
            assert not violations(subject["prompt"]), (subject["request_id"], violations(subject["prompt"]))
