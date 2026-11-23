"""Keep every Ruler Hooked fish in the authored roster and art queue exactly once."""

from collections import Counter
from pathlib import Path
import re

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / 'projects/ruler-hooked/fish/vertical-slice.yaml'
REQUESTS = ROOT / 'projects/art-prompts.yaml'
PREFIX = 'ruler-hooked-fish-'


def assert_exact_fish_ids(roster_slugs, request_ids):
    expected = Counter(PREFIX + slug for slug in roster_slugs)
    actual = Counter(request_ids)
    missing = sorted((expected - actual).elements())
    extra = sorted((actual - expected).elements())
    assert not missing and not extra, (
        f'fish art parity: missing={missing}, extra_or_duplicate={extra}'
    )


def test_roster_and_staged_fish_requests_are_bijective():
    fish = yaml.safe_load(ROSTER.read_text(encoding='utf-8'))['fish']
    slugs = [row['slug'] for row in fish]
    assert len(slugs) == len(set(slugs)), 'duplicate fish roster slugs'
    staged = yaml.safe_load(REQUESTS.read_text(encoding='utf-8'))['requests']
    requests = [
        row for row in staged
        if row.get('id', '').startswith(PREFIX)
    ]
    assert_exact_fish_ids(slugs, [row['id'] for row in requests])
    for row in requests:
        assert row.get('source') == 'ruler-hooked', row['id']
        assert row.get('lane') == 'fish', row['id']
        assert row.get('target_repo') == 'silasfelinus/kind_robots', row['id']


def test_fish_parity_diagnoses_missing_orphan_and_duplicate():
    with pytest.raises(AssertionError, match='missing=.*fish-b'):
        assert_exact_fish_ids(['a', 'b'], [PREFIX + 'a'])
    with pytest.raises(AssertionError, match='extra_or_duplicate=.*fish-z'):
        assert_exact_fish_ids(['a'], [PREFIX + 'a', PREFIX + 'z'])
    with pytest.raises(AssertionError, match='extra_or_duplicate=.*fish-a'):
        assert_exact_fish_ids(['a'], [PREFIX + 'a', PREFIX + 'a'])


def test_runtime_fish_slugs_match_when_app_checkout_is_present():
    runtime = ROOT.parent / 'kind_robots/utils/rulerHooked/fish.ts'
    if not runtime.is_file():
        pytest.skip('kind_robots sibling checkout unavailable in this runner')
    source = runtime.read_text(encoding='utf-8')
    array = source.split('export const RULER_HOOKED_FISH:', 1)[1].split(
        '\n]', 1
    )[0]
    runtime_slugs = re.findall(r"^    slug: '([^']+)'", array, re.MULTILINE)
    roster_slugs = [
        row['slug']
        for row in yaml.safe_load(ROSTER.read_text(encoding='utf-8'))['fish']
    ]
    assert Counter(runtime_slugs) == Counter(roster_slugs), (
        f'runtime fish differ from roster: '
        f'missing={sorted((Counter(roster_slugs) - Counter(runtime_slugs)).elements())}, '
        f'extra={sorted((Counter(runtime_slugs) - Counter(roster_slugs)).elements())}'
    )
