"""Suite-wide fixtures.

The one thing in here keeps the test suite off the network. See
`tests/fake_resource_registry.py` for the measurements that motivated it
(conductor/t-124).
"""

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
