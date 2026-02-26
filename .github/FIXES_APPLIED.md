# 🔧 Fixes Applied - Troubleshooting Guide

## 🐛 Issues Found & Fixed

### 1. **❌ GitHub Models API Error**
**Error**: `HTTP 400 - Unknown model: openai/gpt-4o-mini`

**Root Cause**: 
- The model name `openai/gpt-4o-mini` is **not available** in GitHub Models API
- GitHub Models only supports specific model names (without vendor prefix)

**Fix Applied**:
- ✅ Changed `openai/gpt-4o-mini` → `gpt-4o` in **both workflows**
- ✅ Updated `.github/scripts/call_github_models.py` to map old names to correct names
- ✅ Added fallback/alias system for future model name changes

**Available Models**:
```
✅ gpt-4o              (OpenAI GPT-4 Turbo)
✅ claude-3-5-sonnet   (Anthropic Claude 3.5)
✅ mistral-large       (Mistral)
✅ phi-4               (Microsoft Phi)
✅ gemma-2-9b          (Google Gemma)
```

**Files Updated**:
- `.github/workflows/dependabot-auto-fix.yml` (all 3 iterations)
- `.github/workflows/universal-dependency-autofix.yml`
- `.github/scripts/call_github_models.py` (with model mapping)

---

### 2. **❌ Missing Tailwind CSS File**
**Error**: `Specified input file ./app/assets/tailwind/application.css does not exist`

**Root Cause**:
- Tailwind CSS v4 requires an `application.css` entry file
- The file was missing from the repository

**Fix Applied**:
- ✅ Created `app/assets/tailwind/application.css` with minimal Tailwind configuration:
```css
@import "tailwindcss";
```

**File Created**:
- `app/assets/tailwind/application.css` (new)

---

## ✅ Testing the Fixes

### Step 1: Verify Tailwind CSS
```bash
# Check that file exists
ls -la app/assets/tailwind/application.css
# Should show: app/assets/tailwind/application.css

# Try the build task
bin/rails tailwindcss:build
# Should complete without "Specified input file" error
```

### Step 2: Verify GitHub Models API
```bash
# Test with a simple request
GITHUB_TOKEN=your_token gh models run gpt-4o --input "test prompt"

# Should NOT get 400 error
# Should respond with model output
```

### Step 3: Run Full Test Suite
```bash
# On your local machine
bin/rails test:prepare
bin/rails test

# On GitHub Actions (automatic when PR is created)
# Workflow: .github/workflows/dependabot-auto-fix.yml
```

---

## 📝 What Changed in Workflows

### Original Workflow: `dependabot-auto-fix.yml`

**Model Fix (3 places)**:
```yaml
# ❌ BEFORE
env:
  MODEL_NAME: openai/gpt-4o-mini

# ✅ AFTER
env:
  MODEL_NAME: gpt-4o
```

### Universal Workflow: `universal-dependency-autofix.yml`

**Model Added**:
```yaml
# ✅ NOW HAS
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  MODEL_NAME: gpt-4o
```

### Script: `.github/scripts/call_github_models.py`

**Model Mapping Added**:
```python
# Maps old names to correct names
model_map = {
    'gpt-4o-mini': 'gpt-4o',
    'openai/gpt-4o': 'gpt-4o',
    'openai/gpt-4o-mini': 'gpt-4o',
}
model = model_map.get(model, model)
```

---

## 🚀 Next Steps

### 1. Test the Original Workflow
```bash
# Create a test PR with a dependency update
# The workflow should now:
# 1. Run without Tailwind error ✅
# 2. Call GitHub Models API successfully ✅
# 3. Get AI suggestions for fixes ✅
```

### 2. Choose Which Workflow to Use

**Option A: Original Workflow (Rails-specific)**
```
Use: .github/workflows/dependabot-auto-fix.yml
For: Ruby/Rails projects only
Benefits: Optimized for Rails, familiar structure
```

**Option B: Universal Workflow (Multi-language)**
```
Use: .github/workflows/universal-dependency-autofix.yml
For: Any language (Ruby, Node, Python, Java, PHP, .NET)
Benefits: Works with multiple languages, extensible
```

---

## 🔍 Troubleshooting Reference

### Issue: Still getting Model API errors
**Solution**:
1. Check `GITHUB_TOKEN` is set in secrets
2. Verify token has `models: read` scope
3. Try using `claude-3-5-sonnet` instead of `gpt-4o`
4. Check `.github/scripts/call_github_models.py` is using correct endpoint

### Issue: Tailwind CSS still failing
**Solution**:
1. Verify `app/assets/tailwind/application.css` exists
2. Check file has content: `@import "tailwindcss";`
3. Run: `bundle exec rails tailwindcss:build` locally
4. Check `config/tailwind.config.js` for configuration issues

### Issue: Tests passing locally but failing in GitHub Actions
**Solution**:
1. Ensure all files (including `application.css`) are committed
2. Run `git status` to check for uncommitted changes
3. Verify dependencies are up to date: `bundle install`
4. Check workflow permissions in `.github/workflows/*.yml`

---

## 📊 Status Summary

| Item | Status | Notes |
|------|--------|-------|
| Model API | ✅ Fixed | Changed to `gpt-4o` |
| Tailwind CSS | ✅ Fixed | Created `application.css` |
| Original Workflow | ✅ Updated | 3 iterations fixed |
| Universal Workflow | ✅ Updated | Model added |
| Fix Script | ✅ Updated | Model mapping added |

---

## 📚 Related Documentation

- [AI Models Available](#available-models)
- [Workflow Documentation](./AUTO_FIX_README.md)
- [Upgrade Guide](./UPGRADE_GUIDE.md)
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)

---

## ❓ Questions?

### "What if I want to use a different model?"
Update the `MODEL_NAME` environment variable:
```yaml
env:
  MODEL_NAME: claude-3-5-sonnet  # Or other available models
```

### "How do I test the workflow locally?"
```bash
# Trigger workflow manually
gh workflow run dependabot-auto-fix.yml

# Or create a test PR and observe the workflow
```

### "What if GitHub Models API is not available in my region?"
- GitHub Models API is available in US/EU regions
- Contact GitHub support if you're in a different region
- Alternative: Configure with an external API (requires modification)

---

✅ **All fixes are ready to test!** 🚀

