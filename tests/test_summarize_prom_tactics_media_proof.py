"""Read-only image delivery reporting must not equate source receipts with URLs."""

import json

import pytest
import yaml

from scripts.summarize_prom_tactics_media_proof import (
    apply_log,
    checkpointed_receipts,
    formatted_report,
    main,
    markdown_report,
    summarize,
)


def sample_ledger(tmp_path):
    path = tmp_path / "private-ledger.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "is_public": False,
                "subjects": [
                    {
                        "key": "prom-identities-magic-discipline-hero",
                        "lane": "krea2",
                        "jobs": {"krea2": 50768},
                        "art": {"krea2": {"status": "DONE", "art_image_id": 258175}},
                        "media_proof": {
                            "krea2": {
                                "status": "VERIFIED",
                                "art_job_id": 50768,
                                "art_image_id": 258175,
                                "downloaded_bytes": 12000,
                            }
                        },
                    },
                    {
                        "key": "prom-identities-magic-discipline-villain",
                        "lane": "krea2",
                        "jobs": {"krea2": 50769},
                        "art": {"krea2": {"status": "DONE", "art_image_id": 258176}},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_checkpointed_source_never_proves_a_live_game_url(tmp_path):
    rows = checkpointed_receipts([sample_ledger(tmp_path)])
    report = summarize(rows)
    assert report["counts"]["source"] == {"verified": 1, "failed": 0, "unknown": 1}
    assert report["counts"]["runtime"]["unknown"] == 2
    assert report["counts"]["private"]["unknown"] == 2


def test_failed_game_image_is_reported_by_exact_id_without_leaking_url(tmp_path):
    rows = checkpointed_receipts([sample_ledger(tmp_path)])
    apply_log(
        rows,
        """2026-11-23T00:52Z GAME_PATH_FAILED key=prom-identities-magic-discipline-hero image=258175 reason=HTTPError
2026-11-23T00:52Z GAME_PATH_OK key=prom-identities-magic-discipline-villain job=50769 image=258176 size=1344x768 anonymous=PRIVATE_DENIED
""",
    )
    report = summarize(rows)
    assert report["counts"]["runtime"] == {"verified": 1, "failed": 1, "unknown": 0}
    assert rows[258175]["source"] == "verified"
    assert rows[258175]["private"] == "unknown"
    assert rows[258176]["private"] == "verified"
    output = formatted_report(report)
    assert "image=258175" in output and "reason=HTTPError" in output
    assert "image=258176" not in output
    assert "https://" not in output
    assert "258175" in markdown_report(report)


def test_unknown_id_cannot_create_false_verification(tmp_path):
    rows = checkpointed_receipts([sample_ledger(tmp_path)])
    apply_log(
        rows,
        "GAME_PATH_OK key=prom-identities-magic-discipline-hero job=123 image=258175 anonymous=PRIVATE_DENIED\n"
        "GAME_PATH_OK key=prom-identities-magic-discipline-hero job=50768 image=333333 anonymous=PRIVATE_DENIED\n"
        "PRIVATE_POLICY_VERIFIED=3 ledger=private-ledger.yaml\n",
    )
    assert rows[258175]["runtime"] == "unknown"
    assert rows[258175]["private"] == "unknown"


def test_source_failure_and_incomplete_privacy_group_fail_closed(tmp_path):
    rows = checkpointed_receipts([sample_ledger(tmp_path)])
    apply_log(
        rows,
        "FAILED key=prom-identities-magic-discipline-hero image=258175 reason=RuntimeError\n"
        "GAME_PATH_OK key=prom-identities-magic-discipline-villain job=50769 image=258176 anonymous=PRIVATE_DENIED\n"
        "PRIVATE_POLICY_FAILED=private-ledger.yaml\n",
    )
    assert rows[258175]["source"] == "failed"
    assert rows[258175]["runtime"] == "unknown"
    assert rows[258176]["runtime"] == "verified"
    assert rows[258175]["private"] == "unknown"
    report = summarize(rows)
    assert report["private_group_failures"] == ["private-ledger.yaml"]
    assert "PRIVATE_POLICY_GROUP_FAILED ledger=private-ledger.yaml" in formatted_report(report)


def test_read_only_cli_joins_logs_and_writes_step_summary(tmp_path, capsys):
    ledger = sample_ledger(tmp_path)
    actions_log = tmp_path / "proof.log"
    actions_log.write_text(
        "GAME_PATH_FAILED key=prom-identities-magic-discipline-hero image=258175 reason=HTTPError\n"
    )
    summary = tmp_path / "summary.md"
    json_path = tmp_path / "results.json"
    before = ledger.read_bytes()
    assert main(
        [
            "--ledger", str(ledger),
            "--log", str(actions_log),
            "--summary", str(summary),
            "--json", str(json_path),
        ]
    ) == 0
    assert ledger.read_bytes() == before
    assert "RUNTIME_FAILED=1" in capsys.readouterr().out
    assert "258175" in summary.read_text()
    assert json.loads(json_path.read_text())["counts"]["runtime"]["failed"] == 1


def test_duplicate_art_image_id_is_rejected(tmp_path):
    original = sample_ledger(tmp_path)
    replacement = tmp_path / "duplicate.yaml"
    replacement.write_bytes(original.read_bytes())
    with pytest.raises(ValueError, match="reused"):
        checkpointed_receipts([original, replacement])
