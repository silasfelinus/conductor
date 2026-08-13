"""Relay-side model/LoRA name resolution against ComfyUI's live filename lists.

Reproduces the real 2026-07-28 Kind Robots queue failures: workflows carried
checkpoint/LoRA names whose slash direction, case, or folder prefix drifted
from what ComfyUI's object_info actually lists, so ComfyUI rejected the whole
prompt with HTTP 400 `value_not_in_list` even though the files were on disk.
"""

import sys
from pathlib import Path

RELAY_DIR = Path(__file__).resolve().parents[1] / "ops" / "home-server"
if str(RELAY_DIR) not in sys.path:
    sys.path.insert(0, str(RELAY_DIR))

import relay_agent as relay  # noqa: E402


def object_info(loras=None, checkpoints=None):
    """Minimal object_info: a LoRA loader and a checkpoint loader, each with a
    combo `*_name` input plus a non-combo input that must be left alone."""
    return {
        "LoraLoaderModelOnly": {
            "input": {
                "required": {
                    "lora_name": [list(loras or []), {}],
                    "strength_model": ["FLOAT", {"default": 1.0}],
                }
            }
        },
        "CheckpointLoaderSimple": {
            "input": {"required": {"ckpt_name": [list(checkpoints or []), {}]}}
        },
    }


def lora_node(name):
    return {
        "class_type": "LoraLoaderModelOnly",
        "inputs": {"lora_name": name, "strength_model": 1.0, "model": ["59", 0]},
    }


def ckpt_node(name):
    return {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": name}}


def test_forward_slash_stored_but_list_uses_backslash():
    # Job #2774-style: stored forward-slash, ComfyUI (Windows) lists backslash.
    live = "Flux\\SFW\\3D_Cartoon_Vision_flux_v1.safetensors"
    workflow = {"61": lora_node("Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors")}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, object_info(loras=[live])
    )
    assert workflow["61"]["inputs"]["lora_name"] == live
    assert unresolved == []
    assert remaps and remaps[0][3] == live


def test_backslash_stored_but_list_uses_forward_slash():
    # Job #2615-style: stored `FLUX\impressionist`, list has `flux/impressionist`.
    live = "flux/impressionist.safetensors"
    workflow = {"61": lora_node("FLUX\\impressionist.safetensors")}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, object_info(loras=[live])
    )
    assert workflow["61"]["inputs"]["lora_name"] == live
    assert unresolved == []


def test_case_only_drift_is_resolved():
    # Job #2621-style: `FLUX/...` stored, list has `Flux/...`.
    live = "Flux/manuscript_illustration_kontext.safetensors"
    workflow = {"61": lora_node("FLUX/manuscript_illustration_kontext.safetensors")}
    relay.resolve_workflow_asset_names(workflow, object_info(loras=[live]))
    assert workflow["61"]["inputs"]["lora_name"] == live


def test_checkpoint_backslash_prefix_resolved():
    # Jobs #2758/#2756-style: hardcoded `ltx\ltx-...` vs listed `ltx/ltx-...`.
    live = "ltx/ltx-2.3-22b-dev-fp8.safetensors"
    workflow = {"317": ckpt_node("ltx\\ltx-2.3-22b-dev-fp8.safetensors")}
    relay.resolve_workflow_asset_names(workflow, object_info(checkpoints=[live]))
    assert workflow["317"]["inputs"]["ckpt_name"] == live


def test_unique_basename_fallback_across_different_folder():
    # Same file, moved to a different subfolder than the job recorded.
    live = "styles/acrylic.safetensors"
    workflow = {"61": lora_node("Kontext/SFW/acrylic.safetensors")}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, object_info(loras=[live])
    )
    assert workflow["61"]["inputs"]["lora_name"] == live
    assert unresolved == []


def test_ambiguous_basename_is_not_guessed():
    workflow = {"61": lora_node("a/style.safetensors")}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow,
        object_info(loras=["x/style.safetensors", "y/style.safetensors"]),
    )
    # Two files share the basename -> refuse to guess, leave the value, report it.
    assert workflow["61"]["inputs"]["lora_name"] == "a/style.safetensors"
    assert remaps == []
    assert unresolved == [("LoraLoaderModelOnly", "lora_name", "a/style.safetensors")]


