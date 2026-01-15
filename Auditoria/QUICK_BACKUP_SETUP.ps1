# Scientific AI Engineering Curriculum - Quick Backup Setup Script
# Run this script to set up version control and backup for your project
# Usage: ./QUICK_BACKUP_SETUP.ps1

param(
    [string]$GitHubUsername = "",
    [string]$GitHubRepoName = "ai-engineering-curriculum",
    [string]$BackupDrive = "E:",
    [switch]$SkipGit = $false,
    [switch]$SkipBackup = $false,
    [switch]$SkipGitignore = $false
)

$ProjectPath = "C:\Users\joaop\Downloads\AI Engineering"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Engineering Curriculum - Backup Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create .gitignore
if (-not $SkipGitignore) {
    Write-Host "[1/4] Creating .gitignore file..." -ForegroundColor Green
    
    $gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual Environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Jupyter
.ipynb_checkpoints/

# Environment
.env
.env.local
secrets.json

# OS
Thumbs.db
.DS_Store

# EnergyPlus outputs
*.eso
*.sql
*.mtr
*.err
*.rdd
*.csv~

# Large files
*.zip
*.tar.gz

# API keys
*credentials*
*secret*
*token*
*.key
"@
    
    $gitignorePath = Join-Path $ProjectPath ".gitignore"
    if (Test-Path $gitignorePath) {
        Write-Host "  ⚠️  .gitignore already exists, skipping" -ForegroundColor Yellow
    } else {
        Set-Content -Path $gitignorePath -Value $gitignoreContent
        Write-Host "  ✅ .gitignore created successfully" -ForegroundColor Green
    }
}

# Step 2: Initialize Git Repository
if (-not $SkipGit) {
    Write-Host "[2/4] Initializing Git repository..." -ForegroundColor Green
    
    Push-Location $ProjectPath
    
    if (Test-Path ".git") {
        Write-Host "  ⚠️  Git repository already exists, skipping" -ForegroundColor Yellow
    } else {
        git init
        Write-Host "  ✅ Git repository initialized" -ForegroundColor Green
    }
    
    # Add files
    Write-Host "[2b/4] Staging all files (this may take a moment)..." -ForegroundColor Green
    git add .
    Write-Host "  ✅ Files staged" -ForegroundColor Green
    
    # First commit
    Write-Host "[2c/4] Creating initial commit..." -ForegroundColor Green
    git commit -m "Initial commit: Complete 12-month Scientific AI Engineering curriculum (100% scaffolded) - $Timestamp"
    Write-Host "  ✅ Initial commit created" -ForegroundColor Green
    
    Pop-Location
}

# Step 3: Create Backup ZIP
if (-not $SkipBackup) {
    Write-Host "[3/4] Creating backup ZIP file..." -ForegroundColor Green
    
    $BackupPath = "C:\Users\joaop\Downloads\AI-Engineering-Backup-$Timestamp.zip"
    
    try {
        Compress-Archive -Path $ProjectPath -DestinationPath $BackupPath -Force -ErrorAction Stop
        $BackupSize = (Get-Item $BackupPath).Length / 1MB
        Write-Host "  ✅ Backup created: $BackupPath (~$([Math]::Round($BackupSize, 2)) MB)" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Failed to create backup: $_" -ForegroundColor Red
    }
}

# Step 4: Setup Scheduled Task
Write-Host "[4/4] Setting up scheduled backup task..." -ForegroundColor Green

$TaskName = "AI-Curriculum-Daily-Backup"
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "  ⚠️  Scheduled task already exists, skipping" -ForegroundColor Yellow
} else {
    try {
        $trigger = New-ScheduledTaskTrigger -Daily -At 11:00PM
        $action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument @"
`$source = "$ProjectPath"
`$dest = "C:\Users\joaop\Downloads\AI-Engineering-Backup-`$(Get-Date -Format 'yyyy-MM-dd').zip"
if (!(Test-Path `$dest)) {
  Compress-Archive -Path `$source -DestinationPath `$dest -Force
  Write-Host "Backup created: `$dest" | Out-File -Append "C:\Users\joaop\Downloads\backup.log"
}
"@
        
        Register-ScheduledTask -TaskName $TaskName -Trigger $trigger -Action $action -Force -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  ✅ Scheduled task created: runs daily at 11:00 PM" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Could not create scheduled task (may need admin): $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""

if ($GitHubUsername -eq "") {
    Write-Host "1. Push to GitHub (if not done yet):" -ForegroundColor Cyan
    Write-Host "   git remote add origin https://github.com/joao-petreche/ai-engineering-curriculum.git" -ForegroundColor Gray
    Write-Host "   git branch -M main" -ForegroundColor Gray
    Write-Host "   git push -u origin main" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "1. GitHub Repo: https://github.com/$GitHubUsername/$GitHubRepoName" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "2. Upload backup ZIP to Google Drive or OneDrive" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Copy backup ZIP to external drive (E:\ or your backup location)" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Review BACKUP_AND_VERSION_CONTROL_GUIDE.md for detailed information" -ForegroundColor Cyan
Write-Host ""
Write-Host "[BACKUP STRATEGY: 3-2-1 Rule]" -ForegroundColor Yellow
Write-Host "   - Copy 1: This computer (working directory)" -ForegroundColor Gray
Write-Host "   - Copy 2: GitHub (version control)" -ForegroundColor Gray
Write-Host "   - Copy 3A: Google Drive / OneDrive" -ForegroundColor Gray
Write-Host "   - Copy 3B: External hard drive" -ForegroundColor Gray
Write-Host ""
Write-Host "[STATUS] Ready for development and backup!" -ForegroundColor Green
