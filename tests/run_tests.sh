#!/bin/sh

# BASIC Interpreter Test Runner
# Run from ./tests directory

SRC_DIR="../src"
MAIN="$SRC_DIR/main.py"

# Colours for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Colour

passed=0
failed=0
total=0

echo "========================================="
echo "  BASIC Interpreter Test Suite"
echo "========================================="
echo ""

# Debug: show current directory and check files
echo "Running from: $(pwd)"
echo "Looking for: $MAIN"
echo ""

# Check if main.py exists
if [ ! -f "$MAIN" ]; then
    echo "${RED}Error: $MAIN not found${NC}"
    echo "Contents of ../src:"
    ls -la ../src/ 2>/dev/null || echo "No ../src directory"
    exit 1
fi

# Run each .bas file in current directory
for testFile in *.bas; do
    if [ -f "$testFile" ]; then
        total=$((total + 1))
        testName=$(basename "$testFile")
        
        echo "${YELLOW}Test $total: $testName${NC}"
        echo "----------------------------------------"
        
        # Run the interpreter
        python3 "$MAIN" "$testFile"
        
        # Check exit code
        if [ $? -eq 0 ]; then
            echo "${GREEN}PASSED${NC}"
            passed=$((passed + 1))
        else
            echo "${RED}FAILED${NC}"
            failed=$((failed + 1))
        fi
        
        echo ""
    fi
done

echo "========================================="
echo "  Results: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC}, $total total"
echo "========================================="

# Exit with failure if any tests failed
if [ $failed -gt 0 ]; then
    exit 1
fi

exit 0

