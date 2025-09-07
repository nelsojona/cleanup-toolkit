# Contributing to Cleanup Toolkit

Thank you for your interest in contributing to the Cleanup Toolkit! This project aims to make systematic code cleanup accessible and automated for developers everywhere.

## 🎯 Project Vision

Our goal is to provide a comprehensive, automated toolkit that helps developers:
- Remove bloat and dead code systematically
- Consolidate duplicate logic
- Document code clearly and comprehensively
- Maintain high code quality standards

## 🚀 Getting Started

### Prerequisites
- Git
- Bash (for shell scripts)
- Basic understanding of pre-commit hooks
- Familiarity with at least one supported language (Python, JavaScript, Java, Go, Rust)

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/nelsojona/cleanup-toolkit.git
cd cleanup-toolkit

# Install the toolkit in development mode
./install.sh

# Create a test project to work with
mkdir test-project && cd test-project
git init
bash ../install.sh
```

## 🛠 Development Workflow

### 1. Choose Your Contribution Type

#### 🐛 Bug Fixes
- Fix issues in existing functionality
- Improve error handling
- Resolve compatibility problems

#### ✨ New Features
- Add support for new programming languages
- Create new integration options
- Enhance existing workflows

#### 📚 Documentation
- Improve setup instructions
- Add usage examples
- Create tutorials and guides

#### 🔧 Tooling
- Enhance the pre-commit hook
- Improve shell scripts
- Add new automation features

### 2. Development Process

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Follow our coding standards (see below)
3. **Test thoroughly**: Use the test project to verify changes
4. **Update documentation**: Keep docs in sync with changes
5. **Submit PR**: Include clear description and examples

### 3. Testing Your Changes

```bash
# Test the pre-commit hook
cd test-project
echo "print('debug statement')" > test.py
git add test.py
git commit -m "test: debug statement"  # Should trigger cleanup

# Test shell scripts
bash .cleanup-toolkit/scripts/code_cleanup_gist.sh

# Test Claude Code integration
# (Manually verify claude.md and handover.md work correctly)

# Test Warp Terminal integration
# (If you have Warp, test the workflows)
```

## 📝 Coding Standards

### Shell Scripts
- Use `#!/bin/bash` shebang
- Include error handling with `set -e`
- Use meaningful variable names
- Add comments for complex logic
- Follow the existing color scheme for output

```bash
# Good
print_step() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Bad
echo "Step completed"
```

### Documentation
- Use clear, concise language
- Include code examples
- Add screenshots for UI elements
- Keep README.md up to date

### Configuration
- Use YAML for configuration files
- Provide sensible defaults
- Document all configuration options
- Maintain backward compatibility

## 🎨 Code Style Guidelines

### Pre-commit Hook
- Keep the hook fast (< 5 seconds for typical projects)
- Provide clear, actionable output
- Handle edge cases gracefully
- Support multiple languages

### Integration Scripts
- Make integrations optional
- Provide clear setup instructions
- Handle missing dependencies gracefully
- Follow the established patterns

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] Pre-commit hook runs without errors
- [ ] Language-specific cleanup works correctly
- [ ] Configuration options are respected
- [ ] Error messages are helpful
- [ ] Documentation is accurate

### Test Cases to Cover
1. **Fresh installation** on a new project
2. **Upgrade** from previous version
3. **Multiple languages** in the same project
4. **Large files** and repositories
5. **Edge cases** (empty files, binary files, etc.)

## 📋 Pull Request Guidelines

### PR Title Format
- `feat: add support for Rust language`
- `fix: resolve pre-commit hook error on Windows`
- `docs: update installation instructions`
- `refactor: improve shell script organization`

### PR Description Template
```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tested on fresh installation
- [ ] Tested with multiple languages
- [ ] Updated documentation
- [ ] Added examples if applicable

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🌟 Contribution Ideas

### High Priority
- [ ] Add support for more programming languages
- [ ] Improve Windows compatibility
- [ ] Create VS Code extension
- [ ] Add configuration validation
- [ ] Improve error messages

### Medium Priority
- [ ] Add metrics and analytics
- [ ] Create web-based configuration tool
- [ ] Add integration with more tools (Vim, Emacs, etc.)
- [ ] Improve performance for large repositories

### Low Priority
- [ ] Add GUI installer
- [ ] Create Docker image
- [ ] Add support for custom rules
- [ ] Create plugin system

## 🐛 Reporting Issues

### Bug Reports
Use the bug report template and include:
- Operating system and version
- Shell type and version
- Steps to reproduce
- Expected vs actual behavior
- Relevant log output

### Feature Requests
Use the feature request template and include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if any)
- Examples of similar features

## 📚 Resources

### Learning Resources
- [Pre-commit hooks documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Shell scripting best practices](https://google.github.io/styleguide/shellguide.html)
- [YAML specification](https://yaml.org/spec/)

### Project Resources
- [Project roadmap](https://github.com/nelsojona/cleanup-toolkit/projects)
- [Discussion forum](https://github.com/nelsojona/cleanup-toolkit/discussions)

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks in documentation

### Contribution Levels
- **🌟 Core Contributor**: 10+ merged PRs
- **🚀 Feature Champion**: Major feature implementation
- **📚 Documentation Hero**: Significant documentation improvements
- **🐛 Bug Hunter**: Multiple bug fixes and improvements

## 📞 Getting Help

- **Questions**: Open a [Discussion](https://github.com/nelsojona/cleanup-toolkit/discussions)
- **Bugs**: Create an [Issue](https://github.com/nelsojona/cleanup-toolkit/issues)
- **Chat**: Join our [Discord](https://discord.gg/your-invite) (if available)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make code cleanup systematic and accessible for everyone! 🧹✨

