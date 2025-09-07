#!/bin/bash

# Matt Shumer Code Cleanup Toolkit - Installation Script
# Installs and configures the complete cleanup toolkit

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

TOOLKIT_VERSION="1.0.0"
REPO_URL="https://github.com/nelsojona/matt-shumer-cleanup-toolkit"

print_header() {
    clear
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC}                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}    ${BLUE}Matt Shumer Code Cleanup Toolkit v$TOOLKIT_VERSION${NC}           ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}    ${GREEN}\"Clean up code, remove bloat, document clearly\"${NC}        ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository. Please run this script from your project root."
        exit 1
    fi
    print_step "Git repository detected"
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    local missing_deps=()
    
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_info "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_step "All required dependencies found"
}

# Create toolkit directory structure
create_toolkit_structure() {
    print_info "Creating toolkit directory structure..."
    
    local toolkit_dir=".cleanup-toolkit"
    
    mkdir -p "$toolkit_dir"/{scripts,claude-code,warp-terminal,reports,config}
    
    print_step "Toolkit directory structure created"
}

# Install pre-commit hook
install_precommit_hook() {
    print_info "Installing pre-commit hook..."
    
    local hooks_dir=".git/hooks"
    local toolkit_dir=".cleanup-toolkit"
    
    # Copy the pre-commit hook
    cp "$(dirname "$0")/hooks/pre-commit" "$hooks_dir/pre-commit"
    chmod +x "$hooks_dir/pre-commit"
    
    # Create backup of existing hook if it exists
    if [ -f "$hooks_dir/pre-commit.backup" ]; then
        print_warning "Existing pre-commit hook backed up to pre-commit.backup"
    fi
    
    print_step "Pre-commit hook installed"
}

# Install shell scripts
install_shell_scripts() {
    print_info "Installing shell cleanup scripts..."
    
    local toolkit_dir=".cleanup-toolkit"
    
    # Copy shell scripts
    cp "$(dirname "$0")/scripts/"* "$toolkit_dir/scripts/" 2>/dev/null || true
    
    # Make scripts executable
    chmod +x "$toolkit_dir/scripts/"* 2>/dev/null || true
    
    print_step "Shell scripts installed"
}

