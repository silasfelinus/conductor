"""A log line must never be able to fail a render.

ArtJobs 8276/8278, 2026-08-13. The LoRA name resolver had just been wired into
the path kr-relay actually runs. It worked -- it matched the LoRA and built the
remap message -- and then died here:

    'charmap' codec can't encode character '\\U0001f527' in position 34

U+1F527 is the wrench in align_workflow_asset_names' remap line. On Windows,
Python takes stdout's encoding from the console codepage (cp1252) whenever
stdout is not a terminal, which under pm2 it never is. print() raised,
the exception propagated out of align_workflow_asset_names through run_comfy,
and the job FAILED -- one character from a successful render.

The same trap sat under the two U+26A0 warning lines in
fetch_comfy_object_info, so the message that exists to report an unreachable
/object_info would itself have crashed before reporting it.
"""

import io
import sys
from pathlib import Path

RELAY_DIR = Path(__file__).resolve().parents[1] / "ops" / "home-server"
if str(RELAY_DIR) not in sys.path:
    sys.path.insert(0, str(RELAY_DIR))

import lora_import_agent as lora  # noqa: E402
import relay_agent as relay  # noqa: E402

WRENCH = "\U0001f527"
WARNING = "⚠"


class Cp1252Stdout(io.TextIOWrapper):
    """stdout as pm2 hands it to Python on Silas-PC: a cp1252-encoded pipe."""

    def __init__(self):
        super().__init__(io.BytesIO(), encoding="cp1252", newline="")

    def reconfigure(self, **kwargs):  # noqa: D102 - refuses, like a real pipe can
        raise ValueError("cannot reconfigure this stream")


def test_emit_survives_an_unencodable_character(monkeypatch):
    stream = Cp1252Stdout()
    monkeypatch.setattr(sys, "stdout", stream)
    # Must not raise. Before the fix this is the exact UnicodeEncodeError that
    # failed ArtJobs 8276 and 8278.
    relay.emit(f"{WRENCH} LoraLoaderModelOnly.lora_name: 'a' -> 'b'")


def test_the_remap_line_itself_cannot_fail_a_job(monkeypatch):
    """The real path: a resolvable name, logged, under a cp1252 stdout."""
    stream = Cp1252Stdout()
    monkeypatch.setattr(sys, "stdout", stream)

    live = "Flux\\SFW\\3D_Cartoon_Vision_flux_v1.safetensors"
    info = {
        "LoraLoaderModelOnly": {
            "input": {"required": {"lora_name": [[live], {}]}}
        }
    }
    monkeypatch.setattr(relay, "fetch_comfy_object_info", lambda force=False: info)

    workflow = {
        "61": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"lora_name": "Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors"},
        }
    }
    # This logs the wrench line. It must complete and apply the remap.
    unresolved = relay.align_workflow_asset_names(workflow)
    assert unresolved == []
    assert workflow["61"]["inputs"]["lora_name"] == live


def test_the_object_info_warning_can_be_emitted(monkeypatch):
    # The warning that reports an unreachable /object_info must not crash
    # before it reports it.
    stream = Cp1252Stdout()
    monkeypatch.setattr(sys, "stdout", stream)
    relay.log(f"{WARNING} could not fetch ComfyUI object_info: boom")


def test_lora_import_log_survives_too(monkeypatch):
    stream = Cp1252Stdout()
    monkeypatch.setattr(sys, "stdout", stream)
    lora.log(f"{WRENCH} importing — em dash and wrench")


def test_emit_tolerates_a_closed_stdout(monkeypatch):
    class Closed:
        encoding = "utf-8"

        def write(self, *a, **k):
            raise OSError("stream closed")

        def flush(self, *a, **k):
            raise OSError("stream closed")

    monkeypatch.setattr(sys, "stdout", Closed())
    relay.emit("anything")  # must not raise


def test_utf8_reconfigure_is_attempted_and_never_raises(monkeypatch):
    calls = []

    class Recordable:
        encoding = "cp1252"

        def reconfigure(self, **kwargs):
            calls.append(kwargs)

    monkeypatch.setattr(sys, "stdout", Recordable())
    monkeypatch.setattr(sys, "stderr", Recordable())
    relay._use_utf8_stdout()
    assert calls, "stdout encoding must be forced to UTF-8 at import"
    assert all(c.get("encoding") == "utf-8" for c in calls)
