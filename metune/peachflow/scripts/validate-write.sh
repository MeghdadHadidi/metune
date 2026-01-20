#!/bin/bash
# Peachflow Pre-Write Validation
# Validates file writes for safety

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Block writes to sensitive files
SENSITIVE_PATTERNS=(
    "\.env$"
    "\.env\."
    "credentials"
    "secrets"
    "\.pem$"
    "\.key$"
    "password"
    "\.aws/"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if echo "$FILE_PATH" | grep -qiE "$pattern"; then
        echo "Blocked: Writing to sensitive file pattern '$pattern'" >&2
        echo "File: $FILE_PATH" >&2
        exit 2
    fi
done

# Warn if writing outside specs or src
if [[ ! "$FILE_PATH" =~ ^.*/specs/ ]] && [[ ! "$FILE_PATH" =~ ^.*/src/ ]] && [[ ! "$FILE_PATH" =~ ^.*/poc/ ]]; then
    # Just a warning, don't block
    echo "Note: Writing file outside specs/src/poc directories" >&2
fi

exit 0
