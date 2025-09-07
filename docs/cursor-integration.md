# Cursor Integration for Cleanup Toolkit

> *"After successfully completing your goal, ask: 'Please clean up the code you worked on, remove any bloat you added, and document it very clearly.'"*

Integrate systematic code cleanup workflow with **Cursor**, the AI-powered code editor. This guide shows how to use Cursor's AI capabilities with the Cleanup Toolkit for intelligent, context-aware code improvement.

## 🎯 Why Cursor + Cleanup Toolkit?

| Traditional Cleanup | Cursor + Cleanup Toolkit |
|-------------------|-------------------------|
| ❌ Generic, rule-based | ✅ AI-powered, context-aware |
| ❌ Miss business logic | ✅ Understand code purpose |
| ❌ Break functionality | ✅ Preserve intent while improving |
| ❌ Manual, time-consuming | ✅ Automated with AI assistance |

## 🚀 Quick Setup

### 1. Install Cleanup Toolkit
```bash
# In your project directory
curl -sSL https://raw.githubusercontent.com/your-username/cleanup-toolkit/main/install.sh | bash
```

### 2. Configure for Cursor
```bash
# Enable Cursor-specific features
echo "cursor_integration: true" >> .cleanup-toolkit/config.yml
echo "preferred_framework: cursor" >> .cleanup-toolkit/config.yml
```

### 3. Test Integration
```bash
# Create a messy file
echo "print('debug statement')" > test.py

# Commit to trigger cleanup prompts
git add test.py
git commit -m "test: cursor integration"

# Follow the generated Cursor prompts
```

## 🤖 Cursor AI Integration

### Using Cursor's AI Chat (Cmd+L)

When the pre-commit hook triggers, use these prompts with Cursor's AI:

#### 1. Initial Analysis Prompt
```
I just completed a development goal and my pre-commit hook triggered the cleanup process. 

Please analyze these files for cleanup opportunities:
[paste file list from .cleanup-toolkit/cleanup-context.md]

Focus on:
- Debug statements and dead code
- Duplicate functions and logic
- Missing documentation
- Error handling improvements

Provide a systematic cleanup plan following cleanup principles.
```

#### 2. Systematic Cleanup Prompt
```
Now help me execute cleanup systematically. For each file:

1. **Remove Bloat**: Debug statements, unused imports, dead code
2. **Consolidate Logic**: Merge duplicate functions, extract common patterns
3. **Document Clearly**: Add comprehensive docstrings and comments
4. **Improve Quality**: Better error handling, type hints, validation

Show me the specific changes to make while preserving all functionality.
```

#### 3. Verification Prompt
```
Please verify my cleanup follows cleanup standards:

1. Check that all original functionality is preserved
2. Ensure documentation is comprehensive and clear
3. Confirm error handling is robust and specific
4. Validate that code quality has improved

Generate a cleanup summary with before/after comparison.
```

### Using Cursor's Inline AI (Cmd+K)

For targeted cleanup of specific code sections:

#### Debug Statement Removal
```
# Select debug statements and use Cmd+K
Remove these debug statements following cleanup principles. 
Comment them out for review rather than deleting completely.
```

#### Function Documentation
```
# Select a function and use Cmd+K
Add comprehensive documentation following cleanup standards:
- Clear description of purpose
- Parameter types and descriptions
- Return value documentation
- Exception handling notes
```

#### Code Consolidation
```
# Select duplicate functions and use Cmd+K
These functions appear to be duplicates. Following cleanup 
principles, consolidate them into a single, well-documented function that 
handles all use cases.
```

## 📋 Cursor-Specific Workflows

### 1. Pre-commit Cleanup Workflow

```bash
# After making changes
git add .
git commit -m "feat: implement new feature"

# Pre-commit hook pauses and generates context
# Open .cleanup-toolkit/cursor-prompts.txt in Cursor
# Use Cmd+L with the generated prompts
```

### 2. Interactive Cleanup Session

```bash
# Start cleanup analysis
cat .cleanup-toolkit/cleanup-context.md

# Open files in Cursor
cursor app.py utils.py

# Use Cmd+L for comprehensive analysis
# Use Cmd+K for targeted improvements
# Use Cursor's diff view to review changes
```

### 3. Documentation Generation

```bash
# Select functions needing documentation
# Use Cmd+K with this prompt:
```
```
Following documentation standards, add comprehensive 
docstrings that clearly explain the purpose, parameters, return values, 
and any exceptions. Make the documentation so clear that any developer 
can understand and maintain this code.
```

## 🔧 Cursor Configuration

### Cursor Settings for Cleanup

Add to your Cursor settings (`.cursor-settings`):

```json
{
  "cleanup-toolkit": {
    "enabled": true,
    "auto_prompt_on_commit": true,
    "preferred_ai_model": "gpt-4",
    "cleanup_standards": {
      "require_docstrings": true,
      "require_type_hints": true,
      "max_function_length": 50,
      "consolidate_duplicates": true
    }
  },
  "ai": {
    "context_files": [
      ".cleanup-toolkit/cleanup-context.md",
      ".cleanup-toolkit/cleanup-summary.md"
    ]
  }
}
```

