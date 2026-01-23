#!/bin/bash
# Decision Manager for Peachflow
# Manages draft/final decisions with interview workflow

set -e

DECISIONS_FILE="docs/decisions.json"

# Initialize decisions file if not exists
init_decisions() {
  if [ ! -f "$DECISIONS_FILE" ]; then
    mkdir -p "$(dirname "$DECISIONS_FILE")"
    echo '{"decisions": []}' > "$DECISIONS_FILE"
    echo "Decisions file initialized"
  fi
}

# Add a draft decision
add_draft() {
  local id="$1"
  local category="$2"
  local question="$3"
  local recommendation="$4"
  local alternatives="$5"  # JSON array string
  local rationale="$6"
  local source_doc="$7"

  init_decisions

  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Create decision JSON
  local decision=$(cat <<EOF
{
  "id": "$id",
  "category": "$category",
  "question": "$question",
  "recommendation": "$recommendation",
  "alternatives": $alternatives,
  "rationale": "$rationale",
  "sourceDocument": "$source_doc",
  "status": "draft",
  "finalChoice": null,
  "createdAt": "$timestamp",
  "finalizedAt": null
}
EOF
)

  # Add to decisions array
  jq ".decisions += [$decision]" "$DECISIONS_FILE" > "${DECISIONS_FILE}.tmp" && mv "${DECISIONS_FILE}.tmp" "$DECISIONS_FILE"

  echo "Draft decision added: $id"
}

# Get all draft decisions
get_drafts() {
  init_decisions
  jq -r '.decisions[] | select(.status == "draft") | "\(.id): \(.question) [Recommended: \(.recommendation)]"' "$DECISIONS_FILE"
}

# Get decision by ID
get_decision() {
  local id="$1"
  init_decisions
  jq ".decisions[] | select(.id == \"$id\")" "$DECISIONS_FILE"
}

# Finalize a decision
finalize_decision() {
  local id="$1"
  local final_choice="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  init_decisions

  jq "(.decisions[] | select(.id == \"$id\")) |= . + {\"status\": \"final\", \"finalChoice\": \"$final_choice\", \"finalizedAt\": \"$timestamp\"}" "$DECISIONS_FILE" > "${DECISIONS_FILE}.tmp" && mv "${DECISIONS_FILE}.tmp" "$DECISIONS_FILE"

  echo "Decision finalized: $id = $final_choice"
}

# List all decisions
list_decisions() {
  local status="${1:-all}"
  init_decisions

  echo "=== Decisions ($status) ==="
  echo ""

  if [ "$status" = "all" ]; then
    jq -r '.decisions[] | "[\(.status)] \(.id): \(.question)\n  → \(if .status == "final" then .finalChoice else .recommendation + " (draft)" end)\n"' "$DECISIONS_FILE"
  elif [ "$status" = "draft" ]; then
    jq -r '.decisions[] | select(.status == "draft") | "\(.id): \(.question)\n  Recommendation: \(.recommendation)\n  Alternatives: \(.alternatives | join(", "))\n"' "$DECISIONS_FILE"
  elif [ "$status" = "final" ]; then
    jq -r '.decisions[] | select(.status == "final") | "\(.id): \(.question)\n  Final: \(.finalChoice)\n"' "$DECISIONS_FILE"
  fi
}

# Generate interview format for pending decisions
generate_interview() {
  init_decisions

  local drafts=$(jq -r '.decisions[] | select(.status == "draft")' "$DECISIONS_FILE")

  if [ -z "$drafts" ]; then
    echo "No draft decisions pending"
    exit 0
  fi

  echo "=== Decision Review Interview ==="
  echo ""
  echo "The following decisions have been drafted and need your approval:"
  echo ""

  jq -r '.decisions[] | select(.status == "draft") | "---\nDecision: \(.id)\nCategory: \(.category)\nQuestion: \(.question)\n\nRecommendation: \(.recommendation)\nRationale: \(.rationale)\n\nAlternatives:\n\(.alternatives | to_entries | map("  \(.key + 1). \(.value)") | join("\n"))\n\nSource: \(.sourceDocument)\n"' "$DECISIONS_FILE"

  echo "---"
  echo ""
  echo "To finalize decisions, use:"
  echo "  decision-manager.sh finalize <ID> \"<choice>\""
}

# Export decisions to markdown
export_to_markdown() {
  local output_file="${1:-docs/decision-log.md}"
  init_decisions

  cat > "$output_file" << 'EOF'
# Decision Log

This document tracks all decisions made during the project.

## Summary

EOF

  # Count by status
  local total=$(jq '.decisions | length' "$DECISIONS_FILE")
  local final=$(jq '[.decisions[] | select(.status == "final")] | length' "$DECISIONS_FILE")
  local draft=$(jq '[.decisions[] | select(.status == "draft")] | length' "$DECISIONS_FILE")

  echo "- Total decisions: $total" >> "$output_file"
  echo "- Finalized: $final" >> "$output_file"
  echo "- Pending review: $draft" >> "$output_file"
  echo "" >> "$output_file"

  echo "## Decisions" >> "$output_file"
  echo "" >> "$output_file"

  jq -r '.decisions[] | "### \(.id): \(.question)\n\n**Status**: \(.status)\n**Category**: \(.category)\n\n**Recommendation**: \(.recommendation)\n\n**Rationale**: \(.rationale)\n\n**Final Choice**: \(if .finalChoice then .finalChoice else "_Pending_" end)\n\n**Alternatives Considered**:\n\(.alternatives | map("- \(.)") | join("\n"))\n\n**Source**: \(.sourceDocument)\n\n---\n"' "$DECISIONS_FILE" >> "$output_file"

  echo "Exported to $output_file"
}

# Get pending decision count
pending_count() {
  init_decisions
  jq '[.decisions[] | select(.status == "draft")] | length' "$DECISIONS_FILE"
}

# Main command handler
case "$1" in
  init)
    init_decisions
    ;;
  add)
    add_draft "$2" "$3" "$4" "$5" "$6" "$7" "$8"
    ;;
  get)
    get_decision "$2"
    ;;
  finalize)
    finalize_decision "$2" "$3"
    ;;
  list)
    list_decisions "$2"
    ;;
  drafts)
    get_drafts
    ;;
  interview)
    generate_interview
    ;;
  export)
    export_to_markdown "$2"
    ;;
  pending)
    pending_count
    ;;
  *)
    echo "Peachflow Decision Manager"
    echo ""
    echo "Usage: decision-manager.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  init                          Initialize decisions file"
    echo "  add <id> <category> <question> <recommendation> <alternatives_json> <rationale> <source>"
    echo "                                Add a draft decision"
    echo "  get <id>                      Get decision by ID"
    echo "  finalize <id> <choice>        Finalize a decision"
    echo "  list [status]                 List decisions (all, draft, final)"
    echo "  drafts                        List only draft decisions"
    echo "  interview                     Generate interview format for review"
    echo "  export [file]                 Export to markdown"
    echo "  pending                       Count pending decisions"
    echo ""
    echo "Example:"
    echo "  decision-manager.sh add \"DEC-001\" \"Technology\" \"Which database?\" \"PostgreSQL\" '[\"MongoDB\", \"MySQL\"]' \"Better for relational data\" \"architecture.md\""
    echo "  decision-manager.sh finalize \"DEC-001\" \"PostgreSQL\""
    exit 1
    ;;
esac
