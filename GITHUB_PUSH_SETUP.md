# GitHub Push Setup - Step-by-Step Guide

**Status**: ✅ Your Git repository is initialized and ready to push to GitHub!

---

## 🔑 Step 1: Create GitHub Account (if you don't have one)

1. Go to: https://github.com/signup
2. Enter your email
3. Create a password
4. Choose username (e.g., `your-username`)
5. Verify email

---

## 📦 Step 2: Create a New GitHub Repository

1. Go to: https://github.com/new
2. Fill in the form:
   - **Repository name:** `ai-engineering-curriculum`
   - **Description:** Complete 12-month Scientific AI Engineering Curriculum (100% scaffolded, 53,000+ lines, 132+ exercises)
   - **Visibility:** Public (recommended for portfolio) or Private
   - **Initialize repository:** DO NOT check any boxes
3. Click **Create repository**
4. You'll see a page with your repository URL

---

## 🔗 Step 3: Copy Your Repository URL

After creating the repository, you'll see instructions on GitHub. Look for:

```
https://github.com/YOUR_USERNAME/ai-engineering-curriculum.git
```

Copy this URL (replace YOUR_USERNAME with your actual GitHub username)

---

## 📤 Step 4: Push to GitHub (Run These Commands)

Replace `YOUR_USERNAME` with your actual GitHub username in the command below:

```powershell
cd "C:\Users\joaop\Downloads\AI Engineering"

git remote add origin https://github.com/YOUR_USERNAME/ai-engineering-curriculum.git
git branch -M main
git push -u origin main
```

---

## 🔐 Step 5: Authenticate with GitHub

When you run `git push`, you'll be prompted to authenticate. You have two options:

### **Option A: Personal Access Token (Recommended)**

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. In the **Note** field, type: `AI Engineering Curriculum Backup`
4. Set **Expiration** to: 90 days (or Longer)
5. Check boxes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `write:packages`
6. Click **Generate token**
7. **Copy the token immediately** (you won't see it again!)
8. When PowerShell prompts for password, paste the token

### **Option B: GitHub CLI Authentication**

1. Install GitHub CLI: `winget install --id GitHub.cli`
2. Run: `gh auth login`
3. Follow the prompts (select HTTPS, authorize browser)
4. Then run the `git push` command

---

## ✅ Verify Success

After pushing, you should see:

```
Enumerating objects: 125, done.
Counting objects: 100% (125/125), done.
Delta compression using up to X threads
Compressing objects: 100% (119/119), done.
Writing objects: 100% (125/125), 2.3 MiB | X.XX MiB/s, done.
Total 125 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/ai-engineering-curriculum.git
 * [new branch]      main -> main
Branch 'main' set to track remote branch 'main' from 'origin'.
```

---

## 🎉 You're Done!

Your repository is now on GitHub at:
```
https://github.com/YOUR_USERNAME/ai-engineering-curriculum
```

---

## 📝 Continuing Work with Git

After you push, you can continue development with these commands:

```powershell
# Before starting work
git pull origin main

# After making changes
git add .
git commit -m "Your meaningful message about what changed"
git push origin main
```

---

## 🚀 Quick Reference Commands

```powershell
# Check status
git status

# See commit history
git log --oneline -5

# See what changed
git diff

# Undo last commit (if needed)
git reset --soft HEAD~1

# View branches
git branch -a

# Create a backup branch
git branch backup-2026-01-14
git push origin backup-2026-01-14
```

---

## ❓ Troubleshooting

**"fatal: remote origin already exists"**
```powershell
git remote remove origin
# Then run the git remote add command again
```

**"Permission denied (publickey)"**
- Use a Personal Access Token instead of password
- Or install GitHub CLI: `gh auth login`

**"The branch 'main' is not fully merged"**
```powershell
git branch -D main
git branch -M master main
git push -u origin main
```

**"fatal: unable to access repository"**
- Check your internet connection
- Verify your GitHub username and URL are correct
- Check authentication (token or SSH key)

---

## 📊 What's Being Pushed

| **Component** | **Count** |
|-------------|---------|
| Files | 125 |
| Directories | ~22 |
| Lines of Code | 53,000+ |
| Months Scaffolded | 12/12 (100%) |
| Size | ~2.3 MB |

---

## 💡 Tips for Ongoing Use

1. **Weekly commits**: Commit changes every week to maintain history
2. **Meaningful messages**: Use clear commit messages (e.g., "Add advanced optimization for Mês 8")
3. **Create branches**: For major changes, create a branch: `git checkout -b feature/new-feature`
4. **Keep backups**: Continue using automatic ZIP backups even after GitHub

---

**Ready?** Run those 3 commands with your GitHub username and you're done! 🚀
