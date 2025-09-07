# OpenAI Codex Integration for Cleanup Toolkit

> *"After successfully completing your goal, ask: 'Please clean up the code you worked on, remove any bloat you added, and document it very clearly.'"*

Integrate systematic code cleanup workflow with **OpenAI Codex**, leveraging its powerful code understanding and generation capabilities. This guide shows how to use Codex for intelligent, context-aware code improvement following proven cleanup principles.

## 🎯 Why Codex + Cleanup Toolkit?

| Traditional Cleanup | Codex + Cleanup Toolkit |
|-------------------|------------------------|
| ❌ Static, rule-based | ✅ AI-powered, adaptive |
| ❌ Limited understanding | ✅ Deep code comprehension |
| ❌ Generic improvements | ✅ Context-aware refactoring |
| ❌ Manual, time-consuming | ✅ Automated with intelligence |

## 🚀 Quick Setup

### 1. Install Cleanup Toolkit
```bash
# In your project directory
curl -sSL https://raw.githubusercontent.com/your-username/cleanup-toolkit/main/install.sh | bash
```

### 2. Configure OpenAI API
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Configure for Codex integration
echo "codex_integration: true" >> .cleanup-toolkit/config.yml
echo "preferred_framework: codex" >> .cleanup-toolkit/config.yml
echo "openai_model: code-davinci-002" >> .cleanup-toolkit/config.yml
```

### 3. Install Codex Helper Script
```bash
# Create Codex integration script
cat > .cleanup-toolkit/scripts/codex-cleanup.py << 'EOF'
#!/usr/bin/env python3
import openai
import os
import sys

def cleanup_with_codex(file_path, cleanup_context):
    """Use Codex to clean up code following systematic principles."""
    with open(file_path, 'r') as f:
        code = f.read()
    
    prompt = f"""
# Code Cleanup Task
Following systematic cleanup principles:
1. Remove bloat (debug statements, unused code)
2. Consolidate duplicate logic
3. Document clearly with comprehensive comments
4. Improve error handling and quality

## Context
{cleanup_context}

## Original Code
{code}

## Cleaned Code
"""
    
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        temperature=0.1,
        stop=["##"]
    )
    
    return response.choices[0].text.strip()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: codex-cleanup.py <file_path> <context_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    context_file = sys.argv[2]
    
    with open(context_file, 'r') as f:
        context = f.read()
    
    cleaned_code = cleanup_with_codex(file_path, context)
    print(cleaned_code)
EOF

chmod +x .cleanup-toolkit/scripts/codex-cleanup.py
```

### 4. Test Integration
```bash
# Create a messy file
echo "print('debug'); def test(): return True" > test.py

# Commit to trigger cleanup
git add test.py
git commit -m "test: codex integration"

# Use generated Codex prompts for cleanup
```

## 🤖 Codex Integration Methods

### Method 1: Direct API Integration

#### Automated Cleanup Script
```python
#!/usr/bin/env python3
"""
Automated code cleanup using OpenAI Codex
"""
import openai
import argparse
import json

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

def main():
    parser = argparse.ArgumentParser(description="Clean up code using Codex")
    parser.add_argument("file", help="File to clean up")
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--model", default="code-davinci-002", help="Codex model")
    parser.add_argument("--output", help="Output file (default: overwrite input)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key required")
        return 1
    
    with open(args.file, 'r') as f:
        code = f.read()
    
    cleanup = CodexCleanup(api_key, args.model)
    
    # Analyze code
    print("Analyzing code...")
    analysis = cleanup.analyze_code(code)
    print(f"Analysis: {analysis}")
    
    # Clean up code
    print("Cleaning up code...")
    cleaned_code = cleanup.cleanup_code(code, analysis)
    
    # Write output
    output_file = args.output or args.file
    with open(output_file, 'w') as f:
        f.write(cleaned_code)
    
    print(f"Cleaned code written to {output_file}")

if __name__ == "__main__":
    main()
```

### Method 2: Interactive Codex Prompts

#### Analysis Prompt Template
```
# Code Analysis for Cleanup

Analyze this code for systematic cleanup opportunities:

```{language}
{code}
```

Identify and categorize issues:

## 1. Bloat to Remove
- Debug statements (print, console.log, etc.)
- Unused imports and variables
- Dead code and commented sections
- Temporary test code

## 2. Logic to Consolidate
- Duplicate functions with similar purposes
- Repeated validation patterns
- Similar error handling code
- Redundant utility functions

