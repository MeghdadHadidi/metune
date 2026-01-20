#!/bin/bash
# Peachflow Post-Edit Hook
# Runs after file edits for formatting and notifications

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

# Check if this is a spec file with clarification markers
if echo "$FILE_PATH" | grep -q "specs/.*\.md$"; then
    CLARIFICATIONS=$(grep -c "NEEDS CLARIFICATION\|ASSUMPTION\|TBD\|TODO" "$FILE_PATH" 2>/dev/null || echo "0")
    if [[ "$CLARIFICATIONS" -gt 0 ]]; then
        echo "Note: $CLARIFICATIONS clarification markers in $FILE_PATH"
        echo "Consider running /peachflow.clarify"
    fi
fi

# Run formatters for code files (if available)
if [[ "$EXT" == "ts" || "$EXT" == "tsx" || "$EXT" == "js" || "$EXT" == "jsx" ]]; then
    # Check if in a node project with prettier
    if [[ -f "package.json" ]]; then
        if grep -q "prettier" package.json 2>/dev/null; then
            npx prettier --write "$FILE_PATH" 2>/dev/null || true
        fi
        if grep -q "eslint" package.json 2>/dev/null; then
            npx eslint --fix "$FILE_PATH" 2>/dev/null || true
        fi
    fi
fi

# Check for @peachflow tags in new code files
if [[ "$EXT" == "ts" || "$EXT" == "tsx" ]] && [[ -f "$FILE_PATH" ]]; then
    if ! grep -q "@peachflow" "$FILE_PATH" 2>/dev/null; then
        echo "Reminder: Add @peachflow tag to $FILE_PATH for traceability"
    fi
fi

exit 0
