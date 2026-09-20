param(
    [string]$StatePath = "$PSScriptRoot/pm2-restart-trend-state.json",
    [string]$AdvisoryLogPath = "$PSScriptRoot/pm2-restart-trend-advisories.log",
    [int]$AbsoluteRestartThreshold = 25,
    [int]$WindowRestartDelta = 10,
    [int]$WindowHours = 168
)

$ErrorActionPreference = 'Stop'

function Read-State {
    if (-not (Test-Path -LiteralPath $StatePath)) { return @{} }
    try {
        $raw = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
        $state = @{}
        foreach ($property in $raw.PSObject.Properties) {
            $state[$property.Name] = $property.Value
        }
        return $state
    } catch {
        Write-Warning "Ignoring unreadable restart-trend state: $($_.Exception.Message)"
        return @{}
    }
}

function Write-State([hashtable]$State) {
    $parent = Split-Path -Parent $StatePath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $State | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $StatePath -Encoding UTF8
}

function Write-Advisory([hashtable]$Record) {
    $parent = Split-Path -Parent $AdvisoryLogPath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    ($Record | ConvertTo-Json -Compress) | Add-Content -LiteralPath $AdvisoryLogPath -Encoding UTF8
}

$helper = Join-Path $PSScriptRoot 'pm2-jlist-snapshot.js'
if (-not (Test-Path -LiteralPath $helper)) {
    throw "PM2 snapshot helper not found: $helper"
}

# pm2 can print warnings around its JSON. The existing helper owns extraction and
# normalization so this check consumes the same restart_time semantics as healthcheck.ps1.
$snapshotJson = (& pm2 jlist 2>$null | & node $helper)
if ($LASTEXITCODE -ne 0 -or -not $snapshotJson) {
    throw 'Unable to obtain normalized PM2 process snapshot.'
}
$processes = @($snapshotJson | ConvertFrom-Json)
$now = [DateTimeOffset]::UtcNow
$state = Read-State

foreach ($process in $processes) {
    if (-not $process.name) { continue }
    $name = [string]$process.name
    $restarts = [int]$process.restart_time
    $entry = $state[$name]

    if (-not $entry) {
        $entry = [pscustomobject]@{
            baseline_restart_time = $restarts
            baseline_at = $now.ToString('o')
            last_restart_time = $restarts
            last_seen_at = $now.ToString('o')
            last_alert_restart_time = -1
        }
    }

    $baselineAt = [DateTimeOffset]::Parse([string]$entry.baseline_at)
    if (($now - $baselineAt).TotalHours -ge $WindowHours -or $restarts -lt [int]$entry.baseline_restart_time) {
        $entry.baseline_restart_time = $restarts
        $entry.baseline_at = $now.ToString('o')
        $baselineAt = $now
    }

    $delta = $restarts - [int]$entry.baseline_restart_time
    $absoluteExceeded = $restarts -ge $AbsoluteRestartThreshold
    $trendExceeded = $delta -ge $WindowRestartDelta
    $newRestartEvidence = $restarts -gt [int]$entry.last_alert_restart_time

    if (($absoluteExceeded -or $trendExceeded) -and $newRestartEvidence) {
        $reason = if ($trendExceeded) { 'restart-trend' } else { 'restart-total' }
        Write-Advisory @{
            timestamp = $now.ToString('o')
            severity = 'advisory'
            signal = 'pm2-restart-trend'
            process = $name
            restart_time = $restarts
            baseline_restart_time = [int]$entry.baseline_restart_time
            window_delta = $delta
            window_hours = $WindowHours
            reason = $reason
        }
        Write-Warning "PM2 restart advisory: $name has $restarts total restarts ($delta since baseline)."
        $entry.last_alert_restart_time = $restarts
    }

    $entry.last_restart_time = $restarts
    $entry.last_seen_at = $now.ToString('o')
    $state[$name] = $entry
}

Write-State $state