### Custom Cursor Commands

Create custom commands in Cursor for quick cleanup:

```json
{
  "commands": [
    {
      "name": "Cleanup Analysis",
      "command": "cursor.ai.chat",
      "prompt": "Analyze this code for cleanup opportunities: remove bloat, consolidate logic, document clearly"
    },
    {
      "name": "Generate Cleanup Documentation",
      "command": "cursor.ai.inline",
      "prompt": "Add comprehensive documentation following clear documentation standards"
    },
    {
      "name": "Consolidate Duplicate Functions",
      "command": "cursor.ai.inline", 
      "prompt": "Following cleanup principles, consolidate these duplicate functions into a single, well-designed function"
    }
  ]
}
```

## 📚 Example Cursor Session

### Complete Cleanup Workflow

1. **Trigger Pre-commit Hook**
   ```bash
   git commit -m "feat: user authentication"
   # Hook generates cleanup context and prompts
   ```

2. **Open in Cursor**
   ```bash
   cursor .cleanup-toolkit/cleanup-context.md
   cursor src/auth.py src/user.py
   ```

3. **Use Cursor AI Chat (Cmd+L)**
   ```
   I need to follow the cleanup process. Please read the cleanup 
   context and help me systematically clean up auth.py and user.py. Focus 
   on removing debug statements, consolidating duplicate validation logic, 
   and adding comprehensive documentation.
   ```

4. **Apply Targeted Fixes (Cmd+K)**
   - Select debug statements → "Remove following cleanup principles"
   - Select functions → "Add comprehensive docstrings"
   - Select duplicates → "Consolidate into single function"

5. **Verify and Complete**
   ```bash
   # Review changes in Cursor's diff view
   git add .
   git commit --no-verify -m "feat: user authentication with cleanup"
   ```

## 🎨 Language-Specific Cursor Integration

### Python with Cursor
```python
# Before cleanup (select and use Cmd+K)
def validate_email(email):
    print(f"Validating: {email}")  # Debug statement
    return "@" in email

# Cursor prompt: "Clean up following Python cleanup standards"

# After Cursor AI cleanup
def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email format is valid
        
    Raises:
        ValueError: If email is None or empty
    """
    if not email:
        raise ValueError("Email cannot be empty")
    
    return "@" in email and "." in email
```

### JavaScript with Cursor
```javascript
// Before cleanup (select and use Cmd+K)
function processUser(name, email) {
    console.log(`Processing: ${name}`);  // Debug statement
    if (email) return true;
    return false;
}

// Cursor prompt: "Apply JavaScript cleanup standards"

// After Cursor AI cleanup
/**
 * Process and validate user information.
 * 
 * @param {string} name - User's full name
 * @param {string} email - User's email address
 * @returns {boolean} True if user is valid and processed
 * @throws {Error} If name is empty or email is invalid
 */
function processUser(name, email) {
    if (!name?.trim()) {
        throw new Error("Name cannot be empty");
    }
    
    if (!email?.includes("@")) {
        throw new Error("Invalid email address");
    }
    
    return true;
}
```

## 🔍 Troubleshooting Cursor Integration

### Common Issues

**Cursor AI not understanding context:**
```bash
# Ensure context files are accessible
ls -la .cleanup-toolkit/cleanup-context.md

# Add context files to Cursor workspace
cursor .cleanup-toolkit/
```

**Pre-commit hook not generating Cursor prompts:**
```bash
# Check configuration
grep "cursor" .cleanup-toolkit/config.yml

# Enable Cursor integration
echo "cursor_integration: true" >> .cleanup-toolkit/config.yml
```

**Cursor commands not working:**
```bash
# Check Cursor settings
cat .cursor-settings

# Restart Cursor after configuration changes
```

## 💡 Pro Tips for Cursor + Cleanup Toolkit

### Efficient Workflow
1. **Use Cursor's file explorer** to quickly navigate cleanup context
2. **Leverage Cursor's diff view** to review AI-suggested changes
3. **Use Cmd+L for analysis**, Cmd+K for targeted fixes
4. **Save successful prompts** as Cursor custom commands

### Best Practices
- **Always review AI suggestions** before applying
- **Use Cursor's undo** (Cmd+Z) if changes break functionality
- **Test incrementally** after each cleanup step
- **Combine Cursor AI with manual review** for best results

### Advanced Features
- **Use Cursor's multi-file editing** for consistent changes across files
- **Leverage Cursor's symbol search** to find duplicate functions
- **Use Cursor's integrated terminal** for running tests after cleanup

## 📖 Additional Resources

- [Cursor Documentation](https://cursor.sh/docs)
- [Cleanup Toolkit Main Repository](https://github.com/your-username/cleanup-toolkit)
- [Cursor AI Best Practices](https://cursor.sh/docs/ai-best-practices)

---

*Transform your Cursor workflow with AI-powered systematic code cleanup. Clean code, clear documentation, intelligent refactoring! 🤖✨*