## 3. Documentation Gaps
- Functions missing docstrings/comments
- Complex logic without explanation
- Missing type hints or JSDoc
- Unclear variable names

## 4. Quality Issues
- Generic exception handling
- Magic numbers and strings
- Functions longer than 50 lines
- Deep nesting levels

Analysis:
```

#### Cleanup Execution Prompt
```
# Systematic Code Cleanup

Clean up this code following proven principles:

## Original Code
```{language}
{code}
```

## Issues Identified
{analysis}

## Cleanup Requirements
1. **Remove Bloat**: Eliminate debug statements, unused code, and dead sections
2. **Consolidate Logic**: Merge duplicate functions and extract common patterns
3. **Document Clearly**: Add comprehensive docstrings and meaningful comments
4. **Improve Quality**: Better error handling, type hints, and validation

## Cleaned Code
```{language}
```

#### Documentation Generation Prompt
```
# Comprehensive Documentation Generation

Generate clear, comprehensive documentation for this code:

```{language}
{code}
```

Requirements:
- Clear function/class descriptions
- Parameter types and descriptions
- Return value documentation
- Exception handling notes
- Usage examples where helpful
- Consistent documentation style

Documentation:
```

### Method 3: VS Code Codex Extension Integration

#### VS Code Settings Configuration
```json
{
  "codex.cleanup": {
    "enabled": true,
    "auto_trigger": false,
    "model": "code-davinci-002",
    "temperature": 0.1,
    "max_tokens": 2048
  },
  "codex.prompts": {
    "cleanup_analysis": "Analyze this code for cleanup opportunities following systematic principles...",
    "cleanup_execution": "Clean up this code by removing bloat, consolidating logic, and improving documentation...",
    "documentation": "Generate comprehensive documentation for this code..."
  }
}
```

#### Custom VS Code Commands
```json
{
  "commands": [
    {
      "command": "codex.analyzeForCleanup",
      "title": "Analyze Code for Cleanup",
      "category": "Codex Cleanup"
    },
    {
      "command": "codex.executeCleanup", 
      "title": "Execute Systematic Cleanup",
      "category": "Codex Cleanup"
    },
    {
      "command": "codex.generateDocumentation",
      "title": "Generate Documentation",
      "category": "Codex Cleanup"
    }
  ]
}
```

## 📋 Codex Cleanup Workflows

### 1. Pre-commit Cleanup Workflow

```bash
#!/bin/bash
# .cleanup-toolkit/scripts/codex-precommit.sh

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

for file in $STAGED_FILES; do
    if [[ $file =~ \.(py|js|ts|java|go|rs)$ ]]; then
        echo "Analyzing $file with Codex..."
        
        # Generate cleanup context
        python3 .cleanup-toolkit/scripts/codex-cleanup.py "$file" \
            .cleanup-toolkit/cleanup-context.md > "$file.cleaned"
        
        # Show diff for review
        echo "Proposed changes for $file:"
        diff "$file" "$file.cleaned" || true
        
        # Ask for confirmation
        read -p "Apply changes to $file? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            mv "$file.cleaned" "$file"
            git add "$file"
        else
            rm "$file.cleaned"
        fi
    fi
done
```

### 2. Interactive Cleanup Session

