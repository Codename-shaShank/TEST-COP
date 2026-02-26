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
    """Try multiple regex patterns to find file fixes in AI output."""
    all_matches = []

    # Pattern 1: Standard FIX_FILE format
    pattern1 = r'FIX_FILE:\s*(.+?)\n\s*```\w*\n(.*?)```'
    matches = re.findall(pattern1, content, re.DOTALL)
    for filepath, file_content in matches:
        all_matches.append((filepath.strip(), file_content.rstrip()))

    if all_matches:
        return all_matches

    # Pattern 2: ### FIX: path/to/file format (new format)
    pattern2 = r'###\s*FIX:\s*(.+?)\n\s*```\w*\n(.*?)```'
    matches = re.findall(pattern2, content, re.DOTALL)
    for filepath, file_content in matches:
        all_matches.append((filepath.strip(), file_content.rstrip()))

    if all_matches:
        return all_matches

    # Pattern 3: FIX_FILE with language on same line as backticks
    pattern3 = r'FIX_FILE:\s*(.+?)\n\s*```(\w+)\n(.*?)```'
    matches = re.findall(pattern3, content, re.DOTALL)
    for filepath, lang, file_content in matches:
        all_matches.append((filepath.strip(), file_content.rstrip()))

    if all_matches:
        return all_matches

    # Pattern 4: **filename** or `filename` followed by code block
    pattern4 = r'(?:\*\*|`)([a-zA-Z0-9_/.-]+\.\w+)(?:\*\*|`)\s*(?::|)\s*\n\s*```\w*\n(.*?)```'
    matches = re.findall(pattern4, content, re.DOTALL)
    for filepath, file_content in matches:
        all_matches.append((filepath.strip(), file_content.rstrip()))

    if all_matches:
        return all_matches

    # Pattern 5: Look for file paths followed by code blocks more loosely
    pattern5 = r'(?:^|\n)\s*([a-zA-Z0-9_/.-]+(?:\.rb|\.yml|\.yaml|\.gemspec|Gemfile))\s*(?::|)\s*\n\s*```\w*\n(.*?)```'
    matches = re.findall(pattern5, content, re.DOTALL)
    for filepath, file_content in matches:
        all_matches.append((filepath.strip(), file_content.rstrip()))

    return all_matches


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
