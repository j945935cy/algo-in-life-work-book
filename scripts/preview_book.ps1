# Preview built book locally over HTTP.

$ErrorActionPreference = 'Stop'

$buildPath = Join-Path $PSScriptRoot '..\book\_build\html'
$resolvedPath = (Resolve-Path $buildPath).Path

if (-not (Test-Path (Join-Path $resolvedPath 'index.html'))) {
    throw 'Built HTML site not found. Run .\scripts\build_book.ps1 first.'
}

Write-Host 'Serving built book at http://127.0.0.1:8000/' -ForegroundColor Green
Write-Host 'Press Ctrl+C to stop the preview server.' -ForegroundColor Green

& C:/Users/jack/AppData/Local/Programs/Python/Python313/python.exe -m http.server 8000 --directory $resolvedPath