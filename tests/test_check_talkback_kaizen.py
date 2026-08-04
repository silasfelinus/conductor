"""Tests for scripts/check_talkback_kaizen.py. No network or real roadmaps."""

import scripts.check_talkback_kaizen as checker


def write_project(root, slug, task_ids, talkback):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    lines = ["tasks:"]
    for task_id in task_ids:
        lines.extend([f"  - id: {task_id}", "    status: ready"])
    (project_dir / "roadmap.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (project_dir / "TALKBACK.md").write_text(talkback, encoding="utf-8")


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def scan(root):
    return checker.scan(root / "projects", root / "project-overrides.yaml")


def test_promised_id_that_exists_is_not_flagged(tmp_path):
    write_project(
        tmp_path, "academy", ["t-001"], "**Kaizen task:** t-001 -- do the thing.\n"
    )
    write_overrides(tmp_path, [("academy", "active")])

    missing, checked, scanned = scan(tmp_path)

    assert missing == []
    assert (checked, scanned) == (1, 1)


def test_promised_id_that_was_never_created_is_flagged(tmp_path):
    # The interface-vision/t-093 shape exactly: TALKBACK names the follow-on,
    # the roadmap never got it, and next_free_task_id would hand the id out again.
    write_project(
        tmp_path, "academy", ["t-001"], "**Kaizen task:** t-093 -- never written.\n"
    )
    write_overrides(tmp_path, [("academy", "active")])

    missing, checked, _ = scan(tmp_path)

    assert checked == 1
    assert len(missing) == 1
    assert "academy/t-093" in missing[0]


def test_cross_project_promise_resolves_against_the_named_project(tmp_path):
    # "**Kaizen task:** conductor/t-043" in another project's TALKBACK must be
    # checked against conductor's roadmap, not the file's own.
    write_project(
        tmp_path, "academy", ["t-001"], "**Kaizen task:** conductor/t-043 -- filed.\n"
    )
    write_project(tmp_path, "conductor", ["t-043"], "no promises here\n")
    write_overrides(tmp_path, [("academy", "active"), ("conductor", "active")])

    missing, _, _ = scan(tmp_path)

    assert missing == []


def test_cross_project_promise_is_flagged_when_the_other_roadmap_lacks_it(tmp_path):
    write_project(
        tmp_path, "academy", ["t-043"], "**Kaizen task:** conductor/t-043 -- filed.\n"
    )
    write_project(tmp_path, "conductor", ["t-001"], "no promises here\n")
    write_overrides(tmp_path, [("academy", "active"), ("conductor", "active")])

    missing, _, _ = scan(tmp_path)

    # academy HAS a t-043, but the promise named conductor's — resolving against
    # the wrong roadmap is what would make this pass incorrectly.
    assert len(missing) == 1
    assert "conductor/t-043" in missing[0]


def test_none_filed_is_not_a_promise(tmp_path):
    write_project(
        tmp_path,
        "academy",
        ["t-001"],
        "**Kaizen task:** none this cycle -- t-999 already covers it.\n",
    )
    write_overrides(tmp_path, [("academy", "active")])

    missing, checked, _ = scan(tmp_path)

    assert missing == []
    assert checked == 0


def test_inactive_projects_are_skipped(tmp_path):
    # A retired project's unkept promises are exactly the stale noise CLAUDE.md's
    # session-startup rule says not to resurface.
    write_project(
        tmp_path, "pinball-hero", ["t-001"], "**Kaizen task:** t-777 -- never written.\n"
    )
    write_overrides(tmp_path, [("pinball-hero", "retired")])

    missing, checked, scanned = scan(tmp_path)

    assert missing == []
    assert (checked, scanned) == (0, 0)


def test_project_absent_from_overrides_defaults_to_active(tmp_path):
    write_project(
        tmp_path, "academy", ["t-001"], "**Kaizen task:** t-093 -- never written.\n"
    )
    write_overrides(tmp_path, [("other-project", "paused")])

    missing, _, scanned = scan(tmp_path)

    assert scanned == 1
    assert len(missing) == 1


def test_unbolded_and_backticked_forms_are_both_recognised(tmp_path):
    write_project(
        tmp_path,
        "academy",
        ["t-001"],
        "Kaizen task: `t-050` -- backticked.\n\n**Kaizen task:** t-051 -- bold.\n",
    )
    write_overrides(tmp_path, [("academy", "active")])

    missing, checked, _ = scan(tmp_path)

    assert checked == 2
    assert sorted(entry.split()[0] for entry in missing) == [
        "academy/t-050",
        "academy/t-051",
    ]


def test_missing_overrides_file_treats_everything_as_active(tmp_path):
    write_project(
        tmp_path, "academy", ["t-001"], "**Kaizen task:** t-093 -- never written.\n"
    )

    missing, _, scanned = scan(tmp_path)

    assert scanned == 1
    assert len(missing) == 1
