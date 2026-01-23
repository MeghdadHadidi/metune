#!/bin/bash
# State Manager for Peachflow 2
# Manages .peachflow-state.json for tracking project progress

STATE_FILE=".peachflow-state.json"

init_state() {
  local project_name="${1:-Untitled Project}"
  local project_type="${2:-new}"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << EOF
{
  "version": "2.0.0",
  "initialized": "$timestamp",
  "projectName": "$project_name",
  "projectType": "$project_type",
  "phases": {
    "discovery": { "status": "pending", "completedAt": null },
    "definition": { "status": "pending", "completedAt": null },
    "design": { "status": "pending", "completedAt": null },
    "plan": { "status": "pending", "completedAt": null }
  },
  "currentQuarter": null,
  "quarters": {},
  "requirements": {
    "planned": [],
    "unplanned": []
  },
  "features": [],
  "planUpdates": [],
  "lastUpdated": "$timestamp"
}
EOF
    echo "State initialized for '$project_name'"
  else
    echo "State file already exists"
  fi
}

# Project name management
get_project_name() {
  if [ -f "$STATE_FILE" ]; then
    jq -r '.projectName // "Untitled Project"' "$STATE_FILE"
  else
    echo "Untitled Project"
  fi
}

set_project_name() {
  local name="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    jq ".projectName = \"${name}\" | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Project name set to '$name'"
  else
    echo "Error: State file not found"
    exit 1
  fi
}

get_phase_status() {
  local phase="$1"
  if [ -f "$STATE_FILE" ]; then
    jq -r ".phases.${phase}.status // \"pending\"" "$STATE_FILE"
  else
    echo "pending"
  fi
}

set_phase_status() {
  local phase="$1"
  local status="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    local completed_at="null"
    if [ "$status" = "completed" ]; then
      completed_at="\"$timestamp\""
    fi

    jq ".phases.${phase}.status = \"${status}\" | .phases.${phase}.completedAt = ${completed_at} | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Phase '$phase' set to '$status'"
  else
    echo "Error: State file not found. Run 'init' first."
    exit 1
  fi
}

set_current_quarter() {
  local quarter="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    jq ".currentQuarter = \"${quarter}\" | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Current quarter set to '$quarter'"
  else
    echo "Error: State file not found"
    exit 1
  fi
}

get_current_quarter() {
  if [ -f "$STATE_FILE" ]; then
    jq -r ".currentQuarter // \"none\"" "$STATE_FILE"
  else
    echo "none"
  fi
}

# Quarter status management
set_quarter_status() {
  local quarter="$1"
  local status="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    # Ensure quarters object exists and set status
    jq ".quarters[\"${quarter}\"].status = \"${status}\" | .quarters[\"${quarter}\"].updatedAt = \"${timestamp}\" | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Quarter '$quarter' set to '$status'"
  else
    echo "Error: State file not found"
    exit 1
  fi
}

get_quarter_status() {
  local quarter="$1"
  if [ -f "$STATE_FILE" ]; then
    jq -r ".quarters[\"${quarter}\"].status // \"pending\"" "$STATE_FILE"
  else
    echo "pending"
  fi
}

# Get next quarter (Q1 -> Q2, etc.)
get_next_quarter() {
  local current="$1"
  if [ -z "$current" ] || [ "$current" = "none" ]; then
    echo "q01"
    return
  fi

  # Extract number from q01, q02, etc.
  local num=$(echo "$current" | sed 's/q0*//')
  local next=$((num + 1))
  printf "q%02d" "$next"
}

# Check if quarter has remaining tasks
get_quarter_progress() {
  local quarter="$1"
  local tasks_dir="docs/04-plan/quarters/${quarter}/tasks"

  if [ ! -d "$tasks_dir" ]; then
    echo "no_tasks"
    return
  fi

  local total=$(find "$tasks_dir" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  local completed=$(grep -l "status: completed" "$tasks_dir"/*.md 2>/dev/null | wc -l | tr -d ' ')
  local in_progress=$(grep -l "status: in_progress" "$tasks_dir"/*.md 2>/dev/null | wc -l | tr -d ' ')
  local pending=$((total - completed - in_progress))

  echo "${completed}/${total}:${in_progress}:${pending}"
}

# List all quarters with status
list_quarters() {
  if [ -f "$STATE_FILE" ]; then
    echo "=== Quarter Status ==="
    for dir in docs/04-plan/quarters/q*/; do
      if [ -d "$dir" ]; then
        quarter=$(basename "$dir")
        status=$(get_quarter_status "$quarter")
        progress=$(get_quarter_progress "$quarter")
        echo "  $quarter: $status ($progress completed/total)"
      fi
    done
  fi
}

# Worktree management
set_quarter_worktree() {
  local quarter="$1"
  local worktree_path="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    jq ".quarters[\"${quarter}\"].worktree = \"${worktree_path}\" | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Worktree for '$quarter' set to '$worktree_path'"
  fi
}

get_quarter_worktree() {
  local quarter="$1"
  if [ -f "$STATE_FILE" ]; then
    jq -r ".quarters[\"${quarter}\"].worktree // \"\"" "$STATE_FILE"
  fi
}

# Requirements tracking
get_planned() {
  if [ -f "$STATE_FILE" ]; then
    jq -r '.requirements.planned // [] | .[]' "$STATE_FILE"
  fi
}

get_unplanned() {
  if [ -f "$STATE_FILE" ]; then
    jq -r '.requirements.unplanned // [] | .[]' "$STATE_FILE"
  fi
}

add_to_planned() {
  local req_id="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    # Add to planned if not already there
    jq "if (.requirements.planned | index(\"${req_id}\")) then . else .requirements.planned += [\"${req_id}\"] end | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Added '$req_id' to planned"
  fi
}

add_to_unplanned() {
  local req_id="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    # Add to unplanned if not already there and not in planned
    jq "if ((.requirements.unplanned | index(\"${req_id}\")) or (.requirements.planned | index(\"${req_id}\"))) then . else .requirements.unplanned += [\"${req_id}\"] end | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Added '$req_id' to unplanned"
  fi
}

move_to_planned() {
  local req_id="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    # Remove from unplanned and add to planned
    jq ".requirements.unplanned -= [\"${req_id}\"] | if (.requirements.planned | index(\"${req_id}\")) then . else .requirements.planned += [\"${req_id}\"] end | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Moved '$req_id' to planned"
  fi
}

bulk_add_unplanned() {
  # Reads requirement IDs from stdin, one per line
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local ids=$(cat)

  if [ -f "$STATE_FILE" ] && [ -n "$ids" ]; then
    for req_id in $ids; do
      jq "if ((.requirements.unplanned | index(\"${req_id}\")) or (.requirements.planned | index(\"${req_id}\"))) then . else .requirements.unplanned += [\"${req_id}\"] end" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    done
    jq ".lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Added requirements to unplanned"
  fi
}

bulk_move_to_planned() {
  # Reads requirement IDs from stdin, one per line
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local ids=$(cat)

  if [ -f "$STATE_FILE" ] && [ -n "$ids" ]; then
    for req_id in $ids; do
      jq ".requirements.unplanned -= [\"${req_id}\"] | if (.requirements.planned | index(\"${req_id}\")) then . else .requirements.planned += [\"${req_id}\"] end" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    done
    jq ".lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Moved requirements to planned"
  fi
}

# Add plan update record
add_plan_update() {
  local added="$1"       # comma-separated list: BR-015,BR-016,F-020
  local quarters="$2"    # comma-separated list: Q1,Q2
  local migrations="$3"  # comma-separated list: M-001
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    # Convert comma-separated to JSON arrays
    local added_json=$(echo "$added" | tr ',' '\n' | jq -R . | jq -s .)
    local quarters_json=$(echo "$quarters" | tr ',' '\n' | jq -R . | jq -s .)
    local migrations_json=$(echo "$migrations" | tr ',' '\n' | jq -R . | jq -s .)

    jq ".planUpdates += [{\"date\": \"${timestamp}\", \"added\": ${added_json}, \"affectedQuarters\": ${quarters_json}, \"migrations\": ${migrations_json}}] | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Plan update recorded"
  fi
}

# Feature tracking
add_feature() {
  local feature_id="$1"
  local feature_name="$2"
  local discovery_type="${3:-full}"  # full or feature
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    jq ".features += [{\"id\": \"${feature_id}\", \"name\": \"${feature_name}\", \"addedAt\": \"${timestamp}\", \"discoveryType\": \"${discovery_type}\", \"status\": \"unplanned\"}] | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Feature '$feature_id' added"
  fi
}

set_feature_status() {
  local feature_id="$1"
  local status="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ -f "$STATE_FILE" ]; then
    jq "(.features[] | select(.id == \"${feature_id}\")).status = \"${status}\" | .lastUpdated = \"${timestamp}\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    echo "Feature '$feature_id' status set to '$status'"
  fi
}

get_requirements_summary() {
  if [ -f "$STATE_FILE" ]; then
    local planned=$(jq '.requirements.planned | length' "$STATE_FILE")
    local unplanned=$(jq '.requirements.unplanned | length' "$STATE_FILE")
    echo "planned:${planned},unplanned:${unplanned}"
  else
    echo "planned:0,unplanned:0"
  fi
}

show_status() {
  if [ -f "$STATE_FILE" ]; then
    project_name=$(jq -r '.projectName // "Untitled Project"' "$STATE_FILE")
    echo "=== $project_name - Project Status ==="
    echo ""
    project_type=$(jq -r ".projectType // \"unknown\"" "$STATE_FILE")
    echo "Project Type: $project_type"
    echo ""
    echo "Phases:"
    for phase in discovery definition design plan; do
      status=$(jq -r ".phases.${phase}.status" "$STATE_FILE")
      case "$status" in
        "completed") icon="[x]" ;;
        "in_progress") icon="[>]" ;;
        *) icon="[ ]" ;;
      esac
      echo "  $icon $phase: $status"
    done
    echo ""

    # Requirements summary
    planned=$(jq '.requirements.planned | length' "$STATE_FILE")
    unplanned=$(jq '.requirements.unplanned | length' "$STATE_FILE")
    echo "Requirements:"
    echo "  Planned: $planned"
    echo "  Unplanned: $unplanned"

    if [ "$unplanned" -gt 0 ]; then
      echo ""
      echo "  Unplanned IDs:"
      jq -r '.requirements.unplanned[]' "$STATE_FILE" | while read id; do
        echo "    - $id"
      done
    fi

    echo ""
    current=$(jq -r ".currentQuarter // \"none\"" "$STATE_FILE")
    echo "Current Quarter: $current"

    # List quarters if any
    if [ -d "docs/04-plan/quarters" ]; then
      echo ""
      echo "Quarters:"
      for dir in docs/04-plan/quarters/q*/; do
        if [ -d "$dir" ]; then
          quarter=$(basename "$dir")
          status=$(get_quarter_status "$quarter")
          progress=$(get_quarter_progress "$quarter")
          echo "  $quarter: $status ($progress)"
        fi
      done
    fi

    echo ""
    last=$(jq -r ".lastUpdated // \"never\"" "$STATE_FILE")
    echo "Last Updated: $last"
  else
    echo "No state file found. Run /peachflow:init to initialize."
  fi
}

# Main command handler
case "$1" in
  init)
    init_state "$2" "$3"
    ;;
  get-project-name)
    get_project_name
    ;;
  set-project-name)
    set_project_name "$2"
    ;;
  get-phase)
    get_phase_status "$2"
    ;;
  set-phase)
    set_phase_status "$2" "$3"
    ;;
  get-quarter)
    get_current_quarter
    ;;
  set-quarter)
    set_current_quarter "$2"
    ;;
  get-quarter-status)
    get_quarter_status "$2"
    ;;
  set-quarter-status)
    set_quarter_status "$2" "$3"
    ;;
  get-next-quarter)
    get_next_quarter "$2"
    ;;
  get-quarter-progress)
    get_quarter_progress "$2"
    ;;
  list-quarters)
    list_quarters
    ;;
  set-worktree)
    set_quarter_worktree "$2" "$3"
    ;;
  get-worktree)
    get_quarter_worktree "$2"
    ;;
  # Requirements tracking
  get-planned)
    get_planned
    ;;
  get-unplanned)
    get_unplanned
    ;;
  add-planned)
    add_to_planned "$2"
    ;;
  add-unplanned)
    add_to_unplanned "$2"
    ;;
  move-to-planned)
    move_to_planned "$2"
    ;;
  bulk-add-unplanned)
    bulk_add_unplanned
    ;;
  bulk-move-to-planned)
    bulk_move_to_planned
    ;;
  add-plan-update)
    add_plan_update "$2" "$3" "$4"
    ;;
  # Feature tracking
  add-feature)
    add_feature "$2" "$3" "$4"
    ;;
  set-feature-status)
    set_feature_status "$2" "$3"
    ;;
  get-requirements-summary)
    get_requirements_summary
    ;;
  status)
    show_status
    ;;
  *)
    echo "Usage: state-manager.sh <command> [args]"
    echo ""
    echo "Project Commands:"
    echo "  init <name> [type]          Initialize state file (type: new|existing|continued)"
    echo "  get-project-name            Get the project name"
    echo "  set-project-name <name>     Set the project name"
    echo "  status                      Show full project status"
    echo ""
    echo "Phase Commands:"
    echo "  get-phase <phase>           Get status of a phase"
    echo "  set-phase <phase> <status>  Set phase status"
    echo ""
    echo "Quarter Commands:"
    echo "  get-quarter                 Get current quarter"
    echo "  set-quarter <quarter>       Set current quarter"
    echo "  get-quarter-status <q>      Get quarter status"
    echo "  set-quarter-status <q> <s>  Set quarter status"
    echo "  get-next-quarter <current>  Get next quarter ID"
    echo "  get-quarter-progress <q>    Get completion stats"
    echo "  list-quarters               List all quarters with status"
    echo "  set-worktree <q> <path>     Set worktree path for quarter"
    echo "  get-worktree <q>            Get worktree path for quarter"
    echo ""
    echo "Requirements Commands:"
    echo "  get-planned                 List all planned requirement IDs"
    echo "  get-unplanned               List all unplanned requirement IDs"
    echo "  add-planned <id>            Add requirement to planned list"
    echo "  add-unplanned <id>          Add requirement to unplanned list"
    echo "  move-to-planned <id>        Move requirement from unplanned to planned"
    echo "  bulk-add-unplanned          Add multiple IDs to unplanned (stdin, one per line)"
    echo "  bulk-move-to-planned        Move multiple IDs to planned (stdin, one per line)"
    echo "  get-requirements-summary    Get planned/unplanned counts"
    echo ""
    echo "Feature Commands:"
    echo "  add-feature <id> <name> [type]  Add feature (type: full|feature)"
    echo "  set-feature-status <id> <s>     Set feature status"
    echo ""
    echo "Plan Update Commands:"
    echo "  add-plan-update <added> <quarters> <migrations>  Record plan update"
    exit 1
    ;;
esac
