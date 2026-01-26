#!/bin/bash
# Sprint Manager for Peachflow 2
# Manages sprint files and task queries to minimize context usage

DOCS_DIR="docs/04-plan/quarters"

# Helper: Get sprint file path
get_sprint_path() {
  local quarter="$1"
  local sprint="$2"
  echo "${DOCS_DIR}/${quarter}/${sprint}.md"
}

# Helper: Parse task from sprint file
# Returns: id|title|description|depends_on|parallel_with|status
parse_task() {
  local sprint_file="$1"
  local task_id="$2"

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  # Extract task block using awk
  awk -v tid="$task_id" '
    /^### '"$task_id"':/ {
      found=1
      title=$0
      sub(/^### /, "", title)
      getline desc
      deps=""
      parallel=""
      status="pending"
      while (getline > 0) {
        if (/^### T-[0-9]+:/) { break }
        if (/^\*\*Depends on:\*\*/) {
          deps=$0
          sub(/^\*\*Depends on:\*\* */, "", deps)
        }
        if (/^\*\*Parallel with:\*\*/) {
          parallel=$0
          sub(/^\*\*Parallel with:\*\* */, "", parallel)
        }
        if (/^\*\*Status:\*\*/) {
          status=$0
          sub(/^\*\*Status:\*\* */, "", status)
        }
      }
      print title "|" desc "|" deps "|" parallel "|" status
      exit
    }
  ' "$sprint_file"
}

# List all tasks in a sprint (minimal: id, title, status)
list_tasks() {
  local quarter="$1"
  local sprint="$2"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found: $sprint_file"
    return 1
  fi

  echo "=== Tasks in ${quarter}/${sprint} ==="
  grep -E "^### T-[0-9]+:" "$sprint_file" | while read -r line; do
    task_id=$(echo "$line" | grep -oE "T-[0-9]+")
    title=$(echo "$line" | sed 's/^### //')

    # Check if task is marked complete (has Status: completed)
    status=$(awk -v tid="$task_id" '
      /^### '"$task_id"':/ { found=1; next }
      found && /^### T-[0-9]+:/ { exit }
      found && /^\*\*Status:\*\* completed/ { print "completed"; exit }
      END { if (found) print "pending" }
    ' "$sprint_file")

    if [ "$status" = "completed" ]; then
      echo "[x] $title"
    else
      echo "[ ] $title"
    fi
  done
}

# Get pending tasks only (not completed)
pending_tasks() {
  local quarter="$1"
  local sprint="$2"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  echo "=== Pending Tasks ==="
  grep -E "^### T-[0-9]+:" "$sprint_file" | while read -r line; do
    task_id=$(echo "$line" | grep -oE "T-[0-9]+")
    title=$(echo "$line" | sed 's/^### //')

    # Check if NOT completed
    is_completed=$(awk -v tid="$task_id" '
      /^### '"$task_id"':/ { found=1; next }
      found && /^### T-[0-9]+:/ { exit }
      found && /^\*\*Status:\*\* completed/ { print "yes"; exit }
    ' "$sprint_file")

    if [ -z "$is_completed" ]; then
      echo "- $title"
    fi
  done
}

# Get tasks ready to execute (pending + no unfinished dependencies)
ready_tasks() {
  local quarter="$1"
  local sprint="$2"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  # First, get list of completed task IDs
  local completed_ids=$(awk '
    /^### T-[0-9]+:/ { current=$0; sub(/^### /, "", current); sub(/:.*/, "", current) }
    /^\*\*Status:\*\* completed/ { print current }
  ' "$sprint_file")

  echo "=== Ready Tasks (no blocking dependencies) ==="

  # For each pending task, check if dependencies are all completed
  grep -E "^### T-[0-9]+:" "$sprint_file" | while read -r line; do
    task_id=$(echo "$line" | grep -oE "T-[0-9]+")
    title=$(echo "$line" | sed 's/^### //')

    # Get status and dependencies
    task_info=$(awk -v tid="$task_id" '
      /^### '"$task_id"':/ { found=1; status="pending"; deps=""; next }
      found && /^### T-[0-9]+:/ { exit }
      found && /^\*\*Status:\*\*/ {
        status=$0
        sub(/^\*\*Status:\*\* */, "", status)
      }
      found && /^\*\*Depends on:\*\*/ {
        deps=$0
        sub(/^\*\*Depends on:\*\* */, "", deps)
      }
      END { if (found) print status "|" deps }
    ' "$sprint_file")

    status=$(echo "$task_info" | cut -d'|' -f1)
    deps=$(echo "$task_info" | cut -d'|' -f2)

    # Skip if completed
    if [ "$status" = "completed" ]; then
      continue
    fi

    # If no dependencies or deps is "none", task is ready
    if [ -z "$deps" ] || [ "$deps" = "none" ]; then
      echo "- $title"
      continue
    fi

    # Check if all dependencies are completed
    all_deps_done=true
    for dep in $(echo "$deps" | tr ',' '\n' | tr -d ' '); do
      if [ -n "$dep" ] && [ "$dep" != "none" ]; then
        if ! echo "$completed_ids" | grep -q "^${dep}$"; then
          all_deps_done=false
          break
        fi
      fi
    done

    if [ "$all_deps_done" = true ]; then
      echo "- $title"
    fi
  done
}

# Get single task details (for agent context)
get_task() {
  local quarter="$1"
  local task_id="$2"

  # Search all sprint files in quarter
  for sprint_file in "${DOCS_DIR}/${quarter}"/sprint*.md; do
    if [ -f "$sprint_file" ]; then
      if grep -q "^### ${task_id}:" "$sprint_file"; then
        # Extract full task block
        awk -v tid="$task_id" '
          /^### '"$task_id"':/ {
            found=1
            print
            next
          }
          found && /^### T-[0-9]+:/ { exit }
          found { print }
        ' "$sprint_file"
        return 0
      fi
    fi
  done

  echo "ERROR: Task $task_id not found in $quarter"
  return 1
}

# Get sprint status and summary
sprint_status() {
  local quarter="$1"
  local sprint="$2"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  # Extract frontmatter
  local id=$(awk '/^id:/ {print $2; exit}' "$sprint_file")
  local name=$(awk -F': ' '/^name:/ {gsub(/"/, "", $2); print $2; exit}' "$sprint_file")
  local status=$(awk '/^status:/ {print $2; exit}' "$sprint_file")

  # Count tasks
  local total=$(grep -cE "^### T-[0-9]+:" "$sprint_file" || echo 0)
  local completed=$(grep -cE "^\*\*Status:\*\* completed" "$sprint_file" || echo 0)
  local pending=$((total - completed))

  echo "Sprint: $id - $name"
  echo "Status: $status"
  echo "Progress: $completed/$total completed ($pending pending)"
}

# Complete a task (mark as done)
complete_task() {
  local quarter="$1"
  local sprint="$2"
  local task_id="$3"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  # Check if task exists
  if ! grep -q "^### ${task_id}:" "$sprint_file"; then
    echo "ERROR: Task $task_id not found in sprint"
    return 1
  fi

  # Add or update Status line after task description
  awk -v tid="$task_id" '
    /^### '"$task_id"':/ {
      intask=1
      print
      getline
      print
      # Check if Status line exists
      if (/^\*\*Status:\*\*/) {
        print "**Status:** completed"
        getline
      } else {
        print "**Status:** completed"
      }
      next
    }
    intask && /^### T-[0-9]+:/ { intask=0 }
    intask && /^\*\*Status:\*\*/ { next }
    { print }
  ' "$sprint_file" > "${sprint_file}.tmp" && mv "${sprint_file}.tmp" "$sprint_file"

  echo "Task $task_id marked as completed"
}

# Get tasks by tag (FE, BE, DevOps)
tasks_by_tag() {
  local quarter="$1"
  local sprint="$2"
  local tag="$3"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  echo "=== [$tag] Tasks ==="
  grep -E "^### T-[0-9]+:.*\[$tag\]" "$sprint_file" | while read -r line; do
    title=$(echo "$line" | sed 's/^### //')
    echo "- $title"
  done
}

# List all sprints in a quarter
list_sprints() {
  local quarter="$1"
  local quarter_dir="${DOCS_DIR}/${quarter}"

  if [ ! -d "$quarter_dir" ]; then
    echo "ERROR: Quarter directory not found: $quarter_dir"
    return 1
  fi

  echo "=== Sprints in $quarter ==="
  for sprint_file in "${quarter_dir}"/sprint*.md; do
    if [ -f "$sprint_file" ]; then
      local sprint=$(basename "$sprint_file" .md)
      local id=$(awk '/^id:/ {print $2; exit}' "$sprint_file")
      local name=$(awk -F': ' '/^name:/ {gsub(/"/, "", $2); print $2; exit}' "$sprint_file")
      local status=$(awk '/^status:/ {print $2; exit}' "$sprint_file")
      local total=$(grep -cE "^### T-[0-9]+:" "$sprint_file" || echo 0)
      local completed=$(grep -cE "^\*\*Status:\*\* completed" "$sprint_file" || echo 0)

      echo "$id: $name [$status] ($completed/$total)"
    fi
  done
}

# Get next sprint to work on (first non-completed)
next_sprint() {
  local quarter="$1"
  local quarter_dir="${DOCS_DIR}/${quarter}"

  if [ ! -d "$quarter_dir" ]; then
    echo "none"
    return 0
  fi

  for sprint_file in "${quarter_dir}"/sprint*.md; do
    if [ -f "$sprint_file" ]; then
      local status=$(awk '/^status:/ {print $2; exit}' "$sprint_file")
      if [ "$status" != "completed" ]; then
        basename "$sprint_file" .md
        return 0
      fi
    fi
  done

  echo "none"
}

# Update sprint status
set_sprint_status() {
  local quarter="$1"
  local sprint="$2"
  local new_status="$3"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ ! -f "$sprint_file" ]; then
    echo "ERROR: Sprint file not found"
    return 1
  fi

  # Update status and last_updated in frontmatter
  awk -v status="$new_status" -v ts="$timestamp" '
    /^status:/ { print "status: " status; next }
    /^last_updated:/ { print "last_updated: " ts; next }
    { print }
  ' "$sprint_file" > "${sprint_file}.tmp" && mv "${sprint_file}.tmp" "$sprint_file"

  echo "Sprint $sprint status set to $new_status"
}

# Check if sprint is complete (all tasks done)
is_sprint_complete() {
  local quarter="$1"
  local sprint="$2"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    echo "false"
    return 0
  fi

  local total=$(grep -cE "^### T-[0-9]+:" "$sprint_file" || echo 0)
  local completed=$(grep -cE "^\*\*Status:\*\* completed" "$sprint_file" || echo 0)

  if [ "$total" -eq "$completed" ] && [ "$total" -gt 0 ]; then
    echo "true"
  else
    echo "false"
  fi
}

# Get all task IDs from a sprint
get_task_ids() {
  local quarter="$1"
  local sprint="$2"
  local sprint_file=$(get_sprint_path "$quarter" "$sprint")

  if [ ! -f "$sprint_file" ]; then
    return 1
  fi

  grep -oE "^### T-[0-9]+:" "$sprint_file" | grep -oE "T-[0-9]+"
}

# Main command handler
case "$1" in
  list-tasks)
    list_tasks "$2" "$3"
    ;;
  pending-tasks)
    pending_tasks "$2" "$3"
    ;;
  ready-tasks)
    ready_tasks "$2" "$3"
    ;;
  get-task)
    get_task "$2" "$3"
    ;;
  complete-task)
    complete_task "$2" "$3" "$4"
    ;;
  by-tag)
    tasks_by_tag "$2" "$3" "$4"
    ;;
  status)
    sprint_status "$2" "$3"
    ;;
  list-sprints)
    list_sprints "$2"
    ;;
  next-sprint)
    next_sprint "$2"
    ;;
  set-status)
    set_sprint_status "$2" "$3" "$4"
    ;;
  is-complete)
    is_sprint_complete "$2" "$3"
    ;;
  get-task-ids)
    get_task_ids "$2" "$3"
    ;;
  *)
    echo "Sprint Manager - Query tasks from sprint files"
    echo ""
    echo "Usage: sprint-manager.sh <command> [args]"
    echo ""
    echo "Task Commands:"
    echo "  list-tasks <quarter> <sprint>       List all tasks (id, title, status)"
    echo "  pending-tasks <quarter> <sprint>    List pending tasks only"
    echo "  ready-tasks <quarter> <sprint>      List tasks ready to execute (no blocking deps)"
    echo "  get-task <quarter> <task_id>        Get single task details"
    echo "  complete-task <quarter> <sprint> <task_id>  Mark task as completed"
    echo "  by-tag <quarter> <sprint> <tag>     Filter tasks by tag (FE, BE, DevOps)"
    echo "  get-task-ids <quarter> <sprint>     Get all task IDs in sprint"
    echo ""
    echo "Sprint Commands:"
    echo "  list-sprints <quarter>              List all sprints in quarter"
    echo "  next-sprint <quarter>               Get next incomplete sprint"
    echo "  status <quarter> <sprint>           Get sprint status summary"
    echo "  set-status <quarter> <sprint> <s>   Set sprint status"
    echo "  is-complete <quarter> <sprint>      Check if all tasks done"
    echo ""
    echo "Examples:"
    echo "  sprint-manager.sh list-tasks q01 sprint01"
    echo "  sprint-manager.sh ready-tasks q01 sprint01"
    echo "  sprint-manager.sh get-task q01 T-001"
    echo "  sprint-manager.sh complete-task q01 sprint01 T-001"
    exit 1
    ;;
esac
