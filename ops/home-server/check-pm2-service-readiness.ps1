# Read-only preflight for moving the Windows pm2 daemon into session 0.
# conductor/t-181: the service migration removes pidusage's visible PowerShell
# children, but only if the service can see the same saved process list and SMB
# resources as the interactive daemon. This script makes those prerequisites
# explicit before anyone changes the running service.

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$failures = @()

function Check([bool]$ok, [string]$message) {
    if ($ok) {
        Write-Host "OK   $message"
    } else {
        Write-Host "FAIL $message"
        $script:failures += $message
    }
}

$expectedPm2Home = 'C:\ProgramData\pm2\home'
$currentPm2Home = [Environment]::GetEnvironmentVariable('PM2_HOME', 'Process')
if (-not $currentPm2Home) {
    $currentPm2Home = [Environment]::GetEnvironmentVariable('PM2_HOME', 'User')
}
Check ($currentPm2Home -eq $expectedPm2Home) "PM2_HOME is $expectedPm2Home"

$shareRoot = [Environment]::GetEnvironmentVariable('KR_SHARE_ROOT', 'Process')
if (-not $shareRoot) {
    $shareRoot = [Environment]::GetEnvironmentVariable('KR_SHARE_ROOT', 'User')
}
$isUnc = $shareRoot -and ($shareRoot.StartsWith('\\') -or $shareRoot.StartsWith('//'))
Check $isUnc 'KR_SHARE_ROOT is an explicit UNC path, not a mapped drive letter'

if ($isUnc) {
    Check (Test-Path -LiteralPath $shareRoot) 'KR_SHARE_ROOT is readable in this user context'
    $modelRoot = Join-Path $shareRoot 'ai\models'
    Check (Test-Path -LiteralPath $modelRoot) 'model root is readable through the UNC path'
}

$pm2 = Get-Command pm2 -ErrorAction SilentlyContinue
Check ($null -ne $pm2) 'pm2 is available on PATH'

if ($pm2) {
    $json = & pm2 jlist 2>$null
    $apps = @()
    if ($LASTEXITCODE -eq 0 -and $json) {
        try { $apps = @($json | ConvertFrom-Json) } catch {}
    }
    $names = @($apps | ForEach-Object { $_.name })
    Check ($names -contains 'comfyui') 'current pm2 daemon sees comfyui'
    Check ($names -contains 'kr-relay') 'current pm2 daemon sees kr-relay'
}

$dump = Join-Path $expectedPm2Home 'dump.pm2'
Check (Test-Path -LiteralPath $dump) 'shared PM2_HOME contains dump.pm2 for service resurrection'

if ($failures.Count -gt 0) {
    Write-Host ''
    Write-Host ("BLOCKED: {0} service-migration prerequisite(s) failed. Do not switch pm2 to session 0 yet." -f $failures.Count)
    exit 1
}

Write-Host ''
Write-Host 'READY: service prerequisites pass. After installing/configuring the service, verify the next healthcheck tick still lists comfyui and kr-relay before removing logon startup.'
exit 0
