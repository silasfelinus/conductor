import base64
import hashlib
import sys
from pathlib import Path

import pytest

RELAY_DIR = Path(__file__).resolve().parents[1] / "ops" / "home-server"
if str(RELAY_DIR) not in sys.path:
    sys.path.insert(0, str(RELAY_DIR))

import relay_agent as relay
import relay_media_agent as media_relay


def request_payload():
    return {
        "promptString": "A vampire family portrait in a velvet crypt lounge.",
        "workflow": {"59": {"inputs": {"text": "vampire family"}}},
        "provenance": {
            "promptHash": "prompt-hash-a",
            "workflowHash": "workflow-hash-a",
            "workflowPromptHash": "workflow-prompt-hash-a",
        },
    }


def comfy_media(raw=b"job-a-pixels", prompt_id="prompt-a"):
    return {
        "data_b64": base64.b64encode(raw).decode(),
        "file_type": "png",
        "is_video": False,
        "comfy": {
            "prompt_id": prompt_id,
            "output": {
                "filename": "job-a.png",
                "subfolder": "coloring",
                "type": "output",
            },
            "image_hash": hashlib.sha256(raw).hexdigest(),
        },
    }


def test_claim_advertises_strict_completion_proof(monkeypatch):
    captured = {}

    def fake_http(method, url, body=None, bearer=None, timeout=60):
        captured.update(
            method=method,
            url=url,
            body=body,
            bearer=bearer,
            timeout=timeout,
        )
        return 200, {"success": True, "data": {"job": {"id": 42}}}

    monkeypatch.setattr(relay, "http_json", fake_http)
    monkeypatch.setattr(relay, "KR_RELAY_TOKEN", "test-token")
    monkeypatch.setattr(relay, "AGENT_ID", "relay:Silas-PC")
    monkeypatch.setattr(relay, "RELAY_VERSION", "relay-test-v1")

    assert relay.claim_job() == {"id": 42}
    assert captured["body"] == {
        "agentId": "relay:Silas-PC",
        "agentVersion": "relay-test-v1",
        "supportsInputImages": True,
        "supportsCompletionProof": True,
    }


def test_extract_comfy_output_preserves_tuple_prompt_id_and_byte_hash(monkeypatch):
    raw = b"exact-comfy-output-bytes"
    monkeypatch.setattr(relay, "download_comfy_file", lambda _meta: raw)

    result = relay.extract_comfy_output(
        {
            "57": {
                "images": [
                    {
                        "filename": "job-a.png",
                        "subfolder": "coloring",
                        "type": "output",
                    }
                ]
            }
        },
        False,
        prompt_id="prompt-a",
    )

    assert base64.b64decode(result["data_b64"]) == raw
    assert result["comfy"] == {
        "prompt_id": "prompt-a",
        "output": {
            "filename": "job-a.png",
            "subfolder": "coloring",
            "type": "output",
        },
        "image_hash": hashlib.sha256(raw).hexdigest(),
    }


def test_completion_provenance_binds_request_output_and_pixels(monkeypatch):
    monkeypatch.setattr(relay, "RELAY_VERSION", "relay-test-v1")
    monkeypatch.setattr(relay, "RELAY_COMMIT", "abc123")

    proof = relay.completion_provenance(request_payload(), comfy_media())

    assert proof == {
        "relayVersion": "relay-test-v1",
        "relayCommit": "abc123",
        "promptId": "prompt-a",
        "promptHash": "prompt-hash-a",
        "workflowHash": "workflow-hash-a",
        "workflowPromptHash": "workflow-prompt-hash-a",
        "imageHash": hashlib.sha256(b"job-a-pixels").hexdigest(),
        "output": {
            "filename": "job-a.png",
            "subfolder": "coloring",
            "type": "output",
        },
    }


def test_completion_provenance_fails_closed_when_claim_lacks_hashes():
    payload = {"promptString": "unproven prompt", "workflow": {"1": {}}}

    try:
        relay.completion_provenance(payload, comfy_media())
    except RuntimeError as error:
        assert "promptHash" in str(error)
        assert "workflowHash" in str(error)
        assert "workflowPromptHash" in str(error)
    else:
        raise AssertionError("strict relay accepted incomplete request provenance")


def test_complete_job_sends_proof_object(monkeypatch):
    captured = {}
    proof = relay.completion_provenance(request_payload(), comfy_media())

    def fake_http(method, url, body=None, bearer=None, timeout=60):
        captured.update(method=method, url=url, body=body, bearer=bearer)
        return 200, {
            "success": True,
            "data": {"job": {"id": 42, "artImageId": 123}},
        }

    monkeypatch.setattr(relay, "http_json", fake_http)
    monkeypatch.setattr(relay, "KR_RELAY_TOKEN", "test-token")

    completed = relay.complete_job(
        42,
        True,
        art_image_id=123,
        provenance=proof,
    )

    assert completed["artImageId"] == 123
    assert captured["body"] == {
        "success": True,
        "artImageId": 123,
        "provenance": proof,
    }


