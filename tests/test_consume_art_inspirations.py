import textwrap

import scripts.consume_art_inspirations as insp


SAMPLE = textwrap.dedent(
    """\
    # header comment that must survive
    inspirations:
      - project: ai-art-academy
        target_repo: silasfelinus/kind_robots
        images:
          - image_path: public/images/ai-art-academy/great-wave-1.webp
            status: pending
            prompt: the great wave, panel one
          - image_path: public/images/ai-art-academy/great-wave-2.webp
            status: pending
            prompt: the great wave, panel two
    """
)


def test_regeneration_forced_reads_force_field():
    assert insp.regeneration_forced({"force": True}) is True
    assert insp.regeneration_forced({"force": "true"}) is True
    assert insp.regeneration_forced({}) is False
    assert insp.regeneration_forced({"force": False}) is False
    assert insp.regeneration_forced({"force": None}) is False


def test_already_satisfied_ignores_an_existing_file_when_forced(tmp_path, monkeypatch):
    """Mirrors consume_art_requests.py's identical fix (conductor/t-192): a
    stale file from a prior render must not count as fulfillment once the
    entry is re-staged to pending with force: true."""
    monkeypatch.setattr(insp, "ROOT", tmp_path)
    monkeypatch.setattr(insp, "REPO_ROOTS", {"silasfelinus/conductor": tmp_path})
    stale = tmp_path / "public" / "images" / "ai-art-academy" / "great-wave-1.webp"
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"stale render")

    entry = {
        "target_repo": "silasfelinus/conductor",
        "image_path": "public/images/ai-art-academy/great-wave-1.webp",
    }
    assert insp.already_satisfied(entry) is True

    entry["force"] = True
    assert insp.already_satisfied(entry) is False


def with_force(sample, image_path):
    """Insert `force: true` next to `status:` for the given image_path,
    reusing set_image_status's own indent so the fixture can't drift out of
    sync with the module's real block/indent conventions."""
    lines = sample.splitlines(keepends=True)
    for idx, line in enumerate(lines):
        m = insp.IMAGE_PATH_PAT.match(line)
        if m and m.group(1).strip().strip("'\"") == image_path:
            for j in range(idx, len(lines)):
                sm = insp.STATUS_PAT.match(lines[j])
                if sm:
                    indent = sm.group(1)
                    lines.insert(j + 1, f"{indent}force: true\n")
                    return "".join(lines)
    raise AssertionError(f"{image_path} not found in fixture")


def test_with_force_fixture_helper_is_found_by_set_image_status():
    sample = with_force(SAMPLE, "public/images/ai-art-academy/great-wave-1.webp")
    assert "force: true" in sample
    assert insp.regeneration_forced(
        next(i for i in insp.yaml.safe_load(sample)["inspirations"][0]["images"]
             if i["image_path"] == "public/images/ai-art-academy/great-wave-1.webp")
    ) is True


def test_clear_image_field_removes_an_existing_line():
    sample = with_force(SAMPLE, "public/images/ai-art-academy/great-wave-1.webp")
    output, changed = insp.clear_image_field(
        sample, "public/images/ai-art-academy/great-wave-1.webp", "force"
    )
    assert changed is True
    assert "force:" not in output
    assert "panel one" in output
    # The sibling image's own fields (and its own lack of a force field) are untouched.
    assert "panel two" in output


def test_clear_image_field_missing_field_is_noop():
    output, changed = insp.clear_image_field(
        SAMPLE, "public/images/ai-art-academy/great-wave-1.webp", "force"
    )
    assert changed is False
    assert output == SAMPLE


def test_mark_done_clears_the_force_field(tmp_path, monkeypatch):
    sample = with_force(SAMPLE, "public/images/ai-art-academy/great-wave-1.webp")
    file = tmp_path / "art-prompts.yaml"
    file.write_text(sample)
    monkeypatch.setattr(insp, "ART_PROMPTS_FILE", file)

    count = insp.mark_done(["public/images/ai-art-academy/great-wave-1.webp"])
    assert count == 1

    data = insp.yaml.safe_load(file.read_text())
    images = data["inspirations"][0]["images"]
    panel_one = next(i for i in images if i["image_path"] == "public/images/ai-art-academy/great-wave-1.webp")
    assert panel_one["status"] == "done"
    assert "force" not in panel_one


def test_main_resubmits_a_forced_entry_instead_of_marking_it_done_again(
    tmp_path, monkeypatch, capsys
):
    sample = with_force(SAMPLE, "public/images/ai-art-academy/great-wave-1.webp")
    ledger = tmp_path / "art-prompts.yaml"
    ledger.write_text(sample)
    monkeypatch.setattr(insp, "ART_PROMPTS_FILE", ledger)
    monkeypatch.setattr(insp, "ROOT", tmp_path)
    monkeypatch.setattr(insp, "KIND_ROBOTS_ROOT", tmp_path)
    monkeypatch.setattr(
        insp,
        "REPO_ROOTS",
        {"silasfelinus/conductor": tmp_path, "silasfelinus/kind_robots": tmp_path},
    )
    stale = tmp_path / "public" / "images" / "ai-art-academy" / "great-wave-1.webp"
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"stale render")
    # The second panel's file genuinely exists and was never force-flagged --
    # it must still resolve as satisfied, proving the fix is scoped to the
    # forced entry rather than disabling the idempotency check wholesale.
    (tmp_path / "public" / "images" / "ai-art-academy" / "great-wave-2.webp").write_bytes(
        b"a real, current render"
    )
    monkeypatch.setattr(
        insp.sys, "argv", ["consume_art_inspirations.py"]
    )

    insp.main()

    out = capsys.readouterr().out
    assert "1 to generate" in out
    assert "1 already-present" in out
