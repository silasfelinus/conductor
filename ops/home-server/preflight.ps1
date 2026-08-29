# Reboot-readiness check for the render box. Read-only: it changes nothing.
#
# The question this answers is "if I reboot right now, does it all come back?"
# -- which is NOT the same as "is it working right now." Everything in this
# session's outage was working at some point and still died on reboot, because
# the thing that survives a reboot is the SAVED state, not the running state:
#
#   * a drive mapping made without /persistent:yes works until you reboot
#   * a setx made after the last `pm2 save` never reaches the resurrected
#     process, so pm2 faithfully restores the OLD environment every boot
#     (this kept the box on Z: for two days while the config on disk said UNC)
#   * a credential written from an SSH/Termius session is not written at all
#
# So each check below reports the running state AND, where they can differ, the
# state a reboot would actually restore.
#
# Usage, from the console session (not SSH):
#   .\preflight.ps1
#
# Exit codes: 0 all good, 1 something would break on reboot, 2 cannot tell.
#
# Keep this file ASCII-only, same reason as healthcheck.ps1: Windows PowerShell
# 5.1 reads a no-BOM script as the system ANSI codepage, so UTF-8 punctuation
# inside a string literal corrupts parsing.

[CmdletBinding()]
param(
    [string]$ShareHost = $(if ($env:KR_SHARE_UNC -match '^\\\\([^\\]+)\\') { $Matches[1] } else { '192.168.7.172' }),
    [string]$UncProbe  = '\\192.168.7.172\pc\ai\models',
    [string]$ComfyUrl  = 'http://127.0.0.1:8188/system_stats'
)

$ErrorActionPreference = 'SilentlyContinue'

$script:fail = 0
$script:warn = 0
$script:unknown = 0

function Say($level, $name, $detail) {
    $tag = switch ($level) {
        'ok'   { '[ OK ]' }
        'fail' { '[FAIL]'; }
        'warn' { '[WARN]' }
        default { '[ ?? ]' }
    }
    if ($level -eq 'fail') { $script:fail++ }
    elseif ($level -eq 'warn') { $script:warn++ }
    elseif ($level -eq 'unknown') { $script:unknown++ }
    Write-Host "$tag $name"
    if ($detail) { foreach ($d in @($detail)) { Write-Host "       $d" } }
}

function Test-Readable($path) {
    if (-not $path) { return $false }
    try {
        $null = Get-ChildItem -LiteralPath $path -Force -ErrorAction Stop |
            Select-Object -First 1
        return $true
    } catch { return $false }
}

Write-Host ""
Write-Host "Reboot-readiness check -- $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') on $env:COMPUTERNAME as $env:USERNAME"
Write-Host ("-" * 78)

# --- 1. Which session are we in? ---------------------------------------------
# Half the checks below are meaningless from a network logon session: drive
# letters are per-session, and Credential Manager refuses to write from one at
# all ("CMDKEY: Credentials cannot be saved from this logon session"). A net use
# listing read from Termius showing everything Unavailable is how this box's
# 2026-08-25 outage got misdiagnosed as a dead array.
$sessionName = $env:SESSIONNAME
if ($sessionName -eq 'Console' -or $sessionName -like 'RDP-Tcp*') {
    Say 'ok' "logon session: $sessionName" $null
} else {
    $shown = if ($sessionName) { $sessionName } else { '(empty)' }
    Say 'warn' "logon session: $shown -- not the console" @(
        "Drive letters and credentials are per-logon-session. Results below may",
        "not reflect what the console session (or pm2) actually sees. Re-run from",
        "the console before believing a FAIL."
    )
}

# --- 2. Credential ------------------------------------------------------------
# A listed credential is not a working credential: on 2026-08-29 entries existed
# for this host and every share still answered "The user name or password is
# incorrect". Only the UNC read below proves anything.
$cred = (& cmdkey /list 2>&1) -join "`n"
if ($cred -match [regex]::Escape($ShareHost)) {
    Say 'ok' "credential stored for $ShareHost" "(presence only -- the UNC read below is the real test)"
} else {
    Say 'fail' "no stored credential for $ShareHost" @(
        "cmdkey /add:$ShareHost /user:<user> /pass",
        "Must be run from the console; a network logon session cannot save one."
    )
}

# --- 3. The share itself, without any drive letter ---------------------------
if (Test-Readable $UncProbe) {
    Say 'ok' "UNC readable: $UncProbe" $null
} else {
    Say 'fail' "UNC NOT readable: $UncProbe" @(
        "This is the one that matters -- the pipeline should be on UNC, not a letter.",
        "If cmd says 'user name or password is incorrect', re-add the credential."
    )
}

# --- 4. Drive letters, and whether they would survive a reboot ---------------
# Persistence lives in HKCU:\Network\<letter>. A mapping that is working right
# now but absent from that key is gone the moment you reboot -- which is the
# single most common way this box comes back broken.
$mappings = @{}
foreach ($line in (& net use 2>&1)) {
    if ("$line" -match '([A-Za-z]):\s+(\\\\[^\s]+)') {
        $mappings[$Matches[1].ToUpper()] = $Matches[2]
    }
}
if (-not $mappings.Count) {
    Say 'warn' "no drive letters mapped in this session" "Fine if everything runs on UNC. Not fine if you use them."
} else {
    foreach ($letter in ($mappings.Keys | Sort-Object)) {
        $unc = $mappings[$letter]
        $readable = Test-Readable "${letter}:\"
        $persistent = Test-Path "HKCU:\Network\$letter"
        if ($readable -and $persistent) {
            Say 'ok' "${letter}: -> $unc (readable, persistent)" $null
        } elseif ($readable -and -not $persistent) {
            Say 'fail' "${letter}: -> $unc works NOW but is not persistent" @(
                "It will be gone after the next reboot. Fix:",
                "  net use ${letter}: $unc /persistent:yes"
            )
        } elseif ($persistent) {
            Say 'fail' "${letter}: -> $unc is persistent but NOT readable" "Credential or NAS problem, not a mapping problem."
        } else {
            Say 'fail' "${letter}: -> $unc is neither readable nor persistent" $null
        }
    }
}

# --- 5. pm2: what is running, and what a reboot would restore ----------------
# These are different lists. `pm2 save` snapshots the running list AND its
# environment into dump.pm2; `pm2 resurrect` replays that snapshot verbatim.
$jlistRaw = (& pm2 jlist 2>&1) -join ''
$running = $null
try { $running = $jlistRaw | ConvertFrom-Json } catch {}
if (-not $running) {
    Say 'unknown' "pm2 returned no usable process list" @(
        "pm2's daemon is per-user and WSL's pm2 is a separate world entirely.",
        "Run this from the same Windows account that owns the engines."
    )
} else {
    $names = @($running | ForEach-Object { $_.name })
    Say 'ok' "pm2 running: $($names -join ', ')" $null
    foreach ($app in $running) {
        if ($app.pm2_env.status -ne 'online') {
            Say 'fail' "$($app.name) is $($app.pm2_env.status), not online" $null
        }
    }
    if ($names -contains 'sd-webui') {
        Say 'fail' "sd-webui is running -- A1111 was removed 2026-08-29" @(
            "It holds VRAM ComfyUI wants. Clear it from the saved list too:",
            "  pm2 delete sd-webui; pm2 save"
        )
    }
}

$dumpPath = Join-Path $env:USERPROFILE '.pm2\dump.pm2'
if (-not (Test-Path $dumpPath)) {
    Say 'fail' "no pm2 dump at $dumpPath" "Nothing would come back on reboot. Run: pm2 save"
} else {
    $dump = $null
    try { $dump = Get-Content -Raw -Path $dumpPath | ConvertFrom-Json } catch {}
    if (-not $dump) {
        Say 'unknown' "could not parse $dumpPath" $null
    } else {
        $dumpNames = @($dump | ForEach-Object { $_.name })
        Say 'ok' "pm2 would restore on reboot: $($dumpNames -join ', ')" $null
        if ($dumpNames -contains 'sd-webui') {
            Say 'fail' "the SAVED list still contains sd-webui" @(
                "Deleting it from the running list is not enough -- the dump is what",
                "a reboot replays. Fix: pm2 delete sd-webui; pm2 save"
            )
        }
        if ($running) {
            $runNames = @($running | ForEach-Object { $_.name })
            $drift = @($runNames | Where-Object { $dumpNames -notcontains $_ }) +
                     @($dumpNames | Where-Object { $runNames -notcontains $_ })
            if ($drift.Count) {
                Say 'warn' "running list and saved list disagree: $($drift -join ', ')" @(
                    "A reboot restores the SAVED list. Run 'pm2 save' once the running",
                    "list is the one you actually want."
                )
            }
        }
        # The stale-env trap, checked directly rather than inferred.
        foreach ($app in $dump) {
            if ($app.name -eq 'kr-relay') {
                $savedRoot = $app.env.KR_SHARE_ROOT
                $savedProbe = $app.env.KR_SHARE_PROBE_PATH
                if ($savedProbe -match '^[A-Za-z]:') {
                    Say 'fail' "saved kr-relay env still points at a drive letter ($savedProbe)" @(
                        "A reboot restores THIS, not whatever you setx afterwards. Fix:",
                        "  setx KR_SHARE_ROOT `"//192.168.7.172/pc`"",
                        "  (open a NEW shell) pm2 restart ecosystem.config.js --update-env",
                        "  pm2 save"
                    )
                } elseif ($savedProbe) {
                    Say 'ok' "saved kr-relay share probe: $savedProbe" $null
                } elseif ($savedRoot) {
                    Say 'ok' "saved kr-relay KR_SHARE_ROOT: $savedRoot" $null
                } else {
                    Say 'warn' "saved kr-relay env names no share path" @(
                        "With KR_SHARE_PROBE_PATH unset the relay's share gate is DISABLED:",
                        "it will claim jobs it cannot render and drain PENDING into FAILED."
                    )
                }
            }
        }
    }
}

