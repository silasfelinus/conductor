"""Guards for ops/home-server/restore-shares.ps1's `net use` fallback.

CI has no Windows PowerShell, so these cannot execute the script. They cover the
two things that can be checked from the source and that actually broke:

1. A structural guard that `Get-CurrentMappings` copies its regex captures into
   locals before running a second match. `$Matches` is a single global table
   that every successful `-match` overwrites, so reading `$Matches[1]`/`[2]`
   after the status probe keys the map by the status word ("Unavailable") and
   stores a null UNC -- silently emptying the whole table on the one path this
   fallback exists for, a box without `Get-SmbMapping`. Caught in review of
   conductor#3145, 2026-08-29.

2. The two regexes, ported to Python and run against representative `net use`
   output, so a mangled character class fails here rather than on the box.

Neither replaces running the script on Windows; they catch the classes of
mistake that are invisible until a share is already down.
"""

import re
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "ops" / "home-server" / "restore-shares.ps1"


def _function_body(name):
    text = SCRIPT.read_text(encoding="ascii")
    marker = f"function {name}"
    start = text.index(marker)
    # Functions in this file are separated by a top-level closing brace.
    end = text.index("\n}\n", start)
    return text[start:end]


def test_net_use_fallback_copies_captures_before_the_second_match():
    body = _function_body("Get-CurrentMappings")
    fallback = body[body.index("foreach ($line in (& net use"):]

    # The captures must be read into locals on the lines right after the first
    # match, and the constructed object must use those locals.
    assert "$letter = $Matches[1].ToUpper()" in fallback
    assert "$unc = $Matches[2]" in fallback
    assert "$map[$letter] = " in fallback
    assert "Unc    = $unc" in fallback

    # And nothing may read $Matches after the status probe overwrites it.
    lines = fallback.splitlines()
    status_probe = next(
        i for i, line in enumerate(lines) if "$status = $Matches[1] }" in line
    )
    later = lines[status_probe + 1 :]
    offenders = [line.strip() for line in later if "$Matches" in line]
    assert not offenders, f"$Matches read after it is overwritten: {offenders}"


# Representative `net use` output, including the Unavailable rows this box
# actually produced on 2026-08-29 and a blank-status row (the status column is
# empty in some transitional states, which is why the regex anchors on the
# letter and the UNC rather than on a status word).
NET_USE_SAMPLE = """New connections will be remembered.


Status       Local     Remote                    Network

-------------------------------------------------------------------------------
Unavailable  V:        \\\\192.168.7.172\\personal  Microsoft Windows Network
Unavailable  W:        \\\\192.168.7.172\\backups   Microsoft Windows Network
OK           Y:        \\\\192.168.7.172\\appdata   Microsoft Windows Network
             Z:        \\\\192.168.7.172\\pc        Microsoft Windows Network
The command completed successfully.
"""

# The PowerShell regexes, transcribed. PowerShell escapes a literal backslash in
# a single-quoted regex as \\, which is \\\\ for a UNC's two leading slashes.
ROW = re.compile(r"([A-Za-z]:)\s+(\\\\[^\s]+)")
STATUS = re.compile(r"^\s*(\S+)\s+[A-Za-z]:")


def _parse(sample):
    found = {}
    for line in sample.splitlines():
        row = ROW.search(line)
        if not row:
            continue
        letter, unc = row.group(1).upper(), row.group(2)
        status_match = STATUS.search(line)
        status = status_match.group(1) if status_match else "Unknown"
        found[letter] = (unc, status)
    return found


def test_regexes_parse_representative_net_use_output():
    found = _parse(NET_USE_SAMPLE)
    assert sorted(found) == ["V:", "W:", "Y:", "Z:"]
    assert found["V:"] == ("\\\\192.168.7.172\\personal", "Unavailable")
    assert found["Y:"] == ("\\\\192.168.7.172\\appdata", "OK")
    # Blank status column must still yield the mapping, with status unknown.
    assert found["Z:"] == ("\\\\192.168.7.172\\pc", "Unknown")


def test_header_and_footer_lines_are_not_mistaken_for_mappings():
    found = _parse(NET_USE_SAMPLE)
    assert "RE:" not in found  # from "Remote"
    assert len(found) == 4
