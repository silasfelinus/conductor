"""Proof helper must checkpoint partial receipts and preserve private media policy."""

from types import SimpleNamespace

import pytest
import yaml

from scripts.prove_private_media_ledgers import (
    parse_ledger,
    prove_ledger,
    verify_private_metadata,
)


def ledger(tmp_path):
    path = tmp_path / "private.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "is_public": False,
                "subjects": [
                    {
                        "key": "canonical",
                        "asset": "game/characters/canonical",
                        "size": "768x768",
                        "jobs": {"krea2": 123},
                        "art": {
                            "krea2": {
                                "status": "DONE",
                                "art_image_id": 456,
                            }
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_parse_requires_real_ledger_and_exact_positive_count(tmp_path):
    path = ledger(tmp_path)
    assert parse_ledger(f"{path}:1") == (path, 1)
    import argparse

    for value in (f"{path}:0", f"{path}:bad", "missing.yaml:1"):
        with pytest.raises(argparse.ArgumentTypeError):
            parse_ledger(value)


def test_source_runtime_checkpoint_and_private_policy_all_run(tmp_path):
    path = ledger(tmp_path)
    called = []

    def runner(argv, *, check):
        called.append(argv)
        return SimpleNamespace(returncode=0)

    assert prove_ledger(
        path,
        1,
        write_evidence=True,
        require_private=True,
        checkpoint_message="checkpoint verified art [skip ci]",
        runner=runner,
        request=lambda image_id: (200, {"data": {"isPublic": False}}),
    )
    assert len(called) == 3
    assert called[0][1] == "scripts/verify_prom_tactics_media.py"
    assert called[0][-1] == "--write-evidence"
    assert called[1][1] == "scripts/verify_tactics_runtime_media.py"
    assert called[2] == [
        "bash",
        "scripts/checkpoint_art_state.sh",
        "checkpoint verified art [skip ci]",
    ]
    assert called[1][-2:] == ["--require-count", "1"]


def test_failed_source_still_checkpoints_and_never_marks_private(tmp_path):
    path = ledger(tmp_path)
    called = []

    def runner(argv, *, check):
        called.append(argv)
        return SimpleNamespace(returncode=1 if len(called) == 1 else 0)

    assert not prove_ledger(
        path,
        1,
        write_evidence=True,
        require_private=True,
        checkpoint_message="checkpoint",
        runner=runner,
        request=lambda _: (_ for _ in ()).throw(AssertionError("unexpected API")),
    )
    assert len(called) == 2
    assert called[0][1] == "scripts/verify_prom_tactics_media.py"
    assert called[1][1] == "scripts/checkpoint_art_state.sh"


def test_metadata_rejects_public_image_and_wrong_count(tmp_path):
    path = ledger(tmp_path)
    assert (
        verify_private_metadata(
            path, 1, request=lambda image_id: (200, {"data": {"isPublic": False}})
        )
        == 1
    )
    with pytest.raises(PermissionError):
        verify_private_metadata(
            path, 1, request=lambda image_id: (200, {"data": {"isPublic": True}})
        )
    with pytest.raises(ValueError, match="count"):
        verify_private_metadata(path, 2, request=lambda _: None)
    body = yaml.safe_load(path.read_text())
    body["is_public"] = True
    path.write_text(yaml.safe_dump(body))
    with pytest.raises(ValueError, match="visibility"):
        verify_private_metadata(path, 1, request=lambda _: None)


def test_runtime_failure_never_counts_as_verified_or_skips_checkpoint(tmp_path):
    path = ledger(tmp_path)
    calls = []

    def runner(argv, *, check):
        calls.append(argv)
        return SimpleNamespace(returncode=1 if len(calls) == 2 else 0)

    assert not prove_ledger(
        path,
        1,
        write_evidence=True,
        require_private=True,
        checkpoint_message="checkpoint",
        runner=runner,
        request=lambda _: (_ for _ in ()).throw(AssertionError("unexpected API")),
    )
    assert len(calls) == 3
    assert calls[2][1] == "scripts/checkpoint_art_state.sh"



def test_private_metadata_retries_429_and_503_then_verifies(tmp_path):
    path = ledger(tmp_path)
    statuses = [429, 503, 200]
    calls = []
    pauses = []

    def request(image_id):
        assert image_id == 456
        calls.append(image_id)
        status = statuses.pop(0)
        return status, {"data": {"isPublic": False}}

    assert verify_private_metadata(
        path, 1, request=request, pause=pauses.append, pace_seconds=0
    ) == 1
    assert calls == [456, 456, 456]
    assert pauses == [2, 4]


def test_private_metadata_never_retries_revoked_visibility_or_missing_id(tmp_path):
    path = ledger(tmp_path)
    for status, public in [(403, False), (404, False), (200, True)]:
        calls = []
        pauses = []

        def request(image_id):
            calls.append(image_id)
            return status, {"data": {"isPublic": public}}

        with pytest.raises(PermissionError):
            verify_private_metadata(
                path, 1, request=request, pause=pauses.append
            )
        assert calls == [456]
        assert pauses == []


def test_private_metadata_exhausts_retry_budget_and_fails_closed(tmp_path):
    path = ledger(tmp_path)
    calls = []
    pauses = []

    def request(image_id):
        calls.append(image_id)
        return 503, {}

    with pytest.raises(PermissionError, match="Private ArtImage metadata"):
        verify_private_metadata(
            path, 1, request=request, pause=pauses.append
        )
    assert calls == [456] * 4
    assert pauses == [2, 4, 8]


def test_private_metadata_paces_between_images_not_after_last(tmp_path):
    path = ledger(tmp_path)
    document = yaml.safe_load(path.read_text())
    other = dict(document["subjects"][0])
    other["key"] = "second-canonical"
    other["jobs"] = {"krea2": 124}
    other["art"] = {"krea2": {"status": "DONE", "art_image_id": 457}}
    document["subjects"].append(other)
    path.write_text(yaml.safe_dump(document))
    calls = []
    pauses = []

    def request(image_id):
        calls.append(image_id)
        return 200, {"data": {"isPublic": False}}

    assert verify_private_metadata(
        path, 2, request=request, pause=pauses.append, pace_seconds=0.125
    ) == 2
    assert calls == [456, 457]
    assert pauses == [0.125]


def test_private_metadata_reports_exact_failed_image_and_continues(tmp_path, capsys):
    path = ledger(tmp_path)
    document = yaml.safe_load(path.read_text())
    second = dict(document["subjects"][0])
    second["key"] = "distinct-crew"
    second["jobs"] = {"krea2": 124}
    second["art"] = {"krea2": {"status": "DONE", "art_image_id": 457}}
    document["subjects"].append(second)
    path.write_text(yaml.safe_dump(document))
    calls = []

    def request(image_id):
        calls.append(image_id)
        return 200, {"data": {"isPublic": image_id == 456}}

    with pytest.raises(PermissionError, match="Private ArtImage metadata"):
        verify_private_metadata(path, 2, request=request, pace_seconds=0)
    output = capsys.readouterr().out
    assert calls == [456, 457]
    assert (
        "PRIVATE_POLICY_IMAGE_FAILED ledger=private.yaml "
        "image=456 reason=ReportedPublic"
    ) in output
    assert "PRIVATE_POLICY_IMAGE_OK ledger=private.yaml image=457" in output
    assert (
        "PRIVATE_POLICY_IMAGES_CHECKED=2 ledger=private.yaml "
        "verified=1 failed=1"
    ) in output
    assert "http" not in output.lower()
    assert "Authorization" not in output


def test_missing_visibility_and_denied_metadata_have_distinct_failures(
    tmp_path, capsys
):
    path = ledger(tmp_path)
    for status, payload, expected_reason in [
        (200, {"data": {}}, "UnknownVisibility"),
        (404, {}, "MetadataUnavailable"),
    ]:
        with pytest.raises(PermissionError):
            verify_private_metadata(
                path, 1, request=lambda _: (status, payload), pace_seconds=0
            )
        output = capsys.readouterr().out
        assert "image=456 reason=" + expected_reason in output
