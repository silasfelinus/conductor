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

# Port is not redundant with Url: the watchdog probes the URL, but when the app
# is crash-looping it needs to ask a different question - who OWNS this port -
# and a listener check takes a bare port number, not an endpoint path.
$targets = @(
    @{ Name = 'comfyui';  Url = 'http://127.0.0.1:8188/system_stats'; Port = 8188 }
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

# How many pm2 restarts within one 5-minute tick count as a crash loop rather
# than an ordinary restart. A healthy deploy or a watchdog-driven restart moves
# this by 1; the 2026-09-02 ComfyUI loop moved it by roughly 9 per tick (a
# ~31-second cycle). 3 sits well clear of both.
$crashLoopRestarts = 3
if ($env:CRASH_LOOP_RESTARTS) {
    [int]::TryParse($env:CRASH_LOOP_RESTARTS, [ref]$crashLoopRestarts) | Out-Null
}

# How large a gap between consecutive ticks counts as this watchdog having been
# ABSENT rather than merely slow. The task runs every 5 minutes, so two missed
# ticks is the smallest gap that cannot be a single slow run.
$tickGapAlertMinutes = 12
if ($env:TICK_GAP_ALERT_MINUTES) {
    [int]::TryParse($env:TICK_GAP_ALERT_MINUTES, [ref]$tickGapAlertMinutes) | Out-Null
}

# How long to wait for 'pm2 jlist' before giving up on it. Must stay well under
# the scheduled task's 5-minute interval, or a slow pm2 lets each run overlap
# the next and Task Scheduler starts killing them.
$pm2TimeoutSeconds = 60
if ($env:PM2_JLIST_TIMEOUT_SECONDS) {
    [int]::TryParse($env:PM2_JLIST_TIMEOUT_SECONDS, [ref]$pm2TimeoutSeconds) | Out-Null
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

# --- Port ownership ----------------------------------------------------------
# "Why is it crash-looping?" has one answer this watchdog could not previously
# give, and it is a common one: the port is already taken.
#
# 2026-09-06: pm2's comfyui died a few seconds into every start with
#   [ERROR] Port 8188 is already in use on address 127.0.0.1.
# ComfyUI logs that and calls sys.exit, so there is no traceback to find - the
# 'read the FIRST exception' advice in the crash-loop alert below leads nowhere,
# because there is no exception at all. Worse, the HTTP liveness probe is GREEN
# throughout: whoever holds the port answers /system_stats perfectly well, so
# every signal except the pm2 restart counter says the box is fine. And once
# pm2 gives up at max_restarts, the engine that IS running is unsupervised -
# when it eventually dies, nothing brings it back.
#
# Naming the pid that owns the port turns all of that into one line.
function Get-PortListenerPid($port) {
    # Two implementations on purpose. Get-NetTCPConnection is the clean one, but
    # it THROWS rather than returning nothing when no connection matches, and it
    # is missing from some trimmed installs. netstat has shipped with every
    # Windows there has ever been.
    try {
        $conn = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction Stop |
            Select-Object -First 1
        if ($conn) { return [int]$conn.OwningProcess }
    } catch {}

    try {
        $line = netstat -ano -p TCP |
            Where-Object { $_ -match "^\s*TCP\s+\S+:$port\s" -and $_ -match 'LISTENING' } |
            Select-Object -First 1
        if ($line) {
            $fields = ([string]$line).Trim() -split '\s+'
            return [int]$fields[-1]
        }
    } catch {}

    return $null
}

function Get-PortOwnerReport($port, $expectedPid) {
    if (-not $port) { return '' }

    $ownerPid = Get-PortListenerPid $port
    if (-not $ownerPid) { return "nothing is listening on port $port" }

    # Identify it well enough to act on: a start time says whether it predates
    # the crash loop, and the command line separates 'a second ComfyUI' from
    # 'some unrelated python' - which decides whether killing it is safe.
    $desc = "pid $ownerPid"
    try {
        $proc = Get-Process -Id $ownerPid -ErrorAction Stop
        $desc = "$($proc.ProcessName) (pid $ownerPid"
        try { $desc = "$desc, started $($proc.StartTime.ToString('yyyy-MM-dd HH:mm:ss'))" } catch {}
        $desc = "$desc)"
    } catch {}
    try {
        $cim = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $ownerPid" -ErrorAction Stop
        if ($cim -and $cim.CommandLine) {
            $cmd = [string]$cim.CommandLine
            if ($cmd.Length -gt 200) { $cmd = $cmd.Substring(0, 200) + '...' }
            $desc = "$desc cmdline: $cmd"
        }
    } catch {}

    if ($expectedPid -and [int]$expectedPid -gt 0) {
        if ([int]$expectedPid -eq [int]$ownerPid) {
            return "port $port is held by pm2's own supervised process ($desc) - the port is not the problem"
        }
        return "PORT SQUATTER: port $port is held by $desc, which is NOT the process pm2 is supervising (pid $expectedPid). pm2's copy cannot bind and will keep dying at startup until that process is gone. Verify with 'netstat -ano | findstr :$port', then stop it (a stray engine from an old .bat or a pm2 daemon that lost track of it: 'taskkill /PID <pid> /F') and 'pm2 restart <ecosystem file> --only <app> --update-env'."
    }

    return "port $port is held by $desc while pm2 is running NO process for this app - that engine is unsupervised, so nothing will restart it when it dies. Stop it ('taskkill /PID $ownerPid /F') and start the pm2 app so the port belongs to a supervised process again."
}

# --- Sleep and resume --------------------------------------------------------
# A gap in this log has always had two possible meanings and no way to tell them
# apart: the watchdog stopped running (2026-09-01: healthcheck.log ends dead at
# 02:26:07 and stays empty for 37 hours), or the whole BOX stopped running. The
# second is not hypothetical either - the COMFY heartbeat series on
# kindrobots.org shows this box going quiet for 143 minutes (2026-09-06
# 00:15-02:39 local) and 200 minutes (2026-09-05 11:46-15:06), plus a two-hour
# stretch delivering exactly one beat every ~7 minutes when the relay's own
# thread sleeps 60s and can block at most 85s. A frozen process cannot report
# that it was frozen, and every on-box signal - pm2 uptime, the watchdog log,
# ComfyUI's own log - simply skips the missing time without comment.
#
# Windows does say, in the System log. Kernel-Power 42 is "entering sleep" and
# 107 is "resumed"; reading them needs no elevation. Matching them against the
# gap answers, in the log itself, which of the two happened.
#
# Note which way that went on 2026-09-06: sleep was the first hypothesis and the
# System log REFUTED it. Standby and hibernate are both 0 on AC here, and the
# newest 42/107 pair was 7/6 - two months before the gaps. So the value of this
# block is not that it confirms sleep; it is that it settles the question either
# way, in one line, at the moment the gap appears, instead of leaving a hole in
# the log that every future reader has to re-litigate.
function Get-PowerTransitions($since) {
    try {
        return @(Get-WinEvent -ErrorAction Stop -MaxEvents 20 -FilterHashtable @{
            LogName      = 'System'
            ProviderName = 'Microsoft-Windows-Kernel-Power'
            Id           = 42, 107
            StartTime    = $since
        } | Sort-Object TimeCreated)
    } catch {
        # Get-WinEvent THROWS when nothing matches, which is the common case on
        # a healthy box, so this catch is the normal path and not an error path.
        return @()
    }
}

$alertState = Get-AlertState
$hostName = $env:COMPUTERNAME
$watchdogExitCode = 0

# The FIRST thing this script writes, before anything that can block.
#
# The 'tick' heartbeat further down was added 2026-08-27 to answer "did the
# watchdog run?", but it sits AFTER the pm2 block - so it only proves a run got
# PAST pm2. A run that starts and then hangs writes nothing at all, and in the
# log that is indistinguishable from a run that never happened.
#
# Not hypothetical. On 2026-09-01 the log stopped dead at 02:26:07 and stayed
# empty for 37+ hours while Task Scheduler reported the task running every 5
# minutes with LastTaskResult 1073807364 (0x40010004, "terminated") - every run
# was being started and then killed before it finished. Two lines instead of
# one turns that from a mystery into a fact: 'run starting' with no 'tick'
# after it means the pm2 block hung.
Write-Log "run starting as $($env:USERNAME)"

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
    # Bounded, because an unbounded call here can wedge the whole watchdog.
    # 'pm2 jlist' talks to the per-user pm2 daemon over a local socket and will
    # sit there indefinitely if that daemon is unresponsive, or has to be
    # spawned for an account that has none.
    #
    # This task runs with MultipleInstances=IgnoreNew and a 72-hour
    # ExecutionTimeLimit (verified on Silas-PC 2026-09-02), which is the worst
    # possible combination for a hang here: the stuck run is not killed for
    # three days, and every 5-minute trigger in the meantime is silently
    # SKIPPED rather than started. One hang therefore stops the watchdog
    # completely - not for one tick, for days - while Task Scheduler keeps
    # reporting a healthy NextRunTime and the log says nothing at all, because
    # the tick line below is never reached. A bounded call is what keeps a bad
    # minute from becoming a bad weekend.
    $pm2Raw = ''
    $pm2ExitCode = 0
    $pm2Job = Start-Job -ScriptBlock {
        param($exe)
        $text = (& $exe jlist 2>&1 | Out-String)
        [pscustomobject]@{ Output = $text; ExitCode = $LASTEXITCODE }
    } -ArgumentList $pm2Command.Source

    if (Wait-Job $pm2Job -Timeout $pm2TimeoutSeconds) {
        $pm2Result = Receive-Job $pm2Job | Select-Object -Last 1
        if ($pm2Result) {
            $pm2Raw = [string]$pm2Result.Output
            if ($null -ne $pm2Result.ExitCode) { $pm2ExitCode = [int]$pm2Result.ExitCode }
        }
    } else {
        Stop-Job $pm2Job -ErrorAction SilentlyContinue
        $pm2ExitCode = -1
        $pm2Raw = "pm2 jlist did not respond within $pm2TimeoutSeconds seconds"
    }
    Remove-Job $pm2Job -Force -ErrorAction SilentlyContinue

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

# Account for the time since the previous tick before anything else uses it.
# Written every run, so the very next tick after a gap is the one that names it.
$tickNow = Get-Date
$previousTick = $null
if ($alertState.ContainsKey('last_tick_at')) {
    $parsedTick = [datetime]::MinValue
    if ([datetime]::TryParse([string]$alertState['last_tick_at'], [ref]$parsedTick)) {
        $previousTick = $parsedTick
    }
}
$alertState['last_tick_at'] = $tickNow.ToString('yyyy-MM-dd HH:mm:ss')
Save-AlertState $alertState

if ($previousTick -and ($tickNow - $previousTick).TotalMinutes -ge $tickGapAlertMinutes) {
    $gapMinutes = [math]::Round(($tickNow - $previousTick).TotalMinutes, 1)
    $gapFrom = $previousTick.ToString('yyyy-MM-dd HH:mm:ss')
    $transitions = Get-PowerTransitions $previousTick
    $sleeps = @($transitions | Where-Object { $_.Id -eq 42 })
    $wakes = @($transitions | Where-Object { $_.Id -eq 107 })

    if ($sleeps.Count -gt 0 -or $wakes.Count -gt 0) {
        $detail = "$($sleeps.Count) sleep + $($wakes.Count) resume event(s)"
        if ($wakes.Count -gt 0) {
            $detail = "$detail, last resume $($wakes[-1].TimeCreated.ToString('yyyy-MM-dd HH:mm:ss'))"
        }
        Write-Log "GAP of $gapMinutes min since $gapFrom - the BOX SLEPT ($detail); the watchdog was frozen, not stopped"
        if (Test-AlertDue $alertState 'box-slept') {
            $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            Send-Alert "SLEEP: $hostName suspended for $gapMinutes minutes" `
                "This watchdog ran at $gapFrom and not again until $stamp - a gap of $gapMinutes minutes - and the Windows System log attributes it to sleep, not to a stopped task ($detail).`n`nThat matters because this box is a server. While it is suspended nothing renders, the relay posts no heartbeat (so off-box checks read the engine as SILENT), SMB mappings to the model share can come back stale, and ComfyUI keeps a CUDA context and cached folder_paths listings across a cycle it never learns about. Several incidents already written up in ops/home-server/README.md have that shape.`n`nConfirm what is putting it to sleep:`n  powercfg /lastwake`n  powercfg /requests`n  powercfg /q SCHEME_CURRENT SUB_SLEEP`n`nStop it, if this box is meant to stay up:`n  powercfg /change standby-timeout-ac 0`n  powercfg /change hibernate-timeout-ac 0`n  powercfg /change disk-timeout-ac 0`n(monitor-timeout-ac can stay non-zero - a dark screen is not a suspended box.)"
            $alertState['box-slept'] = $stamp
            Save-AlertState $alertState
        }
    } else {
        # No sleep event across the gap, so the box was up and this task was
        # not. That is the 2026-09-01 failure, and it is worth saying out loud
        # rather than leaving as a hole in the log.
        Write-Log "GAP of $gapMinutes min since $gapFrom with NO Kernel-Power sleep/resume event - the box was awake and this task did not run; check Task Scheduler history for AI-Backends-Healthcheck"
    }
}

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
# Set when this tick's share-recovery block below restarts comfyui, so the
# ordinary liveness probe further down does not immediately restart it again
# before it has finished starting up (a real double-restart observed
# 2026-08-28: pm2 marks a just-restarted process 'online' well before
# ComfyUI's own HTTP server is actually answering /system_stats).
$comfyuiJustRestarted = $false
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
            $comfyuiJustRestarted = $true
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

    # The share watchdog above may have just restarted this exact process for
    # the model-share recovery (see $comfyuiJustRestarted). Give it this tick
    # to finish starting up instead of racing it: pm2 reports 'online' almost
    # immediately on restart, well before ComfyUI's HTTP server is actually
    # answering, so probing right away would see a false hang and restart it
    # again for no reason. The regular 5-minute cadence is plenty of warm-up
    # time before the next tick's probe.
    if ($t.Name -eq 'comfyui' -and $comfyuiJustRestarted) {
        Write-Log "$($t.Name): skipping liveness probe this tick - just restarted by the share watchdog"
        continue
    }

    # Only police processes pm2 believes are online - a deliberate `pm2 stop`
    # (e.g. freeing the GPU) must not be fought by the watchdog. Reuses the
    # single $pm2List read above rather than shelling out per target: three
    # `pm2 jlist` calls per tick was wasteful, and worse, each one could fail
    # independently and be silently swallowed.
    $entry = $pm2List |
        Where-Object { $_.name -eq $t.Name } |
        Select-Object -First 1
    $status = $entry | Select-Object -ExpandProperty pm2_env -ErrorAction SilentlyContinue

    # The OS pid pm2 believes it is supervising, or 0 when it is running none.
    # Only used to answer "is the process holding the port ours?" below.
    $pm2Pid = 0
    if ($entry -and $entry.PSObject.Properties['pid'] -and $null -ne $entry.pid) {
        $pm2Pid = [int]$entry.pid
    }

    if (-not $status) {
        Write-Log "$($t.Name): not in pm2's list - not started on this box?"
        continue
    }

    # --- Crash-loop detection ------------------------------------------------
    # A crash loop is neither a hang nor a stop, and until 2026-09-02 this
    # watchdog had no way to say so. ComfyUI died ~26s into every start (a
    # custom node's emoji hit a cp1252 stdout; see ecosystem.config.js), so
    # pm2 cycled it forever. At any single 5-minute tick its status reads
    # 'online' most of the time and 'waiting restart' the rest, and the old
    # blanket 'not online -> leave it alone' treated the second case as a
    # deliberate 'pm2 stop'.
    #
    # The restart COUNTER is the honest signature: it climbs whatever the
    # status says at the instant we look. Compare it against the previous
    # tick.
    #
    # This also catches the end state, which is worse than the loop. With
    # min_uptime 30s and max_restarts 50, pm2 gives up after ~26 minutes and
    # parks the app in 'errored' - at which point the recycling console you
    # were using to notice the problem disappears and the box goes quiet
    # rather than green.
    $restartCount = -1
    if ($status.PSObject.Properties['restart_time'] -and $null -ne $status.restart_time) {
        $restartCount = [int]$status.restart_time
    }
    $restartKey = "restarts_$($t.Name)"
    $prevRestarts = -1
    if ($alertState.ContainsKey($restartKey)) {
        [int]::TryParse([string]$alertState[$restartKey], [ref]$prevRestarts) | Out-Null
    }
    if ($restartCount -ge 0) {
        $alertState[$restartKey] = $restartCount
        Save-AlertState $alertState
    }

    $restartDelta = 0
    if ($restartCount -ge 0 -and $prevRestarts -ge 0 -and $restartCount -ge $prevRestarts) {
        $restartDelta = $restartCount - $prevRestarts
    }

    # --- Replaced without a pm2 restart -------------------------------------
    # restart_time counts only the restarts pm2 PERFORMED. A process replaced
    # any other way -- the pm2 daemon itself restarting, a `pm2 resurrect`, a
    # reboot -- moves the process start time forward while leaving that counter
    # exactly where it was, so every check above stays silent.
    #
    # 2026-09-06: kr-relay read `restarts 0` with 44 minutes of uptime, against
    # an app created 2026-09-02 and a fresh "polling https://kindrobots.org"
    # line in its own log at 02:39:12 -- the same minute a 143-minute hole in
    # the off-box heartbeat series closed. Nothing had crashed. Something had
    # replaced the process, three times in two days, and pm2's own counter was
    # structurally unable to say so.
    $startedKey = "started_$($t.Name)"
    $currentStart = -1
    if ($entry -and $entry.PSObject.Properties['pm_uptime'] -and $null -ne $entry.pm_uptime) {
        $currentStart = [double]$entry.pm_uptime
    }
    $previousStart = -1
    if ($alertState.ContainsKey($startedKey)) {
        $parsedStart = 0.0
        if ([double]::TryParse([string]$alertState[$startedKey], [ref]$parsedStart)) {
            $previousStart = $parsedStart
        }
    }
    if ($currentStart -gt 0) {
        $alertState[$startedKey] = $currentStart
        Save-AlertState $alertState
    }

    if ($currentStart -gt 0 -and $previousStart -gt 0 -and
        $currentStart -gt $previousStart -and $restartDelta -eq 0) {
        $startedAt = ([datetimeoffset]::FromUnixTimeMilliseconds([long]$currentStart)).LocalDateTime
        $startedText = $startedAt.ToString('yyyy-MM-dd HH:mm:ss')
        Write-Log "$($t.Name): REPLACED WITHOUT A PM2 RESTART - process now started $startedText while pm2's restart count stayed at $restartCount; the daemon was restarted, resurrected, or the box rebooted"
        if (Test-AlertDue $alertState "replaced-$($t.Name)") {
            $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            Send-Alert "REPLACED: $($t.Name) on $hostName restarted, but not by pm2" `
                "$($t.Name) is running a process that started at $startedText, newer than the one seen at the previous tick, while pm2's restart counter did not move (still $restartCount). pm2 did not do this: it was a pm2 daemon restart, a 'pm2 resurrect', a logoff, or a reboot.`n`nThat matters because nothing else reports it. The crash-loop and errored checks read the restart counter, which stands still through exactly this event, and the app comes back looking healthy with a clean history. Off the box it shows only as a hole in the heartbeat series.`n`nWhat replaced it:`n  (Get-CimInstance Win32_OperatingSystem).LastBootUpTime`n  Get-WinEvent -MaxEvents 20 -FilterHashtable @{LogName='System'; Id=6005,6006,6008,1074,41} |`n    Format-Table TimeCreated, Id, Message -AutoSize`n`n6005 is the event log starting (a boot), 6006 a clean shutdown, 6008 an unexpected one, 1074 a shutdown someone or something requested (it names the process), 41 a kernel power fault. If none of those line up, the pm2 daemon went down on its own - check whether it is started at logon rather than as a service, since a logoff takes every app with it."
            $alertState["replaced-$($t.Name)"] = $stamp
            Save-AlertState $alertState
        }
    }

    if ($restartDelta -ge $crashLoopRestarts) {
        Write-Log "$($t.Name): CRASH LOOPING - pm2 restart count climbed $prevRestarts->$restartCount since the last tick"
        $portNote = Get-PortOwnerReport $t.Port $pm2Pid
        if ($portNote) { Write-Log "$($t.Name): $portNote" }
        if (Test-AlertDue $alertState "crashloop-$($t.Name)") {
            $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            Send-Alert "CRASH LOOP: $($t.Name) on $hostName is restarting repeatedly" `
                "pm2's restart count for $($t.Name) went from $prevRestarts to $restartCount in one 5-minute tick as of $stamp on $hostName - it is dying and being restarted continuously, not hung. Restarting it again will not help; read the startup error. Run 'pm2 logs $($t.Name) --err --lines 200' and look for the FIRST exception, not the last - and note that a port collision produces no exception at all, only a one-line [ERROR] before the process exits, which is what the port check below is for. If pm2 gives up (max_restarts) the app parks in 'errored' and this alert stops, so do not read silence as recovery.`n`nPort check: $portNote"
            $alertState["crashloop-$($t.Name)"] = $stamp
            Save-AlertState $alertState
        }
        continue
    }

    if ($status.status -eq 'errored') {
        # pm2 has given up on it. Nothing will restart it, and no further
        # symptom will appear on its own - the single most silent failure
        # state a backend can be in.
        Write-Log "$($t.Name): pm2 status is 'errored' - pm2 has GIVEN UP restarting it"
        $portNote = Get-PortOwnerReport $t.Port $pm2Pid
        if ($portNote) { Write-Log "$($t.Name): $portNote" }
        if (Test-AlertDue $alertState "errored-$($t.Name)") {
            $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            Send-Alert "ERRORED: $($t.Name) on $hostName - pm2 stopped trying" `
                "pm2 has marked $($t.Name) 'errored' as of $stamp on $hostName, which means it exceeded max_restarts and pm2 will NOT restart it again. Nothing further will happen without a human. Read 'pm2 logs $($t.Name) --err --lines 200' for the startup failure, fix it, then 'pm2 restart <ecosystem file> --only $($t.Name) --update-env'.`n`nPort check: $portNote"
            $alertState["errored-$($t.Name)"] = $stamp
            Save-AlertState $alertState
        }
        continue
    }

    if ($status.status -eq 'stopped') {
        # The one genuinely deliberate state: someone ran 'pm2 stop', e.g. to
        # free the GPU. Never fight that.
        Write-Log "$($t.Name): pm2 status is 'stopped' - deliberate, leaving it alone"
        continue
    }

    if ($status.status -ne 'online') {
        # launching / waiting restart / one-launch-status: in transition. Not
        # an alarm on its own (the counter above owns that), but do not probe
        # a process that is not up yet.
        Write-Log "$($t.Name): pm2 status is '$($status.status)' - in transition, probing next tick"
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
$krBase = if ($env:KR_BASE_URL) { $env:KR_BASE_URL.TrimEnd('/') } else { 'https://kindrobots.org' }
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
