---
name: peachflow:clarify
description: Review and resolve pending clarifications stored in the graph. Clarifications are questions that arose during discovery, design, or planning.
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# /peachflow:clarify - Resolve Clarifications (v3)

Review and answer pending clarifications stored in the graph. Clarifications are open questions that need human input before proceeding.

## Pre-flight Check

```bash
# Check initialization
if [ ! -f ".peachflow-graph.json" ]; then
  echo "NOT_INITIALIZED"
  exit 1
fi

# Get pending clarifications
pending=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications --pending --format json)
count=$(echo "$pending" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")

if [ "$count" -eq "0" ]; then
  echo "NO_PENDING"
fi
```

**If no pending clarifications:**
```
No pending clarifications.

All questions have been answered. You can proceed with:
  /peachflow:design    (if in discovery phase)
  /peachflow:plan      (if in design phase)
  /peachflow:create-sprint (if in plan phase)
```

---

## Step 1: List Pending Clarifications

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications --pending
```

Display to user:
```
Pending Clarifications ($count items)
─────────────────────────────────────────

CL-001: Should authentication support SSO providers?
  Related to: E-001 (User Authentication)
  Created: 2024-01-15

CL-002: What email provider should be used for notifications?
  Related to: E-004 (Notification System)
  Created: 2024-01-16

CL-003: Is dark mode required for initial release?
  Related to: general
  Created: 2024-01-16
```

---

## Step 2: Present Each Clarification

For each pending clarification, ask the user:

```json
{
  "questions": [{
    "question": "CL-001: Should authentication support SSO providers (Google, GitHub, etc.)?",
    "header": "SSO Support",
    "options": [
      {"label": "Yes, Google only", "description": "Support Google OAuth sign-in"},
      {"label": "Yes, multiple providers", "description": "Support Google, GitHub, Microsoft"},
      {"label": "No, email/password only", "description": "Traditional auth only for MVP"},
      {"label": "Defer to later", "description": "Skip for now, revisit in future quarter"}
    ],
    "multiSelect": false
  }]
}
```

---

## Step 3: Record Answers

After user provides answer:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update clarification CL-001 \
  --status clarified \
  --answer "Yes, support Google OAuth for initial release. Other providers can be added later."
```

---

## Step 4: Update Related Entities (if needed)

If the clarification affects planning:

```bash
# If answer changes scope of an epic
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update epic E-001 \
  --description "Updated description based on CL-001 clarification"

# If answer requires new tasks
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create task \
  --story US-001 \
  --title "Implement Google OAuth" \
  --tag BE \
  --description "Add Google OAuth sign-in based on CL-001"
```

---

## Step 5: Summary

```
Clarifications resolved: $count

Answers recorded:
  CL-001: Support Google OAuth for initial release
  CL-002: Use SendGrid for email notifications
  CL-003: Defer dark mode to Q2

Impact:
  - E-001 updated with OAuth scope
  - 2 new tasks added for OAuth implementation
  - E-007 created for dark mode (Q2)

No remaining clarifications.

Next: Continue with your current phase
```

---

## Clarification Workflow

```
Any phase (discover/design/plan)
    │
    ▼
Agent encounters ambiguity
    │
    ▼
Creates clarification in graph
    │
    ▼
Phase completes with pending clarifications
    │
    ▼
User runs /peachflow:clarify
    │
    ▼
Answers recorded, entities updated
    │
    ▼
Continue to next phase
```

---

## Creating Clarifications Manually

Users can also add their own clarifications:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create clarification \
  --entity E-002 \
  --question "What charting library should we use for analytics?"
```

---

## Viewing Clarification History

See all clarifications (including resolved):

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications
```

Filter by entity:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications --entity E-001
```
