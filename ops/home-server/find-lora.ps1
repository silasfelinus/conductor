<#
.SYNOPSIS
  Find a LoRA file under the LoRA root when its Kind Robots `localPath` no longer
  matches what is actually on disk.

.DESCRIPTION
  Searches in increasing cost order, stopping at the first tier that finds it:

    1. NAME  — exact basename anywhere under the root, then a fuzzy token match.
               Free: directory metadata only.
    2. SIZE  — exact byte length. Free for the same reason, and a strong
               fingerprint: two unrelated LoRAs almost never share an exact size.
    3. HASH  — SHA256, computed ONLY for the handful of size matches.

  The ordering matters because the LoRA root is a network mount (Z: -> alexandria).
  Hashing all ~2200 files would read hundreds of GB across the wire; hashing three
  size-matched candidates reads a few GB.

  A file found under a path different from -LocalPath is the answer to "ComfyUI
  says value_not_in_list": the Resource row points somewhere the file is not.

.PARAMETER Sha256
  Expected SHA256. In Kind Robots this is Resource.hash, which scan_loras.py wrote
  from the file's own contents, so it survives any rename.

.PARAMETER Bytes
  Expected exact file size in bytes. Skip the tier by omitting it.

.EXAMPLE
  # Resource 1055 — "3D Cartoon Vision FLUX"
  .\find-lora.ps1 -Name '3D_Cartoon_Vision_flux_v1.safetensors' `
                  -LocalPath 'Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors' `
                  -Bytes 1374819344 `
                  -Sha256 'e4a2d4b7e4398297b33b0ed8ec4555c2306a508dd854c1962a430971707d4473'

.EXAMPLE
  # Name only, when you do not have the hash handy
  .\find-lora.ps1 -Name 'some_lora.safetensors'
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Name,
  [string]$LocalPath = '',
  [string]$Sha256 = '',
  [long]$Bytes = 0,
  [string]$Root = 'Z:\ai\models\Lora'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Root)) {
  Write-Error "LoRA root not found: $Root"
  exit 1
}

Write-Host "Root      : $Root"
Write-Host "Looking   : $Name"
if ($LocalPath) { Write-Host "DB says   : $LocalPath" }
Write-Host ''

# Enumerate once and reuse. On a network mount this single walk is the expensive
# part; every tier below is an in-memory filter over its result.
Write-Host 'Indexing files (one pass)...'
$all = Get-ChildItem -LiteralPath $Root -Recurse -File -Include *.safetensors,*.ckpt,*.pt,*.gguf -ErrorAction SilentlyContinue
Write-Host ("Indexed {0} model files." -f $all.Count)
Write-Host ''

function Show-Hit {
  param($File, [string]$How)
  $rel = $File.FullName.Substring($Root.Length).TrimStart('\', '/')
  $comfy = $rel -replace '\\', '/'
  Write-Host ''
  Write-Host "  FOUND via $How" -ForegroundColor Green
  Write-Host "    on disk      : $($File.FullName)"
  Write-Host "    size         : $($File.Length) bytes"
  Write-Host "    ComfyUI path : $comfy" -ForegroundColor Cyan
  if ($LocalPath) {
    $want = $LocalPath -replace '\\', '/'
    if ($comfy -ieq $want) {
      Write-Host '    matches the Resource localPath.' -ForegroundColor Green
    }
    else {
      Write-Host "    DB localPath : $want" -ForegroundColor Yellow
      Write-Host '    MISMATCH -> update the Resource row to the ComfyUI path above.' -ForegroundColor Yellow
    }
  }
}

# --- Tier 1: name ----------------------------------------------------------
$exact = $all | Where-Object { $_.Name -ieq $Name }
if ($exact) {
  Write-Host "Tier 1 (exact name): $($exact.Count) match(es)."
  $exact | ForEach-Object { Show-Hit -File $_ -How 'exact filename' }
  exit 0
}
Write-Host 'Tier 1 (exact name): no match.'

# Fuzzy: split the target into alphanumeric tokens and require most of them.
# Catches "3d-cartoon-vision-flux-v1.safetensors", "3DCartoonVision_v1.safetensors",
# copies suffixed with " (1)", and case/separator churn.
$stem = [IO.Path]::GetFileNameWithoutExtension($Name)
$tokens = @($stem -split '[^A-Za-z0-9]+' | Where-Object { $_.Length -ge 2 })
if ($tokens.Count -gt 0) {
  $need = [Math]::Max(2, [int][Math]::Ceiling($tokens.Count * 0.6))
  $fuzzy = $all | ForEach-Object {
    $flat = ($_.BaseName -replace '[^A-Za-z0-9]', '').ToLower()
    $hits = @($tokens | Where-Object { $flat -like "*$($_.ToLower())*" }).Count
    if ($hits -ge $need) { [pscustomobject]@{ File = $_; Score = $hits } }
  } | Sort-Object Score -Descending

  if ($fuzzy) {
    Write-Host ("Tier 1b (fuzzy name): {0} candidate(s), needed {1}/{2} tokens." -f $fuzzy.Count, $need, $tokens.Count)
    $fuzzy | Select-Object -First 10 | ForEach-Object {
      Show-Hit -File $_.File -How "fuzzy name ($($_.Score)/$($tokens.Count) tokens)"
    }
    Write-Host ''
    Write-Host 'Confirm the right one with the hash tier before editing the DB.' -ForegroundColor Yellow
  }
  else {
    Write-Host 'Tier 1b (fuzzy name): no match.'
  }
}

# --- Tier 2: exact size ----------------------------------------------------
if ($Bytes -gt 0) {
  $bySize = $all | Where-Object { $_.Length -eq $Bytes }
  if ($bySize) {
    Write-Host ''
    Write-Host "Tier 2 (exact size $Bytes bytes): $($bySize.Count) match(es)."
    $bySize | ForEach-Object { Show-Hit -File $_ -How 'exact byte size' }
    if (-not $Sha256) { exit 0 }
  }
  else {
    Write-Host ''
    Write-Host "Tier 2 (exact size $Bytes bytes): no match."
  }
}

# --- Tier 3: hash, only over plausible candidates --------------------------
if ($Sha256) {
  $candidates = if ($Bytes -gt 0) { $all | Where-Object { $_.Length -eq $Bytes } } else { $all }
  Write-Host ''
  Write-Host ("Tier 3 (SHA256): hashing {0} candidate(s)..." -f $candidates.Count)
  if ($Bytes -le 0) {
    Write-Host '  No -Bytes given, so this hashes EVERY file. Slow over a network mount.' -ForegroundColor Yellow
  }
  $found = $false
  foreach ($f in $candidates) {
    $h = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
    if ($h -ieq $Sha256) { Show-Hit -File $f -How 'SHA256'; $found = $true; break }
  }
  if (-not $found) {
    Write-Host ''
    Write-Host '  No file under the root has that SHA256.' -ForegroundColor Red
    Write-Host '  The file is genuinely absent, not mislabeled — re-download it from:'
    Write-Host '    https://civitai.com/models/662924?modelVersionId=741868'
  }
}

Write-Host ''
Write-Host 'Note: this finds ONE file. To reconcile every Resource against what'
Write-Host 'ComfyUI actually exposes, capture /object_info and run:'
Write-Host '  python scripts/compare_comfy_lora_paths.py --object-info object-info.json \'
Write-Host '    --resources resources.json --output lora-path-report.json'
Write-Host 'See projects/ai-art-academy/docs/t-044-comfy-lora-path-diagnostics.md'
