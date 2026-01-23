#!/bin/bash
# Document Parser for Peachflow
# Extract structured data from markdown documents without LLM

set -e

DOCS_DIR="docs"

# Extract requirement from FRD by ID
get_fr() {
  local id="$1"
  local file="$DOCS_DIR/03-requirements/FRD.md"

  if [ ! -f "$file" ]; then
    echo "FRD.md not found"
    exit 1
  fi

  # Extract section starting with the FR ID until next FR or section
  awk "/^#{1,4} ${id}:|^\*\*${id}\*\*:/{found=1} found{print} /^#{1,4} FR-|^\*\*FR-/{if(found && !/^#{1,4} ${id}:|^\*\*${id}\*\*:/)exit}" "$file"
}

# Extract NFR by ID
get_nfr() {
  local id="$1"
  local file="$DOCS_DIR/03-requirements/NFRs.md"

  if [ ! -f "$file" ]; then
    echo "NFRs.md not found"
    exit 1
  fi

  awk "/^#{1,4} ${id}:|^\*\*${id}\*\*:/{found=1} found{print} /^#{1,4} NFR-|^\*\*NFR-/{if(found && !/^#{1,4} ${id}:|^\*\*${id}\*\*:/)exit}" "$file"
}

# Extract epic from plan
get_epic() {
  local id="$1"
  local file="$DOCS_DIR/04-plan/plan.md"

  if [ ! -f "$file" ]; then
    echo "plan.md not found"
    exit 1
  fi

  awk "/^#{1,4} ${id}:|^\*\*${id}:|^- \[ \] \*\*${id}:|^- \[x\] \*\*${id}:/{found=1} found{print} /^#{1,4} E-|^- \[ \] \*\*E-|^- \[x\] \*\*E-/{if(found && !/^#{1,4} ${id}:|^\*\*${id}:|^- \[ \] \*\*${id}:|^- \[x\] \*\*${id}:/)exit}" "$file"
}

# Extract user story
get_story() {
  local id="$1"

  # Search in all quarter stories files
  for file in "$DOCS_DIR/04-plan/quarters/"*/stories.md; do
    if [ -f "$file" ]; then
      local result=$(awk "/^#{1,4} ${id}:/{found=1} found{print} /^#{1,4} US-/{if(found && !/^#{1,4} ${id}:/)exit}" "$file")
      if [ -n "$result" ]; then
        echo "Source: $file"
        echo ""
        echo "$result"
        return
      fi
    fi
  done

  echo "Story not found: $id"
}

# Extract task details
get_task() {
  local id="$1"
  local task_num=$(echo "$id" | sed 's/[Tt]-//' | sed 's/^0*//')
  local padded=$(printf "%03d" "$task_num")

  local task_file=$(find "$DOCS_DIR/04-plan/quarters/"*"/tasks/" -name "${padded}.md" 2>/dev/null | head -1)

  if [ -z "$task_file" ] || [ ! -f "$task_file" ]; then
    echo "Task not found: $id"
    exit 1
  fi

  cat "$task_file"
}

# Extract feature from PRD
get_feature() {
  local id="$1"
  local file="$DOCS_DIR/02-product/PRD.md"

  if [ ! -f "$file" ]; then
    echo "PRD.md not found"
    exit 1
  fi

  awk "/^#{1,4} ${id}:/{found=1} found{print} /^#{1,4} F-/{if(found && !/^#{1,4} ${id}:/)exit}" "$file"
}

# Extract business requirement from BRD
get_br() {
  local id="$1"
  local file="$DOCS_DIR/01-business/BRD.md"

  if [ ! -f "$file" ]; then
    echo "BRD.md not found"
    exit 1
  fi

  awk "/^#{1,4} ${id}:|^\*\*${id}\*\*:/{found=1} found{print} /^#{1,4} BR-|^\*\*BR-/{if(found && !/^#{1,4} ${id}:|^\*\*${id}\*\*:/)exit}" "$file"
}

# Get ADR content
get_adr() {
  local pattern="$1"
  local adr_dir="$DOCS_DIR/02-product/architecture/adr"

  local file=$(find "$adr_dir" -name "*${pattern}*" -type f 2>/dev/null | head -1)

  if [ -z "$file" ] || [ ! -f "$file" ]; then
    echo "ADR not found: $pattern"
    exit 1
  fi

  cat "$file"
}

# Extract acceptance criteria from a requirement or story
get_acceptance_criteria() {
  local id="$1"

  # Determine type and get content
  case "$id" in
    FR-*|fr-*)
      content=$(get_fr "$id")
      ;;
    US-*|us-*)
      content=$(get_story "$id")
      ;;
    T-*|t-*)
      content=$(get_task "$id")
      ;;
    *)
      echo "Unsupported type for acceptance criteria: $id"
      exit 1
      ;;
  esac

  # Extract acceptance criteria section
  echo "$content" | awk '/^#{1,4} Acceptance Criteria|^\*\*Acceptance Criteria\*\*|^### Acceptance/{found=1; next} found && /^#{1,4} |^\*\*[A-Z]/{exit} found{print}'
}

