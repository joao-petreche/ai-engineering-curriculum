param(
    [string]$VenvDir = ".venv",
    [string]$RequirementsFile = "requirements.txt",
    [string]$ExpectedMajorMinor = "3.10"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Get-PythonCommand {
    # Prefer py launcher on Windows, then fallback to python in PATH.
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return "py"
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }
    throw "Python nao encontrado. Instale Python 3.10.x e tente novamente."
}

function Get-PythonVersion {
    param([string]$PythonCmd)

    if ($PythonCmd -eq "py") {
        $version = & py -$ExpectedMajorMinor -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>$null
        if (-not $version) {
            throw "Python $ExpectedMajorMinor.x nao encontrado no py launcher."
        }
        return $version.Trim()
    }

    $version = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>$null
    if (-not $version) {
        throw "Falha ao obter versao do python."
    }
    return $version.Trim()
}

function Assert-PythonVersion {
    param([string]$Version)

    if (-not $Version.StartsWith("$ExpectedMajorMinor.")) {
        throw "Versao incompativel detectada: $Version. Esperado: $ExpectedMajorMinor.x"
    }
}

function New-OrUpdateVenv {
    param([string]$PythonCmd)

    if (-not (Test-Path $VenvDir)) {
        Write-Step "Criando ambiente virtual em '$VenvDir'"
        if ($PythonCmd -eq "py") {
            & py -$ExpectedMajorMinor -m venv $VenvDir
        }
        else {
            & python -m venv $VenvDir
        }
    }
    else {
        Write-Step "Ambiente virtual ja existe em '$VenvDir'"
    }
}

function Install-Dependencies {
    if (-not (Test-Path $RequirementsFile)) {
        throw "Arquivo '$RequirementsFile' nao encontrado na raiz do repositorio."
    }

    $venvPython = Join-Path $VenvDir "Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        throw "Python do ambiente virtual nao encontrado em '$venvPython'."
    }

    Write-Step "Atualizando pip"
    & $venvPython -m pip install --upgrade pip

    Write-Step "Instalando dependencias de '$RequirementsFile'"
    & $venvPython -m pip install -r $RequirementsFile
}

function Load-ConfigHints {
    $extensionsPath = "extensions.json"
    if (Test-Path $extensionsPath) {
        Write-Step "Arquivo de configuracao encontrado: $extensionsPath"
    }
    else {
        Write-Host "Aviso: extensions.json nao encontrado. Prosseguindo sem essa etapa." -ForegroundColor Yellow
    }
}

function Activate-Venv {
    $activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        throw "Script de ativacao nao encontrado em '$activateScript'."
    }

    Write-Step "Ativando ambiente virtual nesta sessao"
    . $activateScript
}

try {
    Write-Step "Detectando comando do Python"
    $pythonCmd = Get-PythonCommand

    Write-Step "Validando versao do Python ($ExpectedMajorMinor.x)"
    $pythonVersion = Get-PythonVersion -PythonCmd $pythonCmd
    Assert-PythonVersion -Version $pythonVersion
    Write-Host "Python valido detectado: $pythonVersion" -ForegroundColor Green

    New-OrUpdateVenv -PythonCmd $pythonCmd
    Install-Dependencies
    Load-ConfigHints
    Activate-Venv

    Write-Host "`nAmbiente configurado com sucesso." -ForegroundColor Green
    Write-Host "Comando sugerido para validar: python --version" -ForegroundColor Green
}
catch {
    Write-Host "`nFalha no setup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
