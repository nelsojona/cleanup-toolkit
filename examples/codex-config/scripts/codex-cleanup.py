#!/usr/bin/env python3
"""
Automated code cleanup using OpenAI Codex
"""
import openai
import os
import sys
import argparse
import json
from pathlib import Path

class CodexCleanup:
    def __init__(self, api_key, model="code-davinci-002"):
        openai.api_key = api_key
        self.model = model
    
    def analyze_code(self, code, file_type="python"):
        """Analyze code for cleanup opportunities."""
        prompt = f"""
Analyze this {file_type} code for cleanup opportunities:

{code}

Identify:
1. Debug statements and dead code
2. Duplicate functions and logic
3. Missing documentation
4. Error handling improvements
5. Code quality issues

Analysis:
"""
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=1024,
            temperature=0.1
        )
        
        return response.choices[0].text.strip()
    
    def cleanup_code(self, code, analysis, file_type="python"):
        """Generate cleaned up code based on analysis."""
        prompt = f"""
Clean up this {file_type} code following systematic principles:

Original code:
{code}

Issues identified:
{analysis}

Apply these improvements:
1. Remove debug statements and dead code
2. Consolidate duplicate logic
3. Add comprehensive documentation
4. Improve error handling
5. Enhance code quality

Cleaned code:
"""
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=2048,
            temperature=0.1
        )
        
        return response.choices[0].text.strip()
    
    def generate_documentation(self, code, file_type="python"):
        """Generate comprehensive documentation for code."""
        prompt = f"""
Generate comprehensive documentation for this {file_type} code:

{code}

Include:
- Clear function/class descriptions
- Parameter documentation
- Return value descriptions
- Exception handling notes
- Usage examples where helpful

Documentation:
"""
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=1024,
            temperature=0.1
        )
        
        return response.choices[0].text.strip()
    
    def detect_file_type(self, file_path):
        """Detect programming language from file extension."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp'
        }
        
        ext = Path(file_path).suffix.lower()
        return ext_map.get(ext, 'generic')

def main():
    parser = argparse.ArgumentParser(description="Clean up code using OpenAI Codex")
    parser.add_argument("file", help="File to clean up")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", default="code-davinci-002", help="Codex model to use")
    parser.add_argument("--output", help="Output file (default: overwrite input)")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, don't clean")
    parser.add_argument("--docs-only", action="store_true", help="Only generate documentation")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key required")
        print("Set OPENAI_API_KEY environment variable or use --api-key")
        return 1
    
    # Read file
    try:
        with open(args.file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
        return 1
    
    # Initialize Codex
    cleanup = CodexCleanup(api_key, args.model)
    file_type = cleanup.detect_file_type(args.file)
    
    print(f"Processing {args.file} as {file_type} code...")
    
    # Analyze code
    print("🔍 Analyzing code...")
    analysis = cleanup.analyze_code(code, file_type)
    print(f"\n📊 Analysis:\n{analysis}\n")
    
    if args.analyze_only:
        return 0
    
    # Generate documentation
    if args.docs_only:
        print("📝 Generating documentation...")
        docs = cleanup.generate_documentation(code, file_type)
        print(f"\n📚 Documentation:\n{docs}\n")
        
        # Save documentation
        doc_file = args.output or f"{args.file}.docs.md"
        with open(doc_file, 'w') as f:
            f.write(docs)
        print(f"✅ Documentation saved to {doc_file}")
        return 0
    
    # Clean up code
    print("🧹 Cleaning up code...")
    cleaned_code = cleanup.cleanup_code(code, analysis, file_type)
    
    # Show summary
    orig_lines = len(code.splitlines())
    clean_lines = len(cleaned_code.splitlines())
    print(f"\n📈 Summary:")
    print(f"  Lines: {orig_lines} → {clean_lines} ({clean_lines - orig_lines:+d})")
    
    # Write output
    output_file = args.output or args.file
    
    if output_file == args.file:
        # Create backup
        backup_file = f"{args.file}.backup"
        with open(backup_file, 'w') as f:
            f.write(code)
        print(f"  Backup: {backup_file}")
    
    with open(output_file, 'w') as f:
        f.write(cleaned_code)
    
    print(f"\n✅ Cleaned code written to {output_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())