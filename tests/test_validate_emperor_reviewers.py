from pathlib import Path

from scripts.validate_emperor_reviewers import validate_record


def record():
    return {
        "kind_robots_sha": "abc123",
        "seed": 42,
        "trace_path": "trace.json",
        "transcript_path": "transcript.md",
        "acts": {
            act: {
                "mood": 3,
                "clarity": 4,
                "uniqueness": 3,
                "choices": 4,
                "consequence": 5,
                "total": 19,
            }
            for act in range(1, 6)
        },
    }


def test_complete_scores_pass():
    assert validate_record(record(), Path("reviewer.yaml")) == []


def test_scored_act_requires_trace_and_commit():
    data = record()
    data["trace_path"] = None
    data["kind_robots_sha"] = None
    errors = validate_record(data, Path("reviewer.yaml"))
    assert any("missing trace_path" in error for error in errors)
    assert any("missing kind_robots_sha" in error for error in errors)


def test_na_cannot_have_total():
    data = record()
    data["acts"][2]["mood"] = "N/A"
    errors = validate_record(data, Path("reviewer.yaml"))
    assert any("total requires five numeric" in error for error in errors)


def test_invalid_score_rejected():
    data = record()
    data["acts"][1]["choices"] = 6
    errors = validate_record(data, Path("reviewer.yaml"))
    assert any("must be 1-5" in error for error in errors)


def test_incorrect_total_rejected():
    data = record()
    data["acts"][3]["total"] = 25
    errors = validate_record(data, Path("reviewer.yaml"))
    assert any("total is incorrect" in error for error in errors)
