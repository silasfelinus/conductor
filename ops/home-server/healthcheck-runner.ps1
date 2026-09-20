$ErrorActionPreference = 'Stop'

$healthcheck = Join-Path $PSScriptRoot 'healthcheck.ps1'
$restartTrend = Join-Path $PSScriptRoot 'check-pm2-restart-trend.ps1'

# Keep the existing watchdog as the primary operation. The slow restart trend is
# advisory observability only, so a failure there must not disable health recovery.
& $healthcheck

try {
    & $restartTrend
} catch {
    Write-Warning "PM2 restart trend check failed: $($_.Exception.Message)"
}
