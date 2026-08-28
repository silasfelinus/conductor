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

# The heartbeat line below writes on every tick (~288/day at 5-minute spacing),
# which is the point -- a silent log cannot answer "did the watchdog run?".
# Trim so that never becomes a problem: keep the newest $logKeepLines once the
# file passes $logTrimAt.
$logTrimAt = 8000
$logKeepLines = 4000
function Trim-Log {
    try {
        if (-not (Test-Path $logFile)) { return }
        $lines = @(Get-Content -Path $logFile)
        if ($lines.Count -le $logTrimAt) { return }
        $lines[-$logKeepLines..-1] | Set-Content -Path $logFile
    } catch {}
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
$watchdogExitCode = 0

# --- pm2 visibility ----------------------------------------------------------
# Read pm2's process list ONCE, and distinguish "pm2 says this app is stopped"
# from "pm2 told us nothing at all". They are not the same, and conflating them
# silently disabled this entire watchdog.
#
# Windows PowerShell 5.1's ConvertFrom-Json treats object keys case-insensitively.
# PM2 jlist includes the process environment, where Windows can legitimately
# contain both username and USERNAME. Parsing the raw jlist therefore throws on
# valid PM2 JSON. Project the list through Node first, keeping only name/status;
# Node is already a PM2 dependency and its JSON parser preserves case-distinct
# keys. PowerShell only sees the small collision-free snapshot.
$pm2List = $null
$pm2Error = ''
$pm2Command = Get-Command 'pm2.cmd' -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $pm2Command) {
    $pm2Command = Get-Command 'pm2' -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
}

if (-not $pm2Command) {
    $pm2Error = 'pm2 executable is not visible to the scheduled task'
} else {
    $pm2Raw = (& $pm2Command.Source jlist 2>&1 | Out-String)
    $pm2ExitCode = $LASTEXITCODE
    if ($pm2ExitCode -ne 0) {
        $pm2Error = "pm2 jlist exited $pm2ExitCode`: $($pm2Raw.Trim())"
    } elseif ([string]::IsNullOrWhiteSpace($pm2Raw)) {
        $pm2Error = 'pm2 jlist returned no output'
    } else {
        $snapshotHelper = Join-Path $PSScriptRoot 'pm2-jlist-snapshot.js'
        $nodeCommand = Get-Command 'node.exe' -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if (-not $nodeCommand) {
            $nodeCommand = Get-Command 'node' -CommandType Application -ErrorAction SilentlyContinue |
                Select-Object -First 1
        }

        if (-not $nodeCommand) {
            $pm2Error = 'node executable is not visible to the scheduled task'
        } elseif (-not (Test-Path -LiteralPath $snapshotHelper)) {
            $pm2Error = "pm2 snapshot helper is missing: $snapshotHelper"
        } else {
            $pm2Snapshot = ($pm2Raw | & $nodeCommand.Source $snapshotHelper 2>&1 | Out-String)
            $snapshotExitCode = $LASTEXITCODE
            if ($snapshotExitCode -ne 0) {
                $pm2Error = "pm2 jlist snapshot failed ($snapshotExitCode): $($pm2Snapshot.Trim())"
            } else {
                try {
                    $pm2List = $pm2Snapshot | ConvertFrom-Json
                } catch {
                    $pm2Error = "safe pm2 snapshot could not be decoded: $($_.Exception.Message)"
                }
            }
        }
    }
}

$pm2Names = @()
if ($pm2List) { $pm2Names = @($pm2List | ForEach-Object { $_.name } | Where-Object { $_ }) }
$pm2Visible = $pm2Names.Count -gt 0

# Heartbeat. Previously a healthy tick wrote NOTHING, so an empty log could not
# be told apart from a task that never ran -- which is precisely the question
# that mattered on 2026-08-27. One line per tick, ~288/day, trimmed below.
Write-Log "tick as $($env:USERNAME) - pm2 apps: $(if ($pm2Visible) { $pm2Names -join ', ' } else { 'NONE VISIBLE' })"

