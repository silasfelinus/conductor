"""Guard: every already_satisfied() definition/override in scripts/*.py must
respect regeneration_forced() (or delegate to one that does).

conductor/t-193, kaizen from t-192 (silasfelinus/conductor#5033). The
choirfish regeneration bug's actual production entrypoint was
consume_art_requests_to_media.py's already_satisfied() wrapper, not
consume_art_requests.py's function the original task note named -- that
wrapper bypasses the underlying function entirely for a kind_robots media
target (a live HEAD check instead of target_path().exists()), so a fix
scoped to only the "obvious" module would have shipped green and left the
real bug live. This was caught by hand-grepping for every already_satisfied
definition once t-192's fix was already written; this guard makes that grep
structural so the NEXT override (or a future fifth consumer script) can't
silently reintroduce the same silent-bypass shape.

A definition passes by calling regeneration_forced(...) directly (the two
canonical implementations, consume_art_requests.py and
consume_art_inspirations.py) or by calling an already-guarded function --
original_already_satisfied(...) or module.regeneration_forced(...) (the two
kind-robots-media wrappers, which import the canonical regeneration_forced()
under the sibling module's namespace). Anything else fails loudly rather
than silently missing the check the way the wrapper's first draft did.
"""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

PY_FILES = sorted(SCRIPTS.glob("*.py"))

# A top-level `def already_satisfied(...):` -- indented ones (methods, nested
# helpers) are out of scope; every real definition in this family is a
# top-level module function or override.
DEF_PAT = re.compile(r"^def already_satisfied\([^)]*\):\s*$")

# Any spelling of "check the force marker" or "delegate to something that
# does" is acceptable -- see module docstring for why both shapes exist.
GUARDED_CALL = re.compile(r"\bregeneration_forced\(|\boriginal_already_satisfied\(")


def find_already_satisfied_defs(text):
    """Return [(start_lineno, body_text)] for every top-level already_satisfied
    definition in a module's source. body_text runs from the def line to the
    next top-level (column-0) statement or end of file, so it captures the
    full function regardless of its own internal indentation."""
    lines = text.splitlines()
    defs = []
    i = 0
    while i < len(lines):
        if DEF_PAT.match(lines[i]):
            start = i
            j = i + 1
            while j < len(lines):
                line = lines[j]
                if line.strip() and not line[0].isspace():
                    break
                j += 1
            defs.append((start + 1, "\n".join(lines[start:j])))
            i = j
        else:
            i += 1
    return defs


class AlreadySatisfiedGuardTests(unittest.TestCase):
    def test_scripts_dir_was_scanned(self):
        """A glob that silently matches nothing would pass every test below."""
        self.assertTrue(PY_FILES, "no .py files found under scripts/")

    def test_every_already_satisfied_definition_respects_regeneration_forced(self):
        offenders = []
        found_any = False
        for path in PY_FILES:
            for lineno, body in find_already_satisfied_defs(
                path.read_text(encoding="utf-8")
            ):
                found_any = True
                if not GUARDED_CALL.search(body):
                    offenders.append(f"{path.relative_to(REPO)}:{lineno}")
        self.assertTrue(
            found_any,
            "no already_satisfied() definition found anywhere under scripts/ -- "
            "the scan pattern itself is broken (conductor/t-192's four known "
            "definitions should always be found)",
        )
        self.assertEqual(
            offenders, [],
            "already_satisfied() defined without checking regeneration_forced() "
            "(or a function that does) -- a force: true entry's stale file/media "
            "would silently count as fulfilled again, the conductor/t-192 "
            "(ruler-hooked choirfish) bug:\n" + "\n".join(offenders),
        )

    def test_known_definitions_are_all_found(self):
        """Pins the exact four call sites t-192 fixed, so a future consumer
        script quietly adding a fifth (or removing one) is visible in the diff
        of this test rather than only in the guard's pass/fail count."""
        found = set()
        for path in PY_FILES:
            if find_already_satisfied_defs(path.read_text(encoding="utf-8")):
                found.add(path.name)
        self.assertEqual(
            found,
            {
                "consume_art_requests.py",
                "consume_art_inspirations.py",
                "consume_art_requests_to_media.py",
                "consume_art_inspirations_to_media.py",
            },
        )

    def test_the_guard_itself_catches_an_unguarded_definition(self):
        """Self-test: prove find_already_satisfied_defs()/GUARDED_CALL actually
        fire, not just that today's four files happen to be clean."""
        sample = (
            "import re\n\n\n"
            "def already_satisfied(entry):\n"
            "    return target_path(entry).exists()\n"
        )
        [(lineno, body)] = find_already_satisfied_defs(sample)
        self.assertEqual(lineno, 4)
        self.assertIsNone(GUARDED_CALL.search(body))

    def test_the_guard_accepts_a_direct_regeneration_forced_check(self):
        sample = (
            "def already_satisfied(entry):\n"
            "    if regeneration_forced(entry):\n"
            "        return False\n"
            "    return target_path(entry).exists()\n"
        )
        [(_lineno, body)] = find_already_satisfied_defs(sample)
        self.assertIsNotNone(GUARDED_CALL.search(body))

    def test_the_guard_accepts_a_delegating_wrapper(self):
        sample = (
            "def already_satisfied(entry):\n"
            "    if requests.regeneration_forced(entry):\n"
            "        return False\n"
            "    if _is_kindrobots_media_target(entry, KIND_ROBOTS_REPO):\n"
            "        return _media_exists(_image_path(entry, KIND_ROBOTS_REPO))\n"
            "    return original_already_satisfied(entry)\n"
        )
        [(_lineno, body)] = find_already_satisfied_defs(sample)
        self.assertIsNotNone(GUARDED_CALL.search(body))

    def test_indented_already_satisfied_definitions_are_ignored(self):
        """Only top-level definitions are in scope -- a method or nested
        helper of the same name isn't part of this family's shared contract."""
        sample = (
            "class Foo:\n"
            "    def already_satisfied(self, entry):\n"
            "        return True\n"
        )
        self.assertEqual(find_already_satisfied_defs(sample), [])
