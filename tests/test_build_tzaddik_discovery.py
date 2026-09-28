import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts" / "build_tzaddik_discovery.py"

spec = importlib.util.spec_from_file_location("build_tzaddik_discovery", MODULE_PATH)
btd = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = btd
spec.loader.exec_module(btd)


def _valid_entry(name, **overrides):
    entry = {
        "name": name,
        "region": "Nowhere",
        "domain": "testing",
        "pitch": "A pitch.",
        "wikipedia": "https://en.wikipedia.org/wiki/Test",
        "review_note": "No documented controversy.",
        "tags": ["Education"],
    }
    entry.update(overrides)
    return entry


def _valid_batch(date="2099-01-01"):
    living = [_valid_entry(f"Living Person {i}") for i in range(10)]
    memorial = [_valid_entry(f"Memorial Person {i}") for i in range(10)]
    return {"date": date, "living": living, "memorial": memorial}


def test_parse_docket_extracts_existing_names(tmp_path, monkeypatch):
    docket = tmp_path / "2026-09-26.md"
    docket.write_text(
        "# Daily Tzaddik discovery docket — 2026-09-26\n\n"
        "## Living suggestions\n\n"
        "### José Andrés — Spain / United States — disaster food relief\n"
        "**Pitch:** x\n\n**Wikipedia:** https://en.wikipedia.org/wiki/x\n\n"
        "**Review note:** y\n\n"
        "## Memorial suggestions\n\n"
        "### Wangarĩ Maathai — Kenya — environment\n"
        "**Pitch:** x\n\n**Wikipedia:** https://en.wikipedia.org/wiki/y\n\n"
        "**Review note:** y\n",
        encoding="utf-8",
    )
    parsed = btd.parse_docket(docket)
    names = {e["name"] for e in parsed["entries"]}
    assert names == {"José Andrés", "Wangarĩ Maathai"}
    statuses = {e["name"]: e["status"] for e in parsed["entries"]}
    assert statuses["José Andrés"] == "living"
    assert statuses["Wangarĩ Maathai"] == "deceased"


def test_parse_docket_reads_tzaddik_meta_tags(tmp_path):
    docket = tmp_path / "2026-09-27.md"
    meta = '<!-- tzaddik-meta: {"status": "living", "tags": ["Environment", "Education"]} -->'
    docket.write_text(
        "## Living suggestions\n\n"
        f"### Someone — Region — domain\n{meta}\n"
        "**Pitch:** x\n\n**Wikipedia:** https://en.wikipedia.org/wiki/x\n\n**Review note:** y\n",
        encoding="utf-8",
    )
    parsed = btd.parse_docket(docket)
    assert parsed["entries"][0]["tags"] == ["Environment", "Education"]


def test_validate_batch_accepts_well_formed_batch():
    assert btd.validate_batch(_valid_batch()) == []


def test_validate_batch_rejects_wrong_counts():
    batch = _valid_batch()
    batch["living"] = batch["living"][:9]
    errors = btd.validate_batch(batch)
    assert any("exactly 10" in e for e in errors)


def test_validate_batch_rejects_bad_date():
    batch = _valid_batch(date="not-a-date")
    errors = btd.validate_batch(batch)
    assert any("YYYY-MM-DD" in e for e in errors)


def test_validate_batch_rejects_missing_field():
    batch = _valid_batch()
    batch["living"][0] = _valid_entry("Missing Pitch", pitch="")
    errors = btd.validate_batch(batch)
    assert any("pitch" in e for e in errors)


def test_validate_batch_rejects_uncontrolled_tag():
    batch = _valid_batch()
    batch["living"][0] = _valid_entry("Bad Tag Person", tags=["Not A Real Tag"])
    errors = btd.validate_batch(batch)
    assert any("controlled vocabulary" in e for e in errors)


def test_validate_batch_rejects_duplicate_within_batch():
    batch = _valid_batch()
    batch["memorial"][0] = _valid_entry("Living Person 0")
    errors = btd.validate_batch(batch)
    assert any("duplicate name within this batch" in e for e in errors)


def test_validate_batch_rejects_name_already_excluded(monkeypatch):
    monkeypatch.setattr(btd, "excluded_names", lambda: {"Already Suggested"})
    batch = _valid_batch()
    batch["living"][0] = _valid_entry("Already Suggested")
    errors = btd.validate_batch(batch)
    assert any("dedup violation" in e for e in errors)


def test_excluded_names_matching_is_case_insensitive(monkeypatch):
    monkeypatch.setattr(btd, "excluded_names", lambda: {"already suggested"})
    batch = _valid_batch()
    batch["living"][0] = _valid_entry("Already Suggested")
    errors = btd.validate_batch(batch)
    assert any("dedup violation" in e for e in errors)


