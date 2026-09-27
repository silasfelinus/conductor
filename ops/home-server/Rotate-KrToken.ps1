# Rotate-KrToken.ps1 -- rotate the Kind Robots admin token end to end from the
# render box, without ever printing it.
#
# Runbook: kind_robots docs/runbooks/admin-token-rotation.md. This script does
# the parts of it that are tedious or easy to forget.
#
# Why it runs HERE: the 2026-09-20 rotation updated the server and the GitHub
# secret but left kr-relay holding the old value. It could not claim ArtJobs,
# and from everywhere else that looked like "the box is off" -- Comfy went
# silent minutes after the rotation and stayed that way for about half a day
# (root TALKBACK.md, 2026-09-20). Two traps made that easy:
#
#   1. The relay does not read KR_API_TOKEN. kr-relay and kr-download read
#      KR_RELAY_TOKEN (ecosystem.config.js); only healthcheck.ps1's watchdog
#      reads KR_API_TOKEN. Same value, two names.
#   2. `pm2 restart` alone keeps the old env, and a reboot runs `pm2
#      resurrect`, which replays the env captured at the last `pm2 save`.
#      The change needs `--update-env` from a shell holding the new value,
#      THEN `pm2 save`.
#
# What it does, in order -- and it stops before changing anything if a check fails:
#   1. Reads the CURRENT token from this box's KR_API_TOKEN / KR_RELAY_TOKEN
#      (or prompts, hidden, if neither is set) and asks the server what it is.
#   2. If it is your User.apiKey ("user-api-key"): generates a new 64-hex
#      value and writes it through the machine-content API. No deploy needed.
#      If it is the ADMIN_TOKEN env var ("beta-admin-token"): generates the
#      value, puts it on the clipboard, and waits while you set it on
#      Alexandria and recreate the KindRobots container.
#      With -NewTokenOnly: skips all of that and prompts for a value you have
#      already rotated server-side.
#   3. Verifies the new value is admin and the old one now returns 401.
#   4. Writes KR_RELAY_TOKEN and KR_API_TOKEN at whichever scope each already
#      lives, restarts the pm2 ecosystem with --update-env, and runs pm2 save.
#   5. If the GitHub CLI is installed and logged in: sets the conductor repo's
#      KR_API_TOKEN Actions secret (and kind_robots' CYPRESS_BETA_ADMIN_TOKEN
#      for an env-var token), then runs sync-kind-robots-projection.yml as a
#      smoke test.
#   6. Prints the consumers no script can reach.
#
# Usage (elevated PowerShell if either variable is machine-scoped):
#   cd D:\code\Conductor\ops\home-server
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Rotate-KrToken.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\Rotate-KrToken.ps1 -NewTokenOnly
#
# Everything it prints is safe to paste into a chat. The token never is.
#
# Keep this file ASCII-only and Windows PowerShell 5.1 compatible, like its
# neighbours (Test-PowerShellSyntax.ps1 parses it in CI).

