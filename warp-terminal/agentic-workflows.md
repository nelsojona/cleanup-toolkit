# Warp Terminal Agentic Workflows for Code Cleanup

These workflows integrate with Warp Terminal's AI features to implement systematic cleanup processes using AI prompts and automation.

## Warp AI Integration (Cmd+G / Ctrl+G)

### Pre-commit Cleanup Workflow

#### 1. Context Loading Prompt
```
I just completed a development goal and my pre-commit hook triggered the cleanup process: "Please clean up the code you worked on, remove any bloat you added, and document it very clearly."

My project context:
- Project: [project name from git root]
- Branch: [current branch]
- Modified files: [list from git diff --cached --name-only]

Please help me systematically analyze these files for cleanup opportunities following cleanup best practices.
```

#### 2. Analysis Prompt
```
Based on my project context and the files I just modified, help me identify:

1. **Bloat to Remove**:
   - Debug statements (print, console.log, System.out, etc.)
   - Unused imports and variables
   - Dead code and commented sections
   - Temporary test code

2. **Logic to Consolidate**:
   - Duplicate functions with similar purposes
   - Repeated validation patterns
   - Similar error handling code
   - Redundant utility functions

3. **Documentation Gaps**:
   - Functions missing docstrings/comments
   - Complex logic without explanation
   - Missing type hints or JSDoc
   - Unclear variable names

4. **Quality Issues**:
   - Generic exception handling
   - Magic numbers and strings
   - Functions longer than 50 lines
   - Deep nesting levels

Analyze each file and provide specific recommendations with line numbers.
```

#### 3. Cleanup Execution Prompt
```
Now help me execute the cleanup systematically. For each file, guide me through:

1. **Removing Bloat**:
   - Show me which debug statements to remove/comment
   - Identify unused imports to delete
   - Point out dead code to eliminate

2. **Consolidating Logic**:
   - Suggest how to merge duplicate functions
   - Recommend extracting common patterns
   - Show how to simplify complex conditions

3. **Improving Documentation**:
   - Provide docstring templates for functions
   - Suggest inline comments for complex logic
   - Recommend better variable names

4. **Enhancing Quality**:
   - Show specific exception types to use
   - Suggest breaking down large functions
   - Recommend error message improvements

Give me the exact changes to make while preserving all functionality.
```

#### 4. Verification Prompt
```
Help me verify the cleanup is complete and follows cleanup standards:

1. **Functionality Check**:
   - Confirm all original logic is preserved
   - Verify edge cases are still handled
   - Check that APIs remain compatible

2. **Quality Assessment**:
   - Measure improvement in code clarity
   - Assess documentation completeness
   - Evaluate error handling robustness

3. **Standards Compliance**:
   - Verify adherence to project conventions
   - Check consistency with existing code
   - Confirm best practices are followed

Generate a summary of the cleanup work completed and any remaining recommendations.
```

## Warp Workflows (YAML)

### Cleanup Analysis Workflow
```yaml
name: "🔍 Code Cleanup Analysis"
command: |
  echo "🔍 Analyzing code for cleanup opportunities..."
  echo "============================================="
  echo ""
  
  # Load cleanup context if available
  if [ -f ".cleanup-toolkit/cleanup-context.md" ]; then
    echo "📋 Cleanup Context:"
    head -20 .cleanup-toolkit/cleanup-context.md
    echo ""
  fi
  
  # Show modified files
  echo "📁 Files modified in this commit:"
  git diff --cached --name-only | head -10
  echo ""
  
  # Quick analysis
  echo "🐛 Debug statements found:"
  git diff --cached --name-only | xargs grep -n "print(\|console\.log\|System\.out" 2>/dev/null | wc -l | xargs echo "Count:"
  
  echo "📝 TODO/FIXME comments:"
  git diff --cached --name-only | xargs grep -n "TODO\|FIXME\|XXX\|HACK" 2>/dev/null | wc -l | xargs echo "Count:"
  
  echo "🔄 Potential duplicate functions:"
  git diff --cached --name-only | xargs grep -n "^def \|^function \|^class " 2>/dev/null | cut -d: -f3 | sort | uniq -d | head -5
  echo ""
  
  echo "💡 Next: Use Cmd+G with Warp AI for detailed cleanup guidance"
  echo "📖 Prompts available in: .cleanup-toolkit/warp-ai-prompts.txt"
description: "Analyze staged files for cleanup opportunities"
tags: ["cleanup", "analysis"]
```

