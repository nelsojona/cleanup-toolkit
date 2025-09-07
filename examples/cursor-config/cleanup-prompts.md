# Cursor Cleanup Prompts

## Initial Analysis (Cmd+L)

### Comprehensive Cleanup Analysis
```
I just completed a development goal and my pre-commit hook triggered a cleanup process. 

Please analyze these files for cleanup opportunities:
[paste file list from .cleanup-toolkit/cleanup-context.md]

Focus on:
- Debug statements and dead code
- Duplicate functions and logic
- Missing documentation
- Error handling improvements

Provide a systematic cleanup plan.
```

### Systematic Cleanup Execution
```
Now help me execute cleanup systematically. For each file:

1. **Remove Bloat**: Debug statements, unused imports, dead code
2. **Consolidate Logic**: Merge duplicate functions, extract common patterns
3. **Document Clearly**: Add comprehensive docstrings and comments
4. **Improve Quality**: Better error handling, type hints, validation

Show me the specific changes to make while preserving all functionality.
```

## Targeted Fixes (Cmd+K)

### Remove Debug Statements
```
Remove these debug statements. Comment them out for review rather than deleting completely.
```

### Add Documentation
```
Add comprehensive documentation:
- Clear description of purpose
- Parameter types and descriptions
- Return value documentation
- Exception handling notes
```

### Consolidate Duplicates
```
These functions appear to be duplicates. Consolidate them into a single, well-documented function that handles all use cases.
```

### Improve Error Handling
```
Add robust error handling with:
- Specific error messages
- Proper exception types
- Input validation
- Graceful fallbacks
```

## Verification Prompts

### Final Verification
```
Please verify my cleanup:

1. Check that all original functionality is preserved
2. Ensure documentation is comprehensive and clear
3. Confirm error handling is robust and specific
4. Validate that code quality has improved

Generate a cleanup summary with before/after comparison.
```

### Test Coverage Check
```
Review the cleaned code and suggest:
1. Unit tests for critical functions
2. Edge cases that need testing
3. Integration test scenarios
4. Performance test considerations
```

## Language-Specific Prompts

### Python Cleanup
```
Apply Python best practices:
- Add type hints to all functions
- Use docstrings (Google/NumPy style)
- Follow PEP 8 conventions
- Add proper exception handling
- Remove debug print statements
```

### JavaScript/TypeScript Cleanup
```
Apply JavaScript/TypeScript best practices:
- Add JSDoc comments
- Use proper TypeScript types
- Follow ESLint conventions
- Add error boundaries
- Remove console.log statements
```

### Go Cleanup
```
Apply Go best practices:
- Add godoc comments
- Follow Go conventions
- Add proper error handling
- Use defer for cleanup
- Remove fmt.Println debug statements
```

## Quick Commands

### One-liner Prompts for Common Tasks

- **Quick cleanup**: "Remove debug statements and add documentation"
- **Function improvement**: "Refactor this function for clarity and add error handling"
- **Documentation only**: "Add comprehensive docstrings/comments"
- **Error handling**: "Add proper error handling and validation"
- **Type safety**: "Add type hints/annotations throughout"
- **Consolidation**: "Find and merge duplicate logic"
- **Performance**: "Optimize this code for performance"
- **Security**: "Review for security issues and add validation"