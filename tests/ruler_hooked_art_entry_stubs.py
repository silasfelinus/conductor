"""Hermetic Ruler Hooked art queue entry factories shared by the CLI tests.

An added *_entries producer must explicitly join this contract; otherwise all
tests using it fail before silently depending on checkout-specific content.
"""

ENTRY_FACTORY_NAMES = frozenset(
    {
        "alt_vista_entries",
        "card_entries",
        "concept_entries",
        "console_entries",
        "ending_entries",
        "expression_entries",
        "fish_entries",
        "layer_entries",
        "reward_entries",
        "ruler_entries",
    }
)


def stub_art_entry_factories(monkeypatch, builder, entries_by_factory=None):
    """Replace every discovered entry producer with deterministic fresh rows."""
    available = {
        name
        for name, value in vars(builder).items()
        if name.endswith("_entries") and callable(value)
    }
    if available != ENTRY_FACTORY_NAMES:
        missing = sorted(ENTRY_FACTORY_NAMES - available)
        unexpected = sorted(available - ENTRY_FACTORY_NAMES)
        raise AssertionError(
            f"Art entry factory contract drift: missing={missing}, "
            f"unexpected={unexpected}. Update this fixture with each new lane."
        )

    entries_by_factory = entries_by_factory or {}
    unknown = set(entries_by_factory) - ENTRY_FACTORY_NAMES
    if unknown:
        raise AssertionError(f"Unknown fixture entry factories: {sorted(unknown)}")

    for name in sorted(ENTRY_FACTORY_NAMES):
        rows = tuple(dict(row) for row in entries_by_factory.get(name, ()))

        def build(*_args, _rows=rows):
            return [dict(row) for row in _rows]

        monkeypatch.setattr(builder, name, build)
