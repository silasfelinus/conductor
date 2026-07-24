# Health watchdog for the pm2-managed art backends.
# pm2 restarts a process that EXITS; this catches one that is alive but hung
# (API stops answering) and restarts it via pm2. Schedule via Task Scheduler
# every 5 minutes - see README.md.
#
# It also emails an alert when it has to restart something, so a failing/hung
# ComfyUI reaches you instead of being silently self-healed. A second watchdog
# (see "Render-failure watchdog" below) catches a ComfyUI that answers fine but
# fails every render - it watches the ArtJob queue's FAILED/DONE counts via
# /api/art/queue/stats (needs KR_API_TOKEN) and alerts on a failure burst.
# Alerts reuse the same Brevo secrets as the daily digest; set these once on the
# box (setx), then open a NEW shell:
#   setx BREVO_API_KEY "your-brevo-key"
#   setx DIGEST_TO     "silasfelinus@gmail.com"     (or ALERT_TO)
#   setx DIGEST_FROM   "ops@your-verified-sender"   (or ALERT_FROM)
# With no BREVO_API_KEY set, the watchdog still restarts - it just doesn't email.
#
# Keep this file ASCII-only: Windows PowerShell 5.1 reads a no-BOM script as the
# system ANSI codepage, so any UTF-8 punctuation (em-dash, smart quotes) inside a
# string literal corrupts parsing. Plain ASCII avoids the whole problem.

$ErrorActionPreference = 'SilentlyContinue'

$targets = @(
    @{ Name = 'comfyui';  Url = 'http://127.0.0.1:8188/system_stats' },
    @{ Name = 'sd-webui'; Url = 'http://127.0.0.1:7860/sdapi/v1/progress' }
)

$logFile = Join-Path $PSScriptRoot 'logs\healthcheck.log'
$alertStateFile = Join-Path $PSScriptRoot 'logs\alert-state.json'
New-Item -ItemType Directory -Force -Path (Split-Path $logFile) | Out-Null

# Don't re-email about the same backend more than once per this many minutes,
# so a flapping process can't spam the inbox every 5-minute tick.
$cooldownMinutes = 60
if ($env:ALERT_COOLDOWN_MINUTES) {
    [int]::TryParse($env:ALERT_COOLDOWN_MINUTES, [ref]$cooldownMinutes) | Out-Null
}

function Write-Log($msg) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Add-Content -Path $logFile -Value "$stamp  $msg"
}

function Get-AlertState {
    if (Test-Path $alertStateFile) {
        try {
            $obj = Get-Content -Raw -Path $alertStateFile | ConvertFrom-Json
            $map = @{}
            foreach ($p in $obj.PSObject.Properties) { $map[$p.Name] = $p.Value }
            return $map
        } catch { return @{} }
    }
    return @{}
}

function Save-AlertState($state) {
    try { ($state | ConvertTo-Json) | Set-Content -Path $alertStateFile } catch {}
}

# Returns $true if we haven't alerted about $name within the cooldown window.
function Test-AlertDue($state, $name) {
    if (-not $state.ContainsKey($name)) { return $true }
    $last = [datetime]::MinValue
    if ([datetime]::TryParse([string]$state[$name], [ref]$last)) {
        return ((Get-Date) - $last).TotalMinutes -ge $cooldownMinutes
    }
    return $true
}

function Send-Alert($subject, $body) {
    $apiKey = $env:BREVO_API_KEY
    $to = if ($env:ALERT_TO) { $env:ALERT_TO } else { $env:DIGEST_TO }
    $from = if ($env:ALERT_FROM) { $env:ALERT_FROM } else { $env:DIGEST_FROM }
    if (-not $apiKey -or -not $to -or -not $from) {
        Write-Log "alert skipped (no BREVO_API_KEY / ALERT_TO / ALERT_FROM set): $subject"
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
        Write-Log "alert emailed: $subject"
    } catch {
        Write-Log "alert email FAILED ($($_.Exception.Message)): $subject"
    }
}

$alertState = Get-AlertState
$hostName = $env:COMPUTERNAME

foreach ($t in $targets) {
    # Only police processes pm2 believes are online - a deliberate `pm2 stop`
    # (e.g. freeing the GPU) must not be fought by the watchdog.
    $status = (& pm2 jlist | ConvertFrom-Json) |
        Where-Object { $_.name -eq $t.Name } |
        Select-Object -ExpandProperty pm2_env -ErrorAction SilentlyContinue

    if (-not $status -or $status.status -ne 'online') { continue }

    $ok = $false
    try {
        $resp = Invoke-WebRequest -Uri $t.Url -TimeoutSec 20 -UseBasicParsing
        if ($resp.StatusCode -eq 200) { $ok = $true }
    } catch { $ok = $false }

    if (-not $ok) {
        Write-Log "$($t.Name): health probe failed ($($t.Url)) - restarting via pm2"
        & pm2 restart $t.Name | Out-Null

        # Confirm whether it came back before deciding what to say, then alert
        # (rate-limited by the cooldown).
        Start-Sleep -Seconds 8
        $recovered = $false
        try {
            $after = Invoke-WebRequest -Uri $t.Url -TimeoutSec 20 -UseBasicParsing
            if ($after.StatusCode -eq 200) { $recovered = $true }
        } catch { $recovered = $false }

        if (Test-AlertDue $alertState $t.Name) {
            $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            if ($recovered) {
                Send-Alert "WARNING: $($t.Name) was hung on $hostName - auto-restarted" `
                    "The $($t.Name) backend stopped answering $($t.Url) and the health watchdog restarted it via pm2. It is answering again as of $stamp. No action needed unless this repeats."
            } else {
                Send-Alert "DOWN: $($t.Name) on $hostName - restart did not recover" `
                    "The $($t.Name) backend stopped answering $($t.Url); the watchdog ran 'pm2 restart $($t.Name)' at $stamp but it is still not responding. This one likely needs a look (GPU/driver, disk, crash-loop). Check pm2 logs and logs\healthcheck.log on $hostName."
            }
            $alertState[$t.Name] = $stamp
            Save-AlertState $alertState
        } else {
            Write-Log "$($t.Name): restart alert suppressed (within $($cooldownMinutes)-min cooldown)"
        }
    }
}

