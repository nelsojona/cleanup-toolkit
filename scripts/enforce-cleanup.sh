#!/bin/bash
# Enforce cleanup - prevent bypassing pre-commit hook

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║${NC}         CLEANUP ENFORCEMENT - NO BYPASSING ALLOWED          ${RED}║${NC}"
echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if trying to use --no-verify
if [[ "$@" == *"--no-verify"* ]]; then
    echo -e "${RED}❌ ERROR: --no-verify is DISABLED in this repository${NC}"
    echo ""
    echo -e "${YELLOW}Cleanup is MANDATORY. You must:${NC}"
    echo "  1. Complete the cleanup process"
    echo "  2. Stage your changes: git add ."
    echo "  3. Commit normally: git commit -m 'your message'"
    echo ""
    echo -e "${RED}Rules that MUST be followed:${NC}"
    echo "  • Remove ALL debug statements"
    echo "  • Delete unused code"
    echo "  • Add proper documentation"
    echo "  • Ensure error handling"
    echo ""
    exit 1
fi

# Run normal git commit
git commit "$@"