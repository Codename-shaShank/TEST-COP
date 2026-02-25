# TEST-COP - Rails URL Shortener

A Rails application with Dependabot integration featuring AI-powered auto-fix workflows for gem upgrade failures.

## CI/Workflow Challenges & Resolutions

### 🐛 CI Failures Encountered & Resolved

**1. The "Swallowed Exit Code" Bug (Pipe masking failures)**
* **Issue:** The `bin/rails test` command was piping its output to `tee` (`bin/rails test | tee output.txt`). In standard Bash, the exit code of a pipeline is the exit code of the *last* command. Because `tee` always succeeded, the workflow thought tests were passing perfectly, even when Rails threw exceptions, preventing the AI from ever being triggered.
* **Resolution:** Removed the pipe. Redirected standard output and error directly to a file (`> test_output.txt 2>&1`), added `set +e` to prevent the runner from aborting early, and explicitly captured the raw `$?` exit code into a GitHub step output. 

**2. Strict `Gemfile` vs. `Gemfile.lock` Downgrading (The `sqlite` conflict)**
* **Issue:** Dependabot bumped `sqlite3` to `~> 2.9` inside `Gemfile.lock`. However, the root `Gemfile` still had a strict Rails-default requirement for `~> 1.4`. When GitHub Actions ran `bundle install`, Bundler silently favored the `Gemfile` and downgraded `sqlite3` back to `1.x`. The tests ran against the old gem, passed, and hid the new gem's breaking changes.
* **Resolution:** Created a `.github/scripts/relax_gemfile.rb` ruby script that runs *before* `bundle install`. It dynamically rewrites the strict constraints inside the `Gemfile` in the CI runner (e.g., `~> 1.4` -> `>= 1.4, < 2.0`), forcing Bundler to respect Dependabot's exact `Gemfile.lock` version so the tests can properly fail against it.

**3. YAML Linter & Heredoc Escaping Errors**
* **Issue:** We attempted to dynamically construct the AI's prompt string inside the YAML workflow using a multiline `EOF` bash block. The GitHub Actions parser and YAML linters choked on the nested variables, quotes, and markdown formatting, causing severe syntax errors.
* **Resolution:** Extracted all prompt construction logic out of the `.yml` file and into a dedicated shell script (`.github/scripts/build_ai_prompt.sh`). This completely bypassed GitHub Actions interpolation bugs and made the prompts easier to format securely.

**4. Empty Commit Message Aborts**
* **Issue:** The AI is instructed to provide a `COMMIT_MESSAGE:` block along with its code fixes. Occasionally, the AI failed to provide this, resulting in an empty bash variable. Running `git commit -m ""` natively crashes Git and aborted the workflow right as the fix was being applied.
* **Resolution:** Bolstered the commit message extraction step with bash fallbacks. It now strips carriage returns cleanly (`tr -d '\r'`) and injects a default commit string (`if [ -z "$COMMIT_MSG" ] ...`) if the AI fails to generate one, guaranteeing the fix gets pushed.

**5. Missing `gh models` CLI Extension**
* **Issue:** The workflow crashed with `unknown command "models"` because the GitHub AI inference extension is too new and not natively pre-installed on the `ubuntu-latest` GitHub Actions runner.
* **Resolution:** Added `gh extension install github/gh-models` explicitly to the workflow setup steps to dynamically download the capability before the AI is invoked.

**6. GitHub CLI `--input` Piped Syntax Errors**
* **Issue:** Attempting to pass the multi-page error log to the AI via `gh models run --input prompt.txt` failed with an `unknown flag` error due to recent CLI syntax changes. Attempting to pipe it via `cat` hung the runner infinitely.
* **Resolution:** Updated the syntax to use standard input piping with the explicit hyphen flag (`cat prompt.txt | gh models run openai/gpt-4o -`). This securely streams the massive log context into the LLM without hitting argument length limits or syntax errors.

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