[CmdletBinding()]
param(
    [switch]$NewTokenOnly,
    [string]$BaseUrl = 'https://kindrobots.org',
    [string]$ConductorRepo = 'silasfelinus/conductor',
    [string]$KindRobotsRepo = 'silasfelinus/kind_robots'
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot
$EnvNames = @('KR_RELAY_TOKEN', 'KR_API_TOKEN')

function Read-HiddenValue {
    param([string]$Prompt)
    $secure = Read-Host -Prompt $Prompt -AsSecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr).Trim()
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

function New-HexToken {
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    return (-join ($bytes | ForEach-Object { $_.ToString('x2') }))
}

function Invoke-KrApi {
    # Returns @{ Code = <int>; Body = <object or $null> }. Never throws on HTTP errors.
    param([string]$Token, [hashtable]$Payload)
    $headers = @{ Authorization = ('Bearer ' + $Token) }
    $json = $Payload | ConvertTo-Json -Depth 6 -Compress
    try {
        $body = Invoke-RestMethod -Uri ($BaseUrl + '/api/chatgpt') -Method Post -Headers $headers `
            -ContentType 'application/json' -Body $json -TimeoutSec 30
        return @{ Code = 200; Body = $body }
    } catch {
        $code = 0
        if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
        return @{ Code = $code; Body = $null }
    }
}

function Get-Actor {
    param([string]$Token)
    $r = Invoke-KrApi -Token $Token -Payload @{ operation = 'meta.describe' }
    if ($r.Code -ne 200 -or -not $r.Body) { return @{ Code = $r.Code; Actor = $null } }
    $actor = $r.Body.data.actor
    if (-not $actor) { $actor = $r.Body.actor }
    return @{ Code = 200; Actor = $actor }
}

function Test-IsAdmin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Wait-ForToken {
    param([string]$Token)
    for ($i = 0; $i -lt 60; $i++) {
        $check = Get-Actor -Token $Token
        if ($check.Code -eq 200) { return $check }
        Start-Sleep -Seconds 10
    }
    return $check
}

# --- 1. what are we holding? -------------------------------------------------

$oldToken = $env:KR_API_TOKEN
if (-not $oldToken) { $oldToken = $env:KR_RELAY_TOKEN }
if (-not $oldToken -and -not $NewTokenOnly) {
    $oldToken = Read-HiddenValue -Prompt 'Current (old) token -- input hidden'
}

$source = $null
if ($oldToken) {
    $before = Get-Actor -Token $oldToken
    if ($before.Code -eq 200) {
        $source = $before.Actor.source
        Write-Host ('Current token is live: role={0}, source={1}, userId={2}.' -f `
            $before.Actor.role, $source, $before.Actor.userId)
    } else {
        Write-Host ('Current token on this box is already rejected (HTTP {0}).' -f $before.Code)
        if (-not $NewTokenOnly) {
            Write-Host 'That usually means the server side was rotated already. Re-run with -NewTokenOnly.'
            exit 1
        }
    }
}

# --- 2. make the new value live on the server --------------------------------

if ($NewTokenOnly) {
    $newToken = Read-HiddenValue -Prompt 'New token (already rotated server-side) -- input hidden'
    $confirm = Read-HiddenValue -Prompt 'Paste it again to confirm'
    if (-not $newToken -or $newToken -ne $confirm) {
        Write-Host 'STOP: the two entries were empty or did not match. Nothing was changed.'
        exit 1
    }
    $confirm = $null
} elseif ($source -eq 'user-api-key') {
    $newToken = New-HexToken
    Set-Clipboard -Value $newToken
    Write-Host 'New value generated and copied to the clipboard. Save it in your password manager NOW.'
    [void](Read-Host -Prompt 'Press Enter once it is saved (the old key stops working on the next step)')
    $update = Invoke-KrApi -Token $oldToken -Payload @{
        operation = 'content.update'; resource = 'user'; id = [int]$before.Actor.userId
        data = @{ apiKey = $newToken }
    }
    if ($update.Code -ne 200) {
        Write-Host ('STOP: the apiKey write failed (HTTP {0}). The old key is still the live one.' -f $update.Code)
        exit 1
    }
    Write-Host 'User.apiKey rewritten on the server.'
} elseif ($source -eq 'beta-admin-token') {
    $newToken = New-HexToken
    Set-Clipboard -Value $newToken
    Write-Host 'This token is the ADMIN_TOKEN env var on Alexandria, which no API can change.'
    Write-Host 'New value generated and copied to the clipboard. Save it in your password manager, then:'
    Write-Host '  1. Unraid > Docker > KindRobots > Edit: set ADMIN_TOKEN (or BETA_ADMIN_TOKEN, whichever'
    Write-Host '     exists) to the clipboard value, and check the .env beside docker-compose.yml too.'
    Write-Host '  2. Apply, so the container is RECREATED (a plain restart keeps the old env).'
    [void](Read-Host -Prompt 'Press Enter once the container is back up')
    Write-Host 'Waiting for the server to accept the new value (up to 10 minutes) ...'
} else {
    Write-Host ('STOP: unrecognised auth source "{0}". Follow the runbook by hand.' -f $source)
    exit 1
}

# --- 3. verify both directions ------------------------------------------------

$after = Wait-ForToken -Token $newToken
if ($after.Code -ne 200 -or $after.Actor.role -ne 'admin') {
    Write-Host ('STOP: the new token is not an admin on the server (HTTP {0}). Nothing on this box was changed.' -f $after.Code)
    exit 1
}
Write-Host ('New token verified: role={0}, source={1}.' -f $after.Actor.role, $after.Actor.source)
if ($oldToken) {
    $dead = Get-Actor -Token $oldToken
    if ($dead.Code -eq 401 -or $dead.Code -eq 403) {
        Write-Host ('Old token confirmed dead (HTTP {0}).' -f $dead.Code)
    } else {
        Write-Host ('WARNING: the old token still returns HTTP {0}. Something else still honours it --' -f $dead.Code)
        Write-Host '         check the retired Vercel deployment in the runbook before calling this done.'
    }
}

