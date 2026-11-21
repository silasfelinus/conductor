import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import deliver_emperor_art_to_media as delivery


def record(asset, image=42, verdict="", ledger="ROUND.yaml"):
    return {
        "asset": asset, "artImageId": image,
        "verdict": verdict, "ledger": ledger, "key": "test",
    }


def test_all_eight_original_ending_plates_are_rendered_in_canonical_ledger():
    rows = delivery.load_ledger_entries()
    endings = [r for r in rows if r["ledger"] == "ENDINGS-ROUND-1.yaml"]
    assert len(endings) == 8
    assert {row["artImageId"] for row in endings} == set(range(270430, 270438))
    assert not any(row["verdict"].startswith("keep") for row in endings)
    plan = delivery.build_plan(endings, only=r"^endings/")
    assert plan["summary"]["unreviewed"] == 8
    assert plan["summary"]["keepers"] == 0


def test_keeper_wins_over_rejected_and_unreviewed_redos():
    rows = [
        record("quests/example", 1, "reject: off model"),
        record("quests/example", 2),
        record("quests/example", 3, "keep: reviewed"),
    ]
    plan = delivery.build_plan(rows)
    assert plan["keepers"] == [{
        "asset": "quests/example",
        "artImageId": 3,
        "ledger": "ROUND.yaml",
    }]
    assert not plan["unreviewed"]
    assert not plan["collisions"]


def test_two_competing_keepers_are_not_auto_selected():
    rows = [
        record("quests/example", 2, "keep: good"),
        record("quests/example", 3, "keep: also good"),
        record("quests/other", 4, "keep: accepted"),
    ]
    plan = delivery.build_plan(rows)
    assert plan["summary"]["collisions"] == 1
    assert plan["collisions"][0]["renderIds"] == [2, 3]
    assert plan["keepers"] == [{
        "asset": "quests/other", "artImageId": 4, "ledger": "ROUND.yaml"
    }]


def test_actual_round_roots_and_dynamic_playbook_exclusion():
    plan = delivery.build_plan([
        record("chance-events/dust-weather-1/notice", 201, "keep: reviewed"),
        record("talks/kiyo/kiyo-close-friendship", 202, "keep: reviewed"),
        record("followers/F001/illustrated/happy", 203, "keep: reviewed"),
        record("npcs/young-komodo/neutral", 204, "keep: reviewed"),
        record("playbook/emperor-of-dust/aud:d01-toll", 205, "keep: reviewed"),
    ])
    assert plan["summary"]["keepers"] == 4
    assert plan["summary"]["unsupported"] == 1
    assert plan["unsupported"][0]["artImageId"] == 205
    assert delivery.expected_media_url("followers/F001/illustrated/happy") == (
        "/images/emperor-of-dust/cast/followers/F001/illustrated/happy.webp"
    )
    assert delivery.expected_media_url("npcs/young-komodo/neutral") == (
        "/images/emperor-of-dust/cast/npcs/young-komodo/neutral.webp"
    )


def test_all_rejected_or_unfinished_inputs_never_export():
    plan = delivery.build_plan([
        record("quests/no", 99, "reject: human"),
        record("quests/pending", None),
        record("quests/yes", 100),
    ])
    assert plan["summary"]["rejected"] == 1
    assert plan["summary"]["unreviewed"] == 1
    assert plan["summary"]["keepers"] == 0


def test_live_preview_includes_unreviewed_but_never_marks_curated(monkeypatch):
    monkeypatch.setattr(delivery.core, "KR_API_TOKEN", "test-placeholder")
    calls = []
    def request(method, url, payload, timeout):
        calls.append(payload)
        return 200, {
            "success": True,
            "data": {"results": [{
                "asset": x["asset"],
                "artImageId": x["artImageId"],
                "url": f"/images/emperor-of-dust/{x['asset']}.webp",
                "status": "would-write",
            } for x in payload["targets"]]},
        }
    plan = delivery.build_plan([
        record("endings/iron-peace", 270432),
        record("quests/approved", 21, "keep: checked"),
    ])
    report = delivery.reconcile(plan, http_json=request, base_url="https://example.test")
    assert report["summary"] == {"would-write": 2}
    assert all(call["curated"] is False for call in calls)
    assert all(call["write"] is False for call in calls)


def test_delivery_batches_keepers_only_and_checks_receipts(monkeypatch):
    monkeypatch.setattr(delivery.core, "KR_API_TOKEN", "test-placeholder")
    calls = []
    def request(method, url, payload, timeout):
        calls.append(payload)
        return 200, {
            "success": True,
            "data": {"results": [{
                "asset": x["asset"],
                "artImageId": x["artImageId"],
                "url": f"/images/emperor-of-dust/{x['asset']}.webp",
                "status": "written",
                "sha256": "a" * 64,
            } for x in payload["targets"]]},
        }
    plan = delivery.build_plan(
        [record(f"quests/accepted-{i}", i + 1, "keep: reviewed")
         for i in range(26)]
        + [record("quests/unreviewed", 100)]
    )
    verified = []
    def verify(url, sha256, base_url):
        verified.append((url, sha256))
        return True
    report = delivery.reconcile(
        plan, write=True, http_json=request, verify_media=verify,
    )
    assert report["summary"] == {"written": 26}
    assert len(verified) == 26
    assert len(calls) == 2
    assert [len(call["targets"]) for call in calls] == [24, 2]
    assert all(call["write"] is True and call["curated"] is True for call in calls)
    assert all(
        x["asset"] != "quests/unreviewed"
        for call in calls for x in call["targets"]
    )


def test_delivery_rejects_misbound_receipts(monkeypatch):
    monkeypatch.setattr(delivery.core, "KR_API_TOKEN", "test-placeholder")
    plan = delivery.build_plan([record("quests/accepted", 11, "keep")])
    def bad(method, url, payload, timeout):
        return 200, {"success": True, "data": {"results": [{
            "asset": "quests/accepted",
            "artImageId": 12,
            "url": "/images/emperor-of-dust/quests/accepted.webp",
            "status": "written",
        }]}}
    with pytest.raises(RuntimeError, match="provenance"):
        delivery.reconcile(plan, write=True, http_json=bad)


def test_live_requires_token(monkeypatch):
    monkeypatch.setattr(delivery.core, "KR_API_TOKEN", "")
    with pytest.raises(RuntimeError, match="KR_API_TOKEN absent"):
        delivery.reconcile(delivery.build_plan([]))


def test_cli_offline_plan_and_write_guard(tmp_path, capsys):
    path = tmp_path / "private-ledgers"
    path.mkdir()
    (path / "MINI.yaml").write_text(
        "subjects:\n"
        "- key: original\n"
        "  asset: endings/open-roads\n"
        "  jobs: {arthemy-house: 68221}\n"
        "  art: {arthemy-house: {status: DONE, art_image_id: 270431}}\n"
    )
    assert delivery.main(["--plan", "--ledger-dir", str(path)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["plan"]["summary"]["unreviewed"] == 1
    with pytest.raises(SystemExit):
        delivery.main(["--write", "--ledger-dir", str(path)])


def test_http_verification_checks_actual_served_webp_sha():
    payload = b"RIFF" + b"\\x14\\x00\\x00\\x00" + b"WEBP" + b"VP8 " + b"pixel-data"
    sha = hashlib.sha256(payload).hexdigest()
    class Response:
        status = 200
        headers = {"Content-Type": "image/webp"}
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return payload
    class FakeOpener:
        def __call__(self, request, timeout):
            assert request.full_url.endswith("/images/emperor-of-dust/endings/open-roads.webp")
            return Response()
    args = (
        "/images/emperor-of-dust/endings/open-roads.webp", sha,
    )
    assert delivery.verify_delivered_media(
        *args, base_url="https://example.test", opener=FakeOpener(),
    )
    assert not delivery.verify_delivered_media(
        args[0], "0" * 64, base_url="https://example.test", opener=FakeOpener(),
    )
    assert not delivery.verify_delivered_media(
        "/other/secret.webp", sha, opener=FakeOpener(),
    )


def test_written_receipt_never_counts_as_delivered_if_http_bytes_fail(monkeypatch):
    monkeypatch.setattr(delivery.core, "KR_API_TOKEN", "test-placeholder")
    plan = delivery.build_plan([record("quests/accepted", 11, "keep")])
    def claimed(method, url, payload, timeout):
        return 200, {"success": True, "data": {"results": [{
            "asset": "quests/accepted",
            "artImageId": 11,
            "url": "/images/emperor-of-dust/quests/accepted.webp",
            "sha256": "f" * 64,
            "status": "written",
        }]}}
    receipt = delivery.reconcile(
        plan, write=True, http_json=claimed,
        verify_media=lambda url, sha, base_url: False,
    )
    assert receipt["summary"] == {"http-verification-failed": 1}
    assert "did not match" in receipt["results"][0]["reason"]
