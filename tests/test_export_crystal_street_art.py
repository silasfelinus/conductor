import pytest

pytest.importorskip("PIL")

import scripts.export_crystal_street_art as exp  # noqa: E402


def test_reviewed_rejects_are_not_exported(tmp_path, monkeypatch):
    written = []

    class FakeImage:
        def save(self, dest, *args, **kwargs):
            written.append(dest.name)

    monkeypatch.setattr(exp, "load_image", lambda image_id: FakeImage())
    monkeypatch.setattr(exp, "fit", lambda image, max_edge: image)
    done = {"krea2": {"status": "DONE", "art_image_id": 1}}
    subjects = [
        {"key": "a", "asset": "scenes/kept", "art": done, "verdict": "keep: matches the beat"},
        {"key": "b", "asset": "scenes/rejected", "art": done, "verdict": "redo: wrong room"},
        {"key": "c", "asset": "scenes/unreviewed", "art": done},
        {"key": "d", "asset": "scenes/unrendered", "art": {}},
    ]
    exp.export(subjects, tmp_path, 1024)
    assert sorted(written) == ["kept.webp", "unreviewed.webp"]