def test_render_and_from_json_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(btd, "DISCOVERY_DIR", tmp_path)
    monkeypatch.setattr(btd, "excluded_names", lambda: set())
    batch_path = tmp_path / "batch.json"
    batch_path.write_text(json.dumps(_valid_batch(date="2099-02-02")), encoding="utf-8")

    rc = btd.from_json(batch_path, force=False)
    assert rc == 0

    out = tmp_path / "2099-02-02.md"
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "Living Person 0" in text
    assert "Memorial Person 0" in text
    assert text.count("## Living suggestions") == 1
    assert text.count("## Memorial suggestions") == 1

    # Re-parsing the rendered file should recover all 20 names and their tags.
    reparsed = btd.parse_docket(out)
    assert len(reparsed["entries"]) == 20
    assert all(e["tags"] == ["Education"] for e in reparsed["entries"])


def test_from_json_refuses_to_overwrite_without_force(tmp_path, monkeypatch):
    monkeypatch.setattr(btd, "DISCOVERY_DIR", tmp_path)
    monkeypatch.setattr(btd, "excluded_names", lambda: set())
    existing = tmp_path / "2099-03-03.md"
    existing.write_text("placeholder", encoding="utf-8")

    batch_path = tmp_path / "batch.json"
    batch_path.write_text(json.dumps(_valid_batch(date="2099-03-03")), encoding="utf-8")

    rc = btd.from_json(batch_path, force=False)
    assert rc == 3
    assert existing.read_text(encoding="utf-8") == "placeholder"

    rc_forced = btd.from_json(batch_path, force=True)
    assert rc_forced == 0
    assert "Living Person 0" in existing.read_text(encoding="utf-8")


def test_from_json_rejects_invalid_batch(tmp_path, monkeypatch):
    monkeypatch.setattr(btd, "DISCOVERY_DIR", tmp_path)
    monkeypatch.setattr(btd, "excluded_names", lambda: set())
    batch = _valid_batch()
    batch["living"] = batch["living"][:5]
    batch_path = tmp_path / "batch.json"
    batch_path.write_text(json.dumps(batch), encoding="utf-8")

    rc = btd.from_json(batch_path, force=False)
    assert rc == 1
    assert not (tmp_path / f"{batch['date']}.md").exists()


def test_brief_reports_required_counts_and_excludes_known_names(monkeypatch, capsys):
    monkeypatch.setattr(btd, "excluded_names", lambda: {"Known Person"})
    rc = btd.brief("2099-04-04")
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["required"] == {"living": 10, "deceased": 10}
    assert "Known Person" in payload["excluded_names"]
    assert payload["controlled_tags"] == btd.CONTROLLED_TAGS


def test_brief_rejects_bad_date(capsys):
    rc = btd.brief("not-a-date")
    assert rc == 2


def test_check_reports_docket_count(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(btd, "DISCOVERY_DIR", tmp_path)
    monkeypatch.setattr(btd, "_seed_set_names", lambda: set())
    rc = btd.check()
    assert rc == 1
    assert "never produced one" in capsys.readouterr().out

    batch_path = tmp_path / "batch.json"
    batch_path.write_text(json.dumps(_valid_batch(date="2099-05-05")), encoding="utf-8")
    btd.from_json(batch_path, force=False)

    rc = btd.check()
    out = capsys.readouterr().out
    assert rc == 0
    assert "1 discovery docket(s)" in out


def test_check_ignores_non_dated_file_when_reporting_most_recent(tmp_path, monkeypatch, capsys):
    # A non-dated research-pool file (e.g. living36-research-pool.md) sorts after
    # any 2026-... dated docket alphabetically, so picking dockets[-1] blindly
    # reports "most recent: None" instead of the real latest dated docket.
    monkeypatch.setattr(btd, "DISCOVERY_DIR", tmp_path)
    monkeypatch.setattr(btd, "_seed_set_names", lambda: set())

    older = tmp_path / "2026-09-26.md"
    older.write_text("# Daily Tzaddik discovery docket -- 2026-09-26\n", encoding="utf-8")
    newer = tmp_path / "2026-09-28.md"
    newer.write_text("# Daily Tzaddik discovery docket -- 2026-09-28\n", encoding="utf-8")
    pool = tmp_path / "living36-research-pool.md"
    pool.write_text("# Living-36 candidate research pool\n", encoding="utf-8")

    rc = btd.check()
    out = capsys.readouterr().out
    assert rc == 0
    assert "most recent: 2026-09-28." in out
    assert "None" not in out
