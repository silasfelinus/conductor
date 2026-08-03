import scripts.run_worker as run_worker


def roadmap(project, tasks):
    return {"_project": project, "_path": f"projects/{project}/roadmap.yaml", "tasks": tasks}


def test_find_ready_task_picks_first_ready_in_priority_order():
    roadmaps = [
        roadmap("alpha", [{"id": "t-001", "title": "Alpha task", "status": "ready"}]),
        roadmap("beta", [{"id": "t-002", "title": "Beta task", "status": "ready"}]),
    ]

    result = run_worker.find_ready_task(["beta", "alpha"], roadmaps)

    assert result is not None
    assert result["project"] == "beta"
    assert result["task_id"] == "t-002"


def test_find_ready_task_skips_umbrella_with_open_delegate():
    roadmaps = [
        roadmap(
            "interface-vision",
            [
                {
                    "id": "t-017",
                    "title": "Umbrella sweep",
                    "status": "ready",
                    "remaining_scope_task": "t-058",
                },
                {"id": "t-058", "title": "Dedicated follow-on", "status": "ready"},
            ],
        )
    ]

    result = run_worker.find_ready_task(["interface-vision"], roadmaps)

    assert result is not None
    assert result["task_id"] == "t-058"


def test_find_ready_task_reconsiders_umbrella_once_delegate_is_done():
    roadmaps = [
        roadmap(
            "interface-vision",
            [
                {
                    "id": "t-017",
                    "title": "Umbrella sweep",
                    "status": "ready",
                    "remaining_scope_task": "t-058",
                },
                {"id": "t-058", "title": "Dedicated follow-on", "status": "done"},
            ],
        )
    ]

    result = run_worker.find_ready_task(["interface-vision"], roadmaps)

    assert result is not None
    assert result["task_id"] == "t-017"


def test_find_ready_task_unaffected_by_unknown_delegate_id():
    roadmaps = [
        roadmap(
            "interface-vision",
            [
                {
                    "id": "t-017",
                    "title": "Umbrella sweep",
                    "status": "ready",
                    "remaining_scope_task": "t-999",
                },
            ],
        )
    ]

    result = run_worker.find_ready_task(["interface-vision"], roadmaps)

    assert result is not None
    assert result["task_id"] == "t-017"
