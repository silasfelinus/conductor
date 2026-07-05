# Health watchdog for the pm2-managed art backends.
# pm2 restarts a process that EXITS; this catches one that is alive but hung
# (API stops answering). Schedule via Task Scheduler every 5 minutes — see README.md.

$ErrorActionPreference = 'SilentlyContinue'

$targets = @(
    @{ Name = 'comfyui';  Url = 'http://127.0.0.1:8188/system_stats' },
    @{ Name = 'sd-webui'; Url = 'http://127.0.0.1:7860/sdapi/v1/progress' }
)

$logFile = Join-Path $PSScriptRoot 'logs\healthcheck.log'
New-Item -ItemType Directory -Force -Path (Split-Path $logFile) | Out-Null

function Write-Log($msg) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Add-Content -Path $logFile -Value "$stamp  $msg"
}

foreach ($t in $targets) {
    # Only police processes pm2 believes are online — a deliberate `pm2 stop`
    # (e.g. freeing the GPU) must not be fought by the watchdog.
    $status = (& pm2 jlist | ConvertFrom-Json) |
        Where-Object { $_.name -eq $t.Name } |
        Select-Object -ExpandProperty pm2_env -ErrorAction SilentlyContinue

    if (-not $status -or $status.status -ne 'online') { continue }

    $ok = $false
    try {
        $resp = Invoke-WebRequest -Uri $t.Url -TimeoutSec 20 -UseBasicParsing
        if ($resp.StatusCode -eq 200) { $ok = $true }
    } catch { $ok = $false }

    if (-not $ok) {
        Write-Log "$($t.Name): health probe failed ($($t.Url)) — restarting via pm2"
        & pm2 restart $t.Name | Out-Null
    }
}
