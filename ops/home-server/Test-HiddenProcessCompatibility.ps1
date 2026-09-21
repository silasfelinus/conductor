# Runtime smoke test for healthcheck.ps1's windowless child-process helper.
#
# This intentionally runs under Windows PowerShell 5.1 in CI. PR #4901 was
# behavior-tested under PowerShell 7 on Linux, where ProcessStartInfo.ArgumentList
# exists; SILAS-PC runs Windows PowerShell 5.1 on .NET Framework, where it does not.
# A parser-only check cannot catch that runtime API mismatch.

$ErrorActionPreference = 'Stop'

$healthcheck = Join-Path $PSScriptRoot 'healthcheck.ps1'
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile(
    $healthcheck,
    [ref]$tokens,
    [ref]$errors
)

if ($errors.Count -gt 0) {
    throw "healthcheck.ps1 has parse errors; runtime smoke test cannot continue"
}

foreach ($name in @('ConvertTo-NativeArgumentString', 'Invoke-HiddenProcess')) {
    $definition = $ast.FindAll(
        {
            param($node)
            $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and
                $node.Name -eq $name
        },
        $true
    ) | Select-Object -First 1

    if (-not $definition) {
        throw "healthcheck.ps1 is missing function $name"
    }

    Invoke-Expression $definition.Extent.Text
}

$quoted = ConvertTo-NativeArgumentString @(
    'plain',
    'two words',
    'quote"inside',
    'C:\two words\'
)
$expected = 'plain "two words" "quote\"inside" "C:\two words\\"'
if ($quoted -ne $expected) {
    throw "Windows argument quoting mismatch. Expected [$expected], got [$quoted]"
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) (
    'conductor healthcheck smoke ' + [guid]::NewGuid().ToString('N')
)
$batch = Join-Path $tempRoot 'pm2 fake.cmd'

try {
    New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
    Set-Content -LiteralPath $batch -Encoding ASCII -Value @(
        '@echo off',
        'echo %~1'
    )

    $result = Invoke-HiddenProcess $batch @('hello world') 10 $null

    if ($result.TimedOut) {
        throw 'Invoke-HiddenProcess timed out launching the batch-file smoke target'
    }
    if ($result.ExitCode -ne 0) {
        throw "Invoke-HiddenProcess exited $($result.ExitCode): $($result.Output)"
    }
    if ($result.Output.Trim() -ne 'hello world') {
        throw "Invoke-HiddenProcess argument round-trip failed: [$($result.Output.Trim())]"
    }
} finally {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host 'Windows PowerShell 5.1 hidden-process runtime smoke passed.'
