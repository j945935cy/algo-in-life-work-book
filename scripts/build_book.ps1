# Build Jupyter Book

$ErrorActionPreference = 'Stop'

Write-Host 'Starting Jupyter Book build...' -ForegroundColor Green
Push-Location .\book
try {
	jupyter-book build --site --html
}
finally {
	Pop-Location
}
Write-Host 'Jupyter Book build completed.' -ForegroundColor Green
