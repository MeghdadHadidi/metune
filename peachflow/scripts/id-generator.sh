#!/bin/bash
# ID Generator for Peachflow
# Generates sequential IDs for requirements, epics, stories, tasks

set -e

DOCS_DIR="docs"

# Get next ID for a type
get_next_id() {
  local type="$1"
  local prefix=""
  local search_pattern=""
  local search_dir=""

  case "$type" in
    br|business)
      prefix="BR"
      search_pattern="BR-[0-9]+"
      search_dir="$DOCS_DIR/01-business/"
      ;;
    f|feature)
      prefix="F"
      search_pattern="F-[0-9]+"
      search_dir="$DOCS_DIR/02-product/"
      ;;
    fr|functional)
      prefix="FR"
      search_pattern="FR-[0-9]+"
      search_dir="$DOCS_DIR/03-requirements/"
      ;;
    nfr|nonfunctional)
      prefix="NFR"
      search_pattern="NFR-[0-9]+"
      search_dir="$DOCS_DIR/03-requirements/"
      ;;
    e|epic)
      prefix="E"
      search_pattern="E-[0-9]+"
      search_dir="$DOCS_DIR/04-plan/"
      ;;
    us|story)
      prefix="US"
      search_pattern="US-[0-9]+"
      search_dir="$DOCS_DIR/04-plan/quarters/"
      ;;
    t|task)
      prefix="T"
      search_pattern="T-[0-9]+"
      search_dir="$DOCS_DIR/04-plan/quarters/"
      ;;
    dec|decision)
      prefix="DEC"
      search_pattern="DEC-[0-9]+"
      search_dir="$DOCS_DIR/"
      ;;
    *)
      echo "Unknown type: $type"
      echo "Valid types: br, f, fr, nfr, e, us, t, dec"
      exit 1
      ;;
  esac

  # Find highest existing ID
  local max_id=0
  if [ -d "$search_dir" ]; then
    local ids=$(grep -rhoE "$search_pattern" "$search_dir" --include="*.md" 2>/dev/null | sort -u)
    for id in $ids; do
      local num=$(echo "$id" | grep -oE "[0-9]+" | head -1)
      if [ "$num" -gt "$max_id" ] 2>/dev/null; then
        max_id=$num
      fi
    done
  fi

  local next_id=$((max_id + 1))
  printf "%s-%03d\n" "$prefix" "$next_id"
}

# Get next ADR number
get_next_adr() {
  local adr_dir="$DOCS_DIR/02-product/architecture/adr"
  local max_num=0

  if [ -d "$adr_dir" ]; then
    for f in "$adr_dir"/*.md; do
      if [ -f "$f" ]; then
        local num=$(basename "$f" | grep -oE "^[0-9]+" | head -1)
        if [ "$num" -gt "$max_num" ] 2>/dev/null; then
          max_num=$num
        fi
      fi
    done
  fi

  local next_num=$((max_num + 1))
  printf "%04d\n" "$next_num"
}

# Generate task filename
get_task_filename() {
  local quarter="$1"
  local task_dir="$DOCS_DIR/04-plan/quarters/${quarter}/tasks"
  local max_num=0

  if [ -d "$task_dir" ]; then
    for f in "$task_dir"/*.md; do
      if [ -f "$f" ]; then
        local num=$(basename "$f" .md | grep -oE "^[0-9]+" | head -1)
        if [ "$num" -gt "$max_num" ] 2>/dev/null; then
          max_num=$num
        fi
      fi
    done
  fi

  local next_num=$((max_num + 1))
  printf "%03d.md\n" "$next_num"
}

# Batch generate IDs
batch_generate() {
  local type="$1"
  local count="${2:-5}"

  echo "Generating $count IDs for $type:"
  for i in $(seq 1 $count); do
    get_next_id "$type"
    # Simulate adding to file to increment
  done
}

# Main command handler
case "$1" in
  next)
    get_next_id "$2"
    ;;
  adr)
    get_next_adr
    ;;
  task-file)
    get_task_filename "$2"
    ;;
  batch)
    batch_generate "$2" "$3"
    ;;
  *)
    echo "Peachflow ID Generator"
    echo ""
    echo "Usage: id-generator.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  next <type>           Get next ID (br, f, fr, nfr, e, us, t, dec)"
    echo "  adr                   Get next ADR number (0001, 0002, ...)"
    echo "  task-file <quarter>   Get next task filename for quarter (001.md, 002.md, ...)"
    echo ""
    echo "Examples:"
    echo "  id-generator.sh next fr        # Returns FR-001, FR-002, etc."
    echo "  id-generator.sh adr            # Returns 0001, 0002, etc."
    echo "  id-generator.sh task-file q01  # Returns 001.md, 002.md, etc."
    exit 1
    ;;
esac
