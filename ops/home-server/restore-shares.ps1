# Restore this box's SMB drive mappings after a reboot of THIS machine.
#
# This is the client-reboot companion to healthcheck.ps1's share watchdog. They
# cover different failures and neither substitutes for the other:
#
#   healthcheck.ps1  the NAS went away while this box stayed up. Probes ONE path
#                    (KR_SHARE_PROBE_PATH), remaps ONE letter (KR_SHARE_UNC),
#                    restarts comfyui when the share returns. Runs every 5 min.
#   this script       THIS box rebooted. Every mapping is gone at once, there is
#                    more than one of them, and the 5-minute watchdog may not
#                    even be running yet (a schtasks task created without /RU
#                    runs only while its user is logged on). Runs at logon.
#
# THE THING THAT MAKES THIS ANNOYING: a mapped drive letter belongs to one
# Windows logon session. The letters your desktop sees are not the letters a
# service sees, are not the letters an elevated shell sees, and are not the
# letters a Task Scheduler run sees. Restoring Z: from a task that runs as
# SYSTEM does nothing for you, and restoring it from your desktop does nothing
# for a pm2 service. That is why a `net use` listing read from the wrong
# terminal has twice been misread here as "the array is down" (ai-art-academy
# t-033, 2026-08-25) when the console session's mappings were fine.
#
# So the split this repo settled on, and which this script assumes:
#
#   * THE PIPELINE SHOULD NOT USE LETTERS -- but verify rather than assume.
#     KR_SHARE_ROOT and extra_model_paths.yaml both default to the UNC path
#     (//192.168.7.172/pc), and UNC has no logon session to lose. On 2026-08-29
#     the box was nonetheless still on Z: two days after the repo recorded the
#     move, because pm2 resurrect replays the env captured at the last pm2 save
#     and the setx came after it. Check the process, not the config: pm2 logs
#     kr-relay should say 'share gate armed on //192.168.7.172/pc/ai/models'.
#     Either way it needs the CREDENTIAL, which is per-user and which fails
#     exactly like a dead NAS -- see -Check below.
#   * THE LETTERS ARE FOR YOU. Explorer, shells, anything that wants Z:. Those
#     are worth restoring at logon, which is what this does.
#
# Usage (PowerShell, as your normal user -- NOT elevated, NOT as SYSTEM, or you
# will map letters into a session you are not sitting in):
#
#   .\restore-shares.ps1 -Save     # once, while the mappings are healthy:
#                                  # snapshot them to shares.json
#   .\restore-shares.ps1 -Check    # report only, mutate nothing
#   .\restore-shares.ps1           # restore anything missing or unreadable
#
# Register it to run at every logon (see README for the Run-as caveat):
#
#   schtasks /Create /SC ONLOGON /TN "Restore-SMB-Shares" /RL LIMITED `
#     /TR "powershell -NoProfile -ExecutionPolicy Bypass -File \"<path>\restore-shares.ps1\""
#
# Config, in precedence order:
#   1. KR_SHARE_MAP env var:  "Z=\\192.168.7.172\pc;Y=\\192.168.7.172\media"
#   2. shares.json next to this script (written by -Save, gitignored -- the
#      letter/UNC table is box-specific, and the file is not tracked so a
#      checkout on another machine cannot map someone else's shares)
#
# Keep this file ASCII-only, same reason as healthcheck.ps1: Windows PowerShell
# 5.1 reads a no-BOM script as the system ANSI codepage, so UTF-8 punctuation
# inside a string literal corrupts parsing.

[CmdletBinding()]
param(
    [switch]$Save,
    [switch]$Check,
    # Seconds to keep retrying the file server at boot before giving up. A
    # logon trigger fires while the NIC may still be negotiating, so the first
    # attempt failing is normal and is not a reason to alert.
    [int]$WaitSeconds = 90
)

$ErrorActionPreference = 'SilentlyContinue'

$configFile = Join-Path $PSScriptRoot 'shares.json'
$logFile = Join-Path $PSScriptRoot 'logs\restore-shares.log'
New-Item -ItemType Directory -Force -Path (Split-Path $logFile) | Out-Null

function Write-Log($msg) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $line = "$stamp  $msg"
    Add-Content -Path $logFile -Value $line
    Write-Host $line
}

function Trim-Log {
    try {
        if (-not (Test-Path $logFile)) { return }
        $lines = @(Get-Content -Path $logFile)
        if ($lines.Count -le 4000) { return }
        $lines[-2000..-1] | Set-Content -Path $logFile
    } catch {}
}

