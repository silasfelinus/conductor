#!/usr/bin/env python3
"""Refresh or check the committed Ruler Hooked runtime fish snapshot.

Run from any directory; defaults to the sibling kind_robots checkout.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = Path('utils/rulerHooked/fish.ts')
RUNTIME_FIXTURE = ROOT / 'tests/fixtures/ruler_hooked_runtime_fish.json'
SOURCE = 'silasfelinus/kind_robots/utils/rulerHooked/fish.ts'


def parse_runtime_fish_slugs(source):
    """Read only the runtime roster; fail closed on missing or duplicate IDs."""
    match = re.search(
        r'export\s+const\s+RULER_HOOKED_FISH\s*:[^=]*=\s*\[(.*?)^\]',
        source,
        re.MULTILINE | re.DOTALL,
    )
    assert match, 'RULER_HOOKED_FISH array declaration not found'
    slugs = re.findall(r"^\s+slug:\s*'([^']+)'", match.group(1), re.MULTILINE)
    assert slugs, 'RULER_HOOKED_FISH array contains no parsed slugs'
    duplicates = sorted(slug for slug, count in Counter(slugs).items() if count > 1)
    assert not duplicates, f'duplicate runtime fish slugs: {duplicates}'
    return slugs


def snapshot_text(slugs):
    return json.dumps({'source': SOURCE, 'slugs': slugs}, indent=2) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--write', action='store_true')
    parser.add_argument('--app-root', type=Path, default=ROOT.parent / 'kind_robots')
    parser.add_argument('--fixture', type=Path, default=RUNTIME_FIXTURE)
    args = parser.parse_args(argv)
    runtime = args.app_root / RUNTIME_PATH
    try:
        slugs = parse_runtime_fish_slugs(runtime.read_text(encoding='utf-8'))
        expected = snapshot_text(slugs)
        existing = (
            args.fixture.read_text(encoding='utf-8')
            if args.fixture.exists()
            else None
        )
        if existing == expected:
            print(f'Ruler Hooked runtime snapshot current ({len(slugs)} fish)')
            return 0
        if args.check:
            print(
                f'Ruler Hooked runtime snapshot stale or missing: {args.fixture}; '
                'run with --write',
                file=sys.stderr,
            )
            return 1
        args.fixture.parent.mkdir(parents=True, exist_ok=True)
        args.fixture.write_text(expected, encoding='utf-8')
        print(f'Wrote {len(slugs)} runtime fish to {args.fixture}')
        return 0
    except (OSError, UnicodeError, AssertionError) as exc:
        print(f'Cannot refresh Ruler Hooked runtime fish: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
