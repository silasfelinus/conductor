"""Blacklist enforcement for the Tzaddikim discovery pipeline (Silas, 2026-09-30)."""
import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts" / "build_tzaddik_discovery.py"
KIND_ROBOTS_BLACKLIST = ROOT.parent / "kind_robots" / "utils" / "tzaddikBlacklist.ts"

spec = importlib.util.spec_from_file_location("build_tzaddik_discovery_blacklist", MODULE_PATH)
btd = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = btd
spec.loader.exec_module(btd)


def _entry(name):
    return {
        "name": name,
        "region": "Nowhere",
        "domain": "testing",
        "pitch": "A pitch.",
        "wikipedia": "https://en.wikipedia.org/wiki/Test",
        "review_note": "None.",
        "tags": ["Education"],
    }


def _batch():
    return {
        "date": "2099-01-01",
        "living": [_entry(f"Living Person {i}") for i in range(10)],
        "memorial": [_entry(f"Memorial Person {i}") for i in range(10)],
    }


def test_real_blacklist_loads_silas_named_entries():
    table = btd.load_blacklist()
    names = set(table.values())
    assert {"Mahatma Gandhi", "Mother Teresa", "Thomas Jefferson"} <= names


@pytest.mark.parametrize(
    "spelling,expected",
    [
        ("Ghandi", "Mahatma Gandhi"),
        ("mohandas  gandhi", "Mahatma Gandhi"),
        ("César Chávez", "Cesar Chavez"),
        ("JK Rowling", "J. K. Rowling"),
        ("Saint Teresa of Calcutta", "Mother Teresa"),
    ],
)
def test_blacklist_matching_ignores_case_accents_and_punctuation(spelling, expected):
    assert btd.blacklisted_as(spelling) == expected


def test_blacklist_does_not_overmatch():
    assert btd.blacklisted_as("Jimmy Carter") is None
    assert btd.blacklisted_as("Martin Luther King Jr.") is None


def test_validate_batch_rejects_blacklisted_name(monkeypatch):
    monkeypatch.setattr(btd, "excluded_names", lambda: set())
    batch = _batch()
    batch["memorial"][3] = _entry("Mother Teresa")
    errors = btd.validate_batch(batch)
    assert any("blacklist" in e for e in errors)


def test_missing_blacklist_file_means_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(btd, "BLACKLIST_PATH", tmp_path / "nope.yaml")
    assert btd.load_blacklist() == {}


@pytest.mark.skipif(not KIND_ROBOTS_BLACKLIST.exists(), reason="no kind_robots checkout alongside conductor")
def test_kind_robots_blacklist_parity():
    ts = KIND_ROBOTS_BLACKLIST.read_text(encoding="utf-8")
    ts_names = set(re.findall(r"name:\s*'([^']+)'", ts))
    yaml_names = set(btd.load_blacklist().values())
    assert ts_names == yaml_names