### Cleanup Execution Workflow
```yaml
name: "🧹 Execute Code Cleanup"
command: |
  echo "🧹 Executing systematic code cleanup..."
  echo "============================================="
  echo ""
  
  # Check if analysis was done
  if [ ! -f ".cleanup-toolkit/cleanup-context.md" ]; then
    echo "⚠️  Run cleanup analysis first"
    exit 1
  fi
  
  echo "📋 Following cleanup principles:"
  echo "1. Remove bloat (debug statements, unused code)"
  echo "2. Consolidate duplicate logic"
  echo "3. Document clearly with comprehensive comments"
  echo ""
  
  # Show files to process
  echo "📁 Files to clean:"
  git diff --cached --name-only | sed 's/^/  - /'
  echo ""
  
  echo "🤖 Use Warp AI (Cmd+G) with these prompts:"
  echo "  1. Analysis prompt for detailed review"
  echo "  2. Execution prompt for step-by-step cleanup"
  echo "  3. Verification prompt to confirm quality"
  echo ""
  
  echo "📖 Full prompts: .cleanup-toolkit/warp-ai-prompts.txt"
  echo "📊 Context: .cleanup-toolkit/cleanup-context.md"
  echo ""
  
  echo "✅ After cleanup, run: cleanup-verify"
description: "Execute systematic cleanup following best practices"
tags: ["cleanup", "execution"]
```

### Cleanup Verification Workflow
```yaml
name: "✅ Verify Code Cleanup"
command: |
  echo "✅ Verifying cleanup completion..."
  echo "============================================="
  echo ""
  
  # Check remaining issues
  echo "🔍 Checking for remaining issues:"
  
  echo "Debug statements:"
  remaining_debug=$(git diff --cached --name-only | xargs grep -n "print(\|console\.log\|System\.out" 2>/dev/null | wc -l)
  echo "  Count: $remaining_debug"
  
  echo "TODO/FIXME comments:"
  remaining_todos=$(git diff --cached --name-only | xargs grep -n "TODO\|FIXME\|XXX\|HACK" 2>/dev/null | wc -l)
  echo "  Count: $remaining_todos"
  
  echo ""
  
  # Quality check
  echo "📊 Quality assessment:"
  echo "Files processed: $(git diff --cached --name-only | wc -l)"
  echo "Lines changed: $(git diff --cached --numstat | awk '{sum+=$1+$2} END {print sum+0}')"
  echo ""
  
  # Generate completion report
  echo "📝 Generating cleanup report..."
  cat > .cleanup-toolkit/cleanup-completion.md << EOF
# Cleanup Completion Report
Generated: $(date)

## Summary
- Files processed: $(git diff --cached --name-only | wc -l)
- Debug statements remaining: $remaining_debug
- TODO comments remaining: $remaining_todos

## Files Cleaned
$(git diff --cached --name-only | sed 's/^/- /')

## Next Steps
- Review changes: git diff --cached
- Complete commit: git commit --no-verify
- Or continue cleanup if issues remain

---
*Cleanup completed following best practices*
EOF
  
  echo "✅ Report saved: .cleanup-toolkit/cleanup-completion.md"
  echo ""
  
  if [ "$remaining_debug" -eq 0 ] && [ "$remaining_todos" -eq 0 ]; then
    echo "🎉 Cleanup appears complete!"
    echo "💡 Review changes and complete your commit"
  else
    echo "⚠️  Some issues remain - consider additional cleanup"
  fi
description: "Verify cleanup completion and generate report"
tags: ["cleanup", "verification"]
```