def test_genuinely_missing_name_is_reported_not_rewritten():
    # Job #2603-style: a Hugging Face repo id, no extension, no such file.
    workflow = {"61": lora_node("UmeAiRT/FLUX.1-dev-LoRA-Impressionism")}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, object_info(loras=["Flux/SFW/other.safetensors"])
    )
    assert remaps == []
    assert unresolved and unresolved[0][2] == "UmeAiRT/FLUX.1-dev-LoRA-Impressionism"


def test_already_correct_name_is_untouched():
    live = "Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors"
    workflow = {"61": lora_node(live)}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, object_info(loras=[live])
    )
    assert remaps == []
    assert unresolved == []
    assert workflow["61"]["inputs"]["lora_name"] == live


def test_non_combo_inputs_are_left_alone():
    # strength_model is a FLOAT input, never a filename -- must not be touched
    # even if its stringified value somehow collided with the resolver.
    workflow = {"61": lora_node("Flux/SFW/x.safetensors")}
    workflow["61"]["inputs"]["strength_model"] = "0.8"
    relay.resolve_workflow_asset_names(
        workflow, object_info(loras=["Flux/SFW/x.safetensors"])
    )
    assert workflow["61"]["inputs"]["strength_model"] == "0.8"


def test_unknown_node_class_is_skipped():
    workflow = {"99": {"class_type": "SomeCustomNode", "inputs": {"lora_name": "x"}}}
    remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, object_info(loras=["Flux/y.safetensors"])
    )
    assert remaps == []
    assert unresolved == []


def test_align_applies_remaps_and_returns_unresolved(monkeypatch):
    # One name resolves (case drift) and gets rewritten in place; one is truly
    # missing and comes back as unresolved for the caller to fail fast on.
    info = object_info(loras=["Flux/manuscript_illustration_kontext.safetensors"])
    monkeypatch.setattr(relay, "fetch_comfy_object_info", lambda force=False: info)

    workflow = {
        "61": lora_node("FLUX/manuscript_illustration_kontext.safetensors"),
        "62": lora_node("UmeAiRT/FLUX.1-dev-LoRA-Impressionism"),
    }
    unresolved = relay.align_workflow_asset_names(workflow)

    assert (
        workflow["61"]["inputs"]["lora_name"]
        == "Flux/manuscript_illustration_kontext.safetensors"
    )
    assert [u[2] for u in unresolved] == ["UmeAiRT/FLUX.1-dev-LoRA-Impressionism"]


def test_align_skips_when_object_info_unavailable(monkeypatch):
    monkeypatch.setattr(relay, "fetch_comfy_object_info", lambda force=False: None)
    workflow = {"61": lora_node("whatever/x.safetensors")}
    assert relay.align_workflow_asset_names(workflow) == []
    assert workflow["61"]["inputs"]["lora_name"] == "whatever/x.safetensors"


def test_upload_backed_image_input_is_never_touched():
    # LoadImage's `image` combo is populated from Comfy's input dir; the relay
    # uploads that file separately, so a cached object_info won't list it yet.
    # It must not be remapped OR flagged as unresolved.
    info = {
        "LoadImage": {
            "input": {
                "required": {
                    "image": [["existing_a.png", "existing_b.png"], {"image_upload": True}]
                }
            }
        }
    }
    workflow = {
        "10": {"class_type": "LoadImage", "inputs": {"image": "job-2774-source.png"}}
    }
    remaps, unresolved = relay.resolve_workflow_asset_names(workflow, info)
    assert remaps == []
    assert unresolved == []
    assert workflow["10"]["inputs"]["image"] == "job-2774-source.png"


