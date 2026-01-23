#!/bin/bash
# Document Search Tool for Peachflow
# Search for tasks, epics, stories, FRs, NFRs, ADRs by keyword or ID

set -e

DOCS_DIR="docs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Search by ID (exact match)
search_by_id() {
  local id="$1"
  local type=""

  # Determine type from ID prefix
  case "$id" in
    BR-*|br-*)
      type="Business Requirement"
      grep -rn "\\b${id}\\b" "$DOCS_DIR/01-business/" --include="*.md" 2>/dev/null || echo "Not found in business docs"
      ;;
    F-*|f-*)
      type="Feature"
      grep -rn "\\b${id}\\b" "$DOCS_DIR/02-product/PRD.md" 2>/dev/null || echo "Not found in PRD"
      ;;
    FR-*|fr-*)
      type="Functional Requirement"
      grep -rn "\\b${id}\\b" "$DOCS_DIR/03-requirements/FRD.md" 2>/dev/null || echo "Not found in FRD"
      ;;
    NFR-*|nfr-*)
      type="Non-Functional Requirement"
      grep -rn "\\b${id}\\b" "$DOCS_DIR/03-requirements/NFRs.md" 2>/dev/null || echo "Not found in NFRs"
      ;;
    E-*|e-*)
      type="Epic"
      grep -rn "\\b${id}\\b" "$DOCS_DIR/04-plan/" --include="*.md" 2>/dev/null || echo "Not found in plan docs"
      ;;
    US-*|us-*)
      type="User Story"
      grep -rn "\\b${id}\\b" "$DOCS_DIR/04-plan/quarters/" --include="stories.md" 2>/dev/null || echo "Not found in stories"
      ;;
    T-*|t-*)
      type="Task"
      # Search in task files
      local task_num=$(echo "$id" | sed 's/[Tt]-//' | sed 's/^0*//')
      local padded=$(printf "%03d" "$task_num")
      if [ -f "$DOCS_DIR/04-plan/quarters/"*"/tasks/${padded}.md" ]; then
        cat "$DOCS_DIR/04-plan/quarters/"*"/tasks/${padded}.md" 2>/dev/null
      else
        grep -rn "\\b${id}\\b" "$DOCS_DIR/04-plan/quarters/" --include="*.md" 2>/dev/null || echo "Not found"
      fi
      ;;
    ADR-*|adr-*|[0-9][0-9][0-9][0-9]-*)
      type="Architecture Decision Record"
      local adr_pattern=$(echo "$id" | sed 's/[Aa][Dd][Rr]-//')
      find "$DOCS_DIR/02-product/architecture/adr/" -name "*${adr_pattern}*" -exec cat {} \; 2>/dev/null || echo "Not found"
      ;;
    *)
      echo "Unknown ID format: $id"
      echo "Supported formats: BR-XXX, F-XXX, FR-XXX, NFR-XXX, E-XXX, US-XXX, T-XXX, ADR-XXXX or NNNN-title"
      exit 1
      ;;
  esac

  echo ""
  echo -e "${BLUE}Type: $type${NC}"
}

# Search by keyword across all docs
search_by_keyword() {
  local keyword="$1"
  local scope="${2:-all}"

  echo -e "${YELLOW}Searching for: '$keyword'${NC}"
  echo ""

  case "$scope" in
    all)
      grep -rn "$keyword" "$DOCS_DIR/" --include="*.md" 2>/dev/null | head -50
      ;;
    business)
      grep -rn "$keyword" "$DOCS_DIR/01-business/" --include="*.md" 2>/dev/null
      ;;
    product)
      grep -rn "$keyword" "$DOCS_DIR/02-product/" --include="*.md" 2>/dev/null
      ;;
    requirements|reqs)
      grep -rn "$keyword" "$DOCS_DIR/03-requirements/" --include="*.md" 2>/dev/null
      ;;
    plan)
      grep -rn "$keyword" "$DOCS_DIR/04-plan/" --include="*.md" 2>/dev/null
      ;;
    tasks)
      grep -rn "$keyword" "$DOCS_DIR/04-plan/quarters/"*"/tasks/" --include="*.md" 2>/dev/null
      ;;
    stories)
      grep -rn "$keyword" "$DOCS_DIR/04-plan/quarters/" --include="stories.md" 2>/dev/null
      ;;
    ux)
      grep -rn "$keyword" "$DOCS_DIR/02-product/ux/" --include="*.md" 2>/dev/null
      ;;
    architecture|arch)
      grep -rn "$keyword" "$DOCS_DIR/02-product/architecture/" --include="*.md" 2>/dev/null
      ;;
    *)
      echo "Unknown scope: $scope"
      echo "Valid scopes: all, business, product, requirements, plan, tasks, stories, ux, architecture"
      exit 1
      ;;
  esac
}

