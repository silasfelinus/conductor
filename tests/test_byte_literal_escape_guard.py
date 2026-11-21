"""Prevent accidental double-escaped hex bytes in scripts and test fixtures.

A literal written as b"\\\\x10" contains four ASCII characters, not the
single byte expected by binary file signatures. Tokenization avoids flagging
comments, docstrings, and ordinary text that explains the failure mode.
"""

from __future__ import annotations

import io
from pathlib import Path
import re
import tokenize

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCANNED_DIRS = ("scripts", "tests")
# Add an exact (relative path, line) only when a deliberately literal
# backslash-x sequence is needed, with a comment explaining the exception.
ALLOWLIST: set[tuple[str, int]] = set()
DOUBLE_ESCAPE = re.compile(r"(?<!\\)\\\\\\\\x[0-9a-fA-F]{2}")
BYTE_PREFIX = re.compile(r"(?i)^(?:br|rb|b)[\"']")


def suspicious_literals(source: str) -> list[int]:
    """Return source lines containing double-escaped hex inside byte tokens."""
    matches = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if (
                token.type == tokenize.STRING
                and BYTE_PREFIX.match(token.string)
                and DOUBLE_ESCAPE.search(token.string)
            ):
                matches.append(token.start[0])
    except (tokenize.TokenError, IndentationError):
        # Syntax errors belong to the Python parser; do not hide them here.
        raise
    return matches


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ('value = b"' + chr(92) + 'x10"', []),
        ('value = b"' + chr(92) * 2 + 'x10"', [1]),
        ('# value = b"' + chr(92) * 2 + 'x10"', []),
        ('description = "b' + chr(92) * 2 + 'x10"', []),
        ('value = rb"' + chr(92) * 2 + 'x10"', [1]),
    ],
)
def test_byte_escape_detector(source: str, expected: list[int]) -> None:
    assert suspicious_literals(source) == expected


def test_no_double_escaped_hex_bytes_in_python_sources() -> None:
    violations = []
    for directory in SCANNED_DIRS:
        for path in sorted((ROOT / directory).rglob("*.py")):
            relative = path.relative_to(ROOT).as_posix()
            for line in suspicious_literals(path.read_text(encoding="utf-8")):
                if (relative, line) not in ALLOWLIST:
                    violations.append(f"{relative}:{line}")
    assert not violations, (
        "Double-escaped hex in bytes literals (use one source backslash "
        "for actual byte values): " + ", ".join(violations)
    )
