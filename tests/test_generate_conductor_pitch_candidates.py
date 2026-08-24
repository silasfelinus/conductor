"""Tests for scripts/generate_conductor_pitch_candidates.py's pure logic
(tokenization, novelty scoring, server selection). No network calls."""
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "scripts" / "generate_conductor_pitch_candidates.py"

spec = importlib.util.spec_from_file_location(
    "generate_conductor_pitch_candidates", MODULE_PATH
)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_tokenize_strips_stopwords_and_short_words():
    tokens = mod.tokenize("A New Kind Robots Project for the Conductor")
    assert "new" not in tokens  # not a stopword itself but short-ish; check core ones
    assert "the" not in tokens
    assert "for" not in tokens
    assert "kind" not in tokens
    assert "robots" not in tokens
    assert "conductor" not in tokens
    assert "project" not in tokens


def test_tokenize_lowercases_and_dedupes_via_set():
    tokens = mod.tokenize("Sentiment Sentiment KARAOKE")
    assert tokens == {"sentiment", "karaoke"}


def test_jaccard_identical_sets_is_one():
    a = {"fish", "bible", "catalog"}
    assert mod.jaccard(a, set(a)) == 1.0


def test_jaccard_disjoint_sets_is_zero():
    assert mod.jaccard({"fish"}, {"karaoke"}) == 0.0


def test_jaccard_empty_set_is_zero():
    assert mod.jaccard(set(), {"fish"}) == 0.0
    assert mod.jaccard(set(), set()) == 0.0


def test_score_novelty_flags_near_duplicate_of_existing_project():
    corpus = [("project-goal:coloring-book", mod.tokenize(
        "printable coloring pages featuring kind robots characters"
    ))]
    result = mod.score_novelty(
        "Printable coloring pages featuring kind robots characters", corpus
    )
    assert result["closest_match"] == "project-goal:coloring-book"
    assert result["similarity"] > 0.9


def test_score_novelty_low_for_unrelated_text():
    corpus = [("project-goal:coloring-book", mod.tokenize(
        "printable coloring pages featuring kind robots characters"
    ))]
    result = mod.score_novelty("A completely different submarine warfare simulator", corpus)
    assert result["similarity"] < 0.1


def test_score_novelty_empty_corpus_is_zero():
    result = mod.score_novelty("anything at all", [])
    assert result == {"closest_match": None, "similarity": 0.0}


def test_pick_text_server_prefers_backend_keyed_provider():
    servers = [
        {"id": 1, "serverType": "OLLAMA", "category": "text"},
        {"id": 2, "serverType": "OPENAI", "category": "text"},
        {"id": 3, "serverType": "COMFY", "category": "art"},
    ]
    chosen = mod.pick_text_server(servers)
    assert chosen["id"] == 2


def test_pick_text_server_excludes_art_only_servers():
    servers = [{"id": 3, "serverType": "COMFY", "category": "art"}]
    assert mod.pick_text_server(servers) is None


def test_pick_text_server_honors_explicit_override():
    servers = [
        {"id": 1, "serverType": "OPENAI", "category": "text"},
        {"id": 2, "serverType": "ANTHROPIC", "category": "text"},
    ]
    chosen = mod.pick_text_server(servers, explicit_id=1)
    assert chosen["id"] == 1


def test_pick_text_server_explicit_override_missing_returns_none():
    servers = [{"id": 1, "serverType": "OPENAI", "category": "text"}]
    assert mod.pick_text_server(servers, explicit_id=999) is None


def test_pick_text_server_falls_back_to_default_flag_without_backend_keyed():
    servers = [
        {"id": 1, "serverType": "CUSTOM", "category": "text", "isDefault": False},
        {"id": 2, "serverType": "CUSTOM", "category": "text", "isDefault": True},
    ]
    chosen = mod.pick_text_server(servers)
    assert chosen["id"] == 2