```python
#!/usr/bin/env python3
"""
Interactive Codex cleanup session
"""
import openai
import os
from pathlib import Path

class InteractiveCleanup:
    def __init__(self):
        self.codex = CodexCleanup(os.getenv("OPENAI_API_KEY"))
        self.session_log = []
    
    def start_session(self, files):
        """Start interactive cleanup session."""
        print("🧹 Starting systematic cleanup session...")
        print(f"Files to process: {len(files)}")
        
        for file_path in files:
            self.process_file(file_path)
        
        self.generate_session_report()
    
    def process_file(self, file_path):
        """Process a single file interactively."""
        print(f"\n📁 Processing: {file_path}")
        
        with open(file_path, 'r') as f:
            original_code = f.read()
        
        # Step 1: Analysis
        print("🔍 Analyzing code...")
        analysis = self.codex.analyze_code(original_code)
        print(f"Analysis:\n{analysis}")
        
        proceed = input("\nProceed with cleanup? (y/N): ")
        if not proceed.lower().startswith('y'):
            return
        
        # Step 2: Cleanup
        print("🛠️ Generating cleaned code...")
        cleaned_code = self.codex.cleanup_code(original_code, analysis)
        
        # Step 3: Review
        print("\n📊 Cleanup Summary:")
        self.show_diff_summary(original_code, cleaned_code)
        
        apply = input("\nApply changes? (y/N): ")
        if apply.lower().startswith('y'):
            with open(file_path, 'w') as f:
                f.write(cleaned_code)
            print(f"✅ Applied changes to {file_path}")
            
            self.session_log.append({
                'file': file_path,
                'status': 'cleaned',
                'analysis': analysis
            })
        else:
            print(f"⏭️ Skipped {file_path}")
            self.session_log.append({
                'file': file_path,
                'status': 'skipped'
            })
    
    def show_diff_summary(self, original, cleaned):
        """Show summary of changes."""
        orig_lines = len(original.splitlines())
        clean_lines = len(cleaned.splitlines())
        
        print(f"Lines: {orig_lines} → {clean_lines} ({clean_lines - orig_lines:+d})")
        
        # Count improvements
        debug_removed = original.count('print(') - cleaned.count('print(')
        debug_removed += original.count('console.log') - cleaned.count('console.log')
        
        if debug_removed > 0:
            print(f"Debug statements removed: {debug_removed}")
    
    def generate_session_report(self):
        """Generate cleanup session report."""
        cleaned_files = [log for log in self.session_log if log['status'] == 'cleaned']
        skipped_files = [log for log in self.session_log if log['status'] == 'skipped']
        
        print(f"\n📋 Session Complete!")
        print(f"Files cleaned: {len(cleaned_files)}")
        print(f"Files skipped: {len(skipped_files)}")
        
        # Save detailed report
        report_path = ".cleanup-toolkit/reports/codex-session.md"
        with open(report_path, 'w') as f:
            f.write("# Codex Cleanup Session Report\n\n")
            f.write(f"Files processed: {len(self.session_log)}\n")
            f.write(f"Files cleaned: {len(cleaned_files)}\n\n")
            
            for log in cleaned_files:
                f.write(f"## {log['file']}\n")
                f.write(f"Status: {log['status']}\n")
                f.write(f"Analysis: {log['analysis']}\n\n")
        
        print(f"Detailed report saved: {report_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: interactive-cleanup.py <file1> [file2] ...")
        sys.exit(1)
    
    cleanup = InteractiveCleanup()
    cleanup.start_session(sys.argv[1:])
```

### 3. Batch Processing Workflow

```bash
#!/bin/bash
# .cleanup-toolkit/scripts/codex-batch.sh

echo "🔄 Starting batch cleanup with Codex..."

# Find all code files
find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" \
    | grep -v node_modules \
    | grep -v .git \
    | while read file; do
    
    echo "Processing: $file"
    
    # Skip if file is too large
    if [ $(wc -l < "$file") -gt 500 ]; then
        echo "⏭️ Skipping large file: $file"
        continue
    fi
    
    # Create backup
    cp "$file" "$file.backup"
    
    # Process with Codex
    python3 .cleanup-toolkit/scripts/codex-cleanup.py "$file" \
        .cleanup-toolkit/cleanup-context.md > "$file.tmp"
    
    # Check if cleanup was successful
    if [ $? -eq 0 ] && [ -s "$file.tmp" ]; then
        mv "$file.tmp" "$file"
        echo "✅ Cleaned: $file"
    else
        echo "❌ Failed: $file"
        mv "$file.backup" "$file"
        rm -f "$file.tmp"
    fi
    
    rm -f "$file.backup"
done

echo "🎉 Batch cleanup complete!"
```

## 🎨 Language-Specific Codex Integration

### Python Cleanup with Codex
```python
# Example Codex prompt for Python cleanup
prompt = """
Clean up this Python code following best practices:

```python
import os, sys, json, requests
def process_user(name, email):
    print(f"Processing: {name}")
    if email:
        return True
    return False
```

Apply these improvements:
1. Remove debug statements
2. Add type hints
3. Add comprehensive docstring
4. Improve error handling
5. Follow PEP 8

Cleaned Python code:
```python
"""

# Codex generates:
"""
from typing import Optional

def process_user(name: str, email: str) -> bool:
    \"\"\"
    Process and validate user information.
    
    Args:
        name: User's full name
        email: User's email address
        
    Returns:
        bool: True if user is valid and processed successfully
        
    Raises:
        ValueError: If name is empty or email is invalid
    \"\"\"
    if not name.strip():
        raise ValueError("Name cannot be empty")
    
    if not email or '@' not in email:
        raise ValueError("Invalid email address")
    
    return True
```
"""
```

