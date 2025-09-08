#!/bin/bash

# Code Cleanup Gist Script - STRICT ENFORCEMENT MODE
# Based on the "Vibe coding tip" and community insights
# Systematically clean up code after completing development goals
# RULES: NO BYPASSING ALLOWED - Cleanup is MANDATORY

set -e

# Check for bypass attempts
if [[ "$1" == "--skip" ]] || [[ "$1" == "--no-cleanup" ]] || [[ "$SKIP_CLEANUP" == "true" ]]; then
    echo -e "\033[0;31m❌ ERROR: Cleanup cannot be skipped\033[0m"
    echo -e "\033[0;31mCleanup is MANDATORY in this repository\033[0m"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLEANUP_REPORT="cleanup_report.md"
TEMP_DIR="/tmp/code_cleanup_$$"

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}   Code Cleanup Assistant${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    print_step "Checking dependencies..."
    
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) is not installed. Please install it first."
        echo "Visit: https://cli.github.com/"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed."
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} All dependencies found"
}

get_pr_info() {
    print_step "Fetching PR information..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
    
    # Get current branch
    CURRENT_BRANCH=$(git branch --show-current)
    echo "Current branch: $CURRENT_BRANCH"
    
    # Try to find associated PR
    PR_NUMBER=$(gh pr list --head "$CURRENT_BRANCH" --json number --jq '.[0].number' 2>/dev/null || echo "")
    
    if [ -z "$PR_NUMBER" ]; then
        print_warning "No PR found for current branch. Analyzing local changes instead."
        ANALYZE_MODE="local"
    else
        echo "Found PR #$PR_NUMBER"
        ANALYZE_MODE="pr"
    fi
}

analyze_pr_changes() {
    print_step "Analyzing PR changes..."
    
    mkdir -p "$TEMP_DIR"
    
    # Get PR details
    gh pr view "$PR_NUMBER" --json title,body,files > "$TEMP_DIR/pr_info.json"
    
    # Extract changed files
    gh pr diff "$PR_NUMBER" --name-only > "$TEMP_DIR/changed_files.txt"
    
    echo "Changed files:"
    cat "$TEMP_DIR/changed_files.txt" | sed 's/^/  - /'
}

analyze_local_changes() {
    print_step "Analyzing local changes..."
    
    mkdir -p "$TEMP_DIR"
    
    # Get uncommitted changes
    git diff --name-only > "$TEMP_DIR/changed_files.txt"
    
    # Also include staged changes
    git diff --cached --name-only >> "$TEMP_DIR/changed_files.txt"
    
    # Remove duplicates
    sort "$TEMP_DIR/changed_files.txt" | uniq > "$TEMP_DIR/changed_files_clean.txt"
    mv "$TEMP_DIR/changed_files_clean.txt" "$TEMP_DIR/changed_files.txt"
    
    echo "Changed files:"
    cat "$TEMP_DIR/changed_files.txt" | sed 's/^/  - /'
}

generate_cleanup_checklist() {
    print_step "Generating cleanup checklist..."
    
    cat > "$CLEANUP_REPORT" << EOF
# Code Cleanup Report
Generated on: $(date)
Branch: $(git branch --show-current)
Repository: $(git remote get-url origin 2>/dev/null || echo "Local repository")

## Files to Review
EOF

    while IFS= read -r file; do
        if [ -f "$file" ]; then
            echo "- [ ] \`$file\`" >> "$CLEANUP_REPORT"
        fi
    done < "$TEMP_DIR/changed_files.txt"

    cat >> "$CLEANUP_REPORT" << 'EOF'

## Cleanup Checklist

### Code Quality
- [ ] Remove dead/unused code
- [ ] Remove commented-out code blocks
- [ ] Consolidate duplicate logic
- [ ] Remove debug print statements
- [ ] Remove temporary variables and functions
- [ ] Check for TODO/FIXME comments and address them

### Structure & Organization
- [ ] Remove duplicate structures/classes
- [ ] Consolidate similar functions
- [ ] Ensure consistent naming conventions
- [ ] Group related functionality together
- [ ] Remove unused imports/dependencies

### Documentation
- [ ] Add/update function docstrings
- [ ] Add/update class documentation
- [ ] Update README if necessary
- [ ] Add inline comments for complex logic
- [ ] Update API documentation

### Performance & Best Practices
- [ ] Check for performance bottlenecks
- [ ] Ensure proper error handling
- [ ] Validate input parameters
- [ ] Use appropriate data structures
- [ ] Follow language-specific best practices

### Testing
- [ ] Remove test code from production files
- [ ] Ensure tests still pass
- [ ] Add tests for new functionality
- [ ] Remove obsolete tests

### Security
- [ ] Remove hardcoded credentials
- [ ] Validate user inputs
- [ ] Check for potential security vulnerabilities
- [ ] Remove debug information that might leak sensitive data

## Automated Checks
Run these commands to perform automated cleanup:

```bash
# Remove trailing whitespace (if using sed)
find . -name "*.py" -o -name "*.js" -o -name "*.java" -o -name "*.cpp" | xargs sed -i 's/[[:space:]]*$//'

# Remove empty lines at end of files
find . -name "*.py" -o -name "*.js" -o -name "*.java" -o -name "*.cpp" | xargs -I {} sh -c 'sed -i -e :a -e "/^\s*$/{\$d;N;ba" -e "}" {}'
```

## Language-Specific Cleanup

### Python
```bash
# Remove unused imports
autoflake --remove-all-unused-imports --in-place **/*.py

# Format code
black **/*.py

# Sort imports
isort **/*.py
```

### JavaScript/TypeScript
```bash
# Remove unused variables
eslint --fix **/*.js **/*.ts

# Format code
prettier --write **/*.js **/*.ts
```

### Go
```bash
# Format and organize imports
gofmt -w .
goimports -w .

# Remove unused variables
go vet ./...
```

## Notes
Add any specific notes about the cleanup process here.

EOF

    echo -e "${GREEN}✓${NC} Cleanup checklist generated: $CLEANUP_REPORT"
}

