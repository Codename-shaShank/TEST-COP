#!/usr/bin/env python3
"""
Universal fix application script - handles Ruby, JavaScript, Python, Java, PHP, .NET
Parses AI-generated fixes and applies them to source files
"""

import sys
import re
import os
from pathlib import Path

class UniversalFixApplier:
    """Apply fixes from AI model to various file types"""
    
    SUPPORTED_LANGUAGES = {
        'rb': 'ruby',
        'js': 'javascript',
        'ts': 'typescript',
        'jsx': 'jsx',
        'tsx': 'tsx',
        'py': 'python',
        'java': 'java',
        'php': 'php',
        'cs': 'csharp',
        'go': 'go',
        'rs': 'rust',
        'yml': 'yaml',
        'yaml': 'yaml',
        'json': 'json'
    }
    
    def __init__(self, fix_file):
        self.fix_file = fix_file
        self.fixes = []
        self.commit_message = ""
        self.parse_fixes()
    
    def parse_fixes(self):
        """Parse AI output to extract FIX blocks"""
        with open(self.fix_file, 'r') as f:
            content = f.read()
        
        # Extract commit message
        commit_match = re.search(r'COMMIT_MESSAGE:\s*(.+?)(?:\n|$)', content)
        if commit_match:
            self.commit_message = commit_match.group(1).strip()
        
        # Extract ANALYSIS section
        analysis_match = re.search(r'### ANALYSIS:\s*(.+?)(?=###|$)', content, re.DOTALL)
        if analysis_match:
            print(f"📋 Analysis: {analysis_match.group(1).strip()[:200]}...")
        
        # Extract FIX blocks
        fix_pattern = r'### FIX:\s*(.+?)\n```(?:ruby|python|javascript|typescript|java|php|csharp|go|rust|yaml|json)?\n(.*?)\n```'
        matches = re.finditer(fix_pattern, content, re.DOTALL)
        
        for match in matches:
            file_path = match.group(1).strip()
            code = match.group(2).strip()
            
            # Skip if file path or code looks incomplete
            if not file_path or len(code) < 5:
                continue
            
            self.fixes.append({
                'file': file_path,
                'code': code,
                'type': self.detect_change_type(code)
            })
            print(f"📝 Parsed fix for: {file_path}")
    
    def detect_change_type(self, code):
        """Detect if this is a replacement, addition, or deletion"""
        if '---' in code or '!!!' in code:
            return 'replacement'
        elif code.startswith('-'):
            return 'deletion'
        elif code.startswith('+'):
            return 'addition'
        else:
            return 'block_replacement'
    
    def apply_fixes(self):
        """Apply all parsed fixes to their respective files"""
        successful = []
        failed = []
        
        for fix in self.fixes:
            file_path = fix['file']
            code = fix['code']
            
            # Normalize file path
            file_path = file_path.lstrip('./')
            
            try:
                if self.apply_fix(file_path, code, fix['type']):
                    successful.append(file_path)
                    print(f"✅ Applied fix to {file_path}")
                else:
                    failed.append(file_path)
                    print(f"❌ Failed to apply fix to {file_path}")
            except Exception as e:
                failed.append(file_path)
                print(f"❌ Error applying fix to {file_path}: {str(e)}")
        
        print(f"\n📊 Summary: {len(successful)} successful, {len(failed)} failed")
        return len(failed) == 0
    
    def apply_fix(self, file_path, code, fix_type):
        """Apply fix to a specific file"""
        
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            return False
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Different strategies based on fix type
        if fix_type == 'replacement':
            return self.apply_replacement_fix(file_path, content, code)
        elif fix_type == 'block_replacement':
            return self.apply_block_fix(file_path, content, code)
        else:
            return False
    
    def apply_replacement_fix(self, file_path, content, code):
        """Apply fixes with explicit before/after"""
        # Look for before/after pattern
        parts = code.split('---')
        if len(parts) < 2:
            return False
        
        before = parts[0].strip()
        after = parts[1].strip()
        
        if before in content:
            new_content = content.replace(before, after)
            with open(file_path, 'w') as f:
                f.write(new_content)
            return True
        
        return False
    
    def apply_block_fix(self, file_path, content, code):
        """Apply fixes by inserting/replacing code blocks"""
        lines = content.split('\n')
        code_lines = code.split('\n')
        
        # Find best matching location
        # This is a simplified approach - production would need better heuristics
        
        # Try to find import statements or function definitions
        insertion_point = len(lines)
        
        for i, line in enumerate(lines):
            # Find imports section for import fixes
            if any(keyword in code for keyword in ['import ', 'from ', 'require ', 'using ']):
                if any(keyword in line for keyword in ['import ', 'from ', 'require ', 'using ']):
                    insertion_point = i + 1
                    break
            
            # Find function/method for code changes
            elif any(keyword in line for keyword in ['def ', 'function ', 'function(', 'async function', 'class ']):
                if insertion_point == len(lines):
                    insertion_point = i
        
        # Insert code
        lines.insert(insertion_point, "")
        lines.insert(insertion_point + 1, code)
        
        try:
            with open(file_path, 'w') as f:
                f.write('\n'.join(lines))
            return True
        except:
            return False


class RubyFixApplier(UniversalFixApplier):
    """Specialized applier for Ruby/Rails files"""
    
    def apply_fix(self, file_path, code, fix_type):
        """Ruby-specific fix application"""
        if not file_path.endswith('.rb'):
            return super().apply_fix(file_path, code, fix_type)
        
        return super().apply_fix(file_path, code, fix_type)


class JavaScriptFixApplier(UniversalFixApplier):
    """Specialized applier for JavaScript/TypeScript files"""
    
    def apply_fix(self, file_path, code, fix_type):
        """JavaScript-specific fix application"""
        if file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            return super().apply_fix(file_path, code, fix_type)
        
        return super().apply_fix(file_path, code, fix_type)


class PythonFixApplier(UniversalFixApplier):
    """Specialized applier for Python files"""
    
    def apply_fix(self, file_path, code, fix_type):
        """Python-specific fix application"""
        if not file_path.endswith('.py'):
            return super().apply_fix(file_path, code, fix_type)
        
        return super().apply_fix(file_path, code, fix_type)


def get_applier(language):
    """Get appropriate applier based on language"""
    if language == 'ruby':
        return RubyFixApplier
    elif language in ['javascript', 'typescript']:
        return JavaScriptFixApplier
    elif language == 'python':
        return PythonFixApplier
    else:
        return UniversalFixApplier


def main():
    if len(sys.argv) < 2:
        print("Usage: apply_fixes.py <fix_file> [language]")
        sys.exit(1)
    
    fix_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'unknown'
    
    if not os.path.exists(fix_file):
        print(f"❌ Fix file not found: {fix_file}")
        sys.exit(1)
    
    print(f"🔧 Applying fixes from {fix_file}")
    print(f"📝 Language: {language}")
    
    applier_class = get_applier(language)
    applier = applier_class(fix_file)
    
    if applier.apply_fixes():
        print("✅ All fixes applied successfully")
        sys.exit(0)
    else:
        print("⚠️ Some fixes could not be applied")
        sys.exit(1)


if __name__ == '__main__':
    main()