### JavaScript Cleanup with Codex
```javascript
// Example Codex prompt for JavaScript cleanup
const prompt = `
Clean up this JavaScript code following modern best practices:

\`\`\`javascript
function validateUser(name, email) {
    console.log(\`Validating: \${name}\`);
    if (email) return true;
    return false;
}
\`\`\`

Apply these improvements:
1. Remove debug statements
2. Add JSDoc documentation
3. Improve error handling
4. Use modern syntax
5. Add validation logic

Cleaned JavaScript code:
\`\`\`javascript
`;

// Codex generates:
/**
 * Validate user registration data.
 * 
 * @param {string} name - User's full name
 * @param {string} email - User's email address
 * @returns {boolean} True if user data is valid
 * @throws {Error} If user data is invalid
 */
function validateUser(name, email) {
    if (!name?.trim()) {
        throw new Error("Name is required and cannot be empty");
    }
    
    if (!email?.includes("@")) {
        throw new Error("Valid email address is required");
    }
    
    return true;
}
```

## 🔧 Advanced Codex Configuration

### Custom Model Fine-tuning
```python
# Fine-tune Codex for your project's patterns
training_data = [
    {
        "prompt": "Clean up this code following our project standards...",
        "completion": "// Cleaned code with project-specific patterns"
    }
    # Add more examples
]

# Use OpenAI's fine-tuning API
openai.FineTune.create(
    training_file="your-training-data.jsonl",
    model="code-davinci-002",
    suffix="cleanup-specialist"
)
```

### Context-Aware Prompts
```python
def generate_context_prompt(file_path, project_context):
    """Generate context-aware cleanup prompt."""
    
    # Read project patterns
    with open(".cleanup-toolkit/project-patterns.md", 'r') as f:
        patterns = f.read()
    
    # Read coding standards
    with open(".cleanup-toolkit/coding-standards.md", 'r') as f:
        standards = f.read()
    
    prompt = f"""
# Project Context
{project_context}

# Coding Standards
{standards}

# Common Patterns
{patterns}

# File to Clean: {file_path}
Apply systematic cleanup following our project standards...
"""
    
    return prompt
```

## 🔍 Troubleshooting Codex Integration

### Common Issues

**API Rate Limits:**
```python
import time
from openai.error import RateLimitError

def cleanup_with_retry(code, max_retries=3):
    for attempt in range(max_retries):
        try:
            return openai.Completion.create(...)
        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limited, waiting {wait_time}s...")
            time.sleep(wait_time)
    
    raise Exception("Max retries exceeded")
```

**Token Limits:**
```python
def chunk_large_files(code, max_tokens=4000):
    """Split large files into manageable chunks."""
    lines = code.splitlines()
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for line in lines:
        line_tokens = len(line.split())
        if current_tokens + line_tokens > max_tokens:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_tokens = line_tokens
        else:
            current_chunk.append(line)
            current_tokens += line_tokens
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks
```

**Quality Control:**
```python
def validate_codex_output(original, cleaned):
    """Validate that Codex output is reasonable."""
    
    # Check if output is too different
    if len(cleaned) < len(original) * 0.5:
        return False, "Output too short"
    
    # Check for syntax errors
    try:
        compile(cleaned, '<string>', 'exec')
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    
    # Check for preserved functionality
    # (Add more sophisticated checks as needed)
    
    return True, "Output validated"
```

## 💡 Pro Tips for Codex Integration

### Optimize Prompts
1. **Be specific** about cleanup requirements
2. **Provide context** about your project patterns
3. **Use examples** in prompts for better results
4. **Iterate and refine** prompts based on output quality

### Manage Costs
1. **Use appropriate models** (code-davinci-002 vs code-cushman-001)
2. **Optimize token usage** with efficient prompts
3. **Cache results** for similar code patterns
4. **Batch process** multiple files efficiently

### Quality Assurance
1. **Always review** Codex output before applying
2. **Test functionality** after cleanup
3. **Use version control** to track changes
4. **Validate syntax** and logic automatically

## 📖 Additional Resources

- [OpenAI Codex Documentation](https://platform.openai.com/docs/guides/code)
- [Cleanup Toolkit Repository](https://github.com/your-username/cleanup-toolkit)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Codex Best Practices](https://platform.openai.com/docs/guides/code/best-practices)

---

*Leverage OpenAI Codex's powerful code understanding for systematic, intelligent cleanup. Transform messy code into clean, well-documented, maintainable software! 🤖✨*