# Count items in a document
count_items() {
  local type="$1"

  case "$type" in
    frs)
      grep -cE "^#{1,4} FR-[0-9]+:|^\*\*FR-[0-9]+\*\*:" "$DOCS_DIR/03-requirements/FRD.md" 2>/dev/null || echo "0"
      ;;
    nfrs)
      grep -cE "^#{1,4} NFR-[0-9]+:|^\*\*NFR-[0-9]+\*\*:" "$DOCS_DIR/03-requirements/NFRs.md" 2>/dev/null || echo "0"
      ;;
    features)
      grep -cE "^#{1,4} F-[0-9]+:" "$DOCS_DIR/02-product/PRD.md" 2>/dev/null || echo "0"
      ;;
    epics)
      grep -cE "^\*\*E-[0-9]+:|^#{1,4} E-[0-9]+:" "$DOCS_DIR/04-plan/plan.md" 2>/dev/null || echo "0"
      ;;
    stories)
      find "$DOCS_DIR/04-plan/quarters/"*"/stories.md" -exec grep -cE "^#{1,4} US-[0-9]+:" {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}'
      ;;
    tasks)
      find "$DOCS_DIR/04-plan/quarters/"*"/tasks/" -name "*.md" 2>/dev/null | wc -l | tr -d ' '
      ;;
    *)
      echo "Unknown type: $type"
      exit 1
      ;;
  esac
}

# Get all IDs of a type
list_ids() {
  local type="$1"

  case "$type" in
    frs)
      grep -ohE "FR-[0-9]+" "$DOCS_DIR/03-requirements/FRD.md" 2>/dev/null | sort -u
      ;;
    nfrs)
      grep -ohE "NFR-[0-9]+" "$DOCS_DIR/03-requirements/NFRs.md" 2>/dev/null | sort -u
      ;;
    features)
      grep -ohE "F-[0-9]+" "$DOCS_DIR/02-product/PRD.md" 2>/dev/null | sort -u
      ;;
    brs)
      grep -ohE "BR-[0-9]+" "$DOCS_DIR/01-business/BRD.md" 2>/dev/null | sort -u
      ;;
    epics)
      grep -ohE "E-[0-9]+" "$DOCS_DIR/04-plan/plan.md" 2>/dev/null | sort -u
      ;;
    stories)
      grep -rohE "US-[0-9]+" "$DOCS_DIR/04-plan/quarters/"*"/stories.md" 2>/dev/null | sort -u
      ;;
    tasks)
      grep -rohE "T-[0-9]+" "$DOCS_DIR/04-plan/quarters/"*"/tasks/" 2>/dev/null | sort -u
      ;;
    *)
      echo "Unknown type: $type"
      exit 1
      ;;
  esac
}

# Main command handler
case "$1" in
  fr)
    get_fr "$2"
    ;;
  nfr)
    get_nfr "$2"
    ;;
  epic)
    get_epic "$2"
    ;;
  story)
    get_story "$2"
    ;;
  task)
    get_task "$2"
    ;;
  feature)
    get_feature "$2"
    ;;
  br)
    get_br "$2"
    ;;
  adr)
    get_adr "$2"
    ;;
  acceptance|ac)
    get_acceptance_criteria "$2"
    ;;
  count)
    count_items "$2"
    ;;
  ids)
    list_ids "$2"
    ;;
  *)
    echo "Peachflow Document Parser"
    echo ""
    echo "Usage: doc-parser.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  fr <FR-XXX>       Extract functional requirement"
    echo "  nfr <NFR-XXX>     Extract non-functional requirement"
    echo "  epic <E-XXX>      Extract epic"
    echo "  story <US-XXX>    Extract user story"
    echo "  task <T-XXX>      Extract task"
    echo "  feature <F-XXX>   Extract feature from PRD"
    echo "  br <BR-XXX>       Extract business requirement"
    echo "  adr <pattern>     Extract ADR (by number or keyword)"
    echo "  acceptance <ID>   Extract acceptance criteria"
    echo "  count <type>      Count items (frs, nfrs, features, epics, stories, tasks)"
    echo "  ids <type>        List all IDs of type"
    echo ""
    echo "Examples:"
    echo "  doc-parser.sh fr FR-001"
    echo "  doc-parser.sh acceptance US-001"
    echo "  doc-parser.sh count tasks"
    echo "  doc-parser.sh ids frs"
    exit 1
    ;;
esac
