# Who is launching the second ComfyUI?
#
# 2026-09-06: ComfyUI boots overlap. Four startups between 03:48 and 03:53, one
# beginning 16 seconds after the previous one and 35 seconds BEFORE that one
# reached its "Port 8188 is already in use" error. pm2 runs one process per
# fork-mode app and cannot start a replacement until the old one exits, and its
# restart counter moved by 1 across the whole episode - so at least one of those
# processes was not started by pm2. Something relaunches ComfyUI from inside
# ComfyUI. That also accounts for the console windows appearing on the desktop:
# pm2 starts the BASE interpreter with __PYVENV_LAUNCHER__ precisely so no
# console appears, but a relaunch through sys.executable gets
# venv\Scripts\python.exe - the redirector - which spawns a visible one.
#
# Every log we have shows the CONSEQUENCE. This records the CAUSE: it polls for
# ComfyUI processes and, the first time it sees each one, writes down its parent
# while that parent is still alive. A parent captured after the fact is useless
# (Windows reuses pids, and the spawner may exit within seconds), which is why
# this samples rather than being run once by hand after the fact.
#
# Run it, then leave it while the engines run normally:
#
#   pm2 start ecosystem.config.js
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\watch-comfy-spawn.ps1
#
# Ctrl+C to stop. Findings go to the console and to logs\comfy-spawn-watch.log.
#
# Reading it: exactly one ComfyUI whose parent is node.exe is the healthy state
# (node.exe is pm2). A second ComfyUI whose parent is another python.exe - or
# whose parent is a ComfyUI pid this script already listed - is the bug, and the
# parent's command line names the culprit.
#
# Keep this file ASCII-only: Windows PowerShell 5.1 reads a no-BOM script as the
# system ANSI codepage, so UTF-8 punctuation in a string literal corrupts
# parsing.

[CmdletBinding()]
param(
    # Well under a ComfyUI startup (~90 seconds to the port bind), so a spawned
    # child is always seen while its parent is still running.
    [int]$IntervalSeconds = 5,
    # 0 runs until Ctrl+C.
    [int]$Minutes = 0,
    [string]$LogFile
)

$ErrorActionPreference = 'SilentlyContinue'

if (-not $LogFile) {
    $LogFile = Join-Path $PSScriptRoot 'logs\comfy-spawn-watch.log'
}
New-Item -ItemType Directory -Force -Path (Split-Path $LogFile) | Out-Null

function Write-Both($message) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $message"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

function Get-ComfyProcesses {
    # Match on main.py alone. An earlier attempt at this also required "comfy"
    # in the command line and found NOTHING while ComfyUI was running: pm2
    # launches the base interpreter, so the real command line reads
    # "C:\Users\...\Python310\python.exe main.py --listen 127.0.0.1 --port 8188"
    # and contains no "comfy" at all. The cwd is what makes it ComfyUI, not the
    # exe path.
    return @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -like 'python*' -and $_.CommandLine -and $_.CommandLine -like '*main.py*'
        })
}

function Describe-Parent($parentPid) {
    if (-not $parentPid) { return 'parent <none>' }
    $parent = Get-CimInstance Win32_Process -Filter "ProcessId = $parentPid" -ErrorAction SilentlyContinue
    if (-not $parent) {
        # The spawner already exited. Its pid is still worth printing: it can be
        # matched against a ComfyUI pid this script listed earlier.
        return "parent pid $parentPid <already gone>"
    }
    return "parent pid $parentPid ($($parent.Name)) cmdline: $($parent.CommandLine)"
}

Write-Both "watching for ComfyUI processes every ${IntervalSeconds}s - Ctrl+C to stop"

$seen = @{}
$lastCount = -1
$deadline = if ($Minutes -gt 0) { (Get-Date).AddMinutes($Minutes) } else { $null }

while ($true) {
    if ($deadline -and (Get-Date) -gt $deadline) {
        Write-Both "watch finished after $Minutes minute(s)"
        break
    }

    $procs = Get-ComfyProcesses

    foreach ($proc in $procs) {
        if ($seen.ContainsKey($proc.ProcessId)) { continue }
        # Capture the parent NOW, on first sighting, while it is still alive.
        $seen[$proc.ProcessId] = $true
        $started = if ($proc.CreationDate) { $proc.CreationDate.ToString('HH:mm:ss') } else { 'unknown' }
        Write-Both "NEW ComfyUI pid $($proc.ProcessId) started $started - $(Describe-Parent $proc.ParentProcessId)"
        Write-Both "    its own cmdline: $($proc.CommandLine)"
        if ($seen.ContainsKey($proc.ParentProcessId)) {
            Write-Both "    ^^ ITS PARENT IS ANOTHER COMFYUI (pid $($proc.ParentProcessId)) - ComfyUI is relaunching itself"
        }
    }

    if ($procs.Count -ne $lastCount) {
        if ($procs.Count -gt 1) {
            Write-Both "$($procs.Count) ComfyUI processes are running at once: $(($procs | ForEach-Object { $_.ProcessId }) -join ', ')"
        } else {
            Write-Both "$($procs.Count) ComfyUI process(es) running"
        }
        $lastCount = $procs.Count
    }

    Start-Sleep -Seconds $IntervalSeconds
}
