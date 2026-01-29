---
name: peachflow:graph
description: Launch a local visualization server to view the project's work item graph. Shows epics, user stories, tasks, and their relationships in an interactive browser-based interface.
allowed-tools: Bash
---

# /peachflow:graph - Graph Visualization

Launch a local web server that displays an interactive visualization of your project's work item graph. View epics, user stories, tasks, dependencies, and progress at a glance.

## Pre-flight Check

```bash
# Check if graph exists
if [ ! -f ".peachflow-graph.json" ]; then
  echo "NOT_INITIALIZED"
  exit 1
fi

# Check Python is available
if ! command -v python3 &> /dev/null; then
  echo "PYTHON_NOT_FOUND"
  exit 1
fi
```

**If NOT initialized:**
```
Peachflow not initialized. Run /peachflow:init first.
```

**If Python not found:**
```
Python 3 is required for the visualization server.
Please install Python 3 and try again.
```

---

## Launch Server

```bash
# Start the visualization server on port 9876
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py serve --port 9876
```

The server will:
1. Read the current `.peachflow-graph.json`
2. Generate an interactive HTML visualization
3. Open your default browser to `http://localhost:9876`
4. Keep running until you press Ctrl+C

---

## Visualization Features

### Main View

- **Hierarchical layout**: Quarter → Epic → Story → Task
- **Color coding by type**:
  - Quarters: Red diamonds
  - Epics: Dark blue boxes
  - Stories: Purple ellipses
  - Tasks: Color by tag (FE=blue, BE=green, DevOps=orange, Full=purple)

### Status Indicators

- **Green border**: Completed
- **Red border**: Blocked
- **Gray border**: Pending/Draft

### Dependency Lines

- **Solid gray**: Parent-child hierarchy
- **Dashed red**: Task dependencies

### Sidebar Panels

**Epics Tab**:
- Lists all epics by priority
- Shows story/task counts
- Click to focus on epic in graph

**Tasks Tab**:
- Lists incomplete tasks
- Shows blocking status
- Click to focus on task in graph

**Legend Tab**:
- Color reference for all node types
- Line type explanations

### Statistics Header

- Total epic count
- Total story count
- Total task count
- Completed task count

---

## Port Configuration

Default port is 9876 (chosen to avoid conflicts with common development servers).

If port 9876 is in use:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py serve --port 9877
```

---

## Interaction

- **Zoom**: Scroll wheel
- **Pan**: Click and drag on empty space
- **Focus**: Click node in sidebar to center view on it
- **Details**: Hover over nodes for tooltip info

---

## Output

```
Peachflow Graph Visualization
Server running at: http://localhost:9876
Press Ctrl+C to stop
```

The browser will automatically open. If it doesn't, manually navigate to the URL shown.

---

## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :9876

# Kill the process or use a different port
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py serve --port 9877
```

### Browser Doesn't Open

```bash
# Manually open the URL in your browser
open http://localhost:9876  # macOS
xdg-open http://localhost:9876  # Linux
```

### Graph Not Updating

The visualization is generated when the server starts. To see updates:
1. Stop the server (Ctrl+C)
2. Restart: `/peachflow:graph`

---

## Example Visualization

```
╔══════════════════════════════════════════════════════════════╗
║  Peachflow Graph                      Epics: 4  Tasks: 23    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║     ◆ Q1                                                     ║
║     ├──┬── ▢ E-001: User Auth ──┬── ○ US-001 ──┬── ▪ T-001  ║
║     │  │                        │              └── ▪ T-002  ║
║     │  │                        └── ○ US-002 ──── ▪ T-003   ║
║     │  │                                                     ║
║     │  └── ▢ E-002: Dashboard ──── ○ US-003 ──┬── ▪ T-004  ║
║     │                                         └── ▪ T-005   ║
║     │                                                        ║
║     ◆ Q2                                                     ║
║     └──── ▢ E-003: Payments ...                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Legend: ◆ Quarter  ▢ Epic  ○ Story  ▪ Task
        ─── Hierarchy  ╌╌╌ Dependency
```

---

## Alternative: Export to Markdown

If you prefer a text-based view:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py export --format markdown > project-overview.md
```

This creates a markdown file with all quarters, epics, stories, and tasks in outline format.
