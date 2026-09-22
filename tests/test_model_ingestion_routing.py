import importlib
import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HOME_SERVER = ROOT / "ops" / "home-server"
CATALOG = HOME_SERVER / "lora-catalog"


def reload_from(path: Path, name: str):
    sys.path.insert(0, str(path))
    sys.modules.pop(name, None)
    try:
        return importlib.import_module(name)
    finally:
        sys.path.pop(0)


def test_download_agent_routes_every_file_resource_type(monkeypatch):
    monkeypatch.setenv("KR_MODEL_ROOT", "/models")
    monkeypatch.setenv("KR_LORA_DIR", "/models/Lora")
    monkeypatch.setenv("KR_CHECKPOINT_DIR", "/models/checkpoints")
    sys.path.insert(0, str(HOME_SERVER))
    for name in ("relay_download_agent", "relay_agent"):
        sys.modules.pop(name, None)
    try:
        mod = importlib.import_module("relay_download_agent")
    finally:
        sys.path.pop(0)

    expected = {
        "CHECKPOINT": "/models/checkpoints",
        "EMBEDDING": "/models/embeddings",
        "LORA": "/models/Lora",
        "LYCORIS": "/models/Lora",
        "HYPERNETWORK": "/models/hypernetworks",
        "CONTROLNET": "/models/controlnet",
        "VAE": "/models/vae",
        "TEXT_ENCODER": "/models/text_encoders",
        "DIFFUSION_MODEL": "/models/diffusion_models",
        "LATENT_UPSCALER": "/models/latent_upscale_models",
        "UPSCALER": "/models/upscale_models",
    }
    for resource_type, directory in expected.items():
        assert mod.target_dir(resource_type).replace("\\", "/") == directory

    for unsupported in ("API", "URL", "SAMPLER"):
        with pytest.raises(ValueError):
            mod.target_dir(unsupported)


def test_watcher_has_distinct_lora_and_checkpoint_inboxes(monkeypatch):
    monkeypatch.setenv("KR_RELAY_TOKEN", "test-token")
    monkeypatch.setenv("LORA_ROOT", "/models/Lora")
    monkeypatch.setenv("MODEL_ROOT", "/models")
    sys.path.insert(0, str(HOME_SERVER))
    sys.modules.pop("lora_import_agent", None)
    try:
        mod = importlib.import_module("lora_import_agent")
    finally:
        sys.path.pop(0)

    assert mod.LORA_IMPORT_DIR.replace("\\", "/") == "/models/Lora/import"
    assert (
        mod.CHECKPOINT_IMPORT_DIR.replace("\\", "/")
        == "/models/checkpoints/import"
    )
    assert ".gguf" in mod.MODEL_EXTS
    assert not hasattr(mod, "claim_and_download")
    assert mod.missing_config() == []


def test_generic_scanner_catalogs_file_backed_components():
    sys.path.insert(0, str(CATALOG))
    for name in ("scan_models", "scan_loras"):
        sys.modules.pop(name, None)
    try:
        mod = importlib.import_module("scan_models")
    finally:
        sys.path.pop(0)

    expected = {
        "controlnet": "CONTROLNET",
        "hypernetwork": "HYPERNETWORK",
        "embedding": "EMBEDDING",
        "upscaler": "UPSCALER",
        "latent_upscaler": "LATENT_UPSCALER",
        "vae": "VAE",
        "text_encoder": "TEXT_ENCODER",
        "diffusion_model": "DIFFUSION_MODEL",
    }
    for kind, resource_type in expected.items():
        assert kind in mod.RESOURCE_KINDS
        assert mod.KIND_RESOURCE_TYPE[kind] == resource_type

    assert mod.classify("latent_upscale_models/foo.safetensors")[:2] == (
        "latent_upscaler",
        "latent_upscale_models",
    )
    assert mod.classify(
        "checkpoints/import/ltx_spatial_upscaler.safetensors"
    )[:2] == ("latent_upscaler", "latent_upscale_models")
    assert mod.classify("upscale_models/4x_foolhardy.safetensors")[:2] == (
        "upscaler",
        "upscale_models",
    )


def test_checkpoint_import_root_preserves_checkpoint_context(tmp_path):
    sys.path.insert(0, str(CATALOG))
    for name in ("scan_models", "scan_loras"):
        sys.modules.pop(name, None)
    try:
        mod = importlib.import_module("scan_models")
    finally:
        sys.path.pop(0)

    inbox = tmp_path / "models" / "checkpoints" / "import"
    inbox.mkdir(parents=True)
    dropped = inbox / "plain-model.ckpt"
    dropped.write_bytes(b"checkpoint fixture")

    entry, _meta = mod.build_entry(dropped, inbox, None, no_hash=True)

    assert entry.kind == "checkpoint"
    assert entry.comfy_folder == "checkpoints"


def test_vendored_lora_scanner_classifies_civitai_tags():
    sys.path.insert(0, str(CATALOG))
    sys.modules.pop("scan_loras", None)
    try:
        mod = importlib.import_module("scan_loras")
    finally:
        sys.path.pop(0)

    row = mod.LoraEntry(
        name="ambiguous-model.safetensors",
        civitai_tags=["character"],
    )
    assert mod.classify_category(row) == ("CHARACTER", "CIVITAI")
    assert row.loraCategory == ""


