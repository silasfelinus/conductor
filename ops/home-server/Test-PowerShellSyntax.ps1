# Does every .ps1 in this folder actually PARSE?
#
# 2026-09-19: healthcheck.ps1 carried three `Write-Log "$name: ..."` lines.
# PowerShell reads `$name:` as a scope- or drive-qualified variable (the
# `$env:PATH` / `$script:foo` syntax) and raises
# InvalidVariableReferenceWithDrive. That is a PARSE error, so it does not fail
# those three lines - it stops the whole file from loading. The render box's
# watchdog therefore did nothing at all from 2026-09-08 00:36 to 2026-09-19:
# every 5-minute trigger launched, PowerShell refused the file, the action
# returned exit code 1, and the log recorded nothing, because no line of the
# script ever ran. Task Scheduler reported a healthy NextRunTime throughout.
#
# Nothing in CI could have caught it. The runners are Linux, so the structural
# guards in tests/ assert on source TEXT - ASCII-only bytes, brace balance, a
# regex per known bug. healthcheck.ps1 was valid ASCII and perfectly balanced.
# It simply did not parse. Text guards catch the PREVIOUS class of bug; only a
# real parser catches the next one.
#
# Run it here before you push, or let the powershell-syntax workflow run it:
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Test-PowerShellSyntax.ps1
#
# Exits 0 when every file parses, 1 otherwise, naming file, line, column and
# message for each error.
#
# Parse with WINDOWS POWERSHELL 5.1, not pwsh 7. 5.1 is what the render box
# runs, and a file that parses under 7 can still fail under 5.1. The workflow
# pins `shell: powershell` for the same reason.
#
# Keep this file ASCII-only, like its neighbours: Windows PowerShell 5.1 reads a
# no-BOM script as the system ANSI codepage, so UTF-8 punctuation in a string
# literal corrupts parsing.

[CmdletBinding()]
param(
    # Defaults to this script's own folder, which is where every .ps1 lives.
    [string]$Path
)

$ErrorActionPreference = 'Stop'

if (-not $Path) { $Path = $PSScriptRoot }

# -Recurse: this used to stop at $Path's own top level, so a .ps1 moved into a
# subfolder (e.g. lib/Restart-ComfySupervised.ps1, conductor/t-185) would be
# skipped by this checker even though the powershell-syntax workflow's own
# paths filter (ops/home-server/**.ps1) still triggered the run - a green
# check that had quietly stopped checking the new file, the same shape of gap
# this whole script exists to close for the workflow's coverage.
$files = @(Get-ChildItem -Path $Path -Filter '*.ps1' -File -Recurse | Sort-Object FullName)

if ($files.Count -eq 0) {
    # A glob that silently matches nothing would "pass" forever.
    Write-Host "NO .ps1 FILES FOUND under $Path - refusing to report success."
    exit 1
}

Write-Host "PowerShell $($PSVersionTable.PSVersion) parsing $($files.Count) file(s) under $Path"
Write-Host ''

$basePath = (Resolve-Path $Path).Path.TrimEnd('\', '/')

$failed = 0
foreach ($file in $files) {
    $errors = $null
    $tokens = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $file.FullName, [ref]$tokens, [ref]$errors)

    $label = $file.FullName
    if ($label.StartsWith($basePath)) {
        $label = $label.Substring($basePath.Length).TrimStart('\', '/')
    }

    if ($errors -and $errors.Count -gt 0) {
        $failed++
        Write-Host "FAIL  $label - $($errors.Count) parse error(s)"
        foreach ($err in $errors) {
            $start = $err.Extent.StartLineNumber
            $col = $err.Extent.StartColumnNumber
            Write-Host "        ${label}:${start}:${col}  $($err.Message)"
            Write-Host "          > $($err.Extent.Text)"
        }
        Write-Host ''
    } else {
        Write-Host "ok    $label"
    }
}

Write-Host ''
if ($failed -gt 0) {
    Write-Host "$failed of $($files.Count) file(s) do not parse. A parse error disables the ENTIRE script, not just its line."
    exit 1
}

Write-Host "All $($files.Count) file(s) parse."
exit 0
