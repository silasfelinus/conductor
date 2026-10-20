"""kr-download must share the scanner's existing Civitai token convention.

2026-10-20: Windows PM2 had CIVITAI_TOKEN but no KR_CIVITAI_TOKEN, so
scanner metadata enrichment worked while five gated model downloads got 401.
"""
import importlib.util
import sys
import types
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1] / "ops/home-server/relay_download_agent.py"


def load_agent(monkeypatch, *, civitai=None, kr_civitai=None):
    for key, value in (("CIVITAI_TOKEN", civitai), ("KR_CIVITAI_TOKEN", kr_civitai)):
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)

    # Loading this small helper must not start either the scanner or the render relay.
    monkeypatch.setitem(sys.modules, "lora_import_agent", types.ModuleType("lora_import_agent"))
    monkeypatch.setitem(sys.modules, "relay_agent", types.ModuleType("relay_agent"))
    spec = importlib.util.spec_from_file_location("test_civitai_download_agent", AGENT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("legacy", "scoped", "expected"),
    [
        ("scanner-key", None, "scanner-key"),
        (None, "downloader-key", "downloader-key"),
        ("scanner-key", "downloader-key", "scanner-key"),
        ("", "downloader-key", "downloader-key"),
        (None, None, ""),
    ],
)
def test_token_matches_scanner_precedence(monkeypatch, legacy, scoped, expected):
    agent = load_agent(monkeypatch, civitai=legacy, kr_civitai=scoped)
    assert agent.CIVITAI_TOKEN == expected


def test_gated_civitai_urls_receive_existing_scanner_token(monkeypatch):
    agent = load_agent(monkeypatch, civitai="a key+with/slash")
    assert agent.with_civitai_token(
        "https://civitai.com/api/download/models/2230125"
    ) == "https://civitai.com/api/download/models/2230125?token=a%20key%2Bwith%2Fslash"
    assert agent.with_civitai_token(
        "https://www.civitai.com/api/download/models/2?type=Model"
    ) == "https://www.civitai.com/api/download/models/2?type=Model&token=a%20key%2Bwith%2Fslash"


@pytest.mark.parametrize(
    "url",
    [
        "https://civitai.com.evil.invalid/api/download/models/1",
        "https://notcivitai.com/api/download/models/1",
        "https://example.org/?next=https://civitai.com/api/download/models/1",
        "http://civitai.com/api/download/models/1",
        "https://civitaiarchive.com/api/download/models/1",
    ],
)
def test_token_never_leaks_to_other_hosts(monkeypatch, url):
    agent = load_agent(monkeypatch, civitai="private-test-token")
    assert agent.with_civitai_token(url) == url


def test_no_token_preserves_public_url(monkeypatch):
    agent = load_agent(monkeypatch)
    url = "https://civitai.com/api/download/models/3103600"
    assert agent.with_civitai_token(url) == url
