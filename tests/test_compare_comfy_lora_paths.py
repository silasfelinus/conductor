from scripts.compare_comfy_lora_paths import (
    compare,
    extract_comfy_loras,
    extract_resource_paths,
)


def test_extract_comfy_loras_reads_dropdown_values():
    payload = {
        "LoraLoaderModelOnly": {
            "input": {"required": {"lora_name": [["styles\\foo.safetensors"]]}}
        }
    }
    assert extract_comfy_loras(payload) == ["styles\\foo.safetensors"]


def test_extract_resource_paths_accepts_wrapped_payload():
    payload = {"data": [{"localPath": "FLUX/foo.safetensors"}, {"name": "skip"}]}
    assert extract_resource_paths(payload) == ["FLUX/foo.safetensors"]


def test_compare_handles_separator_and_case_differences():
    report = compare(
        ["FLUX/Foo.safetensors"],
        ["flux\\foo.safetensors"],
    )
    assert report["matches"] == [
        {
            "resourcePath": "FLUX/Foo.safetensors",
            "comfyPath": "flux\\foo.safetensors",
            "match": "normalized-exact",
        }
    ]


def test_compare_uses_unique_basename_when_directories_differ():
    report = compare(
        ["Kontext/SFW/impressionist.safetensors"],
        ["models/academy/impressionist.safetensors"],
    )
    assert report["matches"][0]["match"] == "unique-basename"


def test_compare_does_not_guess_ambiguous_basenames():
    report = compare(
        ["FLUX/shared.safetensors"],
        ["a/shared.safetensors", "b/shared.safetensors"],
    )
    assert report["matches"] == []
    assert report["ambiguous"] == [
        {
            "resourcePath": "FLUX/shared.safetensors",
            "candidates": ["a/shared.safetensors", "b/shared.safetensors"],
        }
    ]


def test_compare_reports_missing_resources():
    report = compare(["FLUX/missing.safetensors"], ["other.safetensors"])
    assert report["missing"] == ["FLUX/missing.safetensors"]