# --- 4. this box ----------------------------------------------------------------

$isAdmin = Test-IsAdmin
foreach ($name in $EnvNames) {
    $scopes = @()
    if ([Environment]::GetEnvironmentVariable($name, 'Machine')) { $scopes += 'Machine' }
    if ([Environment]::GetEnvironmentVariable($name, 'User')) { $scopes += 'User' }
    if ($scopes.Count -eq 0) { $scopes = @('User') }
    foreach ($scope in $scopes) {
        if ($scope -eq 'Machine' -and -not $isAdmin) {
            Write-Host ('STOP: {0} is machine-wide; re-run elevated with -NewTokenOnly (server is already rotated).' -f $name)
            exit 1
        }
        [Environment]::SetEnvironmentVariable($name, $newToken, $scope)
        Write-Host ('Set {0} at {1} scope.' -f $name, $scope)
    }
    Set-Item -Path ('Env:' + $name) -Value $newToken
}

# Native tools (pm2, gh) write progress to stderr; under 'Stop', Windows
# PowerShell 5.1 turns that into a terminating error.
$ErrorActionPreference = 'Continue'
Write-Host 'Restarting the pm2 ecosystem with --update-env, then saving the dump ...'
& pm2 restart ecosystem.config.js --update-env | Out-Null
& pm2 save | Out-Null
Start-Sleep -Seconds 15
$apps = & pm2 jlist | ConvertFrom-Json
foreach ($app in $apps) {
    if ($app.name -in @('kr-relay', 'kr-download')) {
        Write-Host ('  {0}: {1}, restarts={2}' -f $app.name, $app.pm2_env.status, $app.pm2_env.restart_time)
    }
}

# --- 5. GitHub secrets -----------------------------------------------------------

$ghDone = $false
if (Get-Command gh -ErrorAction SilentlyContinue) {
    & gh auth status 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        # --body, not a pipe: 5.1 appends CRLF to piped strings, which would
        # become part of the secret.
        & gh secret set KR_API_TOKEN --repo $ConductorRepo --body $newToken | Out-Null
        Write-Host ('Set KR_API_TOKEN on {0}.' -f $ConductorRepo)
        if ($after.Actor.source -eq 'beta-admin-token') {
            & gh secret set CYPRESS_BETA_ADMIN_TOKEN --repo $KindRobotsRepo --body $newToken | Out-Null
            Write-Host ('Set CYPRESS_BETA_ADMIN_TOKEN on {0}.' -f $KindRobotsRepo)
        }
        & gh workflow run sync-kind-robots-projection.yml --repo $ConductorRepo | Out-Null
        Write-Host 'Started sync-kind-robots-projection.yml as a smoke test: gh run list --repo silasfelinus/conductor -L 3'
        $ghDone = $true
    }
}

# --- 6. what no script can reach -----------------------------------------------------

$newToken = $null
$oldToken = $null
Write-Host ''
Write-Host 'Remaining by hand (the new value is still on your clipboard):'
if (-not $ghDone) {
    Write-Host ('  [ ] GitHub > {0} > Settings > Secrets and variables > Actions > KR_API_TOKEN' -f $ConductorRepo)
}
Write-Host '  [ ] claude.ai > Claude Code > your cloud environment > Edit > environment variable KR_API_TOKEN'
Write-Host '      (this is what agent sessions read -- miss it and every session 401s)'
Write-Host '  [ ] Serendipity / Alexa relay: SERENDIPITY_KR_SERVICE_TOKEN, if it carries this value'
Write-Host '  [ ] ChatGPT Custom GPT > Configure > Actions > Authentication, if it uses this value'
Write-Host '  [ ] Any other shell or .env where you keep KR_API_TOKEN (WSL profile, local checkouts)'
Write-Host '  [ ] Clear the clipboard: Set-Clipboard -Value $null'
Write-Host ''
Write-Host 'Then tell Conductor "rotated" and it will close the open rotation task.'
