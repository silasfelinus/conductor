# Which process is popping a console window onto the desktop?
#
# 2026-09-19: Silas reports TWO cmd-style windows appearing every 3-5 minutes.
# There are at least three known candidates on this box and the logs cannot tell
# them apart, because every one of them leaves the same trace - a short-lived
# console process and nothing else:
#
#   1. The "AI-Backends-Healthcheck" scheduled task, every 5 minutes. README.md
#      documented registering it as a bare `powershell -File healthcheck.ps1`,
#      which under "run only when user is logged on" gets a VISIBLE console on
#      the interactive desktop on every tick. healthcheck-hidden.vbs exists to
#      avoid exactly that (shell.Run with window style 0) but no setup snippet
#      ever pointed at it, so a task registered from the README is the popup
#      version.
#   2. healthcheck.ps1's own children. It shells out per tick to pm2.cmd (a
#      BATCH file, so cmd.exe) inside a Start-Job (a second powershell.exe),
#      plus node.exe for the jlist projection. A child console process whose
#      parent has no console of its own gets a brand new, visible one.
#   3. ComfyUI relaunching itself through the venv redirector - see
#      watch-comfy-spawn.ps1, which documents the same class of symptom and is
#      still an open question. The redirector is TWO processes (stub plus the
#      re-exec'd base interpreter), so it can account for a PAIR of windows.
#
# Guessing between these costs a day per wrong guess. This names the culprit
# directly, on the same principle as watch-comfy-spawn.ps1: every log we have
# shows the CONSEQUENCE, so record the CAUSE while it is still on screen.
#
# HOW IT KNOWS a window appeared, rather than merely a process starting: on
# Windows 10/11 every new console window is hosted by its own conhost.exe. One
# new visible console == one new conhost.exe. So a conhost.exe start IS the
# popup, and its parent chain is the answer. Two popups every five minutes means
# two conhost.exe starts, and this prints who owned each one.
#
# It also prints SessionID. A window can only appear on the desktop from an
# interactive session (1 or higher); anything in session 0 is structurally
# invisible, which is what makes "run whether user is logged on or not" a real
# fix rather than a cosmetic one.
#
# Run it ELEVATED and leave it for 15 minutes:
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\watch-window-spawn.ps1 -Minutes 15
#
# Ctrl+C to stop early. Findings go to the console and to
# logs\window-spawn-watch.log, and a summary prints on exit.
#
# SECRETS: this logs process command lines, which on this box can legitimately
# contain a CivitAI token or an API key (lora_import_agent.py redacts exactly
# those in its own logging). Every command line printed here goes through
# Remove-Secret first - AGENTS.md hard rule 15. Do not remove that call before
# pasting output anywhere.
#
# Keep this file ASCII-only: Windows PowerShell 5.1 reads a no-BOM script as the
# system ANSI codepage, so UTF-8 punctuation in a string literal corrupts
# parsing.

[CmdletBinding()]
param(
    # 0 runs until Ctrl+C.
    [int]$Minutes = 0,
    [string]$LogFile,
    # Skip the scheduled-task registration dump at startup.
    [switch]$SkipTaskDump,
    # The task whose registration is most likely to be the answer.
    [string]$TaskName = 'AI-Backends-Healthcheck'
)

$ErrorActionPreference = 'Continue'

if (-not $LogFile) {
    $LogFile = Join-Path $PSScriptRoot 'logs\window-spawn-watch.log'
}
New-Item -ItemType Directory -Force -Path (Split-Path $LogFile) | Out-Null

function Write-Both($message) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $message"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

# AGENTS.md hard rule 15: anything that reaches a log Silas may paste back must
# be incapable of carrying a secret. Masks the value, keeps the flag, so the
# command line stays readable as evidence.
function Remove-Secret([string]$text) {
    if (-not $text) { return $text }
    $out = $text
    # --civitai-token VALUE / --api-key=VALUE / -Token VALUE and friends.
    $out = [regex]::Replace(
        $out,
        '(?i)(-{1,2}(?:civitai-token|api-key|apikey|token|password|passwd|pwd|secret|auth)\b)([=:]|\s+)(\S+)',
        '$1$2<redacted>')
    # KR_API_TOKEN=VALUE, BREVO_API_KEY=VALUE, GITHUB_TOKEN=VALUE, ...
    $out = [regex]::Replace(
        $out,
        '(?i)\b([A-Z0-9_]*(?:TOKEN|KEY|SECRET|PASSWORD|PASSWD)[A-Z0-9_]*)=(\S+)',
        '$1=<redacted>')
    # Anything that looks like a bearer credential or a long opaque blob after
    # a credential-ish word we did not anticipate.
    $out = [regex]::Replace($out, '(?i)\b(bearer)\s+\S+', '$1 <redacted>')
    return $out
}