## Warp AI Context File

### Project-Specific AI Context
```markdown
# Warp AI Context: Code Cleanup

## Project Overview
This project implements systematic code cleanup following the principle:
"After successfully completing your goal, clean up the code you worked on, remove any bloat you added, and document it very clearly."

## Cleanup Standards
- **Remove Bloat**: Debug statements, unused imports, dead code
- **Consolidate Logic**: Duplicate functions, repeated patterns
- **Document Clearly**: Comprehensive docstrings, inline comments
- **Improve Quality**: Error handling, type hints, validation

## Common Patterns to Address
- Debug prints: `print()`, `console.log()`, `System.out.println()`
- TODO comments: `TODO`, `FIXME`, `XXX`, `HACK`
- Duplicate functions: Similar names like `validate_email` and `validate_email_format`
- Missing documentation: Functions without docstrings
- Generic exceptions: `except:` without specific exception types

## Workflow Integration
1. Pre-commit hook triggers cleanup process
2. Use Warp AI (Cmd+G) for analysis and guidance
3. Apply systematic cleanup following prompts
4. Verify completion with quality checks
5. Complete commit with clean code

## Available Commands
- `cleanup-analysis` - Analyze files for cleanup opportunities
- `cleanup-execute` - Execute systematic cleanup process
- `cleanup-verify` - Verify cleanup completion
- `startup` - Load project context and status

## AI Prompt Templates
Use these with Cmd+G for consistent cleanup guidance:
- Analysis: Identify issues and opportunities
- Execution: Step-by-step cleanup instructions
- Verification: Confirm quality and completeness
```

## Shell Integration

### Warp-Specific Aliases
```bash
# Cleanup Aliases for Warp Terminal
alias code-cleanup='echo "🧹 Code Cleanup Process" && cleanup-analysis'
alias cleanup-ai='echo "🤖 Use Cmd+G with prompts from .cleanup-toolkit/warp-ai-prompts.txt"'
alias cleanup-status='cat .cleanup-toolkit/cleanup-context.md 2>/dev/null || echo "No cleanup context found"'
alias cleanup-help='echo "Cleanup Commands:" && echo "  code-cleanup    - Start cleanup process" && echo "  cleanup-ai      - Show AI prompt instructions" && echo "  cleanup-status  - Show current cleanup context" && echo "  cleanup-verify  - Verify cleanup completion"'

# Quick access to cleanup files
alias show-context='bat .cleanup-toolkit/cleanup-context.md 2>/dev/null || cat .cleanup-toolkit/cleanup-context.md 2>/dev/null'
alias show-prompts='bat .cleanup-toolkit/warp-ai-prompts.txt 2>/dev/null || cat .cleanup-toolkit/warp-ai-prompts.txt 2>/dev/null'
```

## Best Practices

### Effective AI Prompting in Warp
1. **Be Specific**: Include file names and line numbers in prompts
2. **Provide Context**: Reference project standards and previous decisions
3. **Chain Prompts**: Use analysis → execution → verification sequence
4. **Verify Results**: Always confirm AI suggestions before applying

### Workflow Optimization
1. **Start with Analysis**: Use `cleanup-analysis` workflow first
2. **Use AI Guidance**: Leverage Cmd+G for detailed instructions
3. **Apply Systematically**: Process files one by one
4. **Verify Completion**: Use `cleanup-verify` workflow to confirm

### Integration Tips
- Keep Warp AI context file updated with project-specific patterns
- Use workflows to automate repetitive analysis tasks
- Combine AI prompts with shell commands for efficiency
- Save successful prompt patterns for reuse

---

*These workflows integrate Warp Terminal's AI capabilities with systematic cleanup principles for efficient, AI-guided code improvement.*

