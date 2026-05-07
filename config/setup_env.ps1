param(
    [string]$VenvDir = ".venv",
    [string]$RequirementsFile = "requirements.txt",
    [string]$ExpectedMajorMinor = "3.10",
    [string]$GCPProject = "gen-lang-client-0464475716",
    [switch]$SkipGCP = $false
)

$ErrorActionPreference = "Stop"
$script:StepCount = 0
$TotalSteps = 8

function Write-Step {
    param([string]$Message)
    $script:StepCount++
    Write-Host ""
    Write-Host "==> [$script:StepCount/$TotalSteps] $Message" -ForegroundColor Cyan
}

function Test-GCPInfrastructure {
    Write-Step "Validando infraestrutura do Google Cloud..."
    if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
        Write-Host "    [!] gcloud CLI nao encontrado." -ForegroundColor Yellow
        return $false
    }
    Write-Host "    [OK] Google Cloud SDK detectado." -ForegroundColor Green
    return $true
}

function Get-SystemDiagnostics {
    Write-Step "Diagnostico de Hardware..."
    # CimInstance funciona no PowerShell 5.1 e 7+
    $memInfo = Get-CimInstance -ClassName Win32_OperatingSystem
    $compInfo = Get-CimInstance -ClassName Win32_ComputerSystem
    $totalMB = [math]::Round($compInfo.TotalPhysicalMemory / 1MB, 0)
    $freeMB = [math]::Round($memInfo.FreePhysicalMemory / 1024, 0)
    Write-Host "    - Memoria: $freeMB MB livre de $totalMB MB" -ForegroundColor Cyan
}

function Clear-PythonProcesses {
    Write-Step "Limpeza de Processos..."
    $procs = Get-Process -Name "python*" -ErrorAction SilentlyContinue
    if ($procs) {
        Stop-Process -Name "python*" -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }
    Write-Host "    [OK] Workspace limpo." -ForegroundColor Green
}

function Set-GCPProject {
    param([string]$Project)
    Write-Step "Configurando GCP..."
    if (Get-Command gcloud -ErrorAction SilentlyContinue) {
        # Temporariamente ignoramos avisos de stderr para evitar falha no setup
        $oldEAP = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        gcloud config set project $Project --quiet 2>$null
        $ErrorActionPreference = $oldEAP
        Write-Host "    [OK] Projeto ativo: $Project" -ForegroundColor Green
    }
}

function Test-ADCCredentials {
    Write-Step "Verificando Credenciais ADC..."
    $adcPath = "$env:APPDATA\gcloud\application_default_credentials.json"
    if (Test-Path $adcPath) {
        Write-Host "    [OK] Credenciais prontas." -ForegroundColor Green
        return $true
    }
    Write-Host "    [!] Requerido: gcloud auth application-default login" -ForegroundColor Yellow
    return $false
}

function Run-BillingReport {
    Write-Step "Relatorio Financeiro..."
    if (Test-Path "analise_faturamento_real.py") {
        $pyPath = Join-Path $VenvDir "Scripts\python.exe"
        try {
            & $pyPath analise_faturamento_real.py 2>&1
        } catch {
            Write-Host "    [!] Erro ao rodar relatorio." -ForegroundColor Yellow
        }
    }
}

function Get-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) { return "py" }
    if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
    throw "Python nao encontrado."
}

function Get-PythonVersion {
    param([string]$Cmd)
    if ($Cmd -eq "py") {
        $vInfo = & $Cmd "-$ExpectedMajorMinor" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
    } else {
        $vInfo = & $Cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
    }
    return $vInfo.Trim()
}

function New-OrUpdateVenv {
    param([string]$Cmd)
    if (-not (Test-Path $VenvDir)) {
        Write-Step "Criando Ambiente Virtual..."
        if ($Cmd -eq "py") { & $Cmd "-$ExpectedMajorMinor" -m venv $VenvDir }
        else { & $Cmd -m venv $VenvDir }
    }
    Write-Host "    [OK] Ambiente virtual em $VenvDir" -ForegroundColor Green
}

function Install-Dependencies {
    $pyExec = Join-Path $VenvDir "Scripts\python.exe"
    Write-Step "Instalando Dependencias..."
    & $pyExec -m pip install --upgrade pip
    & $pyExec -m pip install -r $RequirementsFile
}

try {
    Write-Step "Iniciando Setup v1.2.4"
    $currentCmd = Get-PythonCommand
    $currentVer = Get-PythonVersion -Cmd $currentCmd

    if ($currentVer -ne $ExpectedMajorMinor) { throw "Versao incorreta." }

    if (-not $SkipGCP) {
        $gOk = Test-GCPInfrastructure
        Get-SystemDiagnostics
        Clear-PythonProcesses
        if ($gOk) {
            Set-GCPProject -Project $GCPProject
            $null = Test-ADCCredentials
        }
    }

    New-OrUpdateVenv -Cmd $currentCmd
    Install-Dependencies

    $actPath = Join-Path $VenvDir "Scripts\Activate.ps1"
    if (Test-Path $actPath) { . $actPath }

    if (-not $SkipGCP) { Run-BillingReport }

    Write-Host "`n[OK] Ambiente v1.2.4 pronto para Scientific AI Engineering." -ForegroundColor Green
} catch {
    Write-Host "`nFalha no setup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
