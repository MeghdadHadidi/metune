#!/bin/bash
# Peachflow Session Initialization
# Detects context and provides helpful information

echo "Peachflow initialized."

# Check if in a worktree (feature branch)
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)

    # Check if this is a peachflow quarter branch
    if [[ "$BRANCH" =~ ^[0-9]{3}-Q[0-9]+ ]]; then
        QUARTER=$(echo "$BRANCH" | grep -oE "Q[0-9]+")
        echo "Context: Quarter branch detected"
        echo "  Branch: $BRANCH"
        echo "  Quarter: $QUARTER"

        # Check for tasks file
        if [[ -f "specs/quarterly/$QUARTER/tasks.md" ]]; then
            TOTAL=$(grep -c "^### T[0-9]" "specs/quarterly/$QUARTER/tasks.md" 2>/dev/null || echo "0")
            DONE=$(grep -c "\[x\].*complete\|Status: Done\|status: done" "specs/quarterly/$QUARTER/tasks.md" 2>/dev/null || echo "0")
            echo "  Tasks: $DONE/$TOTAL complete"
        fi

        # Check for uncommitted changes
        CHANGES=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        if [[ "$CHANGES" -gt 0 ]]; then
            echo "  Uncommitted: $CHANGES files"
        fi

        echo ""
        echo "Available commands:"
        echo "  /peachflow:implement next  - Continue implementation"
        echo "  /peachflow:test           - Run tests"
    else
        echo "Context: Main branch"

        # Check for discovery
        if [[ -d "specs/discovery" ]]; then
            echo "  Discovery: Found"
        fi

        # Check for quarterly plan
        if [[ -f "specs/quarterly/roadmap.md" ]]; then
            echo "  Roadmap: Found"
            QUARTERS=$(ls -d specs/quarterly/Q* 2>/dev/null | wc -l | tr -d ' ')
            echo "  Quarters planned: $QUARTERS"
        fi

        echo ""
        echo "Available commands:"
        echo "  /peachflow:discover  - Start product discovery"
        echo "  /peachflow:plan      - Create quarterly roadmap"
        echo "  /peachflow:plan Q1   - Plan specific quarter"
    fi
fi

exit 0