function Get-CurrentMappings {
    $map = @{}
    $smb = Get-SmbMapping -ErrorAction SilentlyContinue
    if ($smb) {
        foreach ($m in $smb) {
            if ($m.LocalPath -match '^([A-Za-z]:)') {
                $map[$Matches[1].ToUpper()] = [pscustomobject]@{
                    Unc    = $m.RemotePath
                    Status = [string]$m.Status
                }
            }
        }
        return $map
    }
    foreach ($line in (& net use 2>&1)) {
        $text = "$line"
        if ($text -match '([A-Za-z]:)\s+(\\\\[^\s]+)') {
            $letter = $Matches[1].ToUpper()
            $unc = $Matches[2]
            $status = 'Unknown'
            if ($text -match '^\s*(\S+)\s+[A-Za-z]:') { $status = $Matches[1] }
            $map[$letter] = [pscustomobject]@{
                Unc    = $unc
                Status = $status
            }
        }
    }
    return $map
}

function Test-PathReadable($path) {
    if (-not $path) { return $false }
    try {
        $null = Get-ChildItem -LiteralPath $path -Force -ErrorAction Stop |
            Select-Object -First 1
        return $true
    } catch {
        return $false
    }
}

function Get-UncHost($unc) {
    if ("$unc" -match '^\\\\([^\\]+)\\') { return $Matches[1] }
    return $null
}

