# 🤖 Auto-Fix Main - AI-Powered CI Resolver

This workflow uses **GitHub Models (Copilot-powered AI)** to automatically diagnose and fix CI failures.

## 🎯 What It Does

### 1. **CI Environment Diagnostics**
- Checks Ruby/Bundler versions
- Analyzes Gemfile and Gemfile.lock for conflicts
- Detects common issues (deployment mode, frozen gems, version mismatches)
- **Uses AI to understand complex dependency issues**

### 2. **Bundle Install Failure Recovery**
- Detects when `bundle install` fails
- **Sends error logs to AI for analysis**
- AI suggests specific fixes
- Automatically applies fixes and retries
- Handles deployment mode issues automatically

### 3. **Test Failure Analysis (3 Iterations)**
- Runs tests and captures failures
- **AI analyzes stack traces and error messages**
- Generates context-aware fixes
- Applies changes and commits
- Re-runs tests to verify
- Up to 3 iterations for complex issues

### 4. **Comprehensive Reporting**
- Detailed diagnostic reports
- AI analysis explanations
- Step-by-step results
- Actionable recommendations

## 🚀 How to Use

### Automatic Trigger
The workflow runs automatically when:
- Dependabot opens a PR with Gemfile changes
- Any PR modifies Gemfile or Gemfile.lock

### Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select **"Auto-Fix Main"**
3. Click **"Run workflow"**
4. Choose the branch/PR to fix
5. Click **"Run workflow"**

### PR Comment Trigger
Comment `/autofix` on any PR to trigger the workflow

## 🔧 Common Issues It Fixes

### ✅ Bundle Install Failures
```
Error: You are trying to install in deployment mode
```
**AI Fix:** Automatically disables deployment mode and updates config

### ✅ Gem Version Conflicts
```
Error: sqlite3 (2.9.0) installed but Gemfile requires (~> 1.4)
```
**AI Fix:** Analyzes version compatibility and updates Gemfile.lock

### ✅ Test Failures
```
Error: NameError: uninitialized constant
```
**AI Fix:** Analyzes code context and suggests require statements or class definitions

### ✅ Breaking Gem Updates
```
Error: sqlite3 2.x has breaking changes from 1.x
```
**AI Fix:** Pins gem to compatible version and updates constraints

## 🤖 AI Models Used

The workflow tries multiple AI models in order:
1. `gpt-4o-mini` (primary)
2. `openai-gpt-4o-mini` (fallback)
3. `gpt-3.5-turbo` (backup)

### Requirements:
- GitHub Models access (preview program)
- Sign up: https://github.com/marketplace/models

## 📊 Understanding the Results

### Success Indicators
- ✅ **Green checkmarks** = Step succeeded
- ⚠️ **Yellow warnings** = Non-critical issues
- ❌ **Red X** = Step failed (may be intentional)

### Exit Codes
- `0` = Tests passed
- `1` = Tests failed (will trigger AI fix)
- `16` = Bundle error (will trigger bundle fix)

### Reading AI Suggestions
AI responses include:
- **Analysis:** What went wrong
- **Fix:** Specific code changes
- **Commands:** Shell commands to run
- **Commit Message:** Suggested commit message

## 🐛 Troubleshooting

### "AI models unavailable"
**Solution:** Check GitHub Models access at https://github.com/marketplace/models

### "Bundle install still failing"
**Solution:** Review the AI's bundle fix suggestions in logs, may need manual Gemfile.lock update

### "Tests pass locally but fail in CI"
**Solution:** Check environment differences (Ruby version, platform-specific gems)

### "No fixes generated"
**Reasons:**
- build_ai_prompt.sh script missing (workflow will create fallback prompts)
- GitHub Models API not accessible
- No clear fix pattern detected

## 📝 Example Workflow Run

```
1. 🔍 CI Diagnostic → Detects sqlite3 2.x vs 1.x conflict
   └─ AI Analysis → "Breaking change in sqlite3 2.x"
   
2. 🤖 AI CI Fix → Suggests pinning sqlite3 < 2.0
   └─ Apply Fix → Updates Gemfile constraint
   └─ Commit → "fix(ci): pin sqlite3 to 1.x for compatibility"
   
3. 📦 Bundle Install → Success!
   
4. 🧪 Run Tests → Pass!
   
5. ✅ Summary → All green, PR is ready
```

## 💡 Pro Tips

1. **Review AI commits** - Check what the bot changed before merging
2. **Read AI analysis** - Understand why changes were needed
3. **Iterate locally** - Use AI suggestions for local development
4. **Update Dependabot config** - Pin problematic gems to prevent future issues

## 🔐 Security Notes

- Workflow has write access to push fixes
- AI never sees secrets or credentials
- Only analyzes public code and logs
- Changes are committed as `github-actions[bot]`

## 📚 Related Files

- [dependabot-auto-fix.yml](dependabot-auto-fix.yml) - Original workflow
- [Dependabot config](../dependabot.yml) - Dependency update settings
- [relax_gemfile.rb](../scripts/relax_gemfile.rb) - Gemfile constraint relaxer

## 🆘 Need Help?

If the workflow fails after 3 iterations:
1. Review the **AI Fix Report** in the job summary
2. Check **AI suggestions** in each iteration
3. Look for **manual intervention** recommendations
4. Consider applying fixes locally and pushing

---

**Powered by:** GitHub Models + Actions  
**AI Provider:** OpenAI GPT-4o-mini  
**Maintained by:** github-actions[bot]
