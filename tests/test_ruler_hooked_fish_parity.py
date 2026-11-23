"""Validate queued Ruler Hooked fish art without rejecting delivered assets."""

from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / 'projects/ruler-hooked/fish/vertical-slice.yaml'
REQUESTS = ROOT / 'projects/art-prompts.yaml'
PREFIX = 'ruler-hooked-fish-'
RUNTIME_FIXTURE = ROOT / 'tests/fixtures/ruler_hooked_runtime_fish.json'
REFRESH_SCRIPT = ROOT / 'scripts/refresh_ruler_hooked_runtime_fish.py'

sys.path.insert(0, str(ROOT / 'scripts'))
from refresh_ruler_hooked_runtime_fish import parse_runtime_fish_slugs, snapshot_text


def assert_valid_staged_fish_ids(roster_slugs, request_ids):
    expected = set(PREFIX + slug for slug in roster_slugs)
    actual = Counter(request_ids)
    extra = sorted(id for id in actual if id not in expected)
    duplicates = sorted(id for id, count in actual.items() if count > 1)
    assert not extra and not duplicates, (
        f'fish art queue: orphan={extra}, duplicate={duplicates}'
    )


def test_staged_fish_requests_are_unique_and_belong_to_roster():
    fish = yaml.safe_load(ROSTER.read_text(encoding='utf-8'))['fish']
    slugs = [row['slug'] for row in fish]
    assert len(slugs) == len(set(slugs)), 'duplicate fish roster slugs'
    staged = yaml.safe_load(REQUESTS.read_text(encoding='utf-8'))['requests']
    requests = [
        row for row in staged
        if row.get('id', '').startswith(PREFIX)
    ]
    assert_valid_staged_fish_ids(slugs, [row['id'] for row in requests])
    for row in requests:
        assert row.get('source') == 'ruler-hooked', row['id']
        assert row.get('lane') == 'fish', row['id']
        assert row.get('target_repo') == 'silasfelinus/kind_robots', row['id']


def test_queue_accepts_pruned_requests_after_delivery():
    # Completed art requests are removed from art-prompts.yaml by design.
    assert_valid_staged_fish_ids(['a', 'b'], [PREFIX + 'a'])
    assert_valid_staged_fish_ids(['a', 'b'], [])


def test_queue_diagnoses_orphan_and_duplicate():
    with pytest.raises(AssertionError, match='orphan=.*fish-z'):
        assert_valid_staged_fish_ids(['a'], [PREFIX + 'a', PREFIX + 'z'])
    with pytest.raises(AssertionError, match='duplicate=.*fish-a'):
        assert_valid_staged_fish_ids(['a'], [PREFIX + 'a', PREFIX + 'a'])


def test_runtime_parser_rejects_missing_or_empty_roster():
    with pytest.raises(AssertionError, match='declaration not found'):
        parse_runtime_fish_slugs('export const OTHER = []\n')
    with pytest.raises(AssertionError, match='no parsed slugs'):
        parse_runtime_fish_slugs('export const RULER_HOOKED_FISH: Fish[] = [\n]\n')


def test_runtime_parser_reads_only_the_fish_array():
    source = (
        'export const RULER_HOOKED_FISH: Fish[] = [\n'
        '  {\n'
        "    slug: 'rainbow-trout',\n"
        "    habitat: { slug: 'nested-not-a-fish' },\n"
        '  },\n'
        '  {\n'
        "    slug: 'moon-carp',\n"
        '    tags: [1, 2],\n'
        '  },\n'
        ']\n'
        'export const OTHER = [\n'
        "  { slug: 'not-a-fish' },\n"
        ']\n'
    )
    assert parse_runtime_fish_slugs(source) == ['rainbow-trout', 'moon-carp']


def test_committed_runtime_fish_fixture_matches_roster():
    fixture_slugs = json.loads(RUNTIME_FIXTURE.read_text(encoding='utf-8'))['slugs']
    roster_slugs = [
        row['slug']
        for row in yaml.safe_load(ROSTER.read_text(encoding='utf-8'))['fish']
    ]
    assert Counter(fixture_slugs) == Counter(roster_slugs), (
        'committed runtime fish fixture differs from Conductor roster'
    )


def test_runtime_fish_slugs_match_when_app_checkout_is_present():
    runtime = ROOT.parent / 'kind_robots/utils/rulerHooked/fish.ts'
    if not runtime.is_file():
        pytest.skip('kind_robots sibling checkout unavailable in this runner')
    runtime_slugs = parse_runtime_fish_slugs(runtime.read_text(encoding='utf-8'))
    roster_slugs = [
        row['slug']
        for row in yaml.safe_load(ROSTER.read_text(encoding='utf-8'))['fish']
    ]
    fixture_slugs = json.loads(RUNTIME_FIXTURE.read_text(encoding='utf-8'))['slugs']
    assert Counter(runtime_slugs) == Counter(fixture_slugs), (
        f'runtime fish differ from committed fixture: '
        f'missing={sorted((Counter(fixture_slugs) - Counter(runtime_slugs)).elements())}, '
        f'extra={sorted((Counter(runtime_slugs) - Counter(fixture_slugs)).elements())}'
    )
    assert Counter(runtime_slugs) == Counter(roster_slugs), (
        'runtime fish differ from Conductor roster'
    )


def test_runtime_parser_rejects_duplicates():
    source = (
        'export const RULER_HOOKED_FISH: Fish[] = [\n'
        "  {\n    slug: 'same-fish',\n  },\n"
        "  {\n    slug: 'same-fish',\n  },\n"
        ']\n'
    )
    with pytest.raises(AssertionError, match='duplicate runtime fish slugs'):
        parse_runtime_fish_slugs(source)


def test_refresh_runtime_snapshot_cli(tmp_path):
    app = tmp_path / 'app'
    runtime = app / 'utils/rulerHooked/fish.ts'
    runtime.parent.mkdir(parents=True)
    fixture = tmp_path / 'fixtures/runtime.json'
    fixture.parent.mkdir()
    fixture.write_text(snapshot_text(['old-fish']), encoding='utf-8')
    runtime.write_text(
        'export const RULER_HOOKED_FISH: Fish[] = [\n'
        "  {\n    slug: 'rainbow-trout',\n  },\n"
        "  {\n    slug: 'moon-carp',\n  },\n"
        ']\n',
        encoding='utf-8',
    )

    def run(mode):
        return subprocess.run(
            [
                sys.executable, str(REFRESH_SCRIPT), mode,
                '--app-root', str(app), '--fixture', str(fixture),
            ],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )

    original = fixture.read_bytes()
    stale = run('--check')
    assert stale.returncode == 1
    assert 'stale' in stale.stderr
    assert fixture.read_bytes() == original
    assert run('--write').returncode == 0
    assert fixture.read_text(encoding='utf-8') == snapshot_text(
        ['rainbow-trout', 'moon-carp']
    )
    assert run('--check').returncode == 0
    refreshed = fixture.read_bytes()
    modified_at = fixture.stat().st_mtime_ns
    assert run('--write').returncode == 0
    assert fixture.stat().st_mtime_ns == modified_at

    runtime.write_text('export const OTHER = []\n', encoding='utf-8')
    assert run('--write').returncode == 2
    assert fixture.read_bytes() == refreshed
    runtime.unlink()
    assert run('--check').returncode == 2
    assert fixture.read_bytes() == refreshed
