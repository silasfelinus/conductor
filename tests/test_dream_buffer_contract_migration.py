from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_dream_creative_contract as contract  # noqa: E402


def _steering_file(path: Path, *, built: bool = False) -> None:
    text = (
        "---\n"
        f"slug: {path.stem}\n"
        "title: Test Dream\n"
        "type: dream\n"
        "status: outline\n"
        "proposal: true\n"
        "proposal_date: '2026-09-11'\n"
        "---\n\n"
        "<!-- proposal-data\n{}\n-->\n"
    )
    if built:
        text += "\n<!-- built-data\n{}\n-->\n"
    path.write_text(text, encoding="utf-8")


def test_built_history_is_not_revalidated_after_contract_changes(tmp_path):
    path = tmp_path / "projects" / "dream-cycle" / "backlog" / "2026-09-10-built.md"
    path.parent.mkdir(parents=True)
    _steering_file(path, built=True)

    assert contract.validate_path(path) == []


def test_all_open_scans_the_entire_buffer_not_only_named_files(tmp_path, monkeypatch, capsys):
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    first = backlog / "2026-09-11-first.md"
    second = backlog / "2026-09-12-second.md"
    _steering_file(first)
    _steering_file(second)

    monkeypatch.setattr(contract, "BACKLOG", backlog)
    checked: list[str] = []

    def fake_validate(path: Path) -> list[str]:
        checked.append(path.name)
        return ["stale contract"] if path == first else []

    monkeypatch.setattr(contract, "validate_path", fake_validate)

    assert contract.main(["--all-open"]) == 1
    assert checked == [first.name, second.name]
    captured = capsys.readouterr()
    assert "2 open steering proposal(s) checked, 1 failed" in captured.out
    assert "stale contract" in captured.err