def test_watcher_importer_requests_generated_resource_previews(monkeypatch, tmp_path):
    monkeypatch.setenv("KR_RELAY_TOKEN", "test-token")
    monkeypatch.setenv("LORA_ROOT", str(tmp_path / "models" / "Lora"))
    monkeypatch.setenv("MODEL_ROOT", str(tmp_path / "models"))
    sys.path.insert(0, str(HOME_SERVER))
    sys.modules.pop("lora_import_agent", None)
    try:
        mod = importlib.import_module("lora_import_agent")
    finally:
        sys.path.pop(0)

    catalog = tmp_path / "lora-catalog.json"
    catalog.write_text('{"entries": []}', encoding="utf-8")
    commands = []

    def fake_run(cmd, timeout):
        commands.append(cmd)
        result_path = Path(cmd[cmd.index("--result-out") + 1])
        result_path.write_text(
            '{"counts":{"created":0,"skipped":0,"failed":0},'
            '"resources":[],"previews":{"queued":0,"deduplicated":0,'
            '"skipped":0,"failed":0,"jobIds":[],"resources":[]}}',
            encoding="utf-8",
        )
        return True

    monkeypatch.setattr(mod, "run", fake_run)
    result = mod.import_catalog(str(catalog), str(tmp_path / "result.json"))

    assert result["counts"]["failed"] == 0
    assert "--queue-previews" in commands[0]
    assert "--upsert" in commands[0]


@pytest.mark.parametrize("resource_type", ["LORA", "LYCORIS", "CHECKPOINT"])
def test_download_agent_routes_image_models_through_canonical_scanner(
    monkeypatch, tmp_path, resource_type
):
    monkeypatch.setenv("KR_MODEL_ROOT", str(tmp_path / "models"))
    monkeypatch.setenv("KR_LORA_DIR", str(tmp_path / "models" / "Lora"))
    monkeypatch.setenv(
        "KR_CHECKPOINT_DIR", str(tmp_path / "models" / "checkpoints")
    )
    monkeypatch.setenv("KR_RELAY_TOKEN", "test-token")
    sys.path.insert(0, str(HOME_SERVER))
    for name in ("relay_download_agent", "relay_agent", "lora_import_agent"):
        sys.modules.pop(name, None)
    try:
        mod = importlib.import_module("relay_download_agent")
    finally:
        sys.path.pop(0)

    request = {
        "id": 41,
        "resourceType": resource_type,
        "downloadUrl": "https://example.invalid/model.safetensors",
        "civitaiModelVersionId": 808,
    }
    calls = {"complete": []}

    def fake_download(_request, _url, dest_dir):
        return (
            os.path.join(dest_dir, "model.safetensors"),
            "model.safetensors",
            1024,
            "abc123",
        )

    def fake_lora(folder, out_dir):
        calls["scanner"] = ("lora", folder, out_dir)
        return {
            "resources": [
                {
                    "id": 77,
                    "hash": "abc123",
                    "civitaiModelVersionId": 808,
                }
            ]
        }

    def fake_model(folder, out_dir):
        calls["scanner"] = ("model", folder, out_dir)
        return {
            "resources": [
                {
                    "id": 77,
                    "hash": "abc123",
                    "civitaiModelVersionId": 808,
                }
            ]
        }

    monkeypatch.setattr(mod, "download_binary", fake_download)
    monkeypatch.setattr(mod.model_import, "process_lora_folder", fake_lora)
    monkeypatch.setattr(mod.model_import, "process_model_folder", fake_model)
    monkeypatch.setattr(
        mod,
        "catalog_resource",
        lambda *_args, **_kwargs: pytest.fail(
            "LoRA/checkpoint DownloadRequests must not bypass the scanners"
        ),
    )
    monkeypatch.setattr(
        mod,
        "complete_download",
        lambda *args, **kwargs: calls["complete"].append((args, kwargs)),
    )

    mod.process_download(request)

    expected_scanner = "model" if resource_type == "CHECKPOINT" else "lora"
    assert calls["scanner"][0] == expected_scanner
    assert ".download-import-41" in calls["scanner"][1].replace("\\", "/")
    assert calls["complete"][0][1]["resource_id"] == 77


def test_download_agent_keeps_component_direct_path(monkeypatch, tmp_path):
    monkeypatch.setenv("KR_MODEL_ROOT", str(tmp_path / "models"))
    monkeypatch.setenv("KR_RELAY_TOKEN", "test-token")
    sys.path.insert(0, str(HOME_SERVER))
    for name in ("relay_download_agent", "relay_agent", "lora_import_agent"):
        sys.modules.pop(name, None)
    try:
        mod = importlib.import_module("relay_download_agent")
    finally:
        sys.path.pop(0)

    request = {
        "id": 42,
        "resourceType": "VAE",
        "downloadUrl": "https://example.invalid/vae.safetensors",
    }
    calls = {}

    monkeypatch.setattr(
        mod,
        "download_binary",
        lambda _request, _url, dest: (
            os.path.join(dest, "vae.safetensors"),
            "vae.safetensors",
            1024,
            "def456",
        ),
    )
    monkeypatch.setattr(
        mod,
        "catalog_resource",
        lambda *_args: calls.setdefault("resource_id", 88),
    )
    monkeypatch.setattr(
        mod,
        "complete_download",
        lambda _request_id, _success, resource_id=None, **_kwargs:
            calls.setdefault("completed", resource_id),
    )

    mod.process_download(request)

    assert calls["resource_id"] == 88
    assert calls["completed"] == 88
