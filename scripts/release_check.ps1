# Run automated release checks for the repository.

$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'common.ps1')

$workspaceRoot = Split-Path $PSScriptRoot -Parent
$bookRoot = Join-Path $workspaceRoot 'book'
$chaptersRoot = Join-Path $bookRoot 'chapters'
$examplesRoot = Join-Path $workspaceRoot 'examples'
$testsRoot = Join-Path $workspaceRoot 'tests'
$requiredFiles = @(
    'README.md',
    'CITATION.cff',
    'LICENSE',
    'publication/RELEASE_CHECKLIST.md',
    'book/index.md',
    'book/preface.md',
    'book/myst.yml'
)
$manualFollowUps = @(
    'Confirm GitHub Actions CI and Pages workflows completed successfully.',
    'Confirm the GitHub Pages URL, repo description, release notes, and version tags are updated.',
    'Confirm CITATION and LICENSE use final publication metadata.'
)

function Assert-PathExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath
    )

    $fullPath = Join-Path $workspaceRoot $RelativePath
    if (-not (Test-Path $fullPath)) {
        throw "Missing required path: $RelativePath"
    }
}

function Assert-NoPlaceholder {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath,
        [Parameter(Mandatory = $true)]
        [string[]]$Patterns
    )

    $fullPath = Join-Path $workspaceRoot $RelativePath
    $content = Get-Content $fullPath -Raw
    foreach ($pattern in $Patterns) {
        if ($content -match $pattern) {
            throw "Placeholder content found in $RelativePath matching pattern: $pattern"
        }
    }
}

Write-Host 'Checking required release files...' -ForegroundColor Cyan
foreach ($requiredFile in $requiredFiles) {
    Assert-PathExists -RelativePath $requiredFile
}

Write-Host 'Checking chapter linkage...' -ForegroundColor Cyan
$mystContent = Get-Content (Join-Path $bookRoot 'myst.yml') -Raw
$chapterDirectories = Get-ChildItem $chaptersRoot -Directory | Sort-Object Name

foreach ($chapterDirectory in $chapterDirectories) {
    if ($chapterDirectory.Name -notmatch '^(ch\d+)') {
        continue
    }

    $chapterKey = $Matches[1]
    $chapterSlug = $chapterDirectory.Name
    $chapterRelativeRoot = "book/chapters/$chapterSlug"
    $chapterIndex = Join-Path $chapterRelativeRoot 'index.md'
    $chapterExercises = Join-Path $chapterRelativeRoot 'exercises.md'
    $exampleDirectory = Join-Path $examplesRoot $chapterKey
    $testMatches = Get-ChildItem $testsRoot -Filter "test_${chapterKey}*.py"

    Assert-PathExists -RelativePath $chapterIndex
    Assert-PathExists -RelativePath $chapterExercises

    if (-not (Test-Path $exampleDirectory)) {
        throw "Missing example directory for $chapterKey at examples/$chapterKey"
    }

    if ($testMatches.Count -eq 0) {
        throw "Missing test file for $chapterKey under tests/"
    }

    if ($mystContent -notmatch [regex]::Escape($chapterSlug + '/index.md')) {
        throw "book/myst.yml does not reference $chapterSlug/index.md"
    }
}

Write-Host 'Checking metadata placeholders...' -ForegroundColor Cyan
Assert-NoPlaceholder -RelativePath 'CITATION.cff' -Patterns @('YourLastName', 'YourFirstName')

Write-Host 'Running test suite...' -ForegroundColor Cyan
Push-Location $workspaceRoot
try {
    Invoke-WorkspacePython -Arguments @('-m', 'pytest', '-q')

    Write-Host 'Building book...' -ForegroundColor Cyan
    & (Join-Path $PSScriptRoot 'build_book.ps1')
}
finally {
    Pop-Location
}

$builtIndex = Join-Path $workspaceRoot 'book/_build/html/index.html'
if (-not (Test-Path $builtIndex)) {
    throw 'Book build did not produce book/_build/html/index.html'
}

Write-Host ''
Write-Host 'Automated release checks passed.' -ForegroundColor Green
Write-Host 'Manual follow-up before publishing:' -ForegroundColor Yellow
foreach ($item in $manualFollowUps) {
    Write-Host "- $item" -ForegroundColor Yellow
}