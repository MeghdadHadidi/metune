#!/bin/bash
# Session initialization for Peachflow 3
# Runs on SessionStart to show project status

STATE_FILE=".peachflow-state.json"

# Check if we're in a peachflow project
if [ -f "$STATE_FILE" ]; then
  echo "Peachflow 3 initialized."

  # Show brief status
  echo "Context: $(jq -r '.currentQuarter // "No quarter selected"' "$STATE_FILE")"
  echo ""
  echo "Available commands:"
  echo "  /peachflow:discover  - Start product discovery (BRD, PRD)"
  echo "  /peachflow:plan      - Create delivery plan & tasks"
  echo "  /peachflow:create-sprint - Start a new sprint"
  echo "  /peachflow:implement - Execute implementation tasks"
  echo "  /peachflow:status    - Show project status"
else
  echo "Peachflow 3 initialized."
  echo ""
  echo "No project state found. Start with:"
  echo "  /peachflow:discover \"your product idea\""
fi
