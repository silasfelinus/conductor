"""Tests for scripts/audit_human_gates.py. No network or real roadmaps."""

import scripts.audit_human_gates as audit


def write_roadmap(root, slug, tasks):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    lines = ["tasks:"]
    for task in tasks:
        lines.extend(
            [
                f"  - id: {task['id']}",
                f"    status: {task['status']}",
                f"    title: \"{task['title']}\"",
            ]
        )
        if task.get("soft_gate"):
            lines.append("    soft_gate: true")
        if task.get("gate_human"):
            lines.append("    gate_human: true")
        if task.get("approved_by_human") is not None:
            value = "true" if task["approved_by_human"] else "false"
            lines.append(f"    approved_by_human: {value}")
        if task.get("note"):
            lines.append("    note: >-")
            lines.append(f"      {task['note']}")
    (project_dir / "roadmap.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def test_scan_lists_active_human_gate_without_calling_it_stale(tmp_path):
    write_roadmap(
        tmp_path,
        "academy",
        [
            {
                "id": "t-001",
                "status": "needs-human",
                "title": "Choose the rights framing",
                "gate_human": True,
                "note": "Silas must choose option A or B before publication.",
            }
        ],
    )
    write_overrides(tmp_path, [("academy", "active")])

    gates = audit.scan(tmp_path / "projects")
    assert len(gates) == 1
    assert gates[0]["stale_reasons"] == []


def test_scan_flags_approved_task_still_waiting(tmp_path):
    write_roadmap(
        tmp_path,
        "storefront",
        [
            {
                "id": "t-002",
                "status": "needs-human",
                "title": "Approve fulfillment",
                "approved_by_human": True,
            }
        ],
    )

    gates = audit.scan(tmp_path / "projects")
    assert gates[0]["stale_reasons"] == [
        "approved-by-human-but-still-needs-human"
    ]


def test_scan_flags_explicit_nothing_left_language(tmp_path):
    write_roadmap(
        tmp_path,
        "conductor",
        [
            {
                "id": "t-003",
                "status": "needs-human",
                "title": "Confirm repaired ledger",
                "note": "The tests pass and there is nothing left to approve or decide.",
            }
        ],
    )

    gates = audit.scan(tmp_path / "projects")
    assert "nothing-left" in gates[0]["stale_reasons"]


def test_scan_skips_paused_projects_by_default(tmp_path):
    write_roadmap(
        tmp_path,
        "mermaids-of-venice",
        [
            {
                "id": "t-004",
                "status": "needs-human",
                "title": "Old content choice",
            }
        ],
    )
    write_overrides(tmp_path, [("mermaids-of-venice", "paused")])

    assert audit.scan(tmp_path / "projects") == []


def test_scan_can_include_paused_projects_explicitly(tmp_path):
    write_roadmap(
        tmp_path,
        "mermaids-of-venice",
        [
            {
                "id": "t-004",
                "status": "needs-human",
                "title": "Old content choice",
            }
        ],
    )
    write_overrides(tmp_path, [("mermaids-of-venice", "paused")])

    gates = audit.scan(tmp_path / "projects", include_inactive=True)
    assert len(gates) == 1
    assert gates[0]["project_status"] == "paused"


def test_render_separates_gate_count_from_stale_signal_count():
    gates = [
        {
            "project": "academy",
            "task_id": "t-001",
            "title": "Real decision",
            "soft_gate": False,
            "stale_reasons": [],
        },
        {
            "project": "conductor",
            "task_id": "t-002",
            "title": "Resolved bookkeeping",
            "soft_gate": True,
            "stale_reasons": ["nothing-left"],
        },
    ]

    output = audit.render(gates)
    assert "Active human gates: 2" in output
    assert "Strong stale-state signals: 1" in output
    assert "REVIEW: nothing-left" in output
