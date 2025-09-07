#!/usr/bin/env python3
"""
Interactive Codex cleanup session with user confirmation
"""
import openai
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import difflib
import json

class InteractiveCleanup:
    def __init__(self, api_key=None):
        """Initialize interactive cleanup session."""
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required")
        
        openai.api_key = api_key
        self.model = "code-davinci-002"
        self.session_log = []
    
    def start_session(self, files: List[str]):
        """Start interactive cleanup session."""
        print("🧹 Starting systematic cleanup session with OpenAI Codex...")
        print(f"📁 Files to process: {len(files)}\n")
        
        for file_path in files:
            if Path(file_path).exists():
                self.process_file(file_path)
            else:
                print(f"⚠️ File not found: {file_path}")
        
        self.generate_session_report()
    
    def process_file(self, file_path: str):
        """Process a single file interactively."""
        print(f"\n{'='*60}")
        print(f"📁 Processing: {file_path}")
        print(f"{'='*60}")
        
        # Read file
        with open(file_path, 'r') as f:
            original_code = f.read()
        
        file_type = self.detect_file_type(file_path)
        
        # Step 1: Analysis
        print("\n🔍 Analyzing code with Codex...")
        analysis = self.analyze_code(original_code, file_type)
        
        print(f"\n📊 Analysis Results:")
        print("-" * 40)
        print(analysis)
        print("-" * 40)
        
        proceed = input("\n❓ Proceed with cleanup? (y/N/s[kip]): ").lower()
        if proceed in ['s', 'skip']:
            print(f"⏭️ Skipped {file_path}")
            self.session_log.append({
                'file': file_path,
                'status': 'skipped',
                'reason': 'User skipped'
            })
            return
        
        if not proceed.startswith('y'):
            return
        
        # Step 2: Cleanup
        print("\n🛠️ Generating cleaned code with Codex...")
        cleaned_code = self.cleanup_code(original_code, analysis, file_type)
        
        # Step 3: Show diff
        print("\n📊 Proposed Changes:")
        self.show_diff(original_code, cleaned_code)
        
        # Step 4: Summary
        print("\n📈 Cleanup Summary:")
        self.show_summary(original_code, cleaned_code)
        
        # Step 5: Apply changes
        apply = input("\n❓ Apply changes? (y/N/v[iew]): ").lower()
        
        if apply == 'v':
            print("\n📄 Cleaned Code:")
            print("-" * 40)
            print(cleaned_code)
            print("-" * 40)
            apply = input("\n❓ Apply changes now? (y/N): ").lower()
        
        if apply.startswith('y'):
            # Create backup
            backup_path = f"{file_path}.backup"
            with open(backup_path, 'w') as f:
                f.write(original_code)
            
            # Write cleaned code
            with open(file_path, 'w') as f:
                f.write(cleaned_code)
            
            print(f"✅ Applied changes to {file_path}")
            print(f"💾 Backup saved to {backup_path}")
            
            self.session_log.append({
                'file': file_path,
                'status': 'cleaned',
                'analysis': analysis,
                'lines_changed': len(cleaned_code.splitlines()) - len(original_code.splitlines())
            })
        else:
            print(f"⏭️ Changes not applied to {file_path}")
            self.session_log.append({
                'file': file_path,
                'status': 'analyzed',
                'reason': 'User declined changes'
            })
    
    def analyze_code(self, code: str, file_type: str) -> str:
        """Analyze code for cleanup opportunities."""
        prompt = f"""
Analyze this {file_type} code for systematic cleanup opportunities:

```{file_type}
{code[:2000]}  # Truncate for analysis
```

Identify and list:
1. Debug statements and console output
2. Duplicate or similar functions
3. Missing or inadequate documentation
4. Poor error handling
5. Code quality issues
6. Unused imports or variables

Provide specific, actionable findings:
"""
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=500,
            temperature=0.1
        )
        
        return response.choices[0].text.strip()
    
    def cleanup_code(self, code: str, analysis: str, file_type: str) -> str:
        """Generate cleaned up code."""
        prompt = f"""
Clean up this {file_type} code based on the analysis:

Analysis findings:
{analysis}

Original code:
```{file_type}
{code}
```

Apply these systematic improvements:
1. Remove all debug statements and console output
2. Consolidate duplicate logic
3. Add comprehensive documentation
4. Improve error handling
5. Follow best practices for {file_type}

Cleaned code:
```{file_type}
"""
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=2048,
            temperature=0.1,
            stop=["```"]
        )
        
        return response.choices[0].text.strip()
    
    def show_diff(self, original: str, cleaned: str):
        """Show unified diff between original and cleaned code."""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            cleaned.splitlines(keepends=True),
            fromfile="original",
            tofile="cleaned",
            n=3
        )
        
        diff_text = ''.join(diff)
        if diff_text:
            # Limit diff output
            lines = diff_text.splitlines()
            if len(lines) > 50:
                print('\n'.join(lines[:25]))
                print(f"\n... ({len(lines) - 50} lines omitted) ...\n")
                print('\n'.join(lines[-25:]))
            else:
                print(diff_text)
        else:
            print("No changes detected")
    
    def show_summary(self, original: str, cleaned: str):
        """Show cleanup summary statistics."""
        orig_lines = original.splitlines()
        clean_lines = cleaned.splitlines()
        
        # Count debug statements
        debug_patterns = ['print(', 'console.log', 'console.debug', 'debugger', 'var_dump']
        debug_original = sum(1 for line in orig_lines 
                           for pattern in debug_patterns if pattern in line)
        debug_cleaned = sum(1 for line in clean_lines 
                          for pattern in debug_patterns if pattern in line)
        
        print(f"  Lines: {len(orig_lines)} → {len(clean_lines)} "
              f"({len(clean_lines) - len(orig_lines):+d})")
        
        if debug_original > debug_cleaned:
            print(f"  Debug statements removed: {debug_original - debug_cleaned}")
        
        # Check for documentation improvements
        doc_patterns = ['"""', "'''", '/**', '//', '#']
        doc_original = sum(1 for line in orig_lines 
                         for pattern in doc_patterns if line.strip().startswith(pattern))
        doc_cleaned = sum(1 for line in clean_lines 
                        for pattern in doc_patterns if line.strip().startswith(pattern))
        
        if doc_cleaned > doc_original:
            print(f"  Documentation lines added: {doc_cleaned - doc_original}")
    
    def detect_file_type(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.swift': 'swift',
            '.kt': 'kotlin'
        }
        
        ext = Path(file_path).suffix.lower()
        return ext_map.get(ext, 'text')
    
    def generate_session_report(self):
        """Generate and save cleanup session report."""
        print(f"\n{'='*60}")
        print("📋 Session Complete!")
        print(f"{'='*60}\n")
        
        # Count statistics
        cleaned = [log for log in self.session_log if log['status'] == 'cleaned']
        analyzed = [log for log in self.session_log if log['status'] == 'analyzed']
        skipped = [log for log in self.session_log if log['status'] == 'skipped']
        
        print(f"✅ Files cleaned: {len(cleaned)}")
        print(f"🔍 Files analyzed only: {len(analyzed)}")
        print(f"⏭️ Files skipped: {len(skipped)}")
        
        if cleaned:
            total_lines = sum(log.get('lines_changed', 0) for log in cleaned)
            print(f"📈 Total lines changed: {total_lines:+d}")
        
        # Save detailed report
        report_dir = Path(".cleanup-toolkit/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = report_dir / "codex-session.json"
        with open(report_path, 'w') as f:
            json.dump(self.session_log, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_path}")
        
        # Generate markdown report
        md_report_path = report_dir / "codex-session.md"
        with open(md_report_path, 'w') as f:
            f.write("# Codex Cleanup Session Report\n\n")
            f.write(f"**Total files processed:** {len(self.session_log)}\n")
            f.write(f"**Files cleaned:** {len(cleaned)}\n")
            f.write(f"**Files analyzed:** {len(analyzed)}\n")
            f.write(f"**Files skipped:** {len(skipped)}\n\n")
            
            if cleaned:
                f.write("## Cleaned Files\n\n")
                for log in cleaned:
                    f.write(f"### {log['file']}\n")
                    f.write(f"- Lines changed: {log.get('lines_changed', 0):+d}\n")
                    if 'analysis' in log:
                        f.write(f"- Issues found: {log['analysis'][:200]}...\n")
                    f.write("\n")
        
        print(f"📝 Markdown report saved: {md_report_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: interactive-cleanup.py <file1> [file2] ...")
        print("\nExample:")
        print("  interactive-cleanup.py src/*.py")
        print("  interactive-cleanup.py main.js utils.js")
        sys.exit(1)
    
    try:
        cleanup = InteractiveCleanup()
        cleanup.start_session(sys.argv[1:])
    except ValueError as e:
        print(f"Error: {e}")
        print("Set OPENAI_API_KEY environment variable")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Session interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()