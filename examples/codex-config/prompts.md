# OpenAI Codex Cleanup Prompts

## Quick Reference Prompts

### Analysis Prompts

#### Basic Analysis
```
Analyze this code for cleanup opportunities:
- Debug statements
- Duplicate functions
- Missing documentation
- Error handling issues
- Code quality problems

Provide specific findings.
```

#### Detailed Analysis
```
Perform comprehensive code analysis:

1. Identify all debug/console output
2. Find duplicate or similar functions
3. List undocumented functions/classes
4. Identify error handling gaps
5. Find unused imports/variables
6. Detect overly complex functions
7. Identify naming convention violations

Categorize findings by severity (High/Medium/Low).
```

### Cleanup Execution Prompts

#### Standard Cleanup
```
Clean up this code following best practices:
1. Remove debug statements
2. Consolidate duplicate logic
3. Add comprehensive documentation
4. Improve error handling
5. Optimize imports

Return only the cleaned code.
```

#### Aggressive Cleanup
```
Perform thorough code cleanup:
1. Remove ALL debug/console output
2. Merge duplicate functions completely
3. Add detailed docstrings/comments
4. Implement robust error handling
5. Apply language-specific best practices
6. Optimize performance where possible
7. Improve variable/function naming

Ensure functionality is preserved.
```

### Documentation Prompts

#### Basic Documentation
```
Add documentation to this code:
- Function/class descriptions
- Parameter explanations
- Return value descriptions
- Basic usage examples
```

#### Comprehensive Documentation
```
Generate complete documentation:
- Detailed function/class descriptions
- Full parameter documentation with types
- Return value specifications
- Exception documentation
- Multiple usage examples
- Edge case explanations
- Performance considerations
```

## Language-Specific Prompts

### Python
```
Clean up this Python code:
1. Remove print() debug statements
2. Add type hints to all functions
3. Add Google-style docstrings
4. Implement proper exception handling
5. Follow PEP 8 conventions
6. Use f-strings for formatting
7. Optimize imports with isort style

Return PEP 8 compliant code.
```

### JavaScript/TypeScript
```
Clean up this JavaScript code:
1. Remove console.log/debug statements
2. Add JSDoc comments
3. Use modern ES6+ syntax
4. Implement async/await properly
5. Add error handling with try/catch
6. Use const/let appropriately
7. Apply destructuring where beneficial

Return modern, clean JavaScript.
```

### Java
```
Clean up this Java code:
1. Remove System.out.println debug statements
2. Add comprehensive Javadoc
3. Use Optional for null safety
4. Implement try-with-resources
5. Follow Java naming conventions
6. Use appropriate design patterns
7. Add proper exception handling

Return enterprise-quality Java code.
```

### Go
```
Clean up this Go code:
1. Remove fmt.Println debug statements
2. Add godoc comments
3. Implement proper error handling
4. Use defer for cleanup
5. Follow Go naming conventions
6. Simplify where possible
7. Use idiomatic Go patterns

Return idiomatic Go code.
```

## Specialized Cleanup Prompts

### Security-Focused Cleanup
```
Clean up this code with security in mind:
1. Remove all debug output that might leak sensitive data
2. Add input validation and sanitization
3. Implement proper authentication checks
4. Add authorization verification
5. Use parameterized queries/prepared statements
6. Implement proper secret management
7. Add security-related documentation

Prioritize security while maintaining functionality.
```

### Performance-Focused Cleanup
```
Clean up and optimize this code:
1. Remove debug overhead
2. Optimize loops and iterations
3. Reduce unnecessary computations
4. Implement caching where beneficial
5. Use efficient data structures
6. Minimize memory allocations
7. Add performance documentation

Balance readability with performance.
```

### Testability-Focused Cleanup
```
Clean up this code for better testability:
1. Remove debug dependencies
2. Extract pure functions
3. Implement dependency injection
4. Reduce coupling between components
5. Add clear interfaces/contracts
6. Make functions deterministic
7. Document test scenarios

Ensure code is easily testable.
```

## Interactive Prompt Templates

### Step-by-Step Cleanup
```
Let's clean up this code systematically:

Step 1: Identify issues
[Show me all problems in the code]

Step 2: Prioritize fixes
[Rank issues by importance]

Step 3: Apply improvements
[Show me the cleaned version]

Step 4: Verify changes
[Confirm functionality is preserved]
```

### Incremental Cleanup
```
Clean up this code incrementally:

Phase 1: Remove obvious issues (debug, dead code)
Phase 2: Improve structure (consolidate, refactor)
Phase 3: Enhance quality (documentation, error handling)
Phase 4: Optimize (performance, readability)

Show results after each phase.
```

## Project-Specific Prompts

### Maintaining Style Consistency
```
Clean up this code while maintaining project style:

Project conventions:
- [List your specific conventions]
- [Documentation format]
- [Naming patterns]
- [Error handling approach]

Apply cleanup while preserving these conventions.
```

### Legacy Code Cleanup
```
Carefully clean up this legacy code:
1. Preserve all existing functionality
2. Add documentation for unclear logic
3. Improve readability without major refactoring
4. Add error handling where critically missing
5. Remove only obvious dead code
6. Document assumptions and gotchas

Be conservative with changes.
```

## Validation Prompts

### Post-Cleanup Verification
```
Verify this cleanup was successful:
1. Confirm all functionality is preserved
2. Check that tests would still pass
3. Verify no breaking changes
4. Ensure documentation is accurate
5. Validate error handling is proper

Report any potential issues.
```

### Quality Assessment
```
Assess the quality of this cleaned code:
- Readability score (1-10)
- Documentation completeness (1-10)
- Error handling robustness (1-10)
- Performance impact assessment
- Maintainability improvement
- Remaining issues to address

Provide metrics and recommendations.
```