# Install Claude Code integration
install_claude_code() {
    print_info "Installing Claude Code integration..."
    
    local toolkit_dir=".cleanup-toolkit"
    
    # Copy Claude Code files
    cp -r "$(dirname "$0")/claude-code/"* "$toolkit_dir/claude-code/" 2>/dev/null || true
    
    # Create project context files if they don't exist
    if [ ! -f "claude.md" ]; then
        cat > "claude.md" << EOF
# $(basename "$PWD") - Code Cleanup Project

## Project Overview
[Add your project description here]

## Tech Stack
[List your technologies]

## Cleanup Standards
- Remove debug statements
- Consolidate duplicate functions
- Add comprehensive documentation
- Improve error handling
- Follow language-specific best practices

## Workflow
1. Complete development goal
2. Run cleanup analysis
3. Apply systematic cleanup
4. Document changes clearly
5. Verify quality
EOF
        print_step "Created claude.md template"
    fi
    
    if [ ! -f "handover.md" ]; then
        cat > "handover.md" << EOF
# Current Tasks and Progress

## Today's Goal
[Describe what you're working on]

## Current Tasks
- [ ] [Add your tasks here]

## Completed Today
- [x] Installed Matt Shumer Code Cleanup Toolkit

## Files to Review
[List files that need cleanup]

## Notes
[Add any relevant notes]
EOF
        print_step "Created handover.md template"
    fi
    
    print_step "Claude Code integration installed"
}

# Install Warp Terminal integration
install_warp_terminal() {
    print_info "Installing Warp Terminal integration..."
    
    local toolkit_dir=".cleanup-toolkit"
    
    # Copy Warp Terminal files
    cp -r "$(dirname "$0")/warp-terminal/"* "$toolkit_dir/warp-terminal/" 2>/dev/null || true
    
    # Run Warp initialization if warp-init.sh exists
    if [ -f "$toolkit_dir/warp-terminal/warp-init.sh" ]; then
        bash "$toolkit_dir/warp-terminal/warp-init.sh"
        print_step "Warp Terminal workflows configured"
    fi
    
    print_step "Warp Terminal integration installed"
}

# Create configuration file
create_config() {
    print_info "Creating configuration file..."
    
    local toolkit_dir=".cleanup-toolkit"
    local config_file="$toolkit_dir/config.yml"
    
    cat > "$config_file" << EOF
# Matt Shumer Code Cleanup Toolkit Configuration

# General settings
cleanup_enabled: true
auto_fix_enabled: true
documentation_required: true

# Integration settings
shell_script_enabled: true
claude_code_enabled: false
warp_terminal_enabled: false

# Language-specific settings
python:
  use_black: true
  use_isort: true
  use_autoflake: true
  
javascript:
  use_prettier: true
  use_eslint: true
  
java:
  use_google_java_format: false
  
go:
  use_gofmt: true
  use_goimports: true

# Quality checks
max_file_lines: 500
max_function_lines: 50
require_docstrings: true

# Pre-commit settings
fail_on_warnings: false
generate_reports: true
update_handover: true
EOF

    print_step "Configuration file created at $config_file"
}

# Setup shell aliases
setup_shell_aliases() {
    print_info "Setting up shell aliases..."
    
    local toolkit_dir=".cleanup-toolkit"
    local alias_file="$toolkit_dir/aliases.sh"
    
    cat > "$alias_file" << 'EOF'
#!/bin/bash
# Matt Shumer Code Cleanup Toolkit - Shell Aliases

# Quick cleanup commands
alias cleanup-now='bash .cleanup-toolkit/scripts/code_cleanup_gist.sh'
alias cleanup-analysis='bash .cleanup-toolkit/scripts/analyze_code.sh'
alias cleanup-report='cat .cleanup-toolkit/reports/cleanup-report.md'

# Git integration
alias commit-clean='git add -A && git commit -m "refactor: code cleanup and documentation"'
alias pre-commit-test='bash .git/hooks/pre-commit'

# Claude Code integration
alias claude-context='cat claude.md handover.md'
alias update-handover='echo "## $(date +%Y-%m-%d)" >> handover.md && echo "- $1" >> handover.md'

# Warp Terminal integration (if available)
if [ -d ".warp" ]; then
    alias warp-startup='warp workflow run project-startup'
    alias warp-cleanup='warp workflow run cleanup-analysis'
fi

# Project context
alias show-todo='grep -rn "TODO\|FIXME\|XXX\|HACK" . --include="*.py" --include="*.js" --include="*.java"'
alias show-debug='grep -rn "print(\|console\.log\|System\.out" . --include="*.py" --include="*.js" --include="*.java"'

echo "Matt Shumer Code Cleanup Toolkit aliases loaded!"
echo "Available commands: cleanup-now, cleanup-analysis, cleanup-report, commit-clean"
EOF

    chmod +x "$alias_file"
    
    print_step "Shell aliases created"
    print_info "💡 Add 'source .cleanup-toolkit/aliases.sh' to your shell profile to use aliases"
}

# Create example files
create_examples() {
    print_info "Creating example files..."
    
    local toolkit_dir=".cleanup-toolkit"
    local examples_dir="$toolkit_dir/examples"
    
    mkdir -p "$examples_dir"
    
    # Create example messy file
    cat > "$examples_dir/messy_example.py" << 'EOF'
#!/usr/bin/env python3
# Example messy file for demonstration

import os
import sys
import json
# import unused_module  # Unused import

def calculate_something(x, y):
    print(f"Debug: calculating {x} + {y}")  # Debug statement
    # TODO: Add proper validation
    return x + y

def calculate_sum(a, b):  # Duplicate function
    print(f"Debug: calculating {a} + {b}")  # Debug statement
    return a + b

# More messy code...
EOF

    # Create example clean file
    cat > "$examples_dir/clean_example.py" << 'EOF'
#!/usr/bin/env python3
"""
Example clean file demonstrating proper code structure.

This module provides mathematical calculation utilities.
"""

from typing import Union


def calculate_sum(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """
    Calculate the sum of two numbers.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        The sum of x and y
        
    Raises:
        TypeError: If inputs are not numbers
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both arguments must be numbers")
    
    return x + y
EOF

    print_step "Example files created in $examples_dir"
}

# Display installation summary
display_summary() {
    local toolkit_dir=".cleanup-toolkit"
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                    Installation Complete!                   ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    print_step "Matt Shumer Code Cleanup Toolkit installed successfully!"
    echo ""
    
    print_info "📁 Toolkit installed in: $toolkit_dir"
    print_info "🪝 Pre-commit hook: .git/hooks/pre-commit"
    print_info "⚙️  Configuration: $toolkit_dir/config.yml"
    print_info "📚 Examples: $toolkit_dir/examples/"
    echo ""
    
    print_info "🚀 Quick Start:"
    echo "   1. Source aliases: source $toolkit_dir/aliases.sh"
    echo "   2. Test pre-commit: pre-commit-test"
    echo "   3. Run cleanup: cleanup-now"
    echo ""
    
    print_info "🔧 Integration Options:"
    if [ -f "claude.md" ]; then
        echo "   ✅ Claude Code: Ready (claude.md found)"
    else
        echo "   📝 Claude Code: Template created"
    fi
    
    if [ -d ".warp" ]; then
        echo "   ✅ Warp Terminal: Ready (.warp directory found)"
    else
        echo "   ⚡ Warp Terminal: Run warp-init.sh to enable"
    fi
    echo ""
    
    print_info "📖 Documentation: $REPO_URL"
    print_info "🐛 Issues: $REPO_URL/issues"
    echo ""
    
    print_warning "💡 Remember: The toolkit works best when you follow the workflow:"
    echo "   1. Complete your development goal"
    echo "   2. Commit your changes (pre-commit hook runs automatically)"
    echo "   3. Review the cleanup report"
    echo "   4. Use additional tools (Claude Code, Warp) for deeper cleanup"
    echo ""
}

# Interactive setup
interactive_setup() {
    echo -e "${BLUE}Would you like to enable additional integrations?${NC}"
    echo ""
    
    # Claude Code
    read -p "Enable Claude Code integration? (y/N): " enable_claude
    if [[ $enable_claude =~ ^[Yy]$ ]]; then
        sed -i 's/claude_code_enabled: false/claude_code_enabled: true/' .cleanup-toolkit/config.yml
        print_step "Claude Code integration enabled"
    fi
    
    # Warp Terminal
    read -p "Enable Warp Terminal integration? (y/N): " enable_warp
    if [[ $enable_warp =~ ^[Yy]$ ]]; then
        sed -i 's/warp_terminal_enabled: false/warp_terminal_enabled: true/' .cleanup-toolkit/config.yml
        print_step "Warp Terminal integration enabled"
    fi
    
    echo ""
}

# Main installation function
main() {
    print_header
    
    print_info "Installing Matt Shumer Code Cleanup Toolkit..."
    print_info "This will set up automated code cleanup based on the 'Vibe coding tip'"
    echo ""
    
    # Run installation steps
    check_git_repo
    check_dependencies
    create_toolkit_structure
    install_precommit_hook
    install_shell_scripts
    install_claude_code
    install_warp_terminal
    create_config
    setup_shell_aliases
    create_examples
    
    # Interactive setup
    interactive_setup
    
    # Show summary
    display_summary
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Matt Shumer Code Cleanup Toolkit Installer"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --version, -v  Show version information"
        echo "  --uninstall    Remove the toolkit"
        echo ""
        exit 0
        ;;
    --version|-v)
        echo "Matt Shumer Code Cleanup Toolkit v$TOOLKIT_VERSION"
        exit 0
        ;;
    --uninstall)
        print_info "Uninstalling Matt Shumer Code Cleanup Toolkit..."
        rm -rf .cleanup-toolkit
        rm -f .git/hooks/pre-commit
        rm -f claude.md handover.md 2>/dev/null || true
        rm -rf .warp 2>/dev/null || true
        print_step "Toolkit uninstalled successfully"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac

