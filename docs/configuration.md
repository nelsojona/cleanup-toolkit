# Configuration Reference

Complete configuration guide for the Cleanup Toolkit, covering all settings and customization options.

## 📁 Configuration File Location

The main configuration file is located at:
```
.cleanup-toolkit/config.yml
```

This file is created automatically during installation with sensible defaults.

## ⚙️ Basic Configuration

### Minimal Setup
```yaml
# Basic configuration for getting started
cleanup_mode: "agentic"
preferred_framework: "claude-code"
auto_generate_prompts: true
```

### Core Settings
```yaml
# General settings
cleanup_enabled: true           # Enable/disable cleanup toolkit
auto_fix_enabled: true         # Allow automatic fixes where safe
documentation_required: false  # Require documentation for all functions

# Integration settings  
shell_script_enabled: true     # Enable shell script fallback
claude_code_enabled: false     # Enable Claude Code integration
warp_terminal_enabled: false   # Enable Warp Terminal integration
```

## 🤖 AI Framework Configuration

### Claude Code Settings
```yaml
claude_code:
  update_handover: true         # Update handover.md automatically
  generate_context: true       # Generate cleanup context files
  create_cleanup_tasks: true   # Add cleanup tasks to handover.md
  project_context_file: "claude.md"
  handover_file: "handover.md"
  cleanup_rules_file: "cleanup-rules.md"
```

### Warp Terminal Settings
```yaml
warp_terminal:
  enable_workflows: true       # Create Warp workflows
  create_ai_context: true     # Generate AI context files
  setup_aliases: true         # Create shell aliases
  workflow_directory: ".warp/workflows"
  ai_context_file: ".warp/ai_prompts.md"
```

### Shell Script Settings
```yaml
shell_script:
  provide_guides: true        # Generate manual cleanup guides
  generate_checklists: true  # Create cleanup checklists
  create_reports: true       # Generate cleanup reports
```

## 🎨 Language-Specific Configuration

### Python Settings
```yaml
python:
  use_black: true            # Format with Black
  use_isort: true           # Sort imports with isort
  use_autoflake: true       # Remove unused imports
  use_mypy: false           # Type checking with mypy
  use_flake8: false         # Linting with flake8
  max_line_length: 88       # Black's default
  
  # Debug patterns to detect
  debug_patterns:
    - "print\\("
    - "pprint\\("
    - "pp\\("
    - "breakpoint\\("
```

### JavaScript/TypeScript Settings
```yaml
javascript:
  use_prettier: true        # Format with Prettier
  use_eslint: true         # Lint with ESLint
  use_typescript: false    # TypeScript-specific rules
  
  # Debug patterns to detect
  debug_patterns:
    - "console\\.log\\("
    - "console\\.debug\\("
    - "debugger"
    - "alert\\("
```

### Java Settings
```yaml
java:
  use_google_java_format: false  # Format with Google Java Format
  use_checkstyle: false         # Lint with Checkstyle
  
  debug_patterns:
    - "System\\.out\\.print"
    - "System\\.err\\.print"
```

### Go Settings
```yaml
go:
  use_gofmt: true          # Format with gofmt
  use_goimports: true      # Organize imports
  use_golint: false        # Lint with golint
  
  debug_patterns:
    - "fmt\\.Print"
    - "log\\.Print"
```

### Rust Settings
```yaml
rust:
  use_rustfmt: true        # Format with rustfmt
  use_clippy: false        # Lint with clippy
  
  debug_patterns:
    - "println!"
    - "dbg!"
    - "eprintln!"
```

## 📊 Quality Gates

### File and Function Limits
```yaml
quality_gates:
  max_file_lines: 500        # Maximum lines per file
  max_function_lines: 50     # Maximum lines per function
  max_complexity: 10         # Maximum cyclomatic complexity
  require_docstrings: true   # Require function documentation
  require_type_hints: false  # Require type annotations
```

### Code Quality Checks
```yaml
quality_checks:
  # TODO/FIXME detection
  todo_patterns: ["TODO", "FIXME", "XXX", "HACK", "BUG"]
  
  # Minimum documentation coverage
  min_doc_coverage: 80
  
  # Maximum code duplication
  max_duplication: 10
```

## 🔧 Pre-commit Hook Settings

### Hook Behavior
```yaml
pre_commit:
  fail_on_warnings: false    # Fail commit on warnings
  generate_reports: true     # Generate cleanup reports
  update_handover: true      # Update handover.md
  create_cleanup_branch: false  # Create separate cleanup branch
  
  # Skip conditions
  skip_patterns:
    - "SKIP_CLEANUP"
    - "NO_CLEANUP"
    - "WIP"
```

### Report Generation
```yaml
reporting:
  report_format: "markdown"     # Report format (markdown, json, html)
  include_metrics: true         # Include quality metrics
  include_suggestions: true     # Include improvement suggestions
  save_reports: true           # Save reports to disk
  report_directory: ".cleanup-toolkit/reports"
```

## 👥 Team Configuration

### Collaboration Settings
```yaml
team:
  enforce_standards: true      # Enforce team coding standards
  require_review: false        # Require cleanup review
  shared_prompts: true        # Use shared AI prompts
  
  # Auto-assign reviewers for cleanup PRs
  auto_assign_reviewers: 
    - "@team-lead"
    - "@senior-dev"
```

### Notifications
```yaml
notifications:
  slack_webhook: "${SLACK_WEBHOOK_URL}"  # Slack integration
  email_team: false                      # Email notifications
  create_jira_ticket: false             # JIRA integration
```

### Code Review Integration
```yaml
code_review:
  auto_request_review: false    # Auto-request review for cleanup
  block_merge_on_issues: false  # Block merge if issues found
  require_cleanup_approval: false  # Require approval for cleanup changes
```

## 🚀 CI/CD Integration

### Continuous Integration
```yaml
ci:
  run_on_pr: true             # Run cleanup check on PRs
  run_on_push: false          # Run on every push
  fail_build_on_issues: false # Fail build if cleanup issues found
  
  # Environment-specific settings
  environments:
    development:
      strict_mode: false
    staging:
      strict_mode: true
    production:
      strict_mode: true
      require_approval: true
```

## 🎯 Custom Rules

### Project-Specific Patterns
```yaml
custom_patterns:
  # Patterns to remove
  remove:
    - "# DEBUG:"
    - "// DEBUG:"
    - "/* DEBUG"
    - "console\\.trace\\("
  
  # Functions to consolidate
  consolidate:
    - "validate_.*email"
    - "format_.*date"
    - "parse_.*input"
  
  # Functions requiring documentation
  document:
    - "class \\w+:"
    - "function \\w+\\("
    - "def \\w+\\("
    - "pub fn \\w+\\("
```

### Custom Quality Rules
```yaml
custom_rules:
  - name: "No console.log in production"
    pattern: "console\\.log"
    severity: "error"
    auto_fix: true
    environments: ["production", "staging"]
    
  - name: "Require JSDoc for public functions"
    pattern: "export function \\w+\\("
    requires: "jsdoc_comment"
    severity: "warning"
    
  - name: "No TODO comments in main branch"
    pattern: "TODO|FIXME"
    severity: "error"
    branches: ["main", "master", "production"]
```

## 📱 Environment Variables

### Override Configuration
```bash
# Override preferred framework
export CLEANUP_PREFERRED_FRAMEWORK="warp-terminal"

# Skip cleanup for this session
export SKIP_CLEANUP=true

# Enable debug mode
export CLEANUP_DEBUG=true

# Custom configuration file
export CLEANUP_CONFIG_FILE="/path/to/custom-config.yml"
```

### Framework-Specific Variables
```bash
# Claude Code
export CLAUDE_PROJECT_CONTEXT="custom-claude.md"
export CLAUDE_HANDOVER_FILE="custom-handover.md"

# Warp Terminal
export WARP_WORKFLOWS_DIR=".custom-warp"
export WARP_AI_CONTEXT="custom-ai-context.md"

# Slack integration
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

## 🔍 Configuration Validation

### Validate Your Configuration
```bash
# Check configuration syntax
python -c "import yaml; yaml.safe_load(open('.cleanup-toolkit/config.yml'))"

# Test configuration with dry run
CLEANUP_DRY_RUN=true git commit -m "test config"

# Validate against schema (if available)
cleanup-toolkit validate-config
```

### Common Configuration Issues

**Invalid YAML syntax:**
```bash
# Check for syntax errors
yamllint .cleanup-toolkit/config.yml
```

**Missing required tools:**
```bash
# Check if configured tools are available
which black isort prettier eslint
```

**Permission issues:**
```bash
# Ensure scripts are executable
chmod +x .git/hooks/pre-commit
chmod +x .cleanup-toolkit/scripts/*
```

## 📚 Configuration Examples

See the `examples/config-templates/` directory for:
- `basic-config.yml` - Minimal setup
- `advanced-config.yml` - Full features
- `team-config.yml` - Team collaboration

## 🔧 Troubleshooting Configuration

### Debug Configuration Loading
```bash
# Enable debug mode
export CLEANUP_DEBUG=true
git commit -m "test"

# Check which config file is loaded
echo "Config file: $CLEANUP_CONFIG_FILE"

# Validate configuration
cleanup-toolkit check-config
```

### Reset to Defaults
```bash
# Backup current config
cp .cleanup-toolkit/config.yml .cleanup-toolkit/config.yml.backup

# Regenerate default config
bash install.sh --reset-config
```

---

*This configuration reference covers all available options. Start with basic configuration and gradually add features as needed.*

