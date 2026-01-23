#!/bin/bash
# State Manager for Peachflow 2
# Manages .peachflow-state.json for tracking project progress

STATE_FILE=".peachflow-state.json"

init_state() {
  if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'EOF'
{
  "version": "2.0.0",
  "phases": {
    "discovery": { "status": "pending", "completedAt": null },
    "definition": { "status": "pending", "completedAt": null },
    "design": { "status": "pending", "completedAt": null },
    "plan": { "status": "pending", "completedAt": null }
  },
  "currentQuarter": null,
  "quarters": {},
  "lastUpdated": null
}
EOF
    echo "State initialized"
  else
    echo "State file already exists"
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

show_status() {
  if [ -f "$STATE_FILE" ]; then
    echo "=== Peachflow Project Status ==="
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
    current=$(jq -r ".currentQuarter // \"none\"" "$STATE_FILE")
    echo "Current Quarter: $current"
    echo ""
    last=$(jq -r ".lastUpdated // \"never\"" "$STATE_FILE")
    echo "Last Updated: $last"
  else
    echo "No state file found. Run a phase command to initialize."
  fi
}

# Main command handler
case "$1" in
  init)
    init_state
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
  status)
    show_status
    ;;
  *)
    echo "Usage: state-manager.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  init                        Initialize state file"
    echo "  get-phase <phase>           Get status of a phase"
    echo "  set-phase <phase> <status>  Set phase status"
    echo "  get-quarter                 Get current quarter"
    echo "  set-quarter <quarter>       Set current quarter"
    echo "  get-quarter-status <q>      Get quarter status (pending|in_progress|completed)"
    echo "  set-quarter-status <q> <s>  Set quarter status"
    echo "  get-next-quarter <current>  Get next quarter ID"
    echo "  get-quarter-progress <q>    Get completion stats (completed/total:in_progress:pending)"
    echo "  list-quarters               List all quarters with status"
    echo "  set-worktree <q> <path>     Set worktree path for quarter"
    echo "  get-worktree <q>            Get worktree path for quarter"
    echo "  status                      Show full project status"
    exit 1
    ;;
esac
