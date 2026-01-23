#!/bin/bash
# Session initialization for Peachflow 2
# Runs on SessionStart to show project status

STATE_FILE=".peachflow-state.json"

# Check if we're in a peachflow project
if [ -f "$STATE_FILE" ]; then
  echo "Peachflow 2 initialized."

  # Show brief status
  echo "Context: $(jq -r '.currentQuarter // "No quarter selected"' "$STATE_FILE")"
  echo ""
  echo "Available commands:"
  echo "  /peachflow:discover  - Start product discovery (BRD, PRD)"
  echo "  /peachflow:define    - Define requirements (FRD, NFRs)"
  echo "  /peachflow:design    - Create design specs (UX, Architecture)"
  echo "  /peachflow:plan      - Create delivery plan"
  echo "  /peachflow:plan Q1   - Plan specific quarter"
  echo "  /peachflow:implement - Execute implementation tasks"
  echo "  /peachflow:status    - Show project status"
else
  echo "Peachflow 2 initialized."
  echo ""
  echo "No project state found. Start with:"
  echo "  /peachflow:discover \"your product idea\""
fi
