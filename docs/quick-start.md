# Quick Start Guide

Get up and running with the Code Cleanup Toolkit in under 5 minutes!

## 🚀 Installation

### One-Line Install (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/nelsojona/cleanup-toolkit/main/install.sh | bash
```

### Manual Install
```bash
git clone https://github.com/nelsojona/cleanup-toolkit.git
cd your-project
bash /path/to/toolkit/install.sh
```

## ✅ Verification

Test that everything is working:

```bash
# Create a test file with debug statements
echo "print('Hello, world!')" > test.py

# Add and commit (pre-commit hook will run)
git add test.py
git commit -m "test: add hello world"

# Check if debug statement was commented out
cat test.py
# Should show: # DEBUG: print('Hello, world!')
```

## 🎯 Basic Usage

### Automatic Cleanup (Pre-commit Hook)
The toolkit automatically runs on every commit:

```bash
git add .
git commit -m "feat: implement new feature"
# ✅ Cleanup runs automatically!
```

### Manual Cleanup
Run cleanup anytime:

```bash
# Load aliases
source .cleanup-toolkit/aliases.sh

# Run cleanup
cleanup-now

# View report
cleanup-report
```

## 🔧 Configuration

### Basic Setup
The toolkit works out of the box, but you can customize it:

```bash
# Edit configuration
nano .cleanup-toolkit/config.yml

# Use a template
cp examples/config-templates/basic-config.yml .cleanup-toolkit/config.yml
```

### Enable Integrations

#### Claude Code
```bash
# Files are created automatically
# Just start using them:
cat claude.md    # Project context
cat handover.md  # Current tasks
```

#### Warp Terminal
```bash
# Initialize Warp workflows
bash .cleanup-toolkit/warp-terminal/warp-init.sh

# Use workflows
startup
cleanup-analysis
```

## 📊 What Gets Cleaned

### Automatically Fixed
- ✅ Debug statements → Commented out
- ✅ Code formatting → Applied
- ✅ Import organization → Sorted
- ✅ Trailing whitespace → Removed

### Flagged for Review
- ⚠️ TODO/FIXME comments
- ⚠️ Duplicate functions
- ⚠️ Large files/functions
- ⚠️ Missing documentation

## 🎨 Language Support

| Language | Status | Auto-format | Linting |
|----------|--------|-------------|---------|
| Python | ✅ Full | Black, isort | Flake8 |
| JavaScript | ✅ Full | Prettier | ESLint |
| TypeScript | ✅ Full | Prettier | ESLint |
| Java | 🟡 Basic | Google Format | Checkstyle |
| Go | 🟡 Basic | gofmt | go vet |
| Rust | 🟡 Basic | rustfmt | clippy |

## 🔍 Troubleshooting

### Pre-commit Hook Not Running
```bash
# Check if hook is installed
ls -la .git/hooks/pre-commit

# Reinstall if missing
bash /path/to/toolkit/install.sh
```

### Permission Errors
```bash
# Make scripts executable
chmod +x .git/hooks/pre-commit
chmod +x .cleanup-toolkit/scripts/*
```

### Tool Not Found Errors
```bash
# Install missing tools
pip install black isort autoflake  # Python
npm install -g prettier eslint     # JavaScript
```

## 💡 Pro Tips

### Skip Cleanup for Specific Commits
```bash
# Add to commit message
git commit -m "wip: work in progress SKIP_CLEANUP"

# Or set environment variable
SKIP_CLEANUP=true git commit -m "wip: work in progress"
```

### Team Setup
```bash
# Use team configuration
cp examples/team-setup/team-config.yml .cleanup-toolkit/config.yml

# Share with team
git add .cleanup-toolkit/
git commit -m "chore: add code cleanup toolkit"
```

### Integration with CI/CD
```bash
# Add to your CI pipeline
- name: Run cleanup check
  run: bash .git/hooks/pre-commit
```

## 📚 Next Steps

- [Read the full documentation](README.md)
- [Configure for your team](examples/team-setup/)
- [Set up Claude Code integration](claude-code/)
- [Enable Warp Terminal workflows](warp-terminal/)
- [Contribute to the project](CONTRIBUTING.md)

## 🆘 Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/nelsojona/cleanup-toolkit/issues)
- 💬 [Discussions](https://github.com/nelsojona/cleanup-toolkit/discussions)
- 📧 [Email Support](mailto:support@example.com)

---

*Happy coding with clean code! 🧹✨*

