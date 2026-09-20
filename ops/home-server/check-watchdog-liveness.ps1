# Watchdog liveness check - is AI-Backends-Healthcheck actually running?
#
# healthcheck.ps1 cannot report its own absence: a PowerShell parse error
# stops the WHOLE file from loading, so a script that fails to run also
# fails to write "I didn't run" anywhere. That is exactly what happened
# 2026-09-08 to 2026-09-19 -- eleven days of LastTaskResult: 1 sitting
# beside a perfectly healthy NextRunTime and NumberOfMissedRuns: 0, plus a
# frozen log whose last line was a normal COMPLETE run, so it did not even
# read as a crash. See ops/home-server/README.md's "Why a 24-hour outage
# produced no alerts" section for the full incident.
#
# This script is deliberately separate from healthcheck.ps1 and depends on
# nothing it defines, so a bug in healthcheck.ps1 cannot take this down
# too. It only reads two local signals and only alerts -- it never
# restarts anything. Report freshness BEFORE content: a watchdog whose log
# is stale is not reporting good news, it is not reporting.
#
# Register as its OWN Task Scheduler entry (see README.md), separate from
# AI-Backends-Healthcheck, so a hang or parse error in the thing being
# watched cannot also stop the thing watching it.
#
# Keep this file ASCII-only - see healthcheck.ps1's header for why.

$ErrorActionPreference = 'SilentlyContinue'

$watchedTaskName = if ($env:HEALTHCHECK_TASK_NAME) { $env:HEALTHCHECK_TASK_NAME } else { 'AI-Backends-Healthcheck' }
$logFile = Join-Path $PSScriptRoot 'logs\healthcheck.log'
$stateFile = Join-Path $PSScriptRoot 'logs\watchdog-liveness-state.json'

# A non-zero LastTaskResult or a stale log means the watchdog is not doing
# its job; neither is something a restart of THIS script can fix, so this
# never re-checks more often than it can usefully say something new.
$staleMinutes = 30
if ($env:WATCHDOG_STALE_MINUTES) {
    [int]::TryParse($env:WATCHDOG_STALE_MINUTES, [ref]$staleMinutes) | Out-Null
}

# Don't re-email about the same still-broken watchdog every tick of this
# checker's own schedule.
$cooldownMinutes = 60
if ($env:WATCHDOG_ALERT_COOLDOWN_MINUTES) {
    [int]::TryParse($env:WATCHDOG_ALERT_COOLDOWN_MINUTES, [ref]$cooldownMinutes) | Out-Null
}

function Get-LivenessState {
    if (Test-Path $stateFile) {
        try {
            $obj = Get-Content -Raw -Path $stateFile | ConvertFrom-Json
            $map = @{}
            foreach ($p in $obj.PSObject.Properties) { $map[$p.Name] = $p.Value }
            return $map
        } catch { return @{} }
    }
    return @{}
}

function Save-LivenessState($state) {
    try { ($state | ConvertTo-Json) | Set-Content -Path $stateFile } catch {}
}

function Test-LivenessAlertDue($state) {
    if (-not $state.ContainsKey('last_alert')) { return $true }
    $last = [datetime]::MinValue
    if ([datetime]::TryParse([string]$state['last_alert'], [ref]$last)) {
        return ((Get-Date) - $last).TotalMinutes -ge $cooldownMinutes
    }
    return $true
}

function Send-LivenessAlert($subject, $body) {
    $apiKey = $env:BREVO_API_KEY
    $to = if ($env:ALERT_TO) { $env:ALERT_TO } else { $env:DIGEST_TO }
    $from = if ($env:ALERT_FROM) { $env:ALERT_FROM } else { $env:DIGEST_FROM }
    if (-not $apiKey -or -not $to -or -not $from) {
        return
    }
    $toName = if ($env:DIGEST_TO_NAME) { $env:DIGEST_TO_NAME } else { 'Silas' }
    $fromName = if ($env:DIGEST_FROM_NAME) { $env:DIGEST_FROM_NAME } else { 'Conductor Ops' }
    $payload = @{
        subject     = $subject
        textContent = $body
        sender      = @{ email = $from; name = $fromName }
        to          = @(@{ email = $to; name = $toName })
    } | ConvertTo-Json -Depth 5
    $headers = @{
        'api-key'      = $apiKey
        'accept'       = 'application/json'
        'Content-Type' = 'application/json'
    }
    try {
        Invoke-RestMethod -Uri 'https://api.brevo.com/v3/smtp/email' `
            -Method Post -Headers $headers -Body $payload -TimeoutSec 30 | Out-Null
    } catch {
        # No log of its own to record this failure to without risking the
        # exact silent-failure shape this script exists to catch.
    }
}

$findings = @()

$taskInfo = Get-ScheduledTaskInfo -TaskName $watchedTaskName -ErrorAction SilentlyContinue
if (-not $taskInfo) {
    $findings += "scheduled task '$watchedTaskName' not found - it may have been removed, renamed, or never registered"
} elseif ($taskInfo.LastTaskResult -ne 0) {
    $findings += "LastTaskResult is $($taskInfo.LastTaskResult) (non-zero), NextRunTime $($taskInfo.NextRunTime) - the task is firing on schedule and failing every time, which looks identical to healthy from the outside"
}

if (Test-Path $logFile) {
    $lastWrite = (Get-Item $logFile).LastWriteTime
    $ageMinutes = (New-TimeSpan -Start $lastWrite -End (Get-Date)).TotalMinutes
    if ($ageMinutes -gt $staleMinutes) {
        $findings += "healthcheck.log last wrote $([math]::Round($ageMinutes, 1)) minutes ago (threshold $staleMinutes) - the watchdog process is not reaching its own tick line, whatever Task Scheduler reports"
    }
} else {
    $findings += "healthcheck.log does not exist at $logFile - the watchdog has never completed a tick, or logs were cleared"
}

$state = Get-LivenessState

if ($findings.Count -gt 0) {
    if (Test-LivenessAlertDue $state) {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $hostName = $env:COMPUTERNAME
        $body = "Watchdog liveness check found $($findings.Count) issue(s) on $hostName as of $stamp`:`n`n" + ($findings -join "`n") + "`n`nThis check only reports - it does not restart anything. See ops/home-server/README.md, 'Why a 24-hour outage produced no alerts', for how to read LastTaskResult and the log-write-age signal by hand."
        Send-LivenessAlert "WATCHDOG LIVENESS: $($findings.Count) issue(s) on $hostName" $body
        $state['last_alert'] = $stamp
        Save-LivenessState $state
    }
} elseif ($state.ContainsKey('last_alert')) {
    # Recovered - clear the cooldown so a future break alerts promptly
    # instead of waiting out a cooldown windows that started before the fix.
    $state.Remove('last_alert')
    Save-LivenessState $state
}
