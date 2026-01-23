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
  status)
    show_status
    ;;
  *)
    echo "Usage: state-manager.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  init                    Initialize state file"
    echo "  get-phase <phase>       Get status of a phase"
    echo "  set-phase <phase> <status>  Set phase status (pending|in_progress|completed)"
    echo "  get-quarter             Get current quarter"
    echo "  set-quarter <quarter>   Set current quarter (Q1, Q2, etc.)"
    echo "  status                  Show full project status"
    exit 1
    ;;
esac
