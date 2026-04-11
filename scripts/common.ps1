# Shared helpers for workspace scripts.

function Get-WorkspacePythonSpec {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        return @{
            Command = $pythonCommand.Source
            PrefixArgs = @()
        }
    }

    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        return @{
            Command = $pyLauncher.Source
            PrefixArgs = @('-3')
        }
    }

    throw 'Python executable not found. Activate a Python environment or install Python before running workspace scripts.'
}

function Invoke-WorkspacePython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $pythonSpec = Get-WorkspacePythonSpec
    $allArgs = @($pythonSpec.PrefixArgs + $Arguments)
    & $pythonSpec.Command @allArgs
}