# Processes worth a correlation line even when they do not pop a window. A
# popup's parent is often one of these, and seeing the tick itself land makes
# the 5-minute alignment obvious in the log.
$watched = @(
    'conhost.exe', 'cmd.exe', 'powershell.exe', 'pwsh.exe',
    'wscript.exe', 'cscript.exe', 'python.exe', 'pythonw.exe',
    'node.exe', 'git.exe', 'taskeng.exe', 'schtasks.exe'
)

# pid -> description, so an ancestor that has already exited can still be named.
$known = @{}

function Get-ProcInfo($procId) {
    if (-not $procId) { return $null }
    $cim = Get-CimInstance Win32_Process -Filter "ProcessId = $procId" -ErrorAction SilentlyContinue
    if ($cim) {
        $info = [pscustomobject]@{
            ProcessId = [int]$cim.ProcessId
            Name      = [string]$cim.Name
            Parent    = [int]$cim.ParentProcessId
            Command   = Remove-Secret ([string]$cim.CommandLine)
            Alive     = $true
        }
        $known[[int]$cim.ProcessId] = $info
        return $info
    }
    if ($known.ContainsKey([int]$procId)) {
        $cached = $known[[int]$procId]
        return [pscustomobject]@{
            ProcessId = $cached.ProcessId
            Name      = $cached.Name
            Parent    = $cached.Parent
            Command   = $cached.Command
            Alive     = $false
        }
    }
    return $null
}

# Walk up while the ancestors are still alive. The immediate parent of a
# conhost.exe is the process whose console it is hosting; one or two levels above
# that is what actually decided to launch it (Task Scheduler, pm2's node.exe, a
# ComfyUI python.exe re-exec).
function Write-Ancestry($startPid, $prefix) {
    $currentPid = $startPid
    for ($depth = 0; $depth -lt 4 -and $currentPid; $depth++) {
        $info = Get-ProcInfo $currentPid
        if (-not $info) {
            Write-Both "$prefix pid $currentPid <gone, never seen>"
            return
        }
        $state = if ($info.Alive) { '' } else { ' <already exited>' }
        Write-Both "$prefix pid $($info.ProcessId) ($($info.Name))$state"
        if ($info.Command) { Write-Both "$prefix     cmdline: $($info.Command)" }
        $currentPid = $info.Parent
        $prefix = "$prefix  "
    }
}

$currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = (New-Object Security.Principal.WindowsPrincipal($currentIdentity)).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)

Write-Both '================================================================'
Write-Both "window-spawn watch starting (elevated: $isAdmin)"

# ---------------------------------------------------------------------------
# Part 1: the registration of the task that is the most likely single answer.
# This alone resolves candidate 1, in one shot, before any waiting.
# ---------------------------------------------------------------------------
if (-not $SkipTaskDump) {
    Write-Both "--- scheduled task registration: $TaskName ---"
    $raw = & schtasks /Query /TN $TaskName /V /FO LIST 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Both "  schtasks could not read '$TaskName' (exit $LASTEXITCODE). It may be"
        Write-Both '  registered under a different name; list them with: schtasks /Query /FO TABLE'
    } else {
        # Only the fields that decide whether a window can appear, each one
        # redacted: "Task To Run" is a command line like any other.
        foreach ($line in $raw) {
            if ($line -match '^\s*(TaskName|Task To Run|Run As User|Logon Mode|Schedule Type|Repeat: Every|Scheduled Task State|Start In)\s*:') {
                Write-Both "  $(Remove-Secret ([string]$line).Trim())"
            }
        }
        $joined = ($raw -join "`n")
        if ($joined -match '(?im)^\s*Logon Mode\s*:\s*Interactive only') {
            Write-Both '  >>> LOGON MODE IS "Interactive only": every tick runs on your desktop,'
            Write-Both '      so a console process here IS a visible window. This is candidate 1.'
        }
        if ($joined -match '(?im)^\s*Task To Run\s*:.*powershell' -and $joined -notmatch '(?i)healthcheck-hidden\.vbs') {
            Write-Both '  >>> TASK RUNS powershell.exe DIRECTLY, not healthcheck-hidden.vbs. That is'
            Write-Both '      the popup form. See README.md "health watchdog" for the wrapper form.'
        }
    }
    Write-Both '--- end registration ---'
}

# ---------------------------------------------------------------------------
# Part 2: catch the popups as they happen.
# ---------------------------------------------------------------------------
# Win32_ProcessStartTrace is ETW-backed and never misses a process, which is the
# whole point here: a console that flashes for 200ms is invisible to any polling
# interval. It needs elevation. __InstanceCreationEvent is the unprivileged
# fallback, but it POLLS (WITHIN 1), so it can miss precisely the short-lived
# flash we are hunting - say so rather than quietly downgrading.
$sourceId = 'WindowSpawnWatch'
Get-EventSubscriber -SourceIdentifier $sourceId -ErrorAction SilentlyContinue |
    Unregister-Event -ErrorAction SilentlyContinue
