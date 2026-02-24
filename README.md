# README

This README would normally document whatever steps are necessary to get the
application up and running.

Things you may want to cover:

* Ruby version

* System dependencies

* Configuration

* Database creation

* Database initialization

* How to run the test suite

* Services (job queues, cache servers, search engines, etc.)

* Deployment instructions

* ...

Full Flow:

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