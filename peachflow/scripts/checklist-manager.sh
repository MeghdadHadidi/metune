#!/bin/bash
# Checklist Manager for Peachflow 2
# Updates checkboxes and task statuses in markdown documents

# Toggle a checkbox in a markdown file
# Usage: toggle_checkbox <file> <item_pattern> [checked|unchecked]
toggle_checkbox() {
  local file="$1"
  local pattern="$2"
  local state="${3:-toggle}"

  if [ ! -f "$file" ]; then
    echo "Error: File not found: $file"
    exit 1
  fi

  case "$state" in
    checked|done|complete)
      # Change [ ] to [x]
      sed -i.bak "s/\[ \] \(.*${pattern}.*\)/[x] \1/g" "$file"
      ;;
    unchecked|undone|pending)
      # Change [x] to [ ]
      sed -i.bak "s/\[x\] \(.*${pattern}.*\)/[ ] \1/g" "$file"
      ;;
    toggle)
      # Toggle state - if checked, uncheck; if unchecked, check
      if grep -q "\[x\] .*${pattern}" "$file"; then
        sed -i.bak "s/\[x\] \(.*${pattern}.*\)/[ ] \1/g" "$file"
      else
        sed -i.bak "s/\[ \] \(.*${pattern}.*\)/[x] \1/g" "$file"
      fi
      ;;
    *)
      echo "Error: Invalid state '$state'. Use: checked, unchecked, or toggle"
      exit 1
      ;;
  esac

  rm -f "${file}.bak"
  echo "Updated checkbox for '$pattern' in $file"
}

# Update task status in a task file
# Usage: update_task_status <file> <new_status>
update_task_status() {
  local file="$1"
  local new_status="$2"

  if [ ! -f "$file" ]; then
    echo "Error: File not found: $file"
    exit 1
  fi

  # Valid statuses
  case "$new_status" in
    pending|in_progress|completed|deferred)
      sed -i.bak "s/^status: .*/status: ${new_status}/" "$file"
      rm -f "${file}.bak"
      echo "Task status updated to: $new_status"
      ;;
    *)
      echo "Error: Invalid status '$new_status'"
      echo "Valid statuses: pending, in_progress, completed, deferred"
      exit 1
      ;;
  esac
}

# Count checkboxes in a file
# Usage: count_checkboxes <file>
count_checkboxes() {
  local file="$1"

  if [ ! -f "$file" ]; then
    echo "Error: File not found: $file"
    exit 1
  fi

  local total=$(grep -c '\[[ x]\]' "$file" 2>/dev/null || echo "0")
  local checked=$(grep -c '\[x\]' "$file" 2>/dev/null || echo "0")
  local unchecked=$((total - checked))

  echo "Total: $total | Checked: $checked | Unchecked: $unchecked"

  if [ "$total" -gt 0 ]; then
    local percent=$((checked * 100 / total))
    echo "Progress: ${percent}%"
  fi
}

# Find all unchecked items in a file
# Usage: list_unchecked <file>
list_unchecked() {
  local file="$1"

  if [ ! -f "$file" ]; then
    echo "Error: File not found: $file"
    exit 1
  fi

  echo "Unchecked items in $file:"
  grep '\[ \]' "$file" | while read -r line; do
    echo "  $line"
  done
}

# Find all tasks with a specific tag
# Usage: find_tagged <directory> <tag>
find_tagged() {
  local dir="$1"
  local tag="$2"

  if [ ! -d "$dir" ]; then
    echo "Error: Directory not found: $dir"
    exit 1
  fi

  echo "Tasks tagged with [$tag]:"
  grep -r "\[$tag\]" "$dir" --include="*.md" | while read -r line; do
    echo "  $line"
  done
}

# Main command handler
case "$1" in
  toggle)
    toggle_checkbox "$2" "$3" "${4:-toggle}"
    ;;
  check)
    toggle_checkbox "$2" "$3" "checked"
    ;;
  uncheck)
    toggle_checkbox "$2" "$3" "unchecked"
    ;;
  status)
    update_task_status "$2" "$3"
    ;;
  count)
    count_checkboxes "$2"
    ;;
  unchecked)
    list_unchecked "$2"
    ;;
  find-tagged)
    find_tagged "$2" "$3"
    ;;
  *)
    echo "Usage: checklist-manager.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  toggle <file> <pattern> [state]   Toggle/set checkbox state"
    echo "  check <file> <pattern>            Mark checkbox as checked"
    echo "  uncheck <file> <pattern>          Mark checkbox as unchecked"
    echo "  status <file> <status>            Update task status field"
    echo "  count <file>                      Count checkboxes in file"
    echo "  unchecked <file>                  List all unchecked items"
    echo "  find-tagged <dir> <tag>           Find tasks with tag (FE, BE, DevOps)"
    echo ""
    echo "States: checked, unchecked, toggle (default)"
    echo "Statuses: pending, in_progress, completed, deferred"
    exit 1
    ;;
esac
