# Git Setup Commands for E-Commerce API

## Step 1: Clean up optional files (OPTIONAL)
```bash
# Remove internal documentation files
rm VERIFICATION_REPORT.md
rm PROJECT_BRIEF.md
```

## Step 2: Initialize Git Repository
```bash
# Initialize git (creates .git folder)
git init

# Verify git was initialized
git status
```

## Step 3: Stage All Files
```bash
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status
```

## Step 4: Create Initial Commit
```bash
# Commit with professional message
git commit -m "feat: Initial commit of production-ready E-Commerce API with 100% test coverage"
```

## Step 5: Rename Branch to main
```bash
# Rename branch from master to main (modern standard)
git branch -M main
```

## Step 6: Connect to GitHub Remote
```bash
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
# Example: git remote add origin https://github.com/johndoe/ecommerce-api.git

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Verify remote was added
git remote -v
```

## Step 7: Push to GitHub
```bash
# Push to GitHub (first time)
git push -u origin main

# For subsequent pushes, just use:
# git push
```

---

## ✅ Verification Steps

### 1. Verify .env was NOT committed:
```bash
# This should return nothing (file not tracked)
git ls-files | grep .env

# This should show .env is ignored
git status --ignored | grep .env
```

### 2. Verify migration file WAS committed:
```bash
# This should show your migration file
git ls-files | grep "alembic/versions"
```

### 3. Check what's tracked:
```bash
# See all tracked files
git ls-files

# Count tracked files
git ls-files | wc -l
```

---

## 🔍 What Should Be Committed?

### ✅ SHOULD be in Git:
- All Python code (`app/`, `tests/`)
- Configuration files (`docker-compose.yml`, `Dockerfile`, `requirements.txt`)
- Alembic migrations (`alembic/versions/*.py`)
- Documentation (`README.md`, `QUICKSTART.md`)
- `.env.example` (template)
- `.gitignore`
- `pytest.ini`, `alembic.ini`

### ❌ Should NOT be in Git (excluded by .gitignore):
- `.env` (contains secrets!)
- `__pycache__/` directories
- `venv/` or `ENV/`
- `.pytest_cache/`
- `postgres_data/` (Docker volume)
- IDE files (`.vscode/`, `.idea/`)
- `*.pyc`, `*.log` files

---

## 🎯 Complete Command Sequence (Copy-Paste Ready)

```bash
# 1. Optional: Remove internal docs
rm VERIFICATION_REPORT.md PROJECT_BRIEF.md

# 2. Initialize repository
git init

# 3. Add all files
git add .

# 4. Verify .env is NOT staged
git status | grep .env
# (Should show nothing or show it's ignored)

# 5. Commit
git commit -m "feat: Initial commit of production-ready E-Commerce API with 100% test coverage"

# 6. Rename to main
git branch -M main

# 7. Add remote (REPLACE WITH YOUR REPO URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 8. Push to GitHub
git push -u origin main
```

---

## 📱 GitHub Repository Setup

Before running these commands, create a repository on GitHub:

1. Go to https://github.com/new
2. Repository name: `enterprise-ecommerce-api` (or your choice)
3. Description: "Production-ready FastAPI E-Commerce Backend with OAuth2, PostgreSQL, and 100% test coverage"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we have those)
6. Click "Create repository"
7. Copy the repository URL shown
8. Use that URL in the `git remote add origin` command above

---

## 🚨 Security Checklist

Before pushing, verify:

- [ ] `.env` file is in `.gitignore`
- [ ] `.env` is NOT staged (`git status` doesn't show it)
- [ ] `.env.example` is staged (template for others)
- [ ] No passwords or secrets in any committed files
- [ ] All sensitive data uses environment variables

---

## 💡 Post-Push Tasks

After successfully pushing:

1. **Add GitHub Topics** (on GitHub repo page):
   - `fastapi`
   - `python`
   - `postgresql`
   - `docker`
   - `oauth2`
   - `jwt`
   - `ecommerce`
   - `rest-api`

2. **Add Repository Description:**
   "Production-ready E-Commerce API built with FastAPI, PostgreSQL, Docker, OAuth2/JWT authentication, SQLAlchemy ORM, Pydantic v2 validation, Alembic migrations, and comprehensive Pytest suite with 100% test coverage."

3. **Consider adding:**
   - GitHub Actions for CI/CD
   - Dependabot for dependency updates
   - Issue templates
   - Contributing guidelines

---

## 🔄 Future Updates

After initial push, use standard git workflow:

```bash
# Make changes to your code

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add payment processing endpoint"

# Push to GitHub
git push
```

---

## 🆘 Troubleshooting

### If you accidentally committed .env:

```bash
# Remove from git but keep local file
git rm --cached .env

# Commit the removal
git commit -m "fix: Remove .env file from git history"

# Push
git push
```

### If push is rejected:

```bash
# Pull first (if others made changes)
git pull origin main --rebase

# Then push
git push
```

---

**You're ready to push! 🚀**