def test_resolution_state_distinguishes_skipped_from_ran(monkeypatch):
    # ArtJob 7905 failed three times on a checkpoint that was present on disk and
    # whose name this resolver could have fixed, and the queue could not say
    # whether the relay had skipped resolution or attempted it and disagreed.
    # These two runs must not look the same afterwards.
    monkeypatch.setattr(relay, "fetch_comfy_object_info", lambda force=False: None)
    relay.align_workflow_asset_names({"61": lora_node("whatever/x.safetensors")})
    assert relay._last_resolution["state"] == "skipped-no-object-info"

    info = object_info(loras=["Flux/manuscript_illustration_kontext.safetensors"])
    monkeypatch.setattr(relay, "fetch_comfy_object_info", lambda force=False: info)
    relay.align_workflow_asset_names(
        {"61": lora_node("FLUX/manuscript_illustration_kontext.safetensors")}
    )
    assert relay._last_resolution["state"] == "ran"
    assert relay._last_resolution["remaps"] == 1


# --- Both submission paths must resolve, not just relay_agent.run_comfy ------
#
# The 2026-08-13 regression: relay_media_agent.run_comfy_with_recovery
# reimplemented Comfy submission (longer timeout + /queue recovery) and did not
# carry the align_workflow_asset_names call across. kr-relay runs the media
# wrapper, so the resolver above -- fully implemented and fully tested -- never
# executed on the only path that actually submits work. ArtJobs 8276/8278 died
# on a LoRA sitting at exactly the path the catalog recorded.
#
# These tests assert the behaviour (the name is rewritten / the submit is
# refused) rather than grepping for a call, so a future third submission path
# that forgets the resolver fails here too.

import relay_media_agent as media  # noqa: E402


def _stub_comfy(monkeypatch, loras, posted):
    """Point the media wrapper at a fake ComfyUI whose list is `loras`.

    Every wait is driven to zero. Without that, a regression does not fail
    these tests -- it HANGS them: submission falls through to the generation
    poll, which sleeps until GEN_TIMEOUT against a stub that never returns an
    output. A test that hangs on the bug it guards is worse than no test,
    because CI reports a timeout instead of the defect.
    """
    monkeypatch.setattr(
        relay, "fetch_comfy_object_info", lambda force=False: object_info(loras=loras)
    )
    monkeypatch.setattr(relay, "upload_comfy_input_images", lambda payload: None)
    monkeypatch.setattr(relay, "GEN_TIMEOUT", 0)
    monkeypatch.setattr(media, "COMFY_PROMPT_TIMEOUT", 1)
    monkeypatch.setattr(media, "COMFY_RECOVERY_SECONDS", 0)

    def fake_post(method, url, body=None, timeout=None):
        posted.append(body)
        return 200, {"prompt_id": "p1"}

    monkeypatch.setattr(relay, "http_json", fake_post)


def test_media_wrapper_resolves_names_before_submitting(monkeypatch):
    # The exact 8276/8278 shape: catalog stores forward slashes, ComfyUI on
    # Windows lists backslashes. The wrapper must rewrite before POSTing.
    live = "Flux\\SFW\\3D_Cartoon_Vision_flux_v1.safetensors"
    posted = []
    _stub_comfy(monkeypatch, [live], posted)

    workflow = {"61": lora_node("Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors")}
    try:
        media.run_comfy_with_recovery({"workflow": workflow})
    except Exception:
        pass  # generation polling is out of scope; submission already happened

    assert posted, "the wrapper never POSTed a prompt"
    assert posted[0]["prompt"]["61"]["inputs"]["lora_name"] == live


def test_media_wrapper_fails_fast_instead_of_posting_unresolvable_name(monkeypatch):
    posted = []
    _stub_comfy(monkeypatch, ["Flux/SFW/something_else.safetensors"], posted)

    workflow = {"61": lora_node("UmeAiRT/FLUX.1-dev-LoRA-Impressionism")}
    try:
        media.run_comfy_with_recovery({"workflow": workflow})
        raise AssertionError("expected a fail-fast for an unresolvable name")
    except RuntimeError as error:
        assert "no matching file" in str(error)

    assert posted == [], "an unresolvable name must never reach ComfyUI"
