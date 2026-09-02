from scripts.check_roadmap_task_id_reuse import suspicious_reuse


def roadmap(*tasks):
    return {"tasks": list(tasks)}


def test_flags_title_and_milestone_rewrite_for_same_id():
    base = roadmap({"id": "t-091", "milestone": "m1", "title": "Investigate Component model"})
    head = roadmap({"id": "t-091", "milestone": "m6", "title": "Repair missing Facets"})

    findings = suspicious_reuse(base, head)

    assert len(findings) == 1
    assert findings[0][0] == "t-091"


def test_allows_title_only_edit():
    base = roadmap({"id": "t-001", "milestone": "m1", "title": "Old wording"})
    head = roadmap({"id": "t-001", "milestone": "m1", "title": "Clearer wording"})
    assert suspicious_reuse(base, head) == []


def test_allows_milestone_only_move():
    base = roadmap({"id": "t-001", "milestone": "m1", "title": "Same task"})
    head = roadmap({"id": "t-001", "milestone": "m2", "title": "Same task"})
    assert suspicious_reuse(base, head) == []


def test_ignores_new_and_removed_ids():
    base = roadmap({"id": "t-001", "milestone": "m1", "title": "Removed"})
    head = roadmap({"id": "t-002", "milestone": "m2", "title": "New"})
    assert suspicious_reuse(base, head) == []
