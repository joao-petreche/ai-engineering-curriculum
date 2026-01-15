# 📦 Backup & Version Control Guide - Scientific AI Engineering Curriculum

**Last Updated:** January 14, 2026  
**Project Size:** 122 files, 22 directories, ~3.9 MB  
**Status:** ✅ Ready for production backup and version control

---

## 🎯 Quick Start: Save Your Work Now

### **Option 1: Git + GitHub (RECOMMENDED)**
Best for version control, collaboration, and disaster recovery.

```powershell
cd "C:\Users\joaop\Downloads\AI Engineering"

# Initialize git repository
git init

# Create .gitignore to exclude unnecessary files
# (See section below for template)

# Stage all files
git add .

# First commit
git commit -m "Initial commit: Complete 12-month Scientific AI Engineering curriculum (100% scaffolded)"

# Create a new repository on GitHub (github.com/new)
# Then push to GitHub:
git remote add origin https://github.com/joao-petreche/ai-engineering-curriculum.git
git branch -M main
git push -u origin main
```

**Benefits:**
- ✅ Complete version history and rollback capability
- ✅ Easy to continue work from any machine
- ✅ Automatic GitHub backup (redundancy)
- ✅ CI/CD integration ready
- ✅ Collaboration-friendly
- ✅ Free for public/private repos

---

### **Option 2: Cloud Storage Backup (COMPLEMENTARY)**
Use alongside Git for additional redundancy.

#### **Google Drive**
```powershell
# Compress entire project
Compress-Archive -Path "C:\Users\joaop\Downloads\AI Engineering" `
  -DestinationPath "C:\Users\joaop\Downloads\AI-Engineering-Backup-2026-01-14.zip"

# Upload to Google Drive
# 1. Go to drive.google.com
# 2. Upload the .zip file
# 3. Share with your account for backup
```

**File**: `AI-Engineering-Backup-2026-01-14.zip` (~4 MB, compresses well)

#### **OneDrive/Dropbox**
Similar process - just drag and drop the folder into your cloud storage.

**Benefits:**
- ✅ Simple point-and-click backup
- ✅ Additional redundancy beyond GitHub
- ✅ Easy file sharing if needed
- ✅ Automatic syncing option

---

### **Option 3: Local External Drive (ADDITIONAL SAFETY)**
For critical work, maintain a local backup on external storage.

```powershell
# Copy entire project to external drive
Copy-Item -Path "C:\Users\joaop\Downloads\AI Engineering" `
  -Destination "E:\Backups\AI-Engineering-2026-01-14" -Recurse -Force

# Or use robocopy for more control
robocopy "C:\Users\joaop\Downloads\AI Engineering" `
  "E:\Backups\AI-Engineering-2026-01-14" /E /V /R:3 /W:10
```

**Benefits:**
- ✅ Offline backup (protection against ransomware)
- ✅ Fast recovery if cloud services are down
- ✅ Keep on external drive for 3+ backups rotation

---

## 📋 .gitignore Template

Create this file at project root: `C:\Users\joaop\Downloads\AI Engineering\.gitignore`

```plaintext
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

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
*.ipynb

# Environment
.env
.env.local
secrets.json

# OS
Thumbs.db
.DS_Store

# EnergyPlus outputs (large simulation files)
*.eso
*.sql
*.mtr
*.err
*.rdd
*.csv~

# Large files
*.zip
*.tar.gz
*.iso
*.img

# API keys and credentials
*credentials*
*secret*
*token*
*.key
```

---

## 🔄 Backup Schedule & Automation

### **Daily Backup (Automated)**

**Windows Task Scheduler:**

```powershell
# Create scheduled backup task
$trigger = New-ScheduledTaskTrigger -Daily -At 11:00PM
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument @'
$source = "C:\Users\joaop\Downloads\AI Engineering"
$dest = "E:\Backups\$(Get-Date -Format 'yyyy-MM-dd')"
if (!(Test-Path $dest)) {
  Copy-Item $source $dest -Recurse -Force
}
'@
Register-ScheduledTask -TaskName "AI-Curriculum-Backup" `
  -Trigger $trigger -Action $action -RunLevel Highest
```

### **Weekly Git Commit**

Schedule a reminder to commit weekly:
- Monday: Review changes
- Tuesday: Commit and push to GitHub

```powershell
# Bash script (save as backup.sh)
#!/bin/bash
cd "/c/Users/joaop/Downloads/AI Engineering"
git add .
git commit -m "Weekly curriculum update - $(date +%Y-%m-%d)"
git push origin main
```

---

## 📊 Current Project Structure

