import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "ops" / "home-server" / "relay_agent.py"
spec = importlib.util.spec_from_file_location("relay_agent", SCRIPT)
relay = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(relay)


# The exact node_errors ComfyUI returned for ArtJob 9511 on 2026-08-25, from the
# kr-relay log Silas pasted. Reading the relay's old message for this, the
# reasonable conclusion was "we're sending bad prompts" -- it led with
# "POST /prompt failed" and dumped the graph's node ids. It is not a prompt
# fault: INPUT_TYPES() takes no arguments and runs before ComfyUI compares any
# submitted value.
WIN_IO_NODE_ERRORS = {
    "1": {
        "errors": [
            {
                "type": "exception_during_inner_validation",
                "message": "Exception when validating inner node",
                "details": (
                    "[WinError 1117] The request could not be performed because "
                    "of an I/O device error: 'Z:\\\\ai\\\\models\\\\unet'"
                ),
                "extra_info": {
                    "input_name": "model",
                    "exception_type": "OSError",
                    "exception_message": (
                        "[WinError 1117] The request could not be performed "
                        "because of an I/O device error: "
                        "'Z:\\\\ai\\\\models\\\\unet'"
                    ),
                },
            }
        ],
        "dependent_outputs": ["9"],
        "class_type": "UnetLoaderGGUF",
    }
}

# What an actual bad value looks like from the same endpoint: ComfyUI compared
# the submitted name against its live list and rejected it. This one IS the
# prompt's fault and must keep the old message.
VALUE_REJECTION_NODE_ERRORS = {
    "2": {
        "errors": [
            {
                "type": "value_not_in_list",
                "message": "Value not in list",
                "details": (
                    "clip_name: 'flux2_klein_text_encoder_fp8_scaled.safetensors' "
                    "not in (list of length 16)"
                ),
                "extra_info": {"input_name": "clip_name"},
            }
        ],
        "class_type": "CLIPLoader",
    }
}


def test_win_io_device_error_is_reported_as_a_host_fault():
    fault = relay.host_fault_in_node_errors(WIN_IO_NODE_ERRORS)
    assert fault is not None
    assert fault.startswith("UnetLoaderGGUF (node 1): OSError -- ")
    assert "WinError 1117" in fault
    assert "Z:" in fault


def test_a_rejected_input_value_is_not_a_host_fault():
    # The whole point of the split: this one is worth repairing or requeuing.
    assert relay.host_fault_in_node_errors(VALUE_REJECTION_NODE_ERRORS) is None


def test_posix_errno_is_detected_without_an_exception_type():
    # A ComfyUI build that doesn't forward exception_type still has [Errno N]
    # in the detail text.
    fault = relay.host_fault_in_node_errors(
        {
            "1": {
                "class_type": "UnetLoaderGGUF",
                "errors": [
                    {
                        "details": "[Errno 5] Input/output error: '/mnt/models/unet'",
                        "extra_info": {},
                    }
                ],
            }
        }
    )
    assert fault is not None
    assert "Errno 5" in fault


def test_malformed_and_empty_node_errors_are_not_host_faults():
    for value in (None, {}, "nope", [], {"1": "not a dict"}, {"1": {"errors": None}}):
        assert relay.host_fault_in_node_errors(value) is None


def test_host_fault_message_collapses_whitespace():
    fault = relay.host_fault_in_node_errors(
        {
            "3": {
                "class_type": "CLIPTextEncode",
                "errors": [
                    {
                        "extra_info": {
                            "exception_type": "OSError",
                            "exception_message": "read\n  failed\ton\tZ:",
                        }
                    }
                ],
            }
        }
    )
    assert fault == "CLIPTextEncode (node 3): OSError -- read failed on Z:"


def _combo_object_info(class_type, input_name, files):
    return {class_type: {"input": {"required": {input_name: [list(files), {}]}}}}


def test_unresolved_error_reports_how_many_files_comfyui_listed():
    # The count is the diagnosis. 30 jobs on 2026-08-25 named
    # qwen3vl_4b_fp8_scaled.safetensors -- registered, and rendering fine that
    # same morning -- and were reported as if the name were wrong.
    workflow = {
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {"clip_name": "qwen3vl_4b_fp8_scaled.safetensors"},
        }
    }
    _remaps, unresolved = relay.resolve_workflow_asset_names(
        workflow, _combo_object_info("CLIPLoader", "clip_name", ["clip_l.safetensors"])
    )
    assert unresolved
    message = str(relay.unresolved_asset_error(unresolved))
    assert "ComfyUI listed 1 file(s) for that input" in message
    assert "lost sight of the file" in message


def test_candidate_counts_do_not_leak_between_resolution_passes():
    short = _combo_object_info("CLIPLoader", "clip_name", ["a.safetensors"])
    long = _combo_object_info(
        "CLIPLoader", "clip_name", [f"m{n}.safetensors" for n in range(9)]
    )
    for info, expected in ((short, "1 file(s)"), (long, "9 file(s)")):
        workflow = {
            "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "gone.safetensors"}}
        }
        _remaps, unresolved = relay.resolve_workflow_asset_names(workflow, info)
        assert expected in str(relay.unresolved_asset_error(unresolved))
