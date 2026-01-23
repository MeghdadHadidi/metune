#!/bin/bash
# Git Helper for Peachflow
# Provides git status checks and commit message generation helpers

# Check if we're on main/master branch
is_main_branch() {
  local branch=$(git branch --show-current 2>/dev/null)
  if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
    echo "true"
  else
    echo "false"
  fi
}

# Get current branch name
get_branch() {
  git branch --show-current 2>/dev/null
}

# Check for uncommitted changes
has_uncommitted_changes() {
  if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "true"
  else
    echo "false"
  fi
}

# Get list of changed files (staged and unstaged)
list_changes() {
  echo "=== Staged Changes ==="
  git diff --cached --name-status 2>/dev/null
  echo ""
  echo "=== Unstaged Changes ==="
  git diff --name-status 2>/dev/null
  echo ""
  echo "=== Untracked Files ==="
  git ls-files --others --exclude-standard 2>/dev/null
}

# Get diff summary for commit message generation
get_diff_summary() {
  echo "=== Files Changed ==="
  git status --short 2>/dev/null
  echo ""
  echo "=== Diff Stats ==="
  git diff --stat 2>/dev/null
  git diff --cached --stat 2>/dev/null
}

# Check if working tree is clean
is_clean() {
  if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
    echo "true"
  else
    echo "false"
  fi
}

# Extract quarter from branch name (e.g., peachflow/q01 -> q01)
extract_quarter_from_branch() {
  local branch="${1:-$(get_branch)}"
  echo "$branch" | grep -oE 'q[0-9]+' | head -1
}

# List worktrees
list_worktrees() {
  git worktree list 2>/dev/null
}

# Check if worktree exists for path
worktree_exists() {
  local path="$1"
  if git worktree list 2>/dev/null | grep -q "$path"; then
    echo "true"
  else
    echo "false"
  fi
}

# Create worktree for quarter
create_quarter_worktree() {
  local quarter="$1"
  local base_dir="${2:-..}"
  local project_name=$(basename "$(pwd)")
  local worktree_path="${base_dir}/${project_name}-${quarter}"
  local branch_name="peachflow/${quarter}"

  # Check if worktree already exists
  if [ "$(worktree_exists "$worktree_path")" = "true" ]; then
    echo "WORKTREE_EXISTS:$worktree_path"
    return 1
  fi

  # Check if branch already exists
  if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
    # Branch exists, create worktree without -b
    git worktree add "$worktree_path" "$branch_name" 2>/dev/null
  else
    # Create new branch with worktree
    git worktree add -b "$branch_name" "$worktree_path" 2>/dev/null
  fi

  if [ $? -eq 0 ]; then
    echo "CREATED:$worktree_path"
  else
    echo "ERROR:Failed to create worktree"
    return 1
  fi
}

# Remove worktree
remove_worktree() {
  local path="$1"
  git worktree remove "$path" 2>/dev/null
  if [ $? -eq 0 ]; then
    echo "Worktree removed: $path"
  else
    echo "Error removing worktree: $path"
    return 1
  fi
}

# Get commits since branching from main
get_branch_commits() {
  local base="${1:-main}"
  git log --oneline "${base}..HEAD" 2>/dev/null
}

# Get files changed since branching from main
get_branch_files() {
  local base="${1:-main}"
  git diff --name-only "${base}...HEAD" 2>/dev/null
}

# Main command handler
case "$1" in
  is-main)
    is_main_branch
    ;;
  branch)
    get_branch
    ;;
  has-changes)
    has_uncommitted_changes
    ;;
  list-changes)
    list_changes
    ;;
  diff-summary)
    get_diff_summary
    ;;
  is-clean)
    is_clean
    ;;
  extract-quarter)
    extract_quarter_from_branch "$2"
    ;;
  list-worktrees)
    list_worktrees
    ;;
  worktree-exists)
    worktree_exists "$2"
    ;;
  create-worktree)
    create_quarter_worktree "$2" "$3"
    ;;
  remove-worktree)
    remove_worktree "$2"
    ;;
  branch-commits)
    get_branch_commits "$2"
    ;;
  branch-files)
    get_branch_files "$2"
    ;;
  *)
    echo "Usage: git-helper.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  is-main                   Check if on main/master branch"
    echo "  branch                    Get current branch name"
    echo "  has-changes               Check for uncommitted changes"
    echo "  list-changes              List all changed files"
    echo "  diff-summary              Get diff summary for commit message"
    echo "  is-clean                  Check if working tree is clean"
    echo "  extract-quarter [branch]  Extract quarter from branch name"
    echo "  list-worktrees            List all git worktrees"
    echo "  worktree-exists <path>    Check if worktree exists at path"
    echo "  create-worktree <q> [dir] Create worktree for quarter"
    echo "  remove-worktree <path>    Remove worktree at path"
    echo "  branch-commits [base]     Get commits since branching"
    echo "  branch-files [base]       Get files changed since branching"
    exit 1
    ;;
esac
