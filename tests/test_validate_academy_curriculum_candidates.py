import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_academy_curriculum_candidates.py"
SPEC = importlib.util.spec_from_file_location("validate_academy_curriculum_candidates", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def complete_candidate() -> str:
    return """<!-- academy-cultural-context: required -->
# Example

## Artists for historical study

### Artist
Rights boundary: verify each work independently.

## Public-domain and generation policy

Use item-level rights review for each work. Do not include protected artist names. Avoid stereotype and negative representation patterns.

## Movement-level remix configuration

```yaml
negative_guidance:
  - named-artist imitation
```

## Promotion checklist

- [ ] Verify reusable rights and license data.
- [ ] A cultural-history reviewer checks representation.
- [ ] No named artist appears in generation prompts.
"""


def test_complete_sensitive_candidate_passes():
    assert MODULE.validate_text(complete_candidate()) == []


def test_formal_candidate_without_sensitive_signal_is_ignored():
    assert MODULE.validate_text("# Geometric abstraction\n\n## Recognition cues\n\nSquares.") == []


def test_explicit_exemption_wins_over_keyword_heuristic():
    text = "<!-- academy-cultural-context: not-applicable -->\n# Japanese-inspired grid terminology audit"
    assert MODULE.validate_text(text) == []


def test_keyword_detects_sensitive_candidate():
    errors = MODULE.validate_text("# Harlem Renaissance\n\nA Black cultural movement.")
    assert "missing artist-level `Rights boundary:` guidance" in errors
    assert "missing `## Promotion checklist` section" in errors


def test_missing_negative_guidance_is_reported():
    text = complete_candidate().replace("negative_guidance:", "avoid_list:")
    assert "remix configuration missing `negative_guidance:` list" in MODULE.validate_text(text)


def test_missing_representation_review_is_reported():
    text = complete_candidate().replace(
        "A cultural-history reviewer checks representation.",
        "Check the lesson formatting.",
    )
    assert "promotion checklist missing representation review item" in MODULE.validate_text(text)
