import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "mce", Path(__file__).resolve().parents[1] / "scripts" / "measure_character_embodiment.py"
)
mce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mce)


def _write(d: Path, name: str, looks):
    body = json.dumps({"characters": [{"look": t} for t in looks]})
    (d / name).write_text(f"---\nx: 1\n---\n<!-- proposal-data\n{body}\n-->\n", encoding="utf-8")


def test_split_by_cutoff_and_axes(tmp_path, monkeypatch):
    _write(tmp_path, "2026-09-10-a.md", ["a stocky man in a coat"])
    _write(tmp_path, "2026-09-20-b.md", ["a 60-year-old woman with long silver hair, smiling"])
    (tmp_path / "README.md").write_text("no block")
    monkeypatch.setattr(mce, "BACKLOG", tmp_path)
    base, new = mce.load("2026-09-15")
    assert len(base) == 1 and len(new) == 1
    assert mce.pct(new, mce.AXES["explicit age"]) == 100.0
    assert mce.pct(new, mce.AXES["long hair"]) == 100.0
    assert mce.pct(base, mce.AXES["hair mentioned"]) == 0.0
    assert mce.pct(base, mce.AXES["coat"]) == 100.0