# --- Render-failure watchdog -------------------------------------------------
# The liveness probes above catch a ComfyUI that stops ANSWERING. They do NOT
# catch a ComfyUI that answers fine but fails every render (a bad model/encoder
# config, a corrupt checkpoint, a broken custom node) - the API stays 200 while
# the ArtJob queue quietly fills with FAILED. This block watches the pipeline's
# own scoreboard (/api/art/queue/stats) and reacts to a burst of new failures
# that are NOT accompanied by new successes.
#
# Policy (set with Silas 2026-07-24): EMAIL ALWAYS on a detected spike (he wants
# to know every time, even asleep), but RESTART comfyui at most once per cooldown
# (a restart won't fix a config bug, so hammering it is pointless - one nudge in
# case it's a transient GPU/driver wedge, then leave it for a human).
#
# Detection uses per-tick DELTAS of the all-time DONE/FAILED counts, so it is
# self-normalizing: re-enqueueing failures (FAILED drops) yields a negative delta
# and never false-alarms; only NEW failures outpacing NEW successes trip it.
$krBase = if ($env:KR_BASE_URL) { $env:KR_BASE_URL.TrimEnd('/') } else { 'https://kind-robots.vercel.app' }
$krToken = $env:KR_API_TOKEN

$failSpikeThreshold = 5
if ($env:FAILURE_SPIKE_THRESHOLD) {
    [int]::TryParse($env:FAILURE_SPIKE_THRESHOLD, [ref]$failSpikeThreshold) | Out-Null
}

if (-not $krToken) {
    Write-Log "render watchdog skipped (no KR_API_TOKEN set)"
} else {
    $stats = $null
    try {
        $stats = Invoke-RestMethod -Uri "$krBase/api/art/queue/stats" -TimeoutSec 30 `
            -Headers @{ 'Authorization' = "Bearer $krToken"; 'accept' = 'application/json' }
    } catch {
        Write-Log "render watchdog: stats fetch FAILED ($($_.Exception.Message))"
    }

    if ($stats -and $stats.data -and $stats.data.queueDepth) {
        $depth = $stats.data.queueDepth
        $done = 0; $failed = 0
        if ($depth.PSObject.Properties['DONE'])   { $done   = [int]$depth.DONE }
        if ($depth.PSObject.Properties['FAILED']) { $failed = [int]$depth.FAILED }

        $haveBaseline = $alertState.ContainsKey('render_last_done') -and $alertState.ContainsKey('render_last_failed')
        $lastDone = 0; $lastFailed = 0
        if ($haveBaseline) {
            [int]::TryParse([string]$alertState['render_last_done'], [ref]$lastDone) | Out-Null
            [int]::TryParse([string]$alertState['render_last_failed'], [ref]$lastFailed) | Out-Null
        }

        # Always roll the baseline forward for the next tick.
        $alertState['render_last_done'] = $done
        $alertState['render_last_failed'] = $failed

        if ($haveBaseline) {
            $deltaDone = $done - $lastDone
            $deltaFailed = $failed - $lastFailed
            Write-Log "render watchdog: DONE $lastDone->$done (+$deltaDone), FAILED $lastFailed->$failed (+$deltaFailed)"

            # Spike = a meaningful burst of NEW failures that outnumber NEW successes.
            if (($deltaFailed -ge $failSpikeThreshold) -and ($deltaFailed -gt $deltaDone)) {
                $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

                # EMAIL ALWAYS (not cooldown-gated). Naturally self-limits: emails
                # stop once failures stop accruing (delta returns to ~0).
                Send-Alert "RENDER FAILURES: +$deltaFailed failed on $hostName (only +$deltaDone done)" `
                    "The art pipeline logged $deltaFailed new FAILED job(s) and only $deltaDone new DONE since the last check (all-time totals now DONE=$done FAILED=$failed) as of $stamp on $hostName. ComfyUI is still answering its API, so this is a RENDER config failure, not a hang - check the newest FAILED job's error (bad model/encoder/checkpoint or a broken custom node). See /api/art/queue/stats recentFailed and pm2 logs."

                # RESTART comfyui at most once per cooldown, in case it's a wedged
                # GPU/driver state a restart can shake loose.
                if (Test-AlertDue $alertState 'render-watchdog-restart') {
                    Write-Log "render watchdog: failure spike (+$deltaFailed) - restarting comfyui via pm2"
                    & pm2 restart comfyui | Out-Null
                    $alertState['render-watchdog-restart'] = $stamp
                } else {
                    Write-Log "render watchdog: comfyui restart suppressed (within $($cooldownMinutes)-min cooldown)"
                }
            }
        } else {
            Write-Log "render watchdog: baseline set (DONE=$done FAILED=$failed) - deltas start next tick"
        }

        Save-AlertState $alertState
    }
}
