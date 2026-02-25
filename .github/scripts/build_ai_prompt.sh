#!/usr/bin/env bash
# Usage: build_ai_prompt.sh <iteration> <test_output_file> [gem_diff_file]
# Writes the AI prompt to stdout.

ITERATION=${1:-1}
TEST_OUTPUT_FILE=${2:-test_output.txt}
GEM_DIFF_FILE=${3:-""}

TEST_FAILURES=$(tail -300 "$TEST_OUTPUT_FILE" 2>/dev/null || echo "No test output found")

if [ "$ITERATION" = "1" ]; then
  GEM_CHANGES=""
  if [ -n "$GEM_DIFF_FILE" ] && [ -f "$GEM_DIFF_FILE" ]; then
    GEM_CHANGES=$(head -200 "$GEM_DIFF_FILE")
  else
    GEM_CHANGES=$(git diff origin/main -- Gemfile.lock 2>/dev/null | head -200 || echo "No gem diff available")
  fi

  FILE_TREE=$(find app config lib -type f 2>/dev/null | head -80 || true)

  cat <<PROMPT
You are an expert Ruby on Rails DevOps engineer. A Dependabot gem upgrade caused CI test failures.

GEM CHANGES (Gemfile.lock diff vs main):
${GEM_CHANGES}

TEST FAILURES:
${TEST_FAILURES}

PROJECT FILES (for context):
${FILE_TREE}

YOUR TASK:
Analyze the test failures caused by the gem upgrade and provide code-level fixes.
You may fix ANY files needed: app/, config/, lib/, Gemfile, test/, etc.

Format your response EXACTLY as shown below (one block per file):

FIX_FILE: path/to/file.ext
\`\`\`language
complete file content here (not partial — write the full file)
\`\`\`

COMMIT_MESSAGE: short description of the fix

If no fixes are needed, respond with only: NO_FIX_NEEDED
PROMPT

elif [ "$ITERATION" = "2" ]; then
  cat <<PROMPT
Fixes were applied in iteration 1 but tests are still failing. Provide additional fixes.

REMAINING TEST FAILURES:
${TEST_FAILURES}

Format EXACTLY as:
FIX_FILE: path/to/file.ext
\`\`\`language
complete file content
\`\`\`

COMMIT_MESSAGE: description

If no further fixes are needed, respond with only: NO_FIX_NEEDED
PROMPT

elif [ "$ITERATION" = "3" ]; then
  cat <<PROMPT
This is the final fix attempt after 2 previous iterations. Tests are still failing.
Carefully analyze what remains and provide all necessary fixes.

REMAINING TEST FAILURES:
${TEST_FAILURES}

Format EXACTLY as:
FIX_FILE: path/to/file.ext
\`\`\`language
complete file content
\`\`\`

COMMIT_MESSAGE: description

If no further fixes are needed, respond with only: NO_FIX_NEEDED
PROMPT
fi
