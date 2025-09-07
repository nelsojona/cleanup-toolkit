# Claude Code Agentic Prompts for Code Cleanup

These prompts are designed to work with Claude Code's project context system to implement systematic cleanup workflows.

## Project Setup Prompts

### Initial Project Context
```
Please read and understand my project context from these files:
- claude.md (project overview and standards)
- handover.md (current tasks and progress)
- cleanup-rules.md (detailed cleanup standards)

I'm implementing systematic code cleanup: After completing a development goal, clean up the code, remove bloat, and document clearly.
```

### Pre-commit Cleanup Trigger
```
I just completed a development goal and my pre-commit hook has triggered the cleanup process.

Please read:
1. .cleanup-toolkit/cleanup-context.md (files modified and issues detected)
2. .cleanup-toolkit/cleanup-summary.md (current commit details)
3. handover.md (updated with cleanup tasks)

Based on this context, create a systematic cleanup plan for the modified files.
```

## Analysis Phase Prompts

### Comprehensive File Analysis
```
Please analyze each file listed in the cleanup context for:

1. **Bloat Detection**:
   - Debug statements (print, console.log, etc.)
   - Unused imports and variables
   - Dead code and commented-out sections
   - Temporary variables and test code

2. **Logic Consolidation**:
   - Duplicate functions with similar names
   - Repeated code patterns
   - Similar validation logic
   - Redundant error handling

3. **Documentation Gaps**:
   - Missing docstrings/comments
   - Unclear variable names
   - Complex logic without explanation
   - Missing type hints

4. **Quality Issues**:
   - Generic exception handling
   - Magic numbers and strings
   - Long functions (>50 lines)
   - Deep nesting levels

Provide a detailed analysis report with specific line numbers and recommendations.
```

### Pattern Recognition
```
Based on our project standards in cleanup-rules.md, identify patterns in the modified files that need attention:

1. Scan for our defined anti-patterns
2. Look for violations of our coding standards
3. Find opportunities to apply our established patterns
4. Suggest consolidation opportunities

Focus on maintaining consistency with the existing codebase while applying cleanup best practices.
```

## Cleanup Execution Prompts

### Systematic Cleanup Implementation
```
Now implement the cleanup plan systematically. For each file:

1. **Remove Bloat**:
   - Comment out or remove debug statements
   - Remove unused imports (verify they're truly unused)
   - Delete dead code and old commented sections
   - Clean up temporary variables

2. **Consolidate Logic**:
   - Merge duplicate functions into a single, well-named function
   - Extract common patterns into reusable utilities
   - Simplify complex conditional logic
   - Reduce code duplication

3. **Improve Documentation**:
   - Add comprehensive docstrings following our project style
   - Add inline comments for complex logic
   - Improve variable and function names for clarity
   - Add type hints where missing

4. **Enhance Quality**:
   - Replace generic exceptions with specific ones
   - Add proper error messages
   - Break down large functions
   - Improve code organization

Show me the before and after for each significant change, and explain your reasoning.
```

### Language-Specific Cleanup
```
Apply language-specific cleanup following our project standards:

**For Python files**:
- Follow PEP 8 conventions
- Add type hints using typing module
- Use proper exception hierarchy
- Add comprehensive docstrings with Args/Returns/Raises

**For JavaScript/TypeScript files**:
- Follow our ESLint configuration
- Add JSDoc comments for functions
- Use proper error handling with try/catch
- Implement proper async/await patterns

**For [Other Languages]**:
- Follow language-specific conventions from cleanup-rules.md
- Apply appropriate documentation standards
- Use language-specific best practices

Ensure all changes preserve existing functionality while improving code quality.
```

## Verification Phase Prompts

### Functionality Verification
```
Please verify that the cleanup changes preserve all functionality:

1. **Logic Preservation**:
   - Confirm all original logic paths are maintained
   - Verify edge cases are still handled
   - Check that error conditions are properly managed
   - Ensure no behavioral changes were introduced

2. **Interface Consistency**:
   - Verify function signatures remain compatible
   - Check that return values are unchanged
   - Confirm public APIs are preserved
   - Validate that imports/exports still work

3. **Test Compatibility**:
   - Review if existing tests will still pass
   - Identify any tests that might need updates
   - Suggest additional tests for new error handling

Provide a verification report with confidence level for each file.
```

### Quality Assessment
```
Assess the quality improvement achieved by the cleanup:

1. **Metrics Comparison**:
   - Lines of code before/after
   - Cyclomatic complexity reduction
   - Documentation coverage improvement
   - Code duplication elimination

2. **Maintainability Improvements**:
   - Clearer function purposes
   - Better error handling
   - Improved readability
   - Enhanced debuggability

3. **Standards Compliance**:
   - Adherence to project coding standards
   - Consistency with existing codebase
   - Following language best practices

Generate a cleanup summary following cleanup standards.
```

## Documentation Update Prompts

### Handover Update
```
Update handover.md with the cleanup progress:

1. Mark completed cleanup tasks as done
2. Add summary of changes made to each file
3. Note any issues discovered during cleanup
4. List any follow-up tasks or recommendations
5. Update the current status for the next development session

Follow our handover.md format and include specific details about the cleanup work completed.
```

### Cleanup Report Generation
```
Generate a comprehensive cleanup report that includes:

1. **Executive Summary**:
   - Files processed and changes made
   - Key improvements achieved
   - Time invested in cleanup

2. **Detailed Changes**:
   - File-by-file breakdown of modifications
   - Before/after code snippets for major changes
   - Rationale for each significant change

3. **Quality Metrics**:
   - Code quality improvements
   - Documentation coverage increase
   - Complexity reduction achieved

4. **Recommendations**:
   - Suggestions for future development
   - Patterns to avoid going forward
   - Process improvements for the team

Save this report as .cleanup-toolkit/reports/cleanup-report-[timestamp].md
```

## Integration Prompts

### Git Integration
```
Help me complete the git workflow after cleanup:

1. Review the changes made during cleanup
2. Suggest appropriate commit message following our conventions
3. Identify if any additional files should be staged
4. Recommend if this should be a separate cleanup commit or combined with the original changes

Provide the exact git commands to execute.
```

### Team Communication
```
Based on the cleanup work completed, help me communicate the changes to the team:

1. Draft a summary for the pull request description
2. Highlight any breaking changes or important modifications
3. Suggest reviewers based on the files modified
4. Recommend any additional testing or validation needed

Format this for our team's communication standards.
```

## Best Practices

### Prompt Chaining
Use these prompts in sequence for best results:
1. Start with project context setup
2. Use analysis prompts to understand the scope
3. Apply cleanup execution prompts systematically
4. Verify with quality assessment prompts
5. Complete with documentation updates

### Context Maintenance
- Always reference the project files (claude.md, handover.md, cleanup-rules.md)
- Keep the cleanup context in mind throughout the conversation
- Maintain consistency with previous cleanup decisions
- Update handover.md as you progress

### Quality Assurance
- Ask for verification at each major step
- Request before/after comparisons for significant changes
- Confirm that functionality is preserved
- Validate that the cleanup meets quality standards

---

*These prompts are designed to work with Claude Code's project context system to provide systematic, AI-guided code cleanup following best practices.*

