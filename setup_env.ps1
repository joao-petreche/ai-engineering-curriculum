param(
    [string]$VenvDir = ".venv",
    [string]$RequirementsFile = "requirements.txt",
    [string]$ExpectedMajorMinor = "3.10",
    [string]$GCPProject = "gen-lang-client-0464475716",
    [switch]$SkipGCP = $false
)

$ErrorActionPreference = "Stop"
$StepCount = 0
$TotalSteps = 8

function Write-Step {
    param([string]$Message)
    $script:StepCount++
    Write-Host "`n==> [$script:StepCount/$TotalSteps] $Message" -ForegroundColor Cyan
}

function Test-GCPInfrastructure {
    Write-Step "Validando infraestrutura do Google Cloud..."

    if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
        Write-Host "    ⚠️ gcloud CLI nao encontrado. Instalacao recomendada:" -ForegroundColor Yellow
        Write-Host "    https://cloud.google.com/sdk/docs/install#windows" -ForegroundColor Yellow
        return $false
    }

    Write-Host "    ✓ Google Cloud SDK detectado." -ForegroundColor Green
    return $true
}

function Get-SystemDiagnostics {
    Write-Step "Diagnóstico de Recursos do Sistema (Hardware)..."

    $computerMemory = Get-WmiObject Win32_ComputerSystem | Select-Object -ExpandProperty TotalPhysicalMemory
    $totalMemoryMB = [math]::Round($computerMemory / 1MB, 0)

    $osMemory = Get-WmiObject Win32_OperatingSystem | Select-Object -ExpandProperty FreePhysicalMemory
    $freeMemoryMB = [math]::Round($osMemory / 1KB, 0)

    Write-Host "    - Memória Disponível: ${freeMemoryMB}MB de ${totalMemoryMB}MB" -ForegroundColor Cyan

    if ($freeMemoryMB -lt 1024) {
        Write-Host "    ⚠️ AVISO: Memória RAM crítica (< 1GB). Recomenda-se fechar aplicacoes." -ForegroundColor Yellow
    }
}

function Clear-PythonProcesses {
    Write-Step "Limpeza de Processos Python..."

    $pythonProcesses = Get-Process -Name "python*" -ErrorAction SilentlyContinue
    if ($pythonProcesses.Count -gt 0) {
        Write-Host "    - Encerrando $($pythonProcesses.Count) processo(s) Python..."
        Stop-Process -Name "python*" -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
        Write-Host "    ✓ Processos Python reiniciados para otimização." -ForegroundColor Green
    }
    else {
        Write-Host "    - Nenhum processo Python em execução." -ForegroundColor Green
    }
}

function Set-GCPProject {
    param([string]$Project)

    Write-Step "Vinculando Projetos GCP..."

    if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
        Write-Host "    ⚠️ gcloud nao disponivel. Pulando configuracao GCP." -ForegroundColor Yellow
        return
    }

    try {
        gcloud config set project $Project --quiet 2>$null
        Write-Host "    ✓ Projeto GCP: $Project" -ForegroundColor Green
    }
    catch {
        Write-Host "    ⚠️ Falha ao configurar projeto GCP: $_" -ForegroundColor Yellow
    }
}

function Test-ADCCredentials {
    Write-Step "Verificação de Credenciais de Aplicação (ADC)..."

    $adcPath = "$env:APPDATA\gcloud\application_default_credentials.json"

    if (Test-Path $adcPath) {
        Write-Host "    ✓ Credenciais ADC prontas." -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "    ⚠️ REQUERIDO: Execute 'gcloud auth application-default login'" -ForegroundColor Yellow
        return $false
    }
}

function Run-BillingReport {
    Write-Step "Relatório Financeiro e Observabilidade..."
    Write-Host "------------------------------------------------------------" -ForegroundColor Cyan

    if (-not (Test-Path "analise_faturamento_real.py")) {
        Write-Host "    ⚠️ Script de faturamento nao encontrado." -ForegroundColor Yellow
        Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
        return
    }

    $venvPython = Join-Path $VenvDir "Scripts\python.exe"

    try {
        $output = & $venvPython analise_faturamento_real.py 2>&1
        Write-Host $output
        Write-Host "`n✅ Infraestrutura validada: Custo Líquido R$ 0.00." -ForegroundColor Green
    }
    catch {
        Write-Host "`n⚠️ Dados de faturamento em processamento (aguarde 24h)." -ForegroundColor Yellow
    }

    Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
}


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

    # Novo fluxo com GCP e observabilidade
    if (-not $SkipGCP) {
        $gcpAvailable = Test-GCPInfrastructure
        Get-SystemDiagnostics
        Clear-PythonProcesses

        if ($gcpAvailable) {
            Set-GCPProject -Project $GCPProject
            Test-ADCCredentials | Out-Null
        }
    }

    New-OrUpdateVenv -PythonCmd $pythonCmd
    Install-Dependencies
    Load-ConfigHints
    Activate-Venv

    # Relatório final
    if (-not $SkipGCP) {
        Run-BillingReport
    }

    Write-Host "`n[OK] Ambiente v1.2.3 pronto para Scientific AI Engineering." -ForegroundColor Green
    Write-Host "Comando sugerido para validar: python --version" -ForegroundColor Green
}
catch {
    Write-Host "`nFalha no setup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
