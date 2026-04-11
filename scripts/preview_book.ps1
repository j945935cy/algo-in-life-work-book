# Preview built book locally over HTTP.

param(
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'common.ps1')

$buildPath = Join-Path $PSScriptRoot '..\book\_build\html'
$resolvedPath = (Resolve-Path $buildPath).Path

if (-not (Test-Path (Join-Path $resolvedPath 'index.html'))) {
    throw 'Built HTML site not found. Run .\scripts\build_book.ps1 first.'
}

Write-Host "Serving built book at http://127.0.0.1:$Port/" -ForegroundColor Green
Write-Host 'Press Ctrl+C to stop the preview server.' -ForegroundColor Green

Invoke-WorkspacePython -Arguments @('-m', 'http.server', $Port.ToString(), '--directory', $resolvedPath)