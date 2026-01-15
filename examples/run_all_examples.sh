#!/usr/bin/env bash

# Run All Examples Script

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' 

# Track results
TOTAL=0
SUCCESS=0
FAILED=0
FAILED_EXAMPLES=()

echo "======================================================================"
echo "Running All Indicator Examples"
echo "======================================================================"
echo ""

EXAMPLES=(
    "atomic_log"
    "derivable_interval_log"
    "explicit_interval_log"
    "uniquely_matched_derivable_interval_log"
    "production"
    "bpi_challenge_2013_incidents"
    "bpi_challenge_2017"
    "it_incident"
    "italian_help_desk"
)

# Get the script directory (examples directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Function to run a single example
run_example() {
    local example_name=$1
    local example_dir="${SCRIPT_DIR}/${example_name}"
    
    if [ ! -f "${example_dir}/indicators.py" ]; then
        echo -e "${YELLOW}⊘ Skipping ${example_name}: indicators.py not found${NC}"
        return
    fi
    
    TOTAL=$((TOTAL + 1))
    
    echo ""
    echo "======================================================================"
    echo -e "${BLUE}[${TOTAL}] Running: ${example_name}${NC}"
    echo "======================================================================"
    
    # Change to example directory and run (needs UV installed)
    if cd "${example_dir}" && uv run python indicators.py; then
        SUCCESS=$((SUCCESS + 1))
        echo -e "${GREEN}✓ ${example_name} completed successfully${NC}"
    else
        FAILED=$((FAILED + 1))
        FAILED_EXAMPLES+=("${example_name}")
        echo -e "${RED}✗ ${example_name} failed${NC}"
    fi
    
    # Return to project root
    cd "${PROJECT_ROOT}"
}

# Run all examples
for example in "${EXAMPLES[@]}"; do
    run_example "$example"
done

# Print summary
echo ""
echo "======================================================================"
echo "Summary"
echo "======================================================================"
echo -e "Total examples: ${TOTAL}"
echo -e "${GREEN}Successful: ${SUCCESS}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"

if [ ${FAILED} -gt 0 ]; then
    echo ""
    echo "Failed examples:"
    for failed_example in "${FAILED_EXAMPLES[@]}"; do
        echo -e "  ${RED}✗ ${failed_example}${NC}"
    done
    echo ""
    exit 1
else
    echo ""
    echo -e "${GREEN}✓ All examples completed successfully!${NC}"
    echo ""
    exit 0
fi
