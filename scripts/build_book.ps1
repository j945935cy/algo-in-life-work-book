# Build Jupyter Book

$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'common.ps1')

Write-Host 'Starting Jupyter Book build...' -ForegroundColor Green
Push-Location .\book
try {
	Invoke-WorkspacePython -Arguments @('-m', 'jupyter_book', 'build', '--html')
}
finally {
	Pop-Location
}
Write-Host 'Jupyter Book build completed.' -ForegroundColor Green