# --- 6. ComfyUI actually answering -------------------------------------------
try {
    $resp = Invoke-WebRequest -Uri $ComfyUrl -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    if ($resp.StatusCode -eq 200) {
        Say 'ok' "ComfyUI answering on $ComfyUrl" $null
    } else {
        Say 'fail' "ComfyUI returned HTTP $($resp.StatusCode)" $null
    }
} catch {
    Say 'fail' "ComfyUI not answering on $ComfyUrl" @(
        "If pm2 says comfyui is 'online', it is probably still booting --",
        "custom nodes and the registry fetch take minutes. Re-run in 2 min.",
        "A green /system_stats says nothing about whether it can read models."
    )
}

# --- 7. Is the relay's share gate armed, and on what? ------------------------
$relayLog = Join-Path $PSScriptRoot 'logs\kr-relay.out.log'
if (Test-Path $relayLog) {
    $gate = Get-Content -Path $relayLog -Tail 400 |
        Select-String -Pattern 'share gate' | Select-Object -Last 1
    if (-not $gate) {
        Say 'unknown' "no 'share gate' line in the last 400 log lines" "Restart kr-relay and re-check; it logs the gate at startup."
    } elseif ("$gate" -match 'disabled') {
        Say 'fail' "relay share gate is DISABLED" @(
            "KR_SHARE_PROBE_PATH is unset in that process. The relay will claim",
            "jobs against an unreadable share and convert PENDING into FAILED."
        )
    } elseif ("$gate" -match '[A-Za-z]:[\\/]') {
        Say 'warn' "relay share gate is armed on a DRIVE LETTER" @(
            ("$gate".Trim()),
            "Works until a reboot or a session change takes the letter away.",
            "Move it to the UNC path via KR_SHARE_ROOT (see the saved-env check)."
        )
    } else {
        Say 'ok' "relay share gate armed" ("$gate".Trim())
    }
} else {
    Say 'unknown' "no relay log at $relayLog" $null
}

# --- 8. ComfyUI's own model paths --------------------------------------------
# Not in this repo -- ComfyUI reads its own copy, and leaving it on Z: while the
# relay runs on UNC splits the two: the relay claims work ComfyUI then fails.
$emp = 'D:\comfy\comfy-fast\extra_model_paths.yaml'
if (Test-Path $emp) {
    $base = Get-Content -Path $emp | Select-String -Pattern '^\s*base_path:' | Select-Object -First 1
    if ("$base" -match '[A-Za-z]:[\\/]') {
        Say 'warn' "ComfyUI base_path is on a drive letter" @(
            ("$base".Trim()),
            "The tracked UNC reference copy is ops/home-server/extra_model_paths.yaml.",
            "Copy it over and restart comfyui (folder_paths caches its file lists)."
        )
    } elseif ($base) {
        Say 'ok' "ComfyUI base_path" ("$base".Trim())
    } else {
        Say 'unknown' "no base_path found in $emp" $null
    }
} else {
    Say 'unknown' "not found: $emp" $null
}

# --- 9. restore-shares snapshot ----------------------------------------------
$sharesJson = Join-Path $PSScriptRoot 'shares.json'
if (Test-Path $sharesJson) {
    Say 'ok' "restore-shares snapshot present" $sharesJson
} else {
    Say 'warn' "no shares.json -- restore-shares.ps1 has nothing to restore from" @(
        "Run once while the mappings are healthy:  .\restore-shares.ps1 -Save"
    )
}

Write-Host ("-" * 78)
if ($script:fail) {
    Write-Host "NOT reboot-safe: $($script:fail) failing, $($script:warn) warning, $($script:unknown) unknown"
    exit 1
} elseif ($script:warn -or $script:unknown) {
    Write-Host "Probably fine, with caveats: $($script:warn) warning, $($script:unknown) unknown"
    exit 0
} else {
    Write-Host "Reboot-safe: all checks passed."
    exit 0
}
