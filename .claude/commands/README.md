# Claude Code Custom Commands

This directory contains custom slash commands for Claude Code that extend its functionality with specialized cleanup operations.

## Available Commands

### `/cleanup` - Comprehensive Code Cleanup
A powerful command that integrates with the Agentic Cleanup Toolkit to systematically clean and improve code quality.

**Quick Usage:**
```
/cleanup --staged              # Clean staged files before commit
/cleanup --all --debug          # Remove all debug statements
/cleanup --test --duplicates   # Find duplicate code (test mode)
```

## How Custom Commands Work

Claude Code automatically discovers and loads `.md` files in this directory as custom slash commands. Each file becomes a command with the same name as the file (without the `.md` extension).

## Creating New Commands

To create a new custom command:

1. Create a new `.md` file in this directory
2. Name it after your command (e.g., `format.md` for `/format`)
3. Document the command's purpose, usage, and behavior
4. Claude will automatically recognize it as a slash command

## Command Structure

Each command file should include:
- **Description**: What the command does
- **Usage**: How to invoke it with options
- **Examples**: Common use cases
- **Workflow**: Step-by-step process
- **Output**: What to expect

## Integration with Cleanup Toolkit

These commands are designed to work seamlessly with the Agentic Cleanup Toolkit:

- **Pre-commit hooks**: Automatic cleanup on git commits
- **Configuration**: Respects `.cleanup-toolkit/config.yml`
- **Patterns**: Uses custom patterns from `.cleanup-toolkit/patterns.yml`
- **Exclusions**: Honors `.cleanup-toolkit/.cleanupignore`

## Global vs Project Commands

- **Project commands** (this directory): Available only in this project
- **Global commands** (`~/.claude/commands/`): Available in all projects

To make these commands available globally, copy them to:
```bash
cp -r .claude/commands/* ~/.claude/commands/
```

## Best Practices

1. **Test First**: Use `--test` flag to preview changes
2. **Incremental**: Clean one aspect at a time
3. **Verify**: Ensure tests pass after cleanup
4. **Document**: Keep track of cleanup operations
5. **Automate**: Integrate with git hooks for consistency

## Support

For issues or suggestions related to custom commands:
- Check the [Cleanup Toolkit Documentation](https://github.com/cleanup-toolkit/cleanup-toolkit)
- Review command-specific help with `/cleanup --help`
- Report issues at the [GitHub repository](https://github.com/cleanup-toolkit/cleanup-toolkit/issues)

---

*Part of the Agentic Cleanup Toolkit - Enhancing Claude Code with AI-powered cleanup capabilities*