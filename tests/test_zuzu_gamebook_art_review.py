"""Round 16 review verifies *delivered* private art; no auto-promotion."""
import pytest
import yaml
from PIL import Image

from scripts import review_zuzu_gamebook_round16 as review


def test_round16_has_nine_distinct_completed_jobs():
    subjects = yaml.safe_load(review.LEDGER.read_text())
    data = list(review.cells(subjects))
    assert len(data) == 9
    assert sorted(job for _, job, _ in data) == list(range(44243, 44252))
    assert sorted(image for _, _, image in data) == list(range(252163, 252172))


def test_private_media_url_is_origin_bound():
    base = "https://kindrobots.org"
    assert review.safe_media_url(base, "/images/private/file.webp") == base + "/images/private/file.webp"
    with pytest.raises(ValueError):
        review.safe_media_url(base, "https://example.com/image.webp")
    with pytest.raises(ValueError):
        review.safe_media_url(base, "//example.com/image.webp")
    with pytest.raises(ValueError):
        review.safe_media_url(base, "http://kindrobots.org/image.webp")
    with pytest.raises(ValueError):
        review.safe_media_url(base, "")


def test_contact_sheet_produces_no_file_without_explicit_call(tmp_path):
    assert not list(tmp_path.iterdir())
    image = Image.new("RGB", (1344, 768), "navy")
    subjects = yaml.safe_load(review.LEDGER.read_text())["subjects"]
    loaded = [(s, 44243 + i, 252163 + i, image, "abc123") for i, s in enumerate(subjects)]
    path = tmp_path / "review.jpg"
    review.review_sheet(loaded, path)
    with Image.open(path) as rendered:
        assert rendered.size == (1170, 906)
