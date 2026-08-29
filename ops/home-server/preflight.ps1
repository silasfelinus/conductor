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
        'info' { '[INFO]' }
        default { '[ ?? ]' }
    }
    if ($level -eq 'fail') { $script:fail++ }
    elseif ($level -eq 'warn') { $script:warn++ }
    elseif ($level -eq 'unknown') { $script:unknown++ }
    Write-Host "$tag $name"
    if ($detail) { foreach ($d in @($detail)) { Write-Host "       $d" } }
}

# PowerShell 5.1's ConvertFrom-Json is JavaScriptSerializer with a MaxJsonLength
# cap it will not tell you about -- pm2's jlist carries every app's full
# environment and blows straight past it. Raise the cap and parse directly.
# Returns nested hashtables/arrays (not PSObjects), so read fields with Prop.
function ConvertFrom-JsonBig($text) {
    if (-not $text) { return $null }
    Add-Type -AssemblyName System.Web.Extensions -ErrorAction Stop
    $ser = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $ser.MaxJsonLength = [int]::MaxValue
    $ser.RecursionLimit = 1024
    return $ser.DeserializeObject($text)
}

# Field access that works on both hashtables (ConvertFrom-JsonBig) and
# PSObjects, so callers do not care which parser produced the object.
function Prop($obj, $key) {
    if ($null -eq $obj) { return $null }
    # Index; do NOT call .Contains(). DeserializeObject returns
    # Dictionary[string,object], which implements the non-generic IDictionary
    # EXPLICITLY -- so `-is [IDictionary]` is true while `.Contains()` is not a
    # publicly bound method and silently resolves to nothing under
    # SilentlyContinue. That returned $null for every field and printed a wall
    # of '[FAIL]  is , not online' on a healthy box (2026-08-29). The indexer is
    # public on both the generic and non-generic shapes.
    if ($obj -is [System.Collections.IDictionary]) { return $obj[$key] }
    return $obj.$key
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
# Reported as INFO, not a warning: SESSIONNAME is empty in plenty of perfectly
# good shells (Windows Terminal among them), and warning on that alone cried
# wolf on a session whose drives, credential and pm2 all worked. It only
# matters as an explanation for a FAIL, so the summary raises it there instead.
$sessionName = $env:SESSIONNAME
$script:onConsole = ($sessionName -eq 'Console' -or $sessionName -like 'RDP-Tcp*')
$shown = if ($sessionName) { $sessionName } else { '(not set)' }
Say 'info' "logon session: $shown" $(if (-not $script:onConsole) {
    "Not identifiably the console. Only matters if something below FAILs."
} else { $null })

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
# 2>$null, not 2>&1: merging pm2's stderr chatter into the string corrupts the
# JSON before it is ever parsed.
$jlistRaw = (& pm2 jlist 2>$null) -join ''
$running = $null
$jlistErr = $null
if ($jlistRaw) {
    try { $running = ConvertFrom-JsonBig $jlistRaw } catch { $jlistErr = $_.Exception.Message }
}
if (-not $running) {
    $why = if (-not $jlistRaw) {
        "pm2 produced no output. Its daemon is per-user, and WSL's pm2 is a separate world -- run this from the Windows account that owns the engines."
    } elseif ($jlistErr) {
        "pm2 answered but the output could not be parsed: $jlistErr"
    } else {
        "pm2 answered with output this script could not read."
    }
    Say 'unknown' "pm2 returned no usable process list" $why
} else {
    $names = @($running | ForEach-Object { Prop $_ 'name' } | Where-Object { $_ })
    if (-not $names.Count) {
        # Never report a wall of failures on the strength of fields we could not
        # read -- that is indistinguishable from every app being down, and it is
        # the script that is broken, not the box.
        Say 'unknown' "pm2 answered but no app names could be read" @(
            "The process list parsed, but its fields did not. Treating this as",
            "'cannot tell', not as every app being down."
        )
    } else {
        Say 'ok' "pm2 running: $($names -join ', ')" $null
        foreach ($app in $running) {
            $appName = Prop $app 'name'
            $st = Prop (Prop $app 'pm2_env') 'status'
            if ($appName -and $st -ne 'online') {
                Say 'fail' "$appName is $st, not online" $null
            }
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
    $dumpErr = $null
    try { $dump = ConvertFrom-JsonBig (Get-Content -Raw -Path $dumpPath) }
    catch { $dumpErr = $_.Exception.Message }
    if (-not $dump) {
        Say 'unknown' "could not parse $dumpPath" $dumpErr
    } else {
        $dumpNames = @($dump | ForEach-Object { Prop $_ 'name' } | Where-Object { $_ })
        if (-not $dumpNames.Count) {
            Say 'unknown' "dump.pm2 parsed but no app names could be read" $null
        } else {
            Say 'ok' "pm2 would restore on reboot: $($dumpNames -join ', ')" $null
        }
        if ($dumpNames -contains 'sd-webui') {
            Say 'fail' "the SAVED list still contains sd-webui" @(
                "Deleting it from the running list is not enough -- the dump is what",
                "a reboot replays. Fix: pm2 delete sd-webui; pm2 save"
            )
        }
        if ($running) {
            $runNames = @($running | ForEach-Object { Prop $_ 'name' })
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
            if ((Prop $app 'name') -eq 'kr-relay') {
                $savedEnv = Prop $app 'env'
                $savedRoot = Prop $savedEnv 'KR_SHARE_ROOT'
                $savedProbe = Prop $savedEnv 'KR_SHARE_PROBE_PATH'
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
    if (-not $script:onConsole) {
        Write-Host ""
        Write-Host "NOTE: this did not run from an identifiable console session. Drive"
        Write-Host "letters and credentials are per-logon-session, so re-run from the"
        Write-Host "console before acting on a FAIL above."
    }
    exit 1
} elseif ($script:warn -or $script:unknown) {
    Write-Host "Probably fine, with caveats: $($script:warn) warning, $($script:unknown) unknown"
    exit 0
} else {
    Write-Host "Reboot-safe: all checks passed."
    exit 0
}
