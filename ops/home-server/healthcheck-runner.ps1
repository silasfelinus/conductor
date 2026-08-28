# Task Scheduler entry point for healthcheck.ps1.
#
# Windows PowerShell 5.1's ConvertFrom-Json treats object keys case-insensitively.
# PM2's jlist includes the process environment, where Windows can legitimately
# contain both username and USERNAME. Parsing the raw jlist therefore throws even
# though PM2 returned valid JSON. Intercept only `pm2 jlist`, project it through
# Node (which PM2 already requires), and hand healthcheck.ps1 a small safe object.
# All other pm2 commands are delegated unchanged.
#
# Keep this file ASCII-only for the same Windows PowerShell 5.1 reason documented
# in healthcheck.ps1.

$healthcheck = Join-Path $PSScriptRoot 'healthcheck.ps1'
$snapshotHelper = Join-Path $PSScriptRoot 'pm2-jlist-snapshot.js'

# Resolve the real executables before defining the pm2 function that shadows the
# command name for the dot-sourced watchdog.
$pm2Command = Get-Command 'pm2.cmd' -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $pm2Command) {
    $pm2Command = Get-Command 'pm2' -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
}
$nodeCommand = Get-Command 'node.exe' -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $nodeCommand) {
    $nodeCommand = Get-Command 'node' -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
}

function pm2 {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$RemainingArgs
    )

    if (-not $pm2Command) {
        Write-Error 'pm2 executable is not visible to the scheduled task'
        return
    }

    if ($RemainingArgs.Count -gt 0 -and $RemainingArgs[0] -eq 'jlist') {
        $raw = (& $pm2Command.Source @RemainingArgs 2>&1 | Out-String)
        $pm2ExitCode = $LASTEXITCODE
        if ($pm2ExitCode -ne 0) {
            Write-Error "pm2 jlist exited $pm2ExitCode`: $($raw.Trim())"
            return
        }
        if ([string]::IsNullOrWhiteSpace($raw)) {
            Write-Error 'pm2 jlist returned no output'
            return
        }
        if (-not $nodeCommand) {
            Write-Error 'node executable is not visible to the scheduled task'
            return
        }
        if (-not (Test-Path -LiteralPath $snapshotHelper)) {
            Write-Error "pm2 snapshot helper is missing: $snapshotHelper"
            return
        }

        $snapshot = ($raw | & $nodeCommand.Source $snapshotHelper 2>&1 | Out-String)
        $snapshotExitCode = $LASTEXITCODE
        if ($snapshotExitCode -ne 0) {
            Write-Error "pm2 jlist snapshot failed ($snapshotExitCode): $($snapshot.Trim())"
            return
        }

        $snapshot.Trim()
        return
    }

    & $pm2Command.Source @RemainingArgs
}

# Dot-source so this wrapper's pm2 function is visible inside healthcheck.ps1 and
# so we can inspect $pm2Visible afterward. The underlying watchdog still performs
# all share/render checks even if PM2 discovery fails.
. $healthcheck

# Fail closed. Task Scheduler must not record a successful watchdog run when the
# liveness checks were skipped because PM2 could not be enumerated.
if (-not $pm2Visible) {
    exit 2
}
exit 0
