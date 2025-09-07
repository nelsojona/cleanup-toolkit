# Warp Terminal Integration

This directory contains the Warp Terminal integration for the Cleanup Toolkit, providing real-time AI assistance for systematic cleanup workflows.

## ⚡ How It Works

Warp Terminal integration provides:
- **Real-time AI assistance** with Cmd+G (or Ctrl+G)
- **Custom workflows** for cleanup tasks
- **Terminal-integrated analysis** and guidance
- **Multi-pane development** environment support

## 📁 Files

- `agentic-workflows.md` - Complete Warp Terminal workflows and AI prompts

## 🚀 Quick Start

1. **Install the toolkit** in your project:
   ```bash
   bash install.sh
   ```

2. **Warp Terminal setup** (if Warp is installed):
   ```bash
   bash .cleanup-toolkit/warp-terminal/warp-init.sh
   ```

3. **Use with commits**:
   ```bash
   git commit -m "feat: new feature"
   # Pre-commit hook generates Warp AI prompts
   ```

4. **Use Warp AI** (Cmd+G or Ctrl+G):
   ```
   I just triggered the cleanup process. Help me systematically
   clean up these files: [file list]. Focus on removing debug statements
   and improving documentation.
   ```

## 🔧 Available Workflows

### Analysis Workflow
```bash
cleanup-analysis
```
Analyzes staged files for cleanup opportunities.

### Execution Workflow  
```bash
cleanup-execute
```
Guides through systematic cleanup process.

### Verification Workflow
```bash
cleanup-verify
```
Verifies cleanup completion and generates reports.

## 🤖 Warp AI Integration

### Real-time Guidance
Use **Cmd+G** (or **Ctrl+G**) in Warp Terminal with these prompts:

1. **Analysis Prompt**: Get detailed file analysis
2. **Execution Prompt**: Step-by-step cleanup instructions  
3. **Verification Prompt**: Confirm quality and completeness

### AI Context
Warp AI understands your project through:
- Project-specific cleanup standards
- Common patterns and anti-patterns
- Language-specific best practices
- Cleanup best practices

## 📊 Workflow Commands

```bash
# Start cleanup session
startup

# Analyze for cleanup opportunities  
cleanup-analysis

# Get AI guidance for execution
# Use Cmd+G with generated prompts

# Verify completion
cleanup-verify

# Show cleanup status
cleanup-status
```

## 💡 Best Practices

- **Use Cmd+G frequently** for real-time AI guidance
- **Reference project context** in your prompts
- **Follow the three-phase workflow**: Analysis → Execution → Verification
- **Combine AI prompts with workflows** for efficiency

## 📚 Example Session

```bash
# After pre-commit hook triggers
$ cleanup-analysis
🔍 Analyzing code for cleanup opportunities...
📁 Files modified: app.py, utils.py
🐛 Debug statements found: 3
📝 TODO comments: 2
💡 Next: Use Cmd+G with Warp AI for detailed cleanup guidance

# Press Cmd+G in Warp Terminal
Cmd+G: "Help me clean up app.py and utils.py following cleanup best practices.
Focus on the 3 debug statements and 2 TODO comments found."

Warp AI: "I'll help you systematically clean up these files. Let's start with 
app.py - I can see debug print statements on lines 15, 32, and 45..."

# After cleanup
$ cleanup-verify
✅ Verifying cleanup completion...
🎉 Cleanup appears complete!
```

See `agentic-workflows.md` for complete workflows and prompts.

