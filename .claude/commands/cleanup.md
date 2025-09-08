# /cleanup - Agentic Code Cleanup Command

## Description
Systematically analyze and clean up code in the current project by removing bloat, consolidating logic, and improving documentation clarity.

## Usage
```
/cleanup [options] [files...]
```

## Options
- `--all` - Analyze all files in the project
- `--staged` - Analyze only git staged files
- `--modified` - Analyze only modified files
- `--debug` - Remove debug statements (print, console.log, etc.)
- `--todos` - Remove or address TODO/FIXME comments
- `--duplicates` - Find and consolidate duplicate code
- `--unused` - Remove unused imports and variables
- `--docs` - Improve documentation and comments
- `--test` - Run in test mode (preview what would be changed)
- `--language <lang>` - Specify language (python, javascript, go, etc.)

## Examples

### Basic cleanup of staged files
```
/cleanup --staged
```

### Remove all debug statements from Python files
```
/cleanup --debug --language python *.py
```

### Full cleanup of all project files
```
/cleanup --all --debug --todos --duplicates --unused --docs
```

### Test mode to preview what would be changed
```
/cleanup --test --all
```

## Workflow

When you invoke `/cleanup`, I will:

1. **🔍 Analysis Phase**
   - Scan specified files for cleanup opportunities
   - Identify debug statements, TODOs, duplicate code
   - Check for unused imports and variables
   - Evaluate documentation quality

2. **📊 Report Generation**
   - Create a summary of issues found
   - Prioritize cleanup tasks by impact
   - Estimate time and complexity

3. **🧹 Cleanup Execution**
   - Remove debug statements and console outputs
   - Consolidate duplicate functions and logic
   - Remove unused imports and dead code
   - Improve or add missing documentation
   - Format code according to language standards

4. **✅ Verification**
   - Ensure functionality is preserved
   - Run basic syntax checks
   - Generate cleanup report

## Cleanup Rules

### Debug Statement Patterns
- **Python**: `print()`, `pprint()`, `breakpoint()`, `import pdb`
- **JavaScript**: `console.log()`, `console.debug()`, `debugger`
- **Go**: `fmt.Print()`, `log.Print()`, `fmt.Printf()`
- **Java**: `System.out.print()`, `System.err.print()`

### Documentation Standards
- Functions should have clear docstrings/comments
- Complex logic should be explained
- TODOs should be actionable or removed
- Remove commented-out code blocks

### Code Quality
- No duplicate function definitions
- No unused imports or variables
- Consistent naming conventions
- Proper error handling

## Integration with Cleanup Toolkit

This command integrates with the Agentic Cleanup Toolkit:

1. **Pre-commit Hook Integration**
   ```bash
   # Automatically triggers on git commit
   git commit -m "feat: add new feature"
   # Pre-commit hook will analyze and prompt for cleanup
   ```

2. **Manual Cleanup Script**
   ```bash
   # Run the cleanup assistant directly
   bash scripts/code_cleanup_gist.sh
   ```

3. **Configuration**
   ```yaml
   # .cleanup-toolkit/config.yml
   cleanup_enabled: true
   preferred_framework: claude-code
   auto_generate_prompts: true
   ```

## Advanced Features

### Custom Patterns
Define custom cleanup patterns in `.cleanup-toolkit/patterns.yml`:
```yaml
patterns:
  debug:
    - "TEMPORARY"
    - "HACK"
    - "XXX"
  sensitive:
    - "password.*=.*['\"]"
    - "api_key.*=.*['\"]"
```

### Exclusions
Specify files or patterns to exclude in `.cleanup-toolkit/.cleanupignore`:
```
tests/
*.min.js
*_test.go
vendor/
node_modules/
```

### Preview Mode
Always preview changes before applying them to verify functionality will be preserved.

### Language-Specific Rules
Configure language-specific rules in `.cleanup-toolkit/languages.yml`:
```yaml
python:
  max_line_length: 88
  use_black: true
  docstring_style: google
javascript:
  use_prettier: true
  semicolons: false
```

## Best Practices

1. **Start with Test Mode**: Always run with `--test` first to review changes
2. **Incremental Cleanup**: Focus on one type of cleanup at a time
3. **Preserve Functionality**: Ensure tests pass after cleanup
4. **Document Changes**: Keep track of what was cleaned up
5. **Regular Maintenance**: Run cleanup regularly, not just before commits

## Error Handling

If cleanup fails or encounters issues:
1. Check the error message for specific file/line
2. Review `.cleanup-toolkit/cleanup.log` for details
3. Use `--debug` flag for verbose output
4. Skip problematic files with exclusions

## Output Format

The cleanup command provides structured output:

```
🧹 Code Cleanup Analysis
========================
📁 Files analyzed: 15
🐛 Debug statements found: 23
📝 TODOs/FIXMEs: 8
🔄 Duplicate functions: 3
📦 Unused imports: 12

✨ Cleanup Complete!
- Removed 23 debug statements
- Consolidated 3 duplicate functions
- Removed 12 unused imports
- Improved documentation in 5 files

💾 Files modified: 10
⏱️ Time saved: ~2 hours of manual cleanup
```

## Tips

- Use `/cleanup --staged` before every commit for consistent code quality
- Combine with `/test` command to ensure cleanup doesn't break functionality
- Create project-specific cleanup rules in `.cleanup-toolkit/`
- Use `--language` flag for better language-specific analysis
- Review cleanup suggestions before applying them

## Related Commands

- `/analyze` - Analyze code quality without making changes
- `/format` - Format code according to style guides
- `/lint` - Run linters and static analysis
- `/test` - Run tests to verify functionality
- `/commit` - Smart commit with automatic cleanup

---

*This command is part of the Agentic Cleanup Toolkit - AI-powered code cleanup for development workflows*