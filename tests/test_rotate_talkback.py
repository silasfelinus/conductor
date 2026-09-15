import datetime as dt

import scripts.rotate_talkback as rt

ROOT_FIXTURE = """# TALKBACK.md — Cross-Agent Critique Log

Append-only. Both Worker (OpenAI) and Reviewer (Claude) write here.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | system | <type>
type: critique | pattern
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-06-30 | Reviewer → Worker | system | pattern
type: response

**Subject:** an old entry.

## 2026-07-15 | Worker → Reviewer | system | critique
type: critique

**Subject:** another old entry.

## 2026-09-01 | Reviewer → Worker | system | pattern
type: response

**Subject:** a current-month entry.

## 2026-09-10 | Worker → Reviewer | system | critique
type: critique

**Subject:** another current-month entry.
"""


def write_fixture(tmp_path, monkeypatch, text=ROOT_FIXTURE):
    monkeypatch.setattr(rt, "ROOT", tmp_path)
    monkeypatch.setattr(rt, "TALKBACK_PATH", tmp_path / "TALKBACK.md")
    monkeypatch.setattr(rt, "ARCHIVE_DIR", tmp_path / "talkback")
    (tmp_path / "TALKBACK.md").write_text(text, encoding="utf-8")


def test_split_entries_ignores_format_template_line():
    """The '## YYYY-MM-DD | ...' template line inside the fenced code block
    must NOT be treated as a real dated entry."""
    preamble, entries = rt.split_entries(ROOT_FIXTURE)
    assert "```" in preamble  # template block stayed in the preamble
    assert len(entries) == 4
    assert [m for m, _ in entries] == ["2026-06", "2026-07", "2026-09", "2026-09"]


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    write_fixture(tmp_path, monkeypatch)
    before = (tmp_path / "TALKBACK.md").read_text(encoding="utf-8")
    result = rt.rotate(apply=False, today=dt.date(2026, 9, 15))
    after = (tmp_path / "TALKBACK.md").read_text(encoding="utf-8")
    assert before == after
    assert not (tmp_path / "talkback").exists()
    assert result["months_archived"] == ["2026-06", "2026-07"]
    assert result["kept_entry_count"] == 2


def test_apply_rotates_old_months_and_keeps_current(tmp_path, monkeypatch):
    write_fixture(tmp_path, monkeypatch)
    result = rt.rotate(apply=True, today=dt.date(2026, 9, 15))
    assert result["applied"] is True
    assert set(result["months_archived"]) == {"2026-06", "2026-07"}

    root_text = (tmp_path / "TALKBACK.md").read_text(encoding="utf-8")
    assert "a current-month entry" in root_text
    assert "another current-month entry" in root_text
    assert "an old entry" not in root_text
    assert "another old entry" not in root_text
    assert rt.POINTER_MARKER in root_text

    archive_06 = (tmp_path / "talkback" / "2026-06.md").read_text(encoding="utf-8")
    archive_07 = (tmp_path / "talkback" / "2026-07.md").read_text(encoding="utf-8")
    assert "an old entry" in archive_06
    assert "another old entry" in archive_07
    # Verbatim: the original entry header/body text is untouched inside the archive.
    assert "## 2026-06-30 | Reviewer → Worker | system | pattern" in archive_06


def test_roundtrip_verified_before_any_write(tmp_path, monkeypatch):
    """If extraction can't reproduce an entry byte-for-byte, nothing is written."""
    write_fixture(tmp_path, monkeypatch)

    def broken_extract(text):
        return ["corrupted"]

    monkeypatch.setattr(rt, "extract_archive_entries", broken_extract)
    result = rt.rotate(apply=True, today=dt.date(2026, 9, 15))
    assert result["months_failed"]
    # Root must be untouched when any month fails verification.
    root_text = (tmp_path / "TALKBACK.md").read_text(encoding="utf-8")
    assert root_text == ROOT_FIXTURE
    assert not (tmp_path / "talkback" / "2026-06.md").exists()


def test_rerun_is_idempotent(tmp_path, monkeypatch):
    write_fixture(tmp_path, monkeypatch)
    rt.rotate(apply=True, today=dt.date(2026, 9, 15))
    root_after_first = (tmp_path / "TALKBACK.md").read_text(encoding="utf-8")

    result2 = rt.rotate(apply=True, today=dt.date(2026, 9, 15))
    root_after_second = (tmp_path / "TALKBACK.md").read_text(encoding="utf-8")

    assert root_after_first == root_after_second
    # Old months no longer exist in root at all after the first rotation, so
    # the second run finds nothing left to archive (a clean no-op) rather
    # than re-detecting them as "already archived".
    assert result2["months_already_archived"] == []
    assert result2["months_archived"] == []


def test_already_archived_month_reported_if_still_present_in_root(tmp_path, monkeypatch):
    """Covers the defensive already-archived path: an old month's entries are
    still in root (e.g. a manual edit) but an identical archive file already
    exists — re-running must recognize it rather than erroring or duplicating."""
    write_fixture(tmp_path, monkeypatch)
    _preamble, entries = rt.split_entries(ROOT_FIXTURE)
    june_bodies = [body for month, body in entries if month == "2026-06"]
    (tmp_path / "talkback").mkdir()
    (tmp_path / "talkback" / "2026-06.md").write_text(
        rt.render_archive("2026-06", june_bodies, today=dt.date(2026, 9, 15)),
        encoding="utf-8",
    )
    result = rt.rotate(apply=True, today=dt.date(2026, 9, 15))
    assert "2026-06" in result["months_already_archived"]
    assert "2026-07" in result["months_archived"]
    assert result["months_failed"] == []


def test_extract_archive_entries_is_inverse_of_render(tmp_path, monkeypatch):
    write_fixture(tmp_path, monkeypatch)
    _preamble, entries = rt.split_entries(ROOT_FIXTURE)
    june_bodies = [body for month, body in entries if month == "2026-06"]
    rendered = rt.render_archive("2026-06", june_bodies, today=dt.date(2026, 9, 15))
    assert rt.extract_archive_entries(rendered) == june_bodies


def test_no_fully_elapsed_month_is_a_clean_noop(tmp_path, monkeypatch):
    text = (
        "# TALKBACK.md\n\n---\n<!-- Entries below. -->\n\n"
        "## 2026-09-01 | Worker → Reviewer | system | critique\nonly this month\n"
    )
    write_fixture(tmp_path, monkeypatch, text=text)
    result = rt.rotate(apply=True, today=dt.date(2026, 9, 15))
    assert result["months_archived"] == []
    assert result["kept_entry_count"] == 1
    assert (tmp_path / "TALKBACK.md").read_text(encoding="utf-8") == text