perform_file_analysis() {
    print_step "Performing detailed file analysis..."
    
    echo "" >> "$CLEANUP_REPORT"
    echo "## Detailed File Analysis" >> "$CLEANUP_REPORT"
    echo "" >> "$CLEANUP_REPORT"
    
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            echo "### $file" >> "$CLEANUP_REPORT"
            
            # Count lines
            lines=$(wc -l < "$file")
            echo "- Lines: $lines" >> "$CLEANUP_REPORT"
            
            # Check for common issues
            if grep -q "TODO\|FIXME\|XXX\|HACK" "$file"; then
                echo "- ⚠️  Contains TODO/FIXME comments" >> "$CLEANUP_REPORT"
            fi
            
            if grep -q "console\.log\|print(\|println\|System\.out" "$file"; then
                echo "- ⚠️  Contains debug print statements" >> "$CLEANUP_REPORT"
            fi
            
            if grep -q "^[[:space:]]*#.*" "$file" | head -20 | grep -q "#"; then
                echo "- ⚠️  Contains commented code blocks" >> "$CLEANUP_REPORT"
            fi
            
            # Check file size
            size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
            if [ "$size" -gt 10000 ]; then
                echo "- ⚠️  Large file (${size} bytes) - consider splitting" >> "$CLEANUP_REPORT"
            fi
            
            echo "" >> "$CLEANUP_REPORT"
        fi
    done < "$TEMP_DIR/changed_files.txt"
}

interactive_cleanup() {
    print_step "Starting interactive cleanup..."
    
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            echo ""
            echo -e "${BLUE}Reviewing: $file${NC}"
            echo "1) Open in editor"
            echo "2) Show file content"
            echo "3) Skip to next file"
            echo "4) Exit cleanup"
            
            read -p "Choose option (1-4): " choice
            
            case $choice in
                1)
                    ${EDITOR:-nano} "$file"
                    ;;
                2)
                    echo "--- File content ---"
                    cat "$file"
                    echo "--- End of file ---"
                    ;;
                3)
                    continue
                    ;;
                4)
                    break
                    ;;
                *)
                    echo "Invalid option"
                    ;;
            esac
        fi
    done < "$TEMP_DIR/changed_files.txt"
}

cleanup_temp() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

main() {
    print_header
    
    # Set up cleanup
    trap cleanup_temp EXIT
    
    # Check dependencies
    check_dependencies
    
    # Get PR or local change information
    get_pr_info
    
    # Analyze changes
    if [ "$ANALYZE_MODE" = "pr" ]; then
        analyze_pr_changes
    else
        analyze_local_changes
    fi
    
    # Generate cleanup checklist
    generate_cleanup_checklist
    
    # Perform file analysis
    perform_file_analysis
    
    echo ""
    echo -e "${GREEN}✓${NC} Cleanup analysis complete!"
    echo -e "📋 Review the checklist: ${BLUE}$CLEANUP_REPORT${NC}"
    echo ""
    
    # Ask if user wants interactive cleanup
    read -p "Start interactive cleanup? (y/N): " start_interactive
    if [[ $start_interactive =~ ^[Yy]$ ]]; then
        interactive_cleanup
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Code cleanup assistant finished!${NC}"
    echo -e "📝 Don't forget to review and check off items in: ${BLUE}$CLEANUP_REPORT${NC}"
}

# Run main function
main "$@"

