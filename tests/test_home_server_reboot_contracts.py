"""Source-level guards for Windows-only reboot recovery scripts.

CI does not execute Windows PowerShell, so these tests protect the decision
contracts that review found in conductor#3145.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "ops" / "home-server"


def test_preflight_unknown_is_indeterminate_not_success():
    text = (ROOT / "preflight.ps1").read_text(encoding="ascii")
    assert "elseif ($script:unknown)" in text
    unknown_branch = text.split("elseif ($script:unknown)", 1)[1].split("elseif ($script:warn)", 1)[0]
    assert "exit 2" in unknown_branch
    assert "exit 0" not in unknown_branch


def test_restore_check_fails_readable_mapping_to_wrong_unc():
    text = (ROOT / "restore-shares.ps1").read_text(encoding="ascii")
    marker = "readable but points at $($existing.Unc)"
    assert marker in text
    assert 'Write-Log "$letter -> $unc : BROKEN (readable but points at $($existing.Unc))"' in text
    assert "$failed += $letter" in text
    assert "remapping to configured target" in text


def test_restore_missing_credential_is_nonzero():
    text = (ROOT / "restore-shares.ps1").read_text(encoding="ascii")
    assert "$credentialFailures += $h" in text
    assert 'Write-Log "missing stored credential: $($credentialFailures -join \', \')"' in text
    assert "if ($failed.Count -or $credentialFailures.Count) { exit 1 }" in text