```
AI Engineering/
├── Plano Mestre Integrado_...md          (Master plan - 480 lines)
├── Science AI Engineering/
│   ├── CURRICULUM_INDEX.md               (Main navigation)
│   ├── curriculum_alignment_matrix.md
│   ├── Exercicios_Fase_0-9.md           (Months 0-9 exercises)
│   ├── mes8_optimization/                (Complete Month 8 code)
│   ├── mes9_production/                  (Complete Month 9 code)
│   ├── mes10_federated_learning/         (Complete Month 10 code)
│   ├── mes11_advanced_analytics/         (Complete Month 11 code)
│   ├── mes12_capstone/                   (Complete Month 12 code)
│   ├── MES_10/11_DELIVERY_SUMMARY.md
│   ├── MES_11_VISUAL_OVERVIEW.md
│   ├── scripts/                          (Utility scripts)
│   ├── tests/                            (Test suites)
│   └── _archive/                         (18 historical files)
└── README_BACKUPS.md                     (This file)

Total: 122 files, ~3.9 MB
```

---

## 🛡️ Recommended Backup Strategy: 2-1 Rule

**Best Practice for Critical Projects:**

| **Copies** | **Location** | **Type** | **Update Frequency** |
|-----------|------------|---------|---------------------|
| **Copy 1** | Local Computer | Live working directory | Continuous (auto-save) |
| **Copy 2** | GitHub | Version control remote | Weekly (manual push) |
| **Copy 3** | External Drive | Offline backup | Monthly (copy to drive) |

**Why this works:**
- ✅ Copy 1: Working version always available
- ✅ Copy 2: Version history + disaster recovery
- ✅ Copy 3: Protection against local hardware failure

---

## 🚀 Implementation Checklist

- [ ] **Week 1:** Initialize Git repo and push to GitHub
- [ ] **Week 2:** Copy to external drive
- [ ] **Ongoing:** Weekly `git push` to GitHub
- [ ] **Monthly:** Update external drive backup
- [ ] **Quarterly:** Review .gitignore and update if needed
- [ ] **Quarterly:** Test restore from backup (verify integrity)

---

## 🔍 Verify Your Backup

```powershell
# Check Git status
git status

# View git log
git log --oneline -5

# Verify all files are tracked
git ls-files

# Count files
(git ls-files | Measure-Object).Count

# Check backup file integrity
(Get-ChildItem "AI-Engineering-Backup-*.zip").Length
```

---

## 📝 Continuation Protocol

When resuming work after a break:

```powershell
# 1. Pull latest from GitHub
cd "C:\Users\joaop\Downloads\AI Engineering"
git pull origin main

# 2. Check status
git status

# 3. Create feature branch for new work
git checkout -b feature/your-feature-name

# 4. Make changes, commit regularly
git add .
git commit -m "Your meaningful commit message"

# 5. Push when ready
git push origin feature/your-feature-name

# 6. Create pull request on GitHub (optional for main projects)
# or merge directly if solo:
# git checkout main
# git merge feature/your-feature-name
# git push origin main
```

---

## 🔐 Security Notes

**Keep Secret:**
- Google API keys
- GitHub personal access tokens
- EnergyPlus API credentials
- Vertex AI credentials

**Safe Storage:**
- Use `.env` file (excluded by .gitignore)
- Use GitHub Secrets for CI/CD
- Use Google Secret Manager for cloud projects

**Example `.env` (never commit):**
```
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_REGION=us-central1
ENERGYPLUS_PATH=C:\EnergyPlusV24-1-0
```

---

## 📞 Troubleshooting

**Git won't push?**
```powershell
# Check remote URL
git remote -v

# Update if needed
git remote set-url origin https://github.com/joao-petreche/new-repo.git
```

**Forgot to commit before making changes?**
```powershell
# See what changed
git diff

# Stage and commit
git add .
git commit -m "Describe what changed"
```

**Need to restore from backup?**
```powershell
# From GitHub
git clone https://github.com/joao-petreche/ai-engineering-curriculum.git

# From zip backup
Expand-Archive "AI-Engineering-Backup-2026-01-14.zip" -DestinationPath "C:\Restore"
```

---

## 📈 Project Statistics

- **Total Files:** 122
- **Total Directories:** 22
- **Total Size:** ~3.9 MB
- **Months Scaffolded:** 12/12 (100%)
- **Total Lines of Code:** 53,000+
- **Total Exercises:** 132+

**Next Steps:**
1. ✅ Initialize Git (this week)
2. ✅ First backup to cloud (this week)
3. ✅ Setup automated backup (next week)
4. 🔄 Regular maintenance (ongoing)

---

**Last Updated:** January 14, 2026  
**Prepared by:** AI Engineering Curriculum Team  
**Status:** ✅ Production Ready for Backup & Version Control
