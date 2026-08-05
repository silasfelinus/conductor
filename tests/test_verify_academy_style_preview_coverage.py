"""
Tests for verify_academy_style_preview_coverage.py — the ai-art-academy/t-055
academy-style-preview coverage checker. Uses small synthetic academyStyles.ts /
art-prompts.yaml fixtures rather than the real (growing) files so these tests
don't churn every time a lane-4 cycle adds a movement.
"""

from pathlib import Path

import scripts.verify_academy_style_preview_coverage as coverage


SAMPLE_ACADEMY_STYLES_TS = """
export const academyStyles: AcademyStyle[] = [
  {
    slug: 'no-preview-style',
    name: 'No Preview Style',
    era: 'c. 1000',
  },
  {
    slug: 'delivered-style',
    name: 'Delivered Style',
    era: 'c. 1500',
    previewImageSrc: '/images/academy/styles/delivered-style.webp',
  },
  {
    slug: 'queued-style',
    name: 'Queued Style',
    era: 'c. 1600',
    previewImageSrc: '/images/academy/styles/queued-style.webp',
  },
  {
    slug: 'gap-style',
    name: 'Gap Style',
    era: 'c. 1700',
    previewImageSrc: '/images/academy/styles/gap-style.webp',
  },
]
"""

SAMPLE_ART_PROMPTS_YAML = """
images: []
inspirations: []
requests:
  - id: kind-robots-academy-style-preview-queued-style
    source: ai-art-academy-style-preview
    status: pending
    target_repo: silasfelinus/kind_robots
    image_path: public/images/academy/styles/queued-style.webp
    prompt: 'a prompt'
  - id: kind-robots-missing-image
    source: kind-robots-missing-image
    status: pending
    target_repo: silasfelinus/kind_robots
    image_path: public/images/userUpload-unrelated.png
    prompt: 'unrelated entry, should never be treated as an academy slug'
"""


def test_load_academy_style_slugs_only_returns_entries_with_preview():
    slugs = coverage.load_academy_style_slugs(SAMPLE_ACADEMY_STYLES_TS)
    assert slugs == {
        "delivered-style": "delivered-style",
        "queued-style": "queued-style",
        "gap-style": "gap-style",
    }
    assert "no-preview-style" not in slugs


def test_load_academy_style_slugs_raises_on_no_slugs():
    try:
        coverage.load_academy_style_slugs("nothing here")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "no `slug:" in str(exc)


def test_load_art_prompts_slugs_filters_to_academy_prefix_and_keys_by_image_path():
    slugs = coverage.load_art_prompts_slugs(SAMPLE_ART_PROMPTS_YAML)
    assert list(slugs.keys()) == ["queued-style"]
    assert slugs["queued-style"]["status"] == "pending"


def test_load_art_prompts_slugs_raises_without_requests_key():
    try:
        coverage.load_art_prompts_slugs("images: []\n")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "requests:" in str(exc)


def test_build_report_offline_classifies_delivered_as_gap_without_live_check():
    """Offline mode can't distinguish delivered-and-pruned from a real gap --
    both `delivered-style` and `gap-style` have no art-prompts.yaml entry, so
    both surface as gaps. This is the documented offline-mode limitation."""
    style_slugs = coverage.load_academy_style_slugs(SAMPLE_ACADEMY_STYLES_TS)
    prompt_slugs = coverage.load_art_prompts_slugs(SAMPLE_ART_PROMPTS_YAML)
    report = coverage.build_report(style_slugs, prompt_slugs, offline=True)

    assert report["offline"] is True
    assert report["delivered_count"] == 0
    assert {row["slug"] for row in report["gaps"]} == {"delivered-style", "gap-style"}
    assert {row["slug"] for row in report["queued"]} == {"queued-style"}
    assert "live_status" not in report["gaps"][0]


def test_build_report_live_check_separates_delivered_from_real_gap(monkeypatch):
    def fake_check_live(slug, timeout=10.0):
        return {"delivered-style": 200, "queued-style": 404, "gap-style": 404}[slug]

    monkeypatch.setattr(coverage, "check_live", fake_check_live)

    style_slugs = coverage.load_academy_style_slugs(SAMPLE_ACADEMY_STYLES_TS)
    prompt_slugs = coverage.load_art_prompts_slugs(SAMPLE_ART_PROMPTS_YAML)
    report = coverage.build_report(style_slugs, prompt_slugs, offline=False)

    assert report["delivered_count"] == 1
    assert report["delivered"][0]["slug"] == "delivered-style"
    assert report["queued_count"] == 1
    assert report["queued"][0]["slug"] == "queued-style"
    assert report["gap_count"] == 1
    assert report["gaps"][0]["slug"] == "gap-style"
    assert report["gaps"][0]["live_status"] == 404


def test_build_report_live_check_treats_network_failure_like_undelivered(monkeypatch):
    monkeypatch.setattr(coverage, "check_live", lambda slug, timeout=10.0: None)

    style_slugs = {"gap-style": "gap-style"}
    report = coverage.build_report(style_slugs, prompt_slugs={}, offline=False)

    assert report["gap_count"] == 1
    assert report["gaps"][0]["live_status"] is None


def test_main_offline_smoke_against_real_files(monkeypatch, capsys):
    """Smoke test against the real academyStyles.ts / art-prompts.yaml, catching
    schema drift early. Offline so it never touches the network."""
    if not coverage.ACADEMY_STYLES_PATH.exists():
        return  # no local kind_robots checkout in this environment -- skip silently
    monkeypatch.setattr(
        "sys.argv", ["verify_academy_style_preview_coverage.py", "--offline"]
    )
    exit_code = coverage.main()
    assert exit_code == 0


def test_main_writes_json(tmp_path, monkeypatch):
    academy_styles = tmp_path / "academyStyles.ts"
    academy_styles.write_text(SAMPLE_ACADEMY_STYLES_TS)
    art_prompts = tmp_path / "art-prompts.yaml"
    art_prompts.write_text(SAMPLE_ART_PROMPTS_YAML)

    monkeypatch.setattr(coverage, "ACADEMY_STYLES_PATH", academy_styles)
    monkeypatch.setattr(coverage, "ART_PROMPTS_PATH", art_prompts)

    out = tmp_path / "report.json"
    monkeypatch.setattr(
        "sys.argv",
        ["verify_academy_style_preview_coverage.py", "--offline", "--json", str(out)],
    )
    exit_code = coverage.main()
    assert exit_code == 0
    assert out.exists()
    assert "gap-style" in out.read_text()


def test_main_strict_exits_1_on_real_gap(tmp_path, monkeypatch):
    academy_styles = tmp_path / "academyStyles.ts"
    academy_styles.write_text(SAMPLE_ACADEMY_STYLES_TS)
    art_prompts = tmp_path / "art-prompts.yaml"
    art_prompts.write_text(SAMPLE_ART_PROMPTS_YAML)

    monkeypatch.setattr(coverage, "ACADEMY_STYLES_PATH", academy_styles)
    monkeypatch.setattr(coverage, "ART_PROMPTS_PATH", art_prompts)
    monkeypatch.setattr(
        "sys.argv", ["verify_academy_style_preview_coverage.py", "--offline", "--strict"]
    )
    assert coverage.main() == 1


def test_main_missing_academy_styles_file_returns_1(tmp_path, monkeypatch):
    monkeypatch.setattr(coverage, "ACADEMY_STYLES_PATH", tmp_path / "does-not-exist.ts")
    monkeypatch.setattr(
        "sys.argv", ["verify_academy_style_preview_coverage.py", "--offline"]
    )
    assert coverage.main() == 1