# List all items of a type
list_items() {
  local type="$1"
  local status="${2:-all}"

  case "$type" in
    tasks)
      echo -e "${YELLOW}=== Tasks ===${NC}"
      if [ "$status" = "pending" ]; then
        grep -rn "status: pending" "$DOCS_DIR/04-plan/quarters/"*"/tasks/" --include="*.md" -l 2>/dev/null | while read f; do
          id=$(grep "^id:" "$f" | head -1 | awk '{print $2}')
          title=$(grep "^title:" "$f" | head -1 | sed 's/title: //')
          echo "  $id: $title"
        done
      elif [ "$status" = "in_progress" ]; then
        grep -rn "status: in_progress" "$DOCS_DIR/04-plan/quarters/"*"/tasks/" --include="*.md" -l 2>/dev/null | while read f; do
          id=$(grep "^id:" "$f" | head -1 | awk '{print $2}')
          title=$(grep "^title:" "$f" | head -1 | sed 's/title: //')
          echo "  $id: $title"
        done
      elif [ "$status" = "completed" ]; then
        grep -rn "status: completed" "$DOCS_DIR/04-plan/quarters/"*"/tasks/" --include="*.md" -l 2>/dev/null | while read f; do
          id=$(grep "^id:" "$f" | head -1 | awk '{print $2}')
          title=$(grep "^title:" "$f" | head -1 | sed 's/title: //')
          echo "  $id: $title"
        done
      else
        find "$DOCS_DIR/04-plan/quarters/"*"/tasks/" -name "*.md" 2>/dev/null | while read f; do
          id=$(grep "^id:" "$f" | head -1 | awk '{print $2}')
          title=$(grep "^title:" "$f" | head -1 | sed 's/title: //')
          status=$(grep "^status:" "$f" | head -1 | awk '{print $2}')
          echo "  [$status] $id: $title"
        done
      fi
      ;;
    epics)
      echo -e "${YELLOW}=== Epics ===${NC}"
      grep -E "^\*\*E-[0-9]+:" "$DOCS_DIR/04-plan/plan.md" 2>/dev/null || grep -E "^## E-[0-9]+" "$DOCS_DIR/04-plan/plan.md" 2>/dev/null
      ;;
    stories)
      echo -e "${YELLOW}=== User Stories ===${NC}"
      grep -E "^## US-[0-9]+:|^### US-[0-9]+:" "$DOCS_DIR/04-plan/quarters/"*"/stories.md" 2>/dev/null
      ;;
    frs)
      echo -e "${YELLOW}=== Functional Requirements ===${NC}"
      grep -E "^#### FR-[0-9]+:|^### FR-[0-9]+:|^\*\*FR-[0-9]+\*\*:" "$DOCS_DIR/03-requirements/FRD.md" 2>/dev/null
      ;;
    nfrs)
      echo -e "${YELLOW}=== Non-Functional Requirements ===${NC}"
      grep -E "^### NFR-[0-9]+:|^\*\*NFR-[0-9]+\*\*:" "$DOCS_DIR/03-requirements/NFRs.md" 2>/dev/null
      ;;
    adrs)
      echo -e "${YELLOW}=== Architecture Decision Records ===${NC}"
      ls -1 "$DOCS_DIR/02-product/architecture/adr/" 2>/dev/null | while read f; do
        echo "  $f"
      done
      ;;
    brs)
      echo -e "${YELLOW}=== Business Requirements ===${NC}"
      grep -E "^\*\*BR-[0-9]+\*\*:|^### BR-[0-9]+:" "$DOCS_DIR/01-business/BRD.md" 2>/dev/null
      ;;
    features)
      echo -e "${YELLOW}=== Features ===${NC}"
      grep -E "^#### F-[0-9]+:|^### F-[0-9]+:|^\*\*F-[0-9]+\*\*:" "$DOCS_DIR/02-product/PRD.md" 2>/dev/null
      ;;
    *)
      echo "Unknown type: $type"
      echo "Valid types: tasks, epics, stories, frs, nfrs, adrs, brs, features"
      exit 1
      ;;
  esac
}

