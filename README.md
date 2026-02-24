# TEST-COP - Rails URL Shortener

A Rails application with Dependabot integration featuring AI-powered auto-fix workflows for gem upgrade failures.

## CI/Workflow Challenges & Resolutions

During setup, several CI failures were encountered and resolved:

| Failure | Type | Cause | Solution |
|---------|------|-------|----------|
| #1 - Permission Denied | CI Config | bin/ scripts not executable in git | `git update-index --chmod=+x bin/*` |
| #2 - Ruby Version Mismatch | CI Config | Gemfile constraint too strict (3.2.0 vs 3.2.10) | Use pessimistic version `ruby "~> 3.2.0"` |
| #3 - SQLite3 Gem Conflict | Gem Compatibility | Dependabot upgraded sqlite3 from ~> 1.4 to 2.9.0 (incompatible) | Auto-fix workflow detects and fixes automatically |

## Getting Started

* Ruby version: 3.2.x (with ~> 3.2.0 flexibility)
* Database: SQLite3
* Testing: Rails integrated tests (bin/rails test)
* Automation: Dependabot with Copilot-powered auto-fix

## Automated Gem Upgrade Workflow

This project uses a **Dependabot Auto-Fix Workflow** that automatically fixes CI failures caused by gem upgrades.

### How It Works

When Dependabot creates a PR with gem updates:

1. **Initial Test Run:**
   - Runs `bin/rails test:prepare` + `bin/rails test`
   - If tests fail → Proceeds to fix iterations

2. **Auto-Fix Loop (up to 3 iterations):**
   - Uses GitHub Copilot to analyze failures
   - Generates fixes for any files (app/, config/, Gemfile, .github/workflows/, etc.)
   - Commits and pushes fixes directly to PR branch
   - Re-runs tests

3. **Result:**
   - ✅ Tests pass at any point → Green PR ready to merge
   - ❌ Still failing after 3 iterations → Requires manual review

### Files Involved

- [.github/workflows/dependabot-auto-fix.yml](.github/workflows/dependabot-auto-fix.yml) - Main auto-fix workflow
- [.github/scripts/gem_diff.rb](.github/scripts/gem_diff.rb) - Gem change analysis script
- [.github/dependabot.yml](.github/dependabot.yml) - Dependabot configuration

### Manual Testing

To manually test the workflow on an existing Dependabot PR:
```bash
@dependabot rebase
```

This triggers a new workflow run on the PR branch.

## Full Flow:

1. Iteration 1:

    - Runs bin/rails test:prepare + bin/rails test
    - If fail → Copilot analyzes gem changes + test failures
    - Copilot generates fixes (any files needed)
    - Commits and pushes fixes to PR branch
    - Re-runs tests
2. Iteration 2 (if still failing):

    - Analyzes remaining failures
    - Copilot generates more refined fixes
    - Commits and pushes
    - Re-runs tests
3. Iteration 3 (final attempt):

    - Same process, last attempt
4. Result:

    - If tests pass at any point → ✅ green PR
    - If still failing after 3 iterations → ⚠️ manual review needed

**You then just**: Review & merge the Dependabot PR