$useTrace = $false
if ($isAdmin) {
    try {
        Register-WmiEvent -Class Win32_ProcessStartTrace -SourceIdentifier $sourceId -ErrorAction Stop
        $useTrace = $true
        Write-Both 'watching Win32_ProcessStartTrace (real-time, misses nothing)'
    } catch {
        Write-Both "could not subscribe to Win32_ProcessStartTrace: $($_.Exception.Message)"
    }
}
if (-not $useTrace) {
    Register-WmiEvent -Query "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_Process'" `
        -SourceIdentifier $sourceId
    Write-Both 'watching __InstanceCreationEvent WITHIN 1 (POLLED - a sub-second console flash can be missed)'
    if (-not $isAdmin) {
        Write-Both 'RE-RUN THIS ELEVATED for the real-time trace if the popups do not show up below.'
    }
}

$deadline = if ($Minutes -gt 0) { (Get-Date).AddMinutes($Minutes) } else { $null }
if ($deadline) {
    Write-Both "watching until $($deadline.ToString('HH:mm:ss')) - Ctrl+C to stop early"
} else {
    Write-Both 'watching until Ctrl+C'
}

# Popup tallies, reported on exit.
$popupsByParent = @{}
$popupMinutes = New-Object System.Collections.ArrayList

try {
    while ($true) {
        if ($deadline -and (Get-Date) -gt $deadline) {
            Write-Both "watch finished after $Minutes minute(s)"
            break
        }

        $evt = Wait-Event -SourceIdentifier $sourceId -Timeout 2
        if (-not $evt) { continue }

        if ($useTrace) {
            $name = [string]$evt.SourceEventArgs.NewEvent.ProcessName
            $newPid = [int]$evt.SourceEventArgs.NewEvent.ProcessID
            $parentPid = [int]$evt.SourceEventArgs.NewEvent.ParentProcessID
            $sessionId = [int]$evt.SourceEventArgs.NewEvent.SessionID
        } else {
            $inst = $evt.SourceEventArgs.NewEvent.TargetInstance
            $name = [string]$inst.Name
            $newPid = [int]$inst.ProcessId
            $parentPid = [int]$inst.ParentProcessId
            $sessionId = [int]$inst.SessionId
        }
        Remove-Event -EventIdentifier $evt.EventIdentifier -ErrorAction SilentlyContinue

        if ($watched -notcontains $name) { continue }

        if ($name -eq 'conhost.exe') {
            # This IS a window appearing.
            $parent = Get-ProcInfo $parentPid
            $parentName = if ($parent) { $parent.Name } else { "pid $parentPid" }
            $visible = if ($sessionId -ge 1) { 'ON THE DESKTOP' } else { 'session 0, not visible' }
            Write-Both ''
            Write-Both "POPUP: new console (conhost.exe pid $newPid) in session $sessionId - $visible"
            Write-Ancestry $parentPid '  owner:'

            $key = $parentName
            if ($parent -and $parent.Command) {
                # First two tokens are enough to group by, and already redacted.
                $key = ($parent.Command -split '\s+' | Select-Object -First 2) -join ' '
            }
            if (-not $popupsByParent.ContainsKey($key)) { $popupsByParent[$key] = 0 }
            $popupsByParent[$key]++
            [void]$popupMinutes.Add((Get-Date).ToString('HH:mm'))
        } else {
            $info = Get-ProcInfo $newPid
            $cmd = if ($info) { $info.Command } else { '' }
            Write-Both "start: $name pid $newPid (session $sessionId, parent pid $parentPid)"
            if ($cmd) { Write-Both "    cmdline: $cmd" }
        }
    }
} finally {
    Get-EventSubscriber -SourceIdentifier $sourceId -ErrorAction SilentlyContinue |
        Unregister-Event -ErrorAction SilentlyContinue

    Write-Both ''
    Write-Both '=== summary ==='
    if ($popupsByParent.Count -eq 0) {
        Write-Both 'no new consoles observed. If windows were appearing on screen during this'
        Write-Both 'run, re-run elevated (the polled fallback misses short flashes).'
    } else {
        Write-Both 'consoles opened, by the process that owned them:'
        foreach ($key in ($popupsByParent.Keys | Sort-Object { -$popupsByParent[$_] })) {
            Write-Both "  $($popupsByParent[$key])x  $key"
        }
        Write-Both "popup times: $($popupMinutes -join ', ')"
    }
    Write-Both "full log: $LogFile"
}