if (-not $pm2Visible) {
    $watchdogExitCode = 2
    $reason = if ($pm2Error) { $pm2Error } else { 'pm2 returned an empty process list' }
    Write-Log "pm2 unavailable ($reason) - backend liveness checks are BLIND; remaining checks continue; run will exit 2"
    if (Test-AlertDue $alertState 'pm2-invisible') {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        Send-Alert "WATCHDOG BLIND on $hostName - pm2 unavailable" `
            "healthcheck.ps1 ran at $stamp on $hostName as user '$($env:USERNAME)' but PM2 could not provide a usable process list ($reason). Backend liveness checks cannot safely run. Share/render checks will still run where possible, and this watchdog invocation will exit 2 instead of falsely reporting success. If pm2 is not found, verify the task's Run as account and PATH; PM2's daemon is per-user."
        $alertState['pm2-invisible'] = $stamp
        Save-AlertState $alertState
    }
}

# --- Share watchdog ----------------------------------------------------------
# Runs FIRST, because both watchdogs below misread a dead model mount.
#
# On 2026-08-26 alexandria rebooted several times during a disk replacement.
# Every SMB mapping on this box went Unavailable, and ComfyUI kept answering
# /system_stats with a 200 the whole time - so the liveness probe was happy,
# while every render died at 'hostbuf_file_reader_read failed' and the queue
# drained PENDING into FAILED at ~5/min. The render watchdog below WOULD have
# fired on that spike and restarted comfyui straight back into the dead mount,
# repeatedly, achieving nothing.
#
# This block: detects the dead share, optionally remaps it, and - the part that
# actually matters - restarts comfyui once the share RETURNS. ComfyUI caches
# folder_paths' filename lists and does not re-enumerate just because the mount
# came back; without that restart it keeps failing reads against names it cached
# while the share was down. That is the step whose omission made this look
# intermittent on both 2026-08-25 and 2026-08-26.
#
# Config (setx, then open a NEW shell):
#   setx KR_SHARE_PROBE_PATH "Z:\ai\models"          REM what to probe
#   setx KR_SHARE_UNC        "\\192.168.7.172\pc"     REM optional: remap target
# KR_SHARE_UNC is only usable when the probe path starts with a drive letter.
# Leave it unset to detect and alert without touching the mapping. The remap
# needs credentials in Credential Manager (cmdkey /add) - see README.
$shareProbePath = if ($env:KR_SHARE_PROBE_PATH) { $env:KR_SHARE_PROBE_PATH } else { 'Z:\ai\models' }
$shareUnc = $env:KR_SHARE_UNC

function Test-ShareReadable($path) {
    # Enumerate; do not settle for Test-Path. A stale SMB handle can satisfy
    # Test-Path and still fail every read - that exact split (ComfyUI holding a
    # dead handle while an interactive 'dir' said the path did not exist) is
    # what made the 2026-08-25 outage so hard to name. An empty directory is
    # readable and must pass: enumerating nothing is not an error.
    if (-not $path) { return $false }
    try {
        $null = Get-ChildItem -LiteralPath $path -Force -ErrorAction Stop |
            Select-Object -First 1
        return $true
    } catch {
        return $false
    }
}

function Repair-ShareMapping($path, $unc) {
    if (-not $unc) { return $false }
    if ($path -notmatch '^([A-Za-z]:)') {
        Write-Log "share watchdog: $path is not a drive letter - cannot remap"
        return $false
    }
    $letter = $Matches[1]
    Write-Log "share watchdog: remapping $letter to $unc"
    # stdin from NUL on purpose. 'net use' prompts for a username when no
    # credential is cached, and a Task Scheduler run has no console to answer
    # with - it would block until the task timeout instead of failing. With
    # stdin closed it returns an error immediately and we alert instead.
    & cmd.exe /c "net use $letter /delete /y < NUL" 2>&1 | Out-Null
    & cmd.exe /c "net use $letter $unc /persistent:yes < NUL" 2>&1 | Out-Null
    return (Test-ShareReadable $path)
}

$shareOk = $true
if ($shareProbePath) {
    $shareOk = Test-ShareReadable $shareProbePath
    $sharePrev = if ($alertState.ContainsKey('share_state')) { [string]$alertState['share_state'] } else { 'ok' }
    $shareStamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

    if (-not $shareOk) {
        Write-Log "share watchdog: $shareProbePath is NOT readable"
        if (Repair-ShareMapping $shareProbePath $shareUnc) {
            $shareOk = $true
            Write-Log "share watchdog: remap restored $shareProbePath"
        }
    }

    if ($shareOk) {
        if ($sharePrev -eq 'down') {
            Write-Log "share watchdog: share is back - restarting comfyui to rebuild folder_paths"
            & pm2 restart comfyui | Out-Null
            Send-Alert "RECOVERED: model share is back on $hostName - comfyui restarted" `
                "The model share $shareProbePath was unreadable and is now answering again as of $shareStamp on $hostName. comfyui has been restarted so folder_paths rebuilds its cached filename lists - without that it would keep failing reads against the names it cached while the share was down. Renders should resume on the next claim. No action needed unless this repeats."
        }
        $alertState['share_state'] = 'ok'
        Save-AlertState $alertState
    } else {
        $alertState['share_state'] = 'down'
        Save-AlertState $alertState
        if (Test-AlertDue $alertState 'share-watchdog') {
            $remapNote = if ($shareUnc) { "An automatic remap to $shareUnc was attempted and did not restore it." } else { "No KR_SHARE_UNC is configured, so no remap was attempted." }
            Send-Alert "MODEL SHARE DOWN on $hostName - renders are paused" `
                "The model share $shareProbePath is unreadable as of $shareStamp on $hostName. $remapNote ComfyUI will keep answering its API while failing every render, so treat a green /system_stats as meaningless here. kr-relay's own share gate should be holding claims (look for 'NOT claiming jobs' in its log); if that gate is not armed, the pending queue is being converted into failures right now. Check the NAS is up and the mapping is present (net use)."
            $alertState['share-watchdog'] = $shareStamp
            Save-AlertState $alertState
        } else {
            Write-Log "share watchdog: alert suppressed (within $($cooldownMinutes)-min cooldown)"
        }
    }
}

foreach ($t in $targets) {
    if (-not $pm2Visible) { continue }

    # Only police processes pm2 believes are online - a deliberate `pm2 stop`
    # (e.g. freeing the GPU) must not be fought by the watchdog. Reuses the
    # single $pm2List read above rather than shelling out per target: three
    # `pm2 jlist` calls per tick was wasteful, and worse, each one could fail
    # independently and be silently swallowed.
    $status = $pm2List |
        Where-Object { $_.name -eq $t.Name } |
        Select-Object -ExpandProperty pm2_env -ErrorAction SilentlyContinue

    if (-not $status) {
        Write-Log "$($t.Name): not in pm2's list - not started on this box?"
        continue
    }
    if ($status.status -ne 'online') {
        Write-Log "$($t.Name): pm2 status is '$($status.status)' - leaving it alone"
        continue
    }

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
                    "The art pipeline logged $deltaFailed new FAILED job(s) and only $deltaDone new DONE since the last check (all-time totals now DONE=$done FAILED=$failed) as of $stamp on $hostName. ComfyUI is still answering its API, so this is a RENDER failure, not a hang. The model share $shareProbePath is $(if ($shareOk) { 'readable' } else { 'NOT READABLE - that is almost certainly the cause; see the share watchdog alert' }). If the share is fine, check the newest FAILED job's error (bad model/encoder/checkpoint or a broken custom node). See /api/art/queue/stats recentFailed and pm2 logs."

                # RESTART comfyui at most once per cooldown, in case it's a wedged
                # GPU/driver state a restart can shake loose - but never while the
                # model share is down. On 2026-08-26 a dead mount produced exactly
                # this spike shape (+failures, no successes) with ComfyUI answering
                # normally; restarting it back into an unreadable share fixes
                # nothing and just churns the GPU. The share watchdog above owns
                # that case and restarts comfyui when the mount actually returns.
                if (-not $shareOk) {
                    Write-Log "render watchdog: comfyui restart suppressed (model share is down - see share watchdog)"
                } elseif (Test-AlertDue $alertState 'render-watchdog-restart') {
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

Trim-Log
exit $watchdogExitCode
