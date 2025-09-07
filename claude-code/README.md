# Claude Code Integration

This directory contains the Claude Code integration for the Cleanup Toolkit, implementing systematic cleanup workflows with AI assistance.

## 🧠 How It Works

Claude Code integration provides:
- **Project context awareness** through `claude.md` and `handover.md`
- **Systematic cleanup prompts** that understand your codebase
- **Progress tracking** and documentation updates
- **Comprehensive analysis** and verification workflows

## 📁 Files

- `agentic-prompts.md` - Complete prompt library for Claude Code cleanup workflows

## 🚀 Quick Start

1. **Install the toolkit** in your project:
   ```bash
   bash install.sh
   ```

2. **Claude Code files are created automatically**:
   - `claude.md` - Project context and standards
   - `handover.md` - Current tasks and progress
   - `cleanup-rules.md` - Detailed cleanup standards

3. **Use with commits**:
   ```bash
   git commit -m "feat: new feature"
   # Pre-commit hook generates Claude Code prompts
   ```

4. **Follow the prompts** in Claude Code:
   ```
   Please read .cleanup-toolkit/cleanup-context.md and handover.md.
   I need to follow the cleanup process for the files I just modified.
   ```

## 📋 Workflow

### 1. Analysis Phase
Claude Code analyzes your modified files for:
- Debug statements and dead code
- Duplicate functions and logic
- Missing documentation
- Quality issues and improvements

### 2. Cleanup Phase
Systematic cleanup following best practices:
- Remove bloat and unnecessary code
- Consolidate duplicate logic
- Add comprehensive documentation
- Improve error handling and quality

### 3. Verification Phase
Ensure cleanup preserves functionality:
- Verify logic preservation
- Check interface compatibility
- Assess quality improvements
- Generate cleanup reports

## 💡 Best Practices

- **Always reference project files** (`claude.md`, `handover.md`, `cleanup-rules.md`)
- **Use prompt chaining** for systematic cleanup
- **Update handover.md** as you progress
- **Verify functionality** before completing commits

## 📚 Example Session

```
You: "Please read claude.md and handover.md to understand the project context. I just completed a feature and need to follow the cleanup process."

Claude: "I'll analyze your project context and the cleanup requirements. Based on handover.md, I can see you have new cleanup tasks for the files you modified..."

You: "Now please execute the cleanup plan systematically for each file."

Claude: "I'll clean up each file following best practices. Let me start with removing debug statements and improving documentation..."
```

See `agentic-prompts.md` for the complete prompt library.

