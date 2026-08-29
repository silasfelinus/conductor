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


def test_human_answer_unread_detects_only_a_trailing_human_note():
    """The Kind Robots gate composer stamps these prefixes; a trailing one means
    Silas spoke and no agent has replied since. See scripts/audit_human_gates.py
    for why this is the tie that was missing from the gate pipeline."""
    assert audit.human_answer_unread({"note": "Worker parked this."}) == ""
    assert audit.human_answer_unread({}) == ""
    assert audit.human_answer_unread({"note": None}) == ""

    answered = {
        "note": "Worker parked this.\n\n"
        "HUMAN ANSWER from silas via Kind Robots. Gate released. Use option B."
    }
    assert audit.human_answer_unread(answered).startswith("HUMAN ANSWER")
    assert "human-answer-unread" in audit.stale_reasons(answered)

    # An agent transition appends its own block, which is what "read" looks
    # like -- the flag must clear rather than nag forever.
    replied = {
        "note": "HUMAN NOTE from silas via Kind Robots. Still gated. x\n\n"
        "Worker: acted on this, still blocked upstream."
    }
    assert audit.human_answer_unread(replied) == ""
    assert "human-answer-unread" not in audit.stale_reasons(replied)


def test_render_surfaces_the_answer_text_and_counts_it():
    gates = [
        {
            "project": "kind-robots",
            "task_id": "t-078",
            "title": "Home page review",
            "soft_gate": False,
            "stale_reasons": ["human-answer-unread"],
            "human_answer": "HUMAN NOTE from silas via Kind Robots. Ship the toggle.",
        },
    ]

    output = audit.render(gates)
    assert "Gates with an unread answer from Silas: 1" in output
    # The flag alone would repeat the original bug: a human answer nobody reads.
    assert "ANSWER FROM SILAS: HUMAN NOTE from silas" in output


def test_scan_sorts_answered_gates_first(tmp_path):
    write_roadmap(
        tmp_path,
        "academy",
        [
            {"id": "t-001", "status": "needs-human", "title": "Plain gate"},
            {
                "id": "t-002",
                "status": "needs-human",
                "title": "Answered gate",
                "note": "HUMAN ANSWER from silas via Kind Robots. Go ahead.",
            },
        ],
    )
    write_overrides(tmp_path, [("academy", "active")])

    gates = audit.scan(tmp_path / "projects", include_inactive=False)
    assert [gate["task_id"] for gate in gates] == ["t-002", "t-001"]
