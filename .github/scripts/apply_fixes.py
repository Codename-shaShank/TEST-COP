#!/usr/bin/env python3
"""Parse AI fix suggestions and apply them to files.

Usage: python3 apply_fixes.py <fixes_file>

The script looks for FIX_FILE blocks in various formats:
  FIX_FILE: path/to/file
  ```ruby
  content
  ```

It also tries alternative patterns the AI might use.
"""
import re
import os
import sys

def parse_fixes(content):
    """Parse AI output for explicit FIX blocks only.

    Accepted formats:

      ### FIX: path/to/file.rb
      ```ruby
      # full file content
      ```

      FIX_FILE: path/to/file.rb
      ```ruby
      # full file content
      ```
    """
    matches = []

    # Format 1: ### FIX: path/to/file
    pattern_fix = r'###\s*FIX:\s*([^\n]+)\n\s*```[\w-]*\n(.*?)```'
    for filepath, file_content in re.findall(pattern_fix, content, re.DOTALL):
        matches.append((filepath.strip(), file_content.rstrip()))

    # Format 2: FIX_FILE: path/to/file
    pattern_fix_file = r'FIX_FILE:\s*([^\n]+)\n\s*```[\w-]*\n(.*?)```'
    for filepath, file_content in re.findall(pattern_fix_file, content, re.DOTALL):
        matches.append((filepath.strip(), file_content.rstrip()))

    return matches


def main():
    if len(sys.argv) < 2:
        print("Usage: apply_fixes.py <fixes_file>")
        sys.exit(1)

    fixes_file = sys.argv[1]

    try:
        with open(fixes_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {fixes_file}")
        sys.exit(0)

    # Check for NO_FIX_NEEDED
    if 'NO_FIX_NEEDED' in content:
        print("AI says no fix needed.")
        sys.exit(0)

    print(f"--- AI Response Preview (first 500 chars) ---")
    print(content[:500])
    print(f"--- End Preview ---")
    print(f"Total response length: {len(content)} chars")

    matches = parse_fixes(content)

    if not matches:
        print("WARNING: Could not parse any FIX_FILE blocks from AI response.")
        print("The AI may not have followed the expected format.")
        sys.exit(0)

    for filepath, file_content in matches:
        # Safety: don't allow writing outside the project
        if filepath.startswith('/') or '..' in filepath:
            print(f"SKIPPED (unsafe path): {filepath}")
            continue

        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(file_content + '\n')
        print(f"Applied fix: {filepath}")

    print(f"Total fixes applied: {len(matches)}")


if __name__ == '__main__':
    main()
