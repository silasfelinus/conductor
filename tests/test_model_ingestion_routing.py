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
