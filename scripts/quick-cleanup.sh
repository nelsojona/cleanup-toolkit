#!/bin/bash

# Quick Cleanup Script - Handle edge cases intelligently
# For minimal changes, hotfixes, and already-clean code

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get change statistics
get_change_stats() {
    local stats=$(git diff --cached --stat | tail -1)
    echo "$stats"
}

# Check if changes are minimal
is_minimal() {
    local changes=$(git diff --cached --stat | tail -1)
    local files=$(echo "$changes" | grep -oE '[0-9]+ file' | grep -oE '[0-9]+' || echo 0)
    local lines=$(echo "$changes" | grep -oE '[0-9]+ (insertion|deletion)' | grep -oE '[0-9]+' | paste -sd+ | bc 2>/dev/null || echo 0)
    
    if [ "$files" -le 2 ] && [ "$lines" -le 10 ]; then
        return 0
    fi
    return 1
}

# Quick scan for issues
quick_scan() {
    local has_issues=false
    local staged_files=$(git diff --cached --name-only)
    
    for file in $staged_files; do
        if [ -f "$file" ]; then
            # Skip generated files
            if [[ "$file" =~ \.(min|bundle|dist|build)\. ]] || [[ "$file" =~ ^(dist|build|node_modules)/ ]]; then
                echo -e "${CYAN}[SKIP]${NC} $file (generated)"
                continue
            fi
            
            # Quick check for debug statements
            if grep -q "console\.log\|print(\|debugger" "$file" 2>/dev/null; then
                echo -e "${YELLOW}[WARN]${NC} Debug statements in $file"
                has_issues=true
            fi
        fi
    done
    
    return $([ "$has_issues" = true ] && echo 1 || echo 0)
}

# Main
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}    Quick Cleanup Assessment${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# Show change summary
echo -e "${BLUE}Changes:${NC} $(get_change_stats)"
echo ""

# Check if minimal
if is_minimal; then
    echo -e "${GREEN}✓ Minimal change detected${NC}"
    echo ""
fi

# Run quick scan
echo -e "${BLUE}Scanning for issues...${NC}"
if quick_scan; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✓ No cleanup issues found!       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
    echo ""
    echo "You can commit with:"
    echo -e "  ${GREEN}git commit --cleanup-done -m 'your message'${NC}"
    echo ""
    
    # Mark cleanup as done
    mkdir -p .cleanup-toolkit
    touch .cleanup-toolkit/.cleanup-done
else
    echo ""
    echo -e "${YELLOW}⚠ Issues found - please fix before committing${NC}"
    echo ""
    echo "After fixing, run this script again or:"
    echo "  git add ."
    echo "  git commit"
fi