def test_media_recovery_passes_exact_prompt_id_to_output_extractor(monkeypatch):
    captured = {}
    payload = request_payload()

    def fake_http(method, url, body=None, bearer=None, timeout=60):
        if method == "POST" and url.endswith("/prompt"):
            return 200, {"prompt_id": "recovered-exact-id"}
        if method == "GET" and "/history/recovered-exact-id" in url:
            return 200, {
                "recovered-exact-id": {
                    "outputs": {"57": {"images": [{"filename": "x.png"}]}}
                }
            }
        raise AssertionError(f"unexpected relay request: {method} {url}")

    def fake_extract(outputs, want_video, prompt_id=None):
        captured.update(
            outputs=outputs,
            want_video=want_video,
            prompt_id=prompt_id,
        )
        return comfy_media(prompt_id=prompt_id)

    monkeypatch.setattr(media_relay.relay, "http_json", fake_http)
    monkeypatch.setattr(media_relay.relay, "upload_comfy_input_images", lambda _p: None)
    monkeypatch.setattr(media_relay.relay, "extract_comfy_output", fake_extract)
    monkeypatch.setattr(media_relay.time, "sleep", lambda _seconds: None)

    result = media_relay.run_comfy_with_recovery(payload)

    assert result["comfy"]["prompt_id"] == "recovered-exact-id"
    assert captured["prompt_id"] == "recovered-exact-id"


def test_direct_media_process_completes_with_proof(monkeypatch, tmp_path):
    captured = {}
    payload = request_payload()
    payload.update(
        targetRepo="silasfelinus/kind_robots",
        imagePath="public/images/coloring/job-a.png",
    )
    job = {"id": 42, "engine": "COMFY", "payload": payload, "attempts": 1}
    rendered = comfy_media()

    monkeypatch.setattr(
        media_relay,
        "direct_media_relative",
        lambda _job: Path("coloring/job-a.png"),
    )
    monkeypatch.setattr(media_relay.relay, "run_comfy", lambda _payload: rendered)
    monkeypatch.setattr(media_relay.relay, "upload_result", lambda _job, _media: 123)
    monkeypatch.setattr(
        media_relay,
        "write_direct_media",
        lambda _job, _media: tmp_path / "job-a.png",
    )

    def fake_complete(job_id, success, art_image_id=None, error=None, provenance=None):
        captured.update(
            job_id=job_id,
            success=success,
            art_image_id=art_image_id,
            error=error,
            provenance=provenance,
        )
        return {"id": job_id, "artImageId": art_image_id}

    monkeypatch.setattr(media_relay.relay, "complete_job", fake_complete)

    media_relay.process_with_media(job)

    assert captured["job_id"] == 42
    assert captured["success"] is True
    assert captured["art_image_id"] == 123
    assert captured["provenance"]["promptId"] == "prompt-a"
    assert captured["provenance"]["imageHash"] == hashlib.sha256(
        b"job-a-pixels"
    ).hexdigest()


def test_describe_comfy_error_extracts_execution_error_detail():
    entry = {
        "status": {
            "status_str": "error",
            "messages": [
                ["execution_start", {}],
                [
                    "execution_error",
                    {
                        "node_id": "7",
                        "node_type": "KSampler",
                        "exception_message": "CUDA out of memory",
                    },
                ],
            ],
        }
    }

    assert relay.describe_comfy_error(entry) == "node 7 (KSampler): CUDA out of memory"


def test_describe_comfy_error_returns_none_without_execution_error():
    assert relay.describe_comfy_error({"status": {"status_str": "error"}}) is None
    assert relay.describe_comfy_error({}) is None


def test_run_comfy_raises_with_execution_error_detail(monkeypatch):
    payload = request_payload()

    def fake_http(method, url, body=None, bearer=None, timeout=60):
        if method == "POST" and url.endswith("/prompt"):
            return 200, {"prompt_id": "prompt-err"}
        if method == "GET" and "/history/prompt-err" in url:
            return 200, {
                "prompt-err": {
                    "outputs": {},
                    "status": {
                        "status_str": "error",
                        "messages": [
                            [
                                "execution_error",
                                {
                                    "node_id": "7",
                                    "node_type": "KSampler",
                                    "exception_message": "CUDA out of memory",
                                },
                            ]
                        ],
                    },
                }
            }
        raise AssertionError(f"unexpected relay request: {method} {url}")

    monkeypatch.setattr(relay, "http_json", fake_http)
    monkeypatch.setattr(relay, "upload_comfy_input_images", lambda _p: None)
    monkeypatch.setattr(relay.time, "sleep", lambda _seconds: None)

    with pytest.raises(RuntimeError, match=r"node 7 \(KSampler\): CUDA out of memory"):
        relay.run_comfy(payload)


def test_run_comfy_with_recovery_raises_with_execution_error_detail(monkeypatch):
    payload = request_payload()

    def fake_http(method, url, body=None, bearer=None, timeout=60):
        if method == "POST" and url.endswith("/prompt"):
            return 200, {"prompt_id": "prompt-err"}
        if method == "GET" and "/history/prompt-err" in url:
            return 200, {
                "prompt-err": {
                    "outputs": {},
                    "status": {
                        "status_str": "error",
                        "messages": [
                            [
                                "execution_error",
                                {
                                    "node_id": "3",
                                    "node_type": "VAEDecode",
                                    "exception_message": "tensor size mismatch",
                                },
                            ]
                        ],
                    },
                }
            }
        raise AssertionError(f"unexpected relay request: {method} {url}")

    monkeypatch.setattr(media_relay.relay, "http_json", fake_http)
    monkeypatch.setattr(media_relay.relay, "upload_comfy_input_images", lambda _p: None)
    monkeypatch.setattr(media_relay.time, "sleep", lambda _seconds: None)

    with pytest.raises(RuntimeError, match=r"node 3 \(VAEDecode\): tensor size mismatch"):
        media_relay.run_comfy_with_recovery(payload)
