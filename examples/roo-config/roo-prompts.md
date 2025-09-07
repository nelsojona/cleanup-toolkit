# Roo Code AI Cleanup Prompts

## Initial Setup Prompts

### Project Analysis
```
Analyze my project structure and codebase to understand:
- Coding conventions and patterns used
- Documentation style preferences
- Error handling approaches
- Testing frameworks and practices

Use this understanding to guide cleanup suggestions that fit naturally with the existing codebase.
```

### Configure Cleanup Standards
```
Based on your analysis, configure cleanup standards that:
- Match existing code style and conventions
- Preserve all business logic and functionality
- Improve code quality incrementally
- Focus on the most impactful improvements first
```

## Systematic Cleanup Prompts

### Comprehensive Analysis
```
I've just completed development and need systematic cleanup. Please:

1. Analyze the modified files for:
   - Debug statements and temporary code
   - Duplicate or similar logic
   - Missing or unclear documentation
   - Weak error handling
   - Complex code that could be simplified

2. Create a prioritized cleanup plan

3. Guide me through improvements step-by-step
```

### Remove Development Artifacts
```
Help me remove all development artifacts:
- Debug print/console.log statements
- Commented-out code blocks
- TODO/FIXME comments that are resolved
- Test data and mock implementations
- Temporary variables and functions

Ensure production code remains clean and professional.
```

### Consolidate and Refactor
```
Identify and consolidate duplicate logic:
- Find similar functions that can be merged
- Extract common patterns into utilities
- Simplify complex conditional logic
- Reduce nesting and improve readability
- Create reusable components/modules
```

### Documentation Enhancement
```
Improve documentation throughout the code:
- Add comprehensive function/method documentation
- Explain complex business logic clearly
- Document parameters, returns, and exceptions
- Add inline comments for non-obvious code
- Create or update API documentation

Make the code self-documenting and maintainable.
```

### Error Handling Improvement
```
Enhance error handling:
- Add proper input validation
- Use specific exception types
- Implement graceful error recovery
- Add meaningful error messages
- Ensure consistent error handling patterns

Make the code robust and user-friendly.
```

## Interactive Cleanup Sessions

### Guided Cleanup
```
Let's do interactive cleanup together:

For each file I've modified:
1. Show me the specific issues you found
2. Explain why each change improves the code
3. Demonstrate the improvement with examples
4. Let me approve or modify each suggestion
5. Apply changes while preserving functionality
```

### Step-by-Step Refactoring
```
Guide me through refactoring step-by-step:

1. Start with the highest priority improvements
2. Show before/after comparisons
3. Explain the benefits of each change
4. Ensure tests still pass after each step
5. Keep changes atomic and reversible
```

## Verification and Quality Checks

### Post-Cleanup Verification
```
Verify the cleanup was successful:

1. Confirm all functionality is preserved
2. Check that tests still pass
3. Validate documentation completeness
4. Assess code quality improvements
5. Identify any remaining issues

Generate a report with metrics and recommendations.
```

### Quality Metrics
```
Measure cleanup effectiveness:
- Lines of code reduced/improved
- Cyclomatic complexity reduction
- Documentation coverage increase
- Error handling improvements
- Code duplication elimination

Provide quantitative metrics showing improvement.
```

## Language-Specific Prompts

### Python Cleanup
```
Apply Python best practices:
- Add type hints to all functions
- Use f-strings for formatting
- Follow PEP 8 style guide
- Add docstrings (Google/NumPy style)
- Implement proper exception handling
- Use context managers where appropriate
```

### JavaScript/TypeScript Cleanup
```
Modernize JavaScript/TypeScript code:
- Use ES6+ features (arrow functions, destructuring)
- Add JSDoc or TypeScript types
- Implement async/await patterns
- Use optional chaining and nullish coalescing
- Follow ESLint recommendations
- Optimize bundle size
```

### Java Cleanup
```
Improve Java code quality:
- Add comprehensive Javadoc
- Use Optional for null safety
- Implement try-with-resources
- Apply SOLID principles
- Use Stream API where appropriate
- Follow Java naming conventions
```

### Go Cleanup
```
Apply Go idioms and best practices:
- Add godoc comments
- Implement proper error handling
- Use defer for cleanup
- Follow Go naming conventions
- Remove unnecessary type declarations
- Optimize for simplicity
```

## Quick Reference Prompts

### One-Line Commands

- `"Remove all debug statements"` - Clean up debug output
- `"Add missing documentation"` - Document undocumented code
- `"Consolidate duplicate functions"` - Merge similar logic
- `"Improve error handling"` - Add robust error management
- `"Simplify complex logic"` - Refactor complicated code
- `"Add type safety"` - Add types/hints throughout
- `"Optimize imports"` - Clean up and organize imports
- `"Fix naming conventions"` - Standardize names
- `"Remove dead code"` - Eliminate unused code
- `"Add unit tests"` - Generate test cases

## Advanced Cleanup Workflows

### Cross-File Refactoring
```
Perform cross-file refactoring:
1. Identify shared patterns across files
2. Extract common functionality to utilities
3. Standardize interfaces and contracts
4. Ensure consistent error handling
5. Update all references and imports
```

### Architecture Improvement
```
Suggest architectural improvements:
1. Identify tightly coupled components
2. Propose better separation of concerns
3. Suggest design pattern applications
4. Improve module boundaries
5. Enhance testability
```

### Performance Optimization
```
Optimize performance during cleanup:
1. Identify performance bottlenecks
2. Suggest algorithmic improvements
3. Optimize database queries
4. Reduce unnecessary computations
5. Improve caching strategies
```