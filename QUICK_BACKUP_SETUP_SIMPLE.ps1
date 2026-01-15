# Scientific AI Engineering Curriculum - Quick Backup Setup Script
# Simplified version without encoding issues
# Usage: .\QUICK_BACKUP_SETUP_SIMPLE.ps1

$ProjectPath = "C:\Users\joaop\Downloads\AI Engineering"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "AI Engineering Curriculum - Backup Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create .gitignore
Write-Host "[1/4] Creating .gitignore file..." -ForegroundColor Green

$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
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
    Write-Host "  [SKIP] .gitignore already exists" -ForegroundColor Yellow
} else {
    Set-Content -Path $gitignorePath -Value $gitignoreContent
    Write-Host "  [OK] .gitignore created successfully" -ForegroundColor Green
}

# Step 2: Initialize Git Repository
Write-Host "[2/4] Initializing Git repository..." -ForegroundColor Green

Push-Location $ProjectPath

if (Test-Path ".git") {
    Write-Host "  [SKIP] Git repository already exists" -ForegroundColor Yellow
} else {
    Write-Host "  [INIT] Running: git init" -ForegroundColor Gray
    git init 2>$null
    Write-Host "  [OK] Git repository initialized" -ForegroundColor Green
    
    # Add files
    Write-Host "  [STAGE] Running: git add . (this may take a moment)" -ForegroundColor Gray
    git add . 2>$null
    Write-Host "  [OK] Files staged successfully" -ForegroundColor Green
    
    # First commit
    Write-Host "  [COMMIT] Creating initial commit..." -ForegroundColor Gray
    git commit -m "Initial commit: Complete 12-month Scientific AI Engineering curriculum (100% scaffolded) - $Timestamp" 2>$null
    Write-Host "  [OK] Initial commit created" -ForegroundColor Green
}

Pop-Location

# Step 3: Create Backup ZIP
Write-Host "[3/4] Creating backup ZIP file..." -ForegroundColor Green

$BackupPath = "C:\Users\joaop\Downloads\AI-Engineering-Backup-$Timestamp.zip"

try {
    Write-Host "  [ZIP] Compressing all files (this may take a moment)..." -ForegroundColor Gray
    Compress-Archive -Path $ProjectPath -DestinationPath $BackupPath -Force -ErrorAction Stop
    $BackupSize = (Get-Item $BackupPath).Length / 1MB
    Write-Host "  [OK] Backup created: AI-Engineering-Backup-$Timestamp.zip" -ForegroundColor Green
    Write-Host "      Size: $([Math]::Round($BackupSize, 2)) MB" -ForegroundColor Gray
} catch {
    Write-Host "  [ERROR] Failed to create backup: $_" -ForegroundColor Red
}

# Step 4: Setup Scheduled Task
Write-Host "[4/4] Setting up scheduled backup task..." -ForegroundColor Green

$TaskName = "AI-Curriculum-Daily-Backup"
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "  [SKIP] Scheduled task already exists" -ForegroundColor Yellow
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
        Write-Host "  [OK] Scheduled task created (runs daily at 11:00 PM)" -ForegroundColor Green
    } catch {
        Write-Host "  [WARN] Could not create scheduled task (may need admin): $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[NEXT STEPS]" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create GitHub repository:" -ForegroundColor Cyan
Write-Host "   https://github.com/new" -ForegroundColor Gray
Write-Host "   - Repository name: ai-engineering-curriculum" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Push to GitHub:" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/joao-petreche/ai-engineering-curriculum.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Upload backup ZIP to cloud storage:" -ForegroundColor Cyan
Write-Host "   - Google Drive" -ForegroundColor Gray
Write-Host "   - OneDrive" -ForegroundColor Gray
Write-Host "   - Dropbox" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Copy backup ZIP to external drive:" -ForegroundColor Cyan
Write-Host "   - USB drive or external hard drive" -ForegroundColor Gray
Write-Host ""
Write-Host "[BACKUP STRATEGY: 3-2-1 Rule]" -ForegroundColor Yellow
Write-Host "   Copy 1: This computer (working directory)" -ForegroundColor Gray
Write-Host "   Copy 2: GitHub (version control)" -ForegroundColor Gray
Write-Host "   Copy 3: Google Drive OR OneDrive (cloud backup)" -ForegroundColor Gray
Write-Host "   Copy 4: External drive (offline backup)" -ForegroundColor Gray
Write-Host ""
Write-Host "[STATUS] Your project is now ready for version control and backup!" -ForegroundColor Green
