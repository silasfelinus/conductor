# Shared ComfyUI restart-handoff logic (conductor/t-185).
#
# Extracted from healthcheck.ps1, which still owns the four watchdog call
# sites this was originally written for (PR #4869: stop pm2, reap only
# processes positively identified as this engine, verify the old process and
# listener are both gone, and only then start the replacement - closing the
# window where PM2's Windows kill can time out silently and a replacement
# gets launched on top of a still-alive old engine, and the two then fight
# over port 8188, comfyui.db, and the GPU).
#
# restore-shares.ps1 dot-sources this too (conductor/t-185): it previously
# called `& pm2 restart comfyui` directly after remapping shares at logon,
# bypassing the safe handoff entirely. Lower exposure than the watchdog's own
# call sites (a fresh reboot usually leaves no old engine to survive), but not
# zero - the script can also be run manually against a live session.
#
# Dot-source this file (`. $PSScriptRoot\lib\Restart-ComfySupervised.ps1` or
# equivalent), do not import it as a module: the functions below are added to
# the CALLING script's own scope, so they resolve `Write-Log` to whichever
# implementation the caller already defined (healthcheck.ps1's file-only
# logger, or restore-shares.ps1's file+console logger) rather than requiring
# a shared one. Dot-source this AFTER defining Write-Log.
#
# $comfyDir / $comfyPython identify "does this process look like our ComfyUI
# engine" (see Test-IsComfyEngine below). healthcheck.ps1 already defines
# both from COMFY_DIR / COMFY_BASE_PYTHON env vars with the same defaults
# used here; the guards below only apply when a caller (restore-shares.ps1)
# has not already set them, so dot-sourcing this is a no-op on the values
# either script already computed for itself.
if (-not $comfyDir) {
    $comfyDir = if ($env:COMFY_DIR) { $env:COMFY_DIR } else { 'D:\comfy\comfy-fast' }
}
if (-not $comfyPython) {
    $comfyPython = if ($env:COMFY_BASE_PYTHON) {
        $env:COMFY_BASE_PYTHON
    } else {
        'C:\Users\silasfelinus\AppData\Local\Programs\Python\Python310\python.exe'
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

# Does this process look like OUR ComfyUI engine?
#
# 2026-09-08: the check this replaces required $comfyDir to appear in the
# command line or executable path, and it never can. pm2 launches the engine
# with a RELATIVE script path from cwd=$comfyDir, so the observed command line
# is `...\Python310\python.exe main.py --listen 127.0.0.1 --port 8188 ...` and
# the executable path is just the interpreter. The install directory exists
# only as the working directory, which Win32_Process does not expose. So
# Invoke-PortReclaim logged REFUSING every tick and had never once fired -
# including through the outage it was written for.
#
# Corroborate the install a different way: it must be a python running main.py,
# AND at least one of - it names $comfyDir outright (a launcher started with an
# absolute path), it IS the interpreter pm2 launches, or it is bound to the
# port we care about.
function Test-IsComfyEngine($cim, $port) {
    if (-not $cim) { return $false }
    $commandLine = [string]$cim.CommandLine
    $imagePath = [string]$cim.ExecutablePath
    $haystack = "$commandLine $imagePath"

    if ($haystack -notmatch 'main\.py') { return $false }

    return (
        ($haystack -match [regex]::Escape($comfyDir)) -or
        ($imagePath -and $comfyPython -and ($imagePath -ieq $comfyPython)) -or
        ($port -and ($commandLine -match "--port\s+$([regex]::Escape([string]$port))"))
    )
}

# ---------------------------------------------------------------------------
# Serialized ComfyUI restart
#
# PM2's Windows kill path is not a safe handoff boundary for this engine.
# Several incidents have shown `pm2 restart comfyui` returning after its kill
# timed out while the old Python process was still alive, then immediately
# spawning a replacement. The two engines then compete for port 8188,
# comfyui.db, and the same GPU.
#
# The old watchdog mitigated that by reaping the survivor eight seconds AFTER
# the replacement had launched. That shortened the collision but still made an
# overlap part of the recovery algorithm.
#
# For ComfyUI, stop PM2 first, reap only processes positively identified as this
# engine, verify both the old process and listener are gone, and only then start
# the replacement. Non-Comfy PM2 apps keep the ordinary restart path.
function Get-ComfyEnginePids($port) {
    @(
        Get-CimInstance -ClassName Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
            Where-Object {
                $cmd = [string]$_.CommandLine
                (Test-IsComfyEngine $_ $port) -and
                    ($cmd -match "(^|\s)--port\s+$([regex]::Escape([string]$port))(\s|$)")
            } |
            Select-Object -ExpandProperty ProcessId
    )
}

# $port is optional: healthcheck.ps1 leaves it unset and this falls back to
# looking the comfyui target up in its own $targets array (unchanged prior
# behavior). restore-shares.ps1 has no $targets, so it passes the port
# explicitly instead.
function Restart-Supervised($name, $port) {
    if ($name -ne 'comfyui') {
        & pm2 restart $name | Out-Null
        return
    }

    if ($port) {
        $port = [int]$port
    } else {
        $target = $targets |
            Where-Object { $_.Name -eq $name } |
            Select-Object -First 1
        $port = if ($target -and $target.Port) { [int]$target.Port } else { 8188 }
    }

    Write-Log "${name}: safe restart - stopping pm2 before reaping the old engine"
    & pm2 stop $name | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "${name}: pm2 stop failed (exit $LASTEXITCODE) - REFUSING to start a replacement on top of an engine pm2 may still own"
        return
    }

    # pm2 may return from stop after its Windows kill timeout while Python is
    # still alive. With the app deliberately stopped, a surviving ComfyUI is
    # unsupervised and can be reaped before any replacement exists.
    foreach ($oldPid in @(Get-ComfyEnginePids $port)) {
        Write-Log "${name}: safe restart - force-killing surviving old engine pid $oldPid before replacement launch"
        try {
            Stop-Process -Id $oldPid -Force -ErrorAction Stop
        } catch {
            Write-Log "${name}: could not kill surviving old engine pid $oldPid ($($_.Exception.Message))"
        }
    }

    # A kill request is not proof of death. A booting engine may not own the
    # port yet, so checking only 8188 could say "free" while an old Python is
    # still alive and about to bind it. Do not start until the old engine set is
    # actually empty.
    $oldEnginesGone = $false
    for ($i = 0; $i -lt 10; $i++) {
        $remaining = @(Get-ComfyEnginePids $port)
        if ($remaining.Count -eq 0) {
            $oldEnginesGone = $true
            break
        }
        Start-Sleep -Seconds 1
    }
    if (-not $oldEnginesGone) {
        $remaining = @(Get-ComfyEnginePids $port)
        Write-Log "${name}: REFUSING safe restart - old ComfyUI pid(s) are still alive after cleanup: $($remaining -join ', ')"
        return
    }

    # The listening port is the second authority. A manually launched ComfyUI
    # could escape the --port process filter above, but it cannot bind 8188
    # invisibly.
    $ownerPid = Get-PortListenerPid $port
    if ($ownerPid) {
        $owner = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $ownerPid" -ErrorAction SilentlyContinue
        if (Test-IsComfyEngine $owner $port) {
            Write-Log "${name}: safe restart - port $port is still held by old ComfyUI pid $ownerPid; force-killing it before replacement launch"
            try {
                Stop-Process -Id $ownerPid -Force -ErrorAction Stop
            } catch {
                Write-Log "${name}: could not kill old port owner pid $ownerPid ($($_.Exception.Message))"
            }
        } else {
            Write-Log "${name}: REFUSING safe restart - port $port is held by unrelated pid $ownerPid; starting ComfyUI would only crash-loop"
            return
        }
    }

    # Give Windows a bounded moment to release the listener. Never launch the
    # replacement while the port is still occupied.
    $portReleased = $false
    for ($i = 0; $i -lt 10; $i++) {
        if (-not (Get-PortListenerPid $port)) {
            $portReleased = $true
            break
        }
        Start-Sleep -Seconds 1
    }
    if (-not $portReleased) {
        $stuckPid = Get-PortListenerPid $port
        $ownerText = if ($stuckPid) { " by pid $stuckPid" } else { "" }
        Write-Log "${name}: REFUSING safe restart - port $port is still occupied$ownerText after cleanup"
        return
    }

    Write-Log "${name}: safe restart - old engine gone and port $port free; starting replacement"
    & pm2 restart $name | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "${name}: replacement start failed (pm2 exit $LASTEXITCODE)"
        return
    }

    # PM2 records the new pid before ComfyUI is ready. This is identity
    # verification only; the normal startup-grace logic owns readiness.
    Start-Sleep -Seconds 8
    $newPid = 0
    [int]::TryParse("$(& pm2 pid $name)".Trim(), [ref]$newPid) | Out-Null
    if ($newPid) {
        Write-Log "${name}: safe restart launched supervised replacement pid $newPid"
    } else {
        Write-Log "${name}: pm2 did not report a replacement pid after safe restart"
    }
}
