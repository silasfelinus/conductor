"""Suite-wide fixtures.

Both things in here keep the test suite off the network. See
`tests/fake_resource_registry.py` for the measurements that motivated it
(conductor/t-124).
"""

import urllib.error
import urllib.request

import pytest

import scripts.consume_art_queue as consumer

from tests.fake_resource_registry import FAKE_RESOURCE_INDEX


@pytest.fixture(autouse=True)
def _stub_resource_registry(monkeypatch):
    """Pin the Resource registry for every test in the suite.

    `scripts/consume_art_queue.py` ends with `sys.modules[__name__] = _core`, so
    `consumer` IS the core module and this patches the real global that
    `_load_resource_index` checks first -- which means no test reaches the
    network for it.

    Autouse and suite-wide on purpose. This started as a fixture inside
    `test_consume_art_queue.py`, which is exactly why that file's tests were the
    ones that did NOT fail when production 502'd on 2026-09-01: the protection
    existed but only one file had it. A test should not have to know that
    building a job hits an HTTP API in order to be insulated from it.

    A test that genuinely wants the unstubbed lookup can still
    `monkeypatch.setattr(consumer, "_RESOURCE_INDEX", None)` and take over from
    there; monkeypatch unwinds this fixture's value afterwards either way.
    """
    monkeypatch.setattr(consumer, "_RESOURCE_INDEX", dict(FAKE_RESOURCE_INDEX))
    yield


_REAL_URLOPEN = urllib.request.urlopen


@pytest.fixture(autouse=True, scope="session")
def _offline_facet_catalog():
    """Answer every Kind Robots /api/facets fetch with "unreachable".

    `build_brief(catalog=None)` reaches `fetch_facet_catalog()`, which pages
    through `https://kindrobots.org/api/facets` for every taxonomy with a 12 s
    timeout each, then falls back to `FALLBACK_FACETS`. The dream tests call it
    that way, so while the site was hanging on 2026-10-08 three test files took
    23 of the suite's 25 minutes and CI was cancelled at its time limit with
    every test green (conductor#5779). Refusing the request at once sends the
    same code down the same fallback path in microseconds.

    Session-scoped so it is in place before module-scoped fixtures run too
    (test_author_dream_proposal's `_live_brief` builds its brief once per
    module, ahead of any function-scoped fixture). Only facet URLs are refused;
    anything else goes to the real `urlopen`, and a test that stubs `urlopen`
    itself still wins, since its monkeypatch is applied after this one.
    """

    def urlopen(request, *args, **kwargs):
        url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
        if "/api/facets" in url:
            raise urllib.error.URLError("facet catalog is offline in tests")
        return _REAL_URLOPEN(request, *args, **kwargs)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(urllib.request, "urlopen", urlopen)
        yield
