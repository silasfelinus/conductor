from scripts.check_pr_handoff_template import REQUIRED_SECTIONS, missing_sections


def complete_body() -> str:
    return "\n\n".join(f"{heading}\ncontent" for heading in REQUIRED_SECTIONS)


def test_complete_handoff_has_no_missing_sections():
    assert missing_sections(complete_body()) == []


def test_missing_stakes_is_reported():
    body = complete_body().replace("### Stakes\ncontent\n\n", "")
    assert missing_sections(body) == ["### Stakes"]


def test_flags_for_reviewer_is_not_required_when_empty():
    assert "### Flags for Reviewer" not in REQUIRED_SECTIONS