function Test-SmbHostUp($hostName, $timeoutMs = 3000) {
    if (-not $hostName) { return $false }
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $async = $client.BeginConnect($hostName, 445, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne($timeoutMs, $false)) { return $false }
        $client.EndConnect($async)
        return $true
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

function Test-CredentialStored($hostName) {
    if (-not $hostName) { return $false }
    $out = (& cmdkey /list 2>&1) -join "`n"
    return ($out -match [regex]::Escape($hostName))
}

function Read-ShareMap {
    if ($env:KR_SHARE_MAP) {
        $entries = @()
        foreach ($pair in ($env:KR_SHARE_MAP -split ';')) {
            if ("$pair".Trim() -match '^([A-Za-z]):?=(.+)$') {
                $entries += [pscustomobject]@{
                    Letter = ($Matches[1].ToUpper() + ':')
                    Unc    = $Matches[2].Trim()
                }
            }
        }
        if ($entries.Count) { return $entries }
        Write-Log "KR_SHARE_MAP is set but parsed to nothing - expected 'Z=\\host\share;Y=\\host\other'"
    }
    if (Test-Path $configFile) {
        try {
            $obj = Get-Content -Raw -Path $configFile | ConvertFrom-Json
            $entries = @()
            foreach ($p in $obj.PSObject.Properties) {
                $entries += [pscustomobject]@{
                    Letter = ($p.Name.TrimEnd(':').ToUpper() + ':')
                    Unc    = [string]$p.Value
                }
            }
            return $entries
        } catch {
            Write-Log "could not parse $configFile - $($_.Exception.Message)"
        }
    }
    return @()
}

function Save-ShareMap {
    $current = Get-CurrentMappings
    if (-not $current.Count) {
        Write-Log "-Save found no drive mappings in this logon session. Nothing written."
        Write-Log "  Run this from the session whose letters you actually want restored"
        Write-Log "  (your desktop shell), while they are healthy."
        return 1
    }
    $out = @{}
    $skipped = @()
    foreach ($letter in ($current.Keys | Sort-Object)) {
        $entry = $current[$letter]
        if (Test-PathReadable "$letter\") {
            $out[$letter] = $entry.Unc
        } else {
            $skipped += "$letter -> $($entry.Unc) (status $($entry.Status), not readable)"
        }
    }
    if (-not $out.Count) {
        Write-Log "-Save found mappings but none are readable right now. Nothing written."
        foreach ($s in $skipped) { Write-Log "  skipped $s" }
        return 1
    }
    ($out | ConvertTo-Json) | Set-Content -Path $configFile
    Write-Log "saved $($out.Count) mapping(s) to $configFile"
    foreach ($letter in ($out.Keys | Sort-Object)) { Write-Log "  $letter -> $($out[$letter])" }
    foreach ($s in $skipped) { Write-Log "  skipped $s" }
    return 0
}

Write-Log "restore-shares starting as user '$($env:USERNAME)' on '$($env:COMPUTERNAME)' (mode: $(if ($Save) {'save'} elseif ($Check) {'check'} else {'restore'}))"

if ($Save) {
    $rc = Save-ShareMap
    Trim-Log
    exit $rc
}

$wanted = Read-ShareMap
if (-not $wanted.Count) {
    Write-Log "no share map configured - set KR_SHARE_MAP or run: .\restore-shares.ps1 -Save"
    Write-Log "  (this script maps letters only; the render pipeline itself runs on UNC"
    Write-Log "   paths via KR_SHARE_ROOT and does not need any of these)"
    Trim-Log
    exit 2
}

$hosts = @($wanted | ForEach-Object { Get-UncHost $_.Unc } | Where-Object { $_ } | Sort-Object -Unique)
$waitFor = if ($Check) { 0 } else { $WaitSeconds }
$credentialFailures = @()
foreach ($h in $hosts) {
    $deadline = (Get-Date).AddSeconds($waitFor)
    $up = Test-SmbHostUp $h
    while (-not $up -and (Get-Date) -lt $deadline) {
        Start-Sleep -Seconds 5
        $up = Test-SmbHostUp $h
    }
    if ($up) {
        Write-Log "$h : SMB (445) reachable"
    } elseif ($Check) {
        Write-Log "$h : NOT reachable on 445 - is the NAS up?"
    } else {
        Write-Log "$h : NOT reachable on 445 after $waitFor s - is the NAS up?"
    }
    if (-not (Test-CredentialStored $h)) {
        Write-Log "$h : NO STORED CREDENTIAL (cmdkey). This looks identical to a dead"
        Write-Log "  NAS from every consumer, including ComfyUI on the UNC path. Fix with:"
        Write-Log "    cmdkey /add:$h /user:<user> /pass"
        Write-Log "  Note cmdkey is per-user: the account pm2 runs as needs its own."
        $credentialFailures += $h
    }
}

$current = Get-CurrentMappings
$restored = @()
$failed = @()
$alreadyOk = @()

foreach ($w in $wanted) {
    $letter = $w.Letter
    $unc = $w.Unc
    $root = "$letter\"
    $existing = $current[$letter]

    if ($existing -and (Test-PathReadable $root)) {
        if ($existing.Unc -and ($existing.Unc.TrimEnd('\') -ne $unc.TrimEnd('\'))) {
            if ($Check) {
                Write-Log "$letter -> $unc : BROKEN (readable but points at $($existing.Unc))"
                $failed += $letter
                continue
            }
            Write-Log "$letter is readable but points at $($existing.Unc), not $unc - remapping to configured target"
        } else {
            $alreadyOk += $letter
            continue
        }
    }

    if ($Check) {
        $why = if ($existing) { 'status ' + $existing.Status + ', not readable' } else { 'not mapped' }
        Write-Log "$letter -> $unc : BROKEN ($why)"
        $failed += $letter
        continue
    }

    $state = if ($existing) { 'status ' + $existing.Status } else { 'not mapped' }
    Write-Log "$letter -> $unc : remapping ($state)"
    & cmd.exe /c "net use $letter /delete /y < NUL" 2>&1 | Out-Null
    $out = (& cmd.exe /c "net use $letter $unc /persistent:yes < NUL" 2>&1) -join ' '
    if (Test-PathReadable $root) {
        Write-Log "$letter : restored"
        $restored += $letter
    } else {
        Write-Log "$letter : REMAP FAILED - $($out.Trim())"
        $failed += $letter
    }
}

if ($alreadyOk.Count) { Write-Log "already healthy: $($alreadyOk -join ', ')" }
if ($restored.Count) { Write-Log "restored: $($restored -join ', ')" }
if ($failed.Count) { Write-Log "still broken: $($failed -join ', ')" }
if ($credentialFailures.Count) { Write-Log "missing stored credential: $($credentialFailures -join ', ')" }

if ($restored.Count -and -not $Check) {
    $jlist = (& pm2 jlist 2>&1) -join ''
    if ($jlist -match '"name"\s*:\s*"comfyui"') {
        Write-Log "restarting comfyui so folder_paths rebuilds its cached filename lists"
        & pm2 restart comfyui | Out-Null
    } else {
        Write-Log "pm2 did not list comfyui from this session - not restarting it."
        Write-Log "  pm2's daemon is per-user; if the engines run under another account,"
        Write-Log "  restart comfyui from that account after this."
    }
}

Trim-Log
if ($failed.Count -or $credentialFailures.Count) { exit 1 }
exit 0
