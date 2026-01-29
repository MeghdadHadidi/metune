---
name: peachflow:migrate
description: Migrate a peachflow v2 project to v3 format. Converts sprint/task files to graph structure.
allowed-tools: Read, Bash, AskUserQuestion
---

# /peachflow:migrate - Migrate v2 to v3

Migrate a peachflow v2 project to the v3 graph-based format.

## Pre-flight Check

```bash
if [ ! -f ".peachflow-state.json" ]; then
  echo "NO_STATE_FILE"
  exit 0
fi

version=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('version', '2.0.0'))")
major_version=$(echo "$version" | cut -d. -f1)

if [ "$major_version" -ge 3 ]; then
  echo "ALREADY_V3 version=$version"
else
  echo "V2_PROJECT version=$version"
fi
```

**Routing:**
- `NO_STATE_FILE` → Error: No peachflow project found
- `ALREADY_V3` → Already on v3, no migration needed
- `V2_PROJECT` → Proceed with migration

---

## No State File

```
No peachflow project found in this directory.

To initialize a new project:
  /peachflow:init
```

---

## Already v3

```
This project is already using v3 format (version X.X.X).

No migration needed.
```

---

## Migration Flow

### Step 1: Preview Migration (Dry Run)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --dry-run --verbose
```

Show the dry run output to the user.

### Step 2: Confirm Migration

```json
{
  "question": "Proceed with migration? (A backup will be created)",
  "header": "Migrate",
  "options": [
    {"label": "Yes, migrate", "description": "Convert v2 files to v3 graph format"},
    {"label": "No, cancel", "description": "Keep current v2 format"}
  ],
  "multiSelect": false
}
```

### Step 3: Run Migration

**If "Yes, migrate":**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --verbose
```

**If migration succeeds:**

```
Migration complete!

What was migrated:
  - State file updated to v3 format
  - Epics, stories, and tasks converted to graph
  - Sprint information preserved

Backup created: .peachflow-state.json.v2.backup

Next steps:
  1. Review settings with /peachflow:config
  2. If you have UX docs in docs/03-ux/, convert them to design skills
  3. Continue with /peachflow:create-sprint or /peachflow:implement
```

**If migration fails:**

```
Migration failed. Your original files have not been modified.

Check the error message above for details.

To debug:
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --dry-run --verbose

Common issues:
  - Missing or malformed plan.md
  - Invalid sprint file format
  - File permission issues
```

**If "No, cancel":**

```
Migration cancelled. No changes made.
```

---

## Manual Usage

The migration script can be run directly from terminal:

```bash
# Preview migration (no changes)
python3 /path/to/peachflow/scripts/migrate-v2-to-v3.py --dry-run --verbose

# Run migration
python3 /path/to/peachflow/scripts/migrate-v2-to-v3.py --verbose
```

---

## What Gets Migrated

| v2 Source | v3 Destination |
|-----------|----------------|
| `.peachflow-state.json` | Updated in place (backup created) |
| `docs/04-plan/plan.md` | Epics in graph |
| `docs/04-plan/stories.md` | User stories in graph |
| `docs/04-plan/sprint-*.md` | Sprint entities + task assignments |
| `docs/04-plan/tasks/*.md` | Task entities with dependencies |

## What's Preserved (Not Changed)

- `docs/01-business/` - BRD documents
- `docs/02-product/` - PRD and architecture docs
- `docs/03-ux/` - UX documentation (needs manual conversion to skills)

## What Needs Manual Work

UX documentation in `docs/03-ux/` should be converted to design skills:

1. Run `/peachflow:design` to generate skill templates
2. Copy relevant patterns from old UX docs to new skills
3. Delete `docs/03-ux/` when done