# Get task by tag
get_tasks_by_tag() {
  local tag="$1"

  echo -e "${YELLOW}=== Tasks tagged [$tag] ===${NC}"
  grep -rn "\\[$tag\\]" "$DOCS_DIR/04-plan/quarters/"*"/tasks/" --include="*.md" 2>/dev/null | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    id=$(grep "^id:" "$file" | head -1 | awk '{print $2}')
    title=$(grep "^title:" "$file" | head -1 | sed 's/title: //')
    status=$(grep "^status:" "$file" | head -1 | awk '{print $2}')
    echo "  [$status] $id: $title"
  done
}

# Get dependencies for a task
get_dependencies() {
  local task_id="$1"
  local task_num=$(echo "$task_id" | sed 's/[Tt]-//' | sed 's/^0*//')
  local padded=$(printf "%03d" "$task_num")

  local task_file=$(find "$DOCS_DIR/04-plan/quarters/"*"/tasks/" -name "${padded}.md" 2>/dev/null | head -1)

  if [ -z "$task_file" ]; then
    echo "Task not found: $task_id"
    exit 1
  fi

  echo -e "${YELLOW}=== Dependencies for $task_id ===${NC}"
  echo ""
  echo "Depends on:"
  grep "^depends_on:" "$task_file" | sed 's/depends_on: /  /'
  echo ""
  echo "Can run parallel with:"
  grep "^parallel_with:" "$task_file" | sed 's/parallel_with: /  /'
}

# Find related items
find_related() {
  local id="$1"

  echo -e "${YELLOW}=== Items related to $id ===${NC}"
  echo ""
  grep -rn "\\b${id}\\b" "$DOCS_DIR/" --include="*.md" 2>/dev/null | grep -v "^Binary"
}

# Main command handler
case "$1" in
  id)
    search_by_id "$2"
    ;;
  keyword|search)
    search_by_keyword "$2" "$3"
    ;;
  list)
    list_items "$2" "$3"
    ;;
  tag)
    get_tasks_by_tag "$2"
    ;;
  deps|dependencies)
    get_dependencies "$2"
    ;;
  related)
    find_related "$2"
    ;;
  *)
    echo "Peachflow Document Search Tool"
    echo ""
    echo "Usage: doc-search.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  id <ID>                  Search by ID (BR-001, FR-001, T-001, etc.)"
    echo "  keyword <term> [scope]   Search by keyword (scopes: all, business, product, requirements, plan, tasks, stories, ux, architecture)"
    echo "  list <type> [status]     List items (types: tasks, epics, stories, frs, nfrs, adrs, brs, features)"
    echo "  tag <tag>                Find tasks by tag (FE, BE, DevOps)"
    echo "  deps <task_id>           Show task dependencies"
    echo "  related <ID>             Find all references to an ID"
    echo ""
    echo "Examples:"
    echo "  doc-search.sh id FR-001"
    echo "  doc-search.sh keyword authentication requirements"
    echo "  doc-search.sh list tasks pending"
    echo "  doc-search.sh tag FE"
    echo "  doc-search.sh deps T-001"
    exit 1
    ;;
esac
