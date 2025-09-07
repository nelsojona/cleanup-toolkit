# Examples

This directory contains examples and templates for the Cleanup Toolkit, demonstrating cleanup best practices in action.

## 📁 Directory Structure

```
examples/
├── python-project/          # Example messy Python code
├── javascript-project/      # Example messy JavaScript code  
├── config-templates/        # Configuration templates
├── team-setup/             # Team collaboration setup
└── README.md               # This file
```

## 🐍 Python Project Example

**File**: `python-project/main.py`

A deliberately messy Python file demonstrating common issues:
- Debug print statements
- Unused imports
- Duplicate functions
- Missing documentation
- Poor error handling

Perfect for testing the cleanup toolkit and seeing the transformation.

## 🟨 JavaScript Project Example

**File**: `javascript-project/app.js`

A messy JavaScript file with similar issues:
- Console.log statements
- Unused variables
- Duplicate logic
- Missing JSDoc comments
- Generic error handling

## ⚙️ Configuration Templates

### Basic Configuration
**File**: `config-templates/basic-config.yml`
- Minimal setup for getting started
- Essential cleanup features only
- Relaxed quality checks

### Advanced Configuration  
**File**: `config-templates/advanced-config.yml`
- All features enabled
- Strict quality gates
- Comprehensive language support

### Team Configuration
**File**: `team-setup/team-config.yml`
- Team collaboration features
- Shared standards and rules
- Code review integration

## 🚀 How to Use Examples

### Test the Toolkit
```bash
# Copy example to your project
cp examples/python-project/main.py .

# Add and commit to trigger cleanup
git add main.py
git commit -m "test: add messy code"

# Follow the generated AI prompts to clean up
```

### Use Configuration Templates
```bash
# Copy a template to your project
cp examples/config-templates/basic-config.yml .cleanup-toolkit/config.yml

# Or for teams
cp examples/team-setup/team-config.yml .cleanup-toolkit/config.yml
```

### Before and After Comparison

#### Before Cleanup (Python)
```python
import os, sys, json, requests  # Unused imports
def process_user(name, email):
    print(f"Processing: {name}")  # Debug statement
    # TODO: Add validation
    if email:
        return True
    return False
```

#### After AI Cleanup
```python
"""User processing utilities with comprehensive validation."""

from typing import Optional

def process_user(name: str, email: str) -> bool:
    """
    Process and validate user information.
    
    Args:
        name: User's full name
        email: User's email address
        
    Returns:
        bool: True if user is valid and processed
        
    Raises:
        ValueError: If name is empty or email is invalid
    """
    if not name.strip():
        raise ValueError("Name cannot be empty")
    
    if not email or '@' not in email:
        raise ValueError("Invalid email address")
    
    return True
```

## 💡 Learning from Examples

### Common Issues Demonstrated
1. **Debug Statements**: `print()`, `console.log()`, etc.
2. **Unused Code**: Imports, variables, functions
3. **Duplicate Logic**: Similar functions with different names
4. **Missing Documentation**: No docstrings or comments
5. **Poor Error Handling**: Generic exceptions, no validation

### AI Cleanup Improvements
1. **Intelligent Removal**: Context-aware debug statement handling
2. **Smart Consolidation**: Merge duplicate functions logically
3. **Comprehensive Documentation**: Generate meaningful docstrings
4. **Robust Error Handling**: Specific exceptions with clear messages
5. **Type Safety**: Add type hints and validation

## 🎯 Best Practices from Examples

### For Python
- Use type hints consistently
- Add comprehensive docstrings
- Handle exceptions specifically
- Follow PEP 8 conventions

### For JavaScript
- Add JSDoc comments
- Use proper async/await patterns
- Implement robust error handling
- Follow modern ES6+ practices

### For Teams
- Establish shared coding standards
- Use consistent configuration
- Implement code review processes
- Track cleanup metrics

## 🔧 Customizing Examples

Feel free to modify these examples for your specific needs:

1. **Add your language**: Create similar messy examples
2. **Customize standards**: Update configuration templates
3. **Team-specific rules**: Modify team setup configurations
4. **Project patterns**: Add your common anti-patterns

## 📚 Additional Resources

- [Quick Start Guide](../docs/quick-start.md)
- [Claude Code Integration](../claude-code/)
- [Warp Terminal Workflows](../warp-terminal/)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

*These examples demonstrate the power of AI-guided cleanup following best practices. Use them to understand the toolkit's capabilities and customize for your projects.*

