import scripts.roadmap_deps as roadmap_deps


def test_zero_diff_close_hint_matches_done_dependency_naming_task_id():
    tasks_by_id = {
        "t-033": {
            "id": "t-033",
            "status": "done",
            "note": "Landed the gating pattern t-031 was auditing for; see kind_robots#2964.",
        },
    }
    task = {"id": "t-031", "depends_on": "t-033"}

    hint = roadmap_deps.zero_diff_close_hint(task, tasks_by_id)

    assert hint is not None
    assert hint["dependency_task_id"] == "t-033"
    assert "t-033" in hint["reason"]


def test_zero_diff_close_hint_none_when_note_does_not_mention_task():
    tasks_by_id = {
        "t-033": {"id": "t-033", "status": "done", "note": "Unrelated closing note."},
    }
    task = {"id": "t-031", "depends_on": "t-033"}

    assert roadmap_deps.zero_diff_close_hint(task, tasks_by_id) is None


def test_zero_diff_close_hint_none_when_dependency_not_done():
    tasks_by_id = {
        "t-033": {"id": "t-033", "status": "review", "note": "Mentions t-031 already."},
    }
    task = {"id": "t-031", "depends_on": "t-033"}

    assert roadmap_deps.zero_diff_close_hint(task, tasks_by_id) is None


def test_zero_diff_close_hint_none_without_depends_on():
    task = {"id": "t-031"}

    assert roadmap_deps.zero_diff_close_hint(task, {}) is None


def test_zero_diff_close_hint_does_not_false_positive_on_substring_ids():
    # t-1 must not match a note mentioning only t-19 -- word-boundary only, not substring.
    tasks_by_id = {
        "t-033": {"id": "t-033", "status": "done", "note": "Closed out t-19 in the same pass."},
    }
    task = {"id": "t-1", "depends_on": "t-033"}

    assert roadmap_deps.zero_diff_close_hint(task, tasks_by_id) is None


def test_zero_diff_close_hint_checks_every_dependency_in_a_list():
    tasks_by_id = {
        "t-020": {"id": "t-020", "status": "done", "note": "Unrelated."},
        "t-021": {"id": "t-021", "status": "done", "note": "Already covers t-022's acceptance criteria."},
    }
    task = {"id": "t-022", "depends_on": ["t-020", "t-021"]}

    hint = roadmap_deps.zero_diff_close_hint(task, tasks_by_id)

    assert hint is not None
    assert hint["dependency_task_id"] == "t-021"
