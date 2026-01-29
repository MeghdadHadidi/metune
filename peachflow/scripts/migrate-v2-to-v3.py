#!/usr/bin/env python3
"""
migrate-v2-to-v3.py - Migrate peachflow v2 projects to v3 graph structure

Parses v2 markdown files (sprints, tasks, stories) and populates the v3 graph.

Usage:
    migrate-v2-to-v3.py [--dry-run] [--verbose]

Options:
    --dry-run   Show what would be migrated without making changes
    --verbose   Show detailed parsing information
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class MigrationError(Exception):
    pass


class V2Parser:
    """Parse v2 markdown files."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def log(self, msg: str):
        if self.verbose:
            print(f"  [PARSE] {msg}")

    def parse_state_v2(self, path: str) -> dict:
        """Parse v2 state file."""
        with open(path) as f:
            state = json.load(f)

        return {
            "projectName": state.get("projectName", "Untitled"),
            "projectType": state.get("projectType", "new"),
            "testingStrategy": state.get("testingStrategy", "none"),
            "testingIntensity": state.get("testingIntensity", "none"),
            "maxParallelTasks": state.get("maxParallelTasks", 3),
            "phases": state.get("phases", {}),
            "currentQuarter": state.get("currentQuarter"),
        }

    def parse_plan_md(self, path: str) -> list:
        """Parse docs/04-plan/plan.md to extract epics."""
        if not os.path.exists(path):
            return []

        with open(path) as f:
            content = f.read()

        epics = []
        current_quarter = None

        # Pattern for quarter headers: ### Q1: Theme
        quarter_pattern = r"###\s+(Q[1-4]):\s*(.+)"
        # Pattern for epics: - [ ] **E-001: Title** - Description
        epic_pattern = r"-\s*\[.\]\s*\*\*([E]-\d+):\s*([^*]+)\*\*\s*-?\s*(.*)"

        for line in content.split("\n"):
            # Check for quarter header
            q_match = re.match(quarter_pattern, line)
            if q_match:
                current_quarter = q_match.group(1)
                self.log(f"Found quarter: {current_quarter}")
                continue

            # Check for epic
            e_match = re.match(epic_pattern, line)
            if e_match and current_quarter:
                epic_id = e_match.group(1)
                title = e_match.group(2).strip()
                description = e_match.group(3).strip() if e_match.group(3) else ""

                epics.append({
                    "id": epic_id,
                    "title": title,
                    "description": description,
                    "quarter": current_quarter,
                    "priority": len([e for e in epics if e["quarter"] == current_quarter]) + 1,
                })
                self.log(f"Found epic: {epic_id} - {title}")

        return epics

    def parse_stories_md(self, path: str) -> list:
        """Parse stories.md to extract user stories."""
        if not os.path.exists(path):
            return []

        with open(path) as f:
            content = f.read()

        stories = []
        current_story = None
        in_acceptance = False

        # Pattern for story headers: ## US-001: Title
        story_pattern = r"##\s+(US-\d+):\s*(.+)"
        # Pattern for epic reference: **Epic:** E-001
        epic_pattern = r"\*\*Epic:\*\*\s*([E]-\d+)"
        # Pattern for acceptance criteria header
        acceptance_header = r"\*\*Acceptance\s+Criteria"

        for line in content.split("\n"):
            # Check for story header
            s_match = re.match(story_pattern, line)
            if s_match:
                if current_story:
                    stories.append(current_story)

                current_story = {
                    "id": s_match.group(1),
                    "title": s_match.group(2).strip(),
                    "description": "",
                    "epicId": None,
                    "acceptanceCriteria": [],
                }
                in_acceptance = False
                self.log(f"Found story: {current_story['id']} - {current_story['title']}")
                continue

            if current_story:
                # Check for epic reference
                e_match = re.search(epic_pattern, line)
                if e_match:
                    current_story["epicId"] = e_match.group(1)
                    continue

                # Check for acceptance criteria header
                if re.search(acceptance_header, line, re.IGNORECASE):
                    in_acceptance = True
                    continue

                # Collect acceptance criteria
                if in_acceptance and line.strip().startswith("-"):
                    criteria = line.strip().lstrip("-").strip()
                    if criteria:
                        current_story["acceptanceCriteria"].append(criteria)

        if current_story:
            stories.append(current_story)

        return stories

    def parse_sprint_md(self, path: str) -> list:
        """Parse sprintNN.md to extract tasks."""
        if not os.path.exists(path):
            return []

        with open(path) as f:
            content = f.read()

        tasks = []
        current_task = None

        # Pattern for task headers: ### T-001: [BE] Title
        task_pattern = r"###\s+(T-\d+):\s*\[(\w+)\]\s*(.+)"
        # Pattern for depends on: **Depends on:** T-001, T-002
        depends_pattern = r"\*\*Depends\s+on:\*\*\s*(.+)"
        # Pattern for story reference: **Story:** US-001
        story_pattern = r"\*\*Story:\*\*\s*(US-\d+)"

        for line in content.split("\n"):
            # Check for task header
            t_match = re.match(task_pattern, line)
            if t_match:
                if current_task:
                    tasks.append(current_task)

                current_task = {
                    "id": t_match.group(1),
                    "tag": t_match.group(2),
                    "title": t_match.group(3).strip(),
                    "description": "",
                    "storyId": None,
                    "dependsOn": [],
                    "status": "pending",
                }
                self.log(f"Found task: {current_task['id']} [{current_task['tag']}] - {current_task['title']}")
                continue

            if current_task:
                # Check for depends on
                d_match = re.search(depends_pattern, line, re.IGNORECASE)
                if d_match:
                    deps_str = d_match.group(1).strip()
                    if deps_str.lower() != "none":
                        deps = [d.strip() for d in deps_str.split(",") if d.strip().startswith("T-")]
                        current_task["dependsOn"] = deps
                    continue

                # Check for story reference
                s_match = re.search(story_pattern, line)
                if s_match:
                    current_task["storyId"] = s_match.group(1)
                    continue

                # Check for status
                if "**Status:** completed" in line:
                    current_task["status"] = "completed"

                # Collect description (first non-empty line after header that's not metadata)
                if (not current_task["description"] and
                    line.strip() and
                    not line.startswith("**") and
                    not line.startswith("-")):
                    current_task["description"] = line.strip()

        if current_task:
            tasks.append(current_task)

        return tasks

    def parse_task_file(self, path: str) -> Optional[dict]:
        """Parse individual task file (T-XXX.md)."""
        if not os.path.exists(path):
            return None

        with open(path) as f:
            content = f.read()

        task = {
            "id": None,
            "tag": "BE",
            "title": "",
            "description": "",
            "storyId": None,
            "dependsOn": [],
            "status": "pending",
        }

        # Try to get task ID from filename
        filename = os.path.basename(path)
        id_match = re.match(r"(T-\d+)", filename)
        if id_match:
            task["id"] = id_match.group(1)

        # Parse YAML frontmatter if present
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]

                # Parse frontmatter
                for line in frontmatter.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip().strip('"').strip("'")

                        if key == "id":
                            task["id"] = value
                        elif key == "tag":
                            task["tag"] = value
                        elif key == "title":
                            task["title"] = value
                        elif key == "story" or key == "story_id":
                            task["storyId"] = value
                        elif key == "status":
                            task["status"] = value
                        elif key == "depends_on":
                            deps = [d.strip() for d in value.split(",") if d.strip()]
                            task["dependsOn"] = deps

                content = body

        # Parse title from first heading
        title_match = re.search(r"#\s+(?:\[(\w+)\])?\s*(.+)", content)
        if title_match:
            if title_match.group(1):
                task["tag"] = title_match.group(1)
            if not task["title"]:
                task["title"] = title_match.group(2).strip()

        # Get description from content
        lines = content.strip().split("\n")
        for line in lines:
            if line.strip() and not line.startswith("#") and not line.startswith("**"):
                task["description"] = line.strip()
                break

        if task["id"]:
            self.log(f"Found task file: {task['id']} [{task['tag']}] - {task['title']}")
            return task

        return None


class V3GraphBuilder:
    """Build v3 graph from parsed v2 data."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.graph = {
            "version": "3.0.0",
            "entities": {
                "quarters": {
                    "Q1": {"id": "Q1", "status": "planned", "theme": "", "goals": []},
                    "Q2": {"id": "Q2", "status": "planned", "theme": "", "goals": []},
                    "Q3": {"id": "Q3", "status": "planned", "theme": "", "goals": []},
                    "Q4": {"id": "Q4", "status": "planned", "theme": "", "goals": []},
                },
                "epics": {},
                "stories": {},
                "tasks": {},
                "clarifications": {},
                "adrs": {},
                "sprints": {},
            },
            "relationships": {
                "quarter_epics": {"Q1": [], "Q2": [], "Q3": [], "Q4": []},
                "epic_stories": {},
                "story_tasks": {},
                "task_dependencies": {},
                "entity_clarifications": {},
                "entity_adrs": {},
            },
            "counters": {
                "epic": 0,
                "story": 0,
                "task": 0,
                "clarification": 0,
                "adr": 0,
                "sprint": 0,
            },
        }

    def log(self, msg: str):
        if self.verbose:
            print(f"  [BUILD] {msg}")

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _extract_counter(self, id_str: str) -> int:
        """Extract numeric part from ID like 'E-001' -> 1."""
        match = re.search(r"(\d+)$", id_str)
        return int(match.group(1)) if match else 0

    def add_epic(self, epic: dict):
        """Add an epic to the graph."""
        epic_id = epic["id"]
        quarter = epic.get("quarter", "Q1")

        self.graph["entities"]["epics"][epic_id] = {
            "id": epic_id,
            "title": epic.get("title", ""),
            "description": epic.get("description", ""),
            "status": "ready",
            "quarter": quarter,
            "priority": epic.get("priority", 5),
            "deliverables": [],
            "createdAt": self._now(),
            "updatedAt": self._now(),
        }

        # Update relationships
        if epic_id not in self.graph["relationships"]["quarter_epics"][quarter]:
            self.graph["relationships"]["quarter_epics"][quarter].append(epic_id)

        # Initialize epic_stories relationship
        if epic_id not in self.graph["relationships"]["epic_stories"]:
            self.graph["relationships"]["epic_stories"][epic_id] = []

        # Update counter
        num = self._extract_counter(epic_id)
        if num > self.graph["counters"]["epic"]:
            self.graph["counters"]["epic"] = num

        self.log(f"Added epic: {epic_id}")

    def add_story(self, story: dict):
        """Add a story to the graph."""
        story_id = story["id"]
        epic_id = story.get("epicId")

        self.graph["entities"]["stories"][story_id] = {
            "id": story_id,
            "title": story.get("title", ""),
            "description": story.get("description", ""),
            "status": "ready",
            "epicId": epic_id,
            "acceptanceCriteria": story.get("acceptanceCriteria", []),
            "createdAt": self._now(),
            "updatedAt": self._now(),
        }

        # Update relationships
        if epic_id and epic_id in self.graph["relationships"]["epic_stories"]:
            if story_id not in self.graph["relationships"]["epic_stories"][epic_id]:
                self.graph["relationships"]["epic_stories"][epic_id].append(story_id)

        # Initialize story_tasks relationship
        if story_id not in self.graph["relationships"]["story_tasks"]:
            self.graph["relationships"]["story_tasks"][story_id] = []

        # Update counter
        num = self._extract_counter(story_id)
        if num > self.graph["counters"]["story"]:
            self.graph["counters"]["story"] = num

        self.log(f"Added story: {story_id}")

    def add_task(self, task: dict):
        """Add a task to the graph."""
        task_id = task["id"]
        story_id = task.get("storyId")

        self.graph["entities"]["tasks"][task_id] = {
            "id": task_id,
            "title": task.get("title", ""),
            "description": task.get("description", ""),
            "status": task.get("status", "pending"),
            "storyId": story_id,
            "tag": task.get("tag", "BE"),
            "sprintId": None,
            "createdAt": self._now(),
            "updatedAt": self._now(),
            "completedAt": None,
        }

        # Update relationships
        if story_id and story_id in self.graph["relationships"]["story_tasks"]:
            if task_id not in self.graph["relationships"]["story_tasks"][story_id]:
                self.graph["relationships"]["story_tasks"][story_id].append(task_id)

        # Set dependencies
        deps = task.get("dependsOn", [])
        self.graph["relationships"]["task_dependencies"][task_id] = deps

        # Update counter
        num = self._extract_counter(task_id)
        if num > self.graph["counters"]["task"]:
            self.graph["counters"]["task"] = num

        self.log(f"Added task: {task_id}")

    def get_graph(self) -> dict:
        return self.graph


def find_quarters(base_path: str) -> list:
    """Find all quarter directories."""
    quarters_path = Path(base_path) / "docs" / "04-plan" / "quarters"
    if not quarters_path.exists():
        return []

    quarters = []
    for item in quarters_path.iterdir():
        if item.is_dir() and re.match(r"q\d+", item.name, re.IGNORECASE):
            quarters.append(item.name.upper() if len(item.name) == 2 else f"Q{item.name[1]}")

    return sorted(quarters)


def migrate(dry_run: bool = False, verbose: bool = False) -> dict:
    """Perform the migration."""
    parser = V2Parser(verbose=verbose)
    builder = V3GraphBuilder(verbose=verbose)

    state_path = ".peachflow-state.json"
    base_path = "."

    # Check if v2 state exists
    if not os.path.exists(state_path):
        raise MigrationError("No .peachflow-state.json found. Is this a peachflow project?")

    # Check version
    with open(state_path) as f:
        state = json.load(f)

    version = state.get("version", "2.0.0")
    if version.startswith("3."):
        raise MigrationError(f"Project is already v3 (version {version})")

    print(f"Migrating from v{version} to v3.0.0")
    print()

    # Parse v2 state
    print("Parsing v2 state file...")
    v2_state = parser.parse_state_v2(state_path)
    print(f"  Project: {v2_state['projectName']}")
    print(f"  Testing: {v2_state['testingStrategy']} / {v2_state['testingIntensity']}")
    print()

    # Parse plan.md for epics
    plan_path = os.path.join(base_path, "docs", "04-plan", "plan.md")
    print("Parsing plan.md for epics...")
    epics = parser.parse_plan_md(plan_path)
    print(f"  Found {len(epics)} epics")

    for epic in epics:
        builder.add_epic(epic)
    print()

    # Find and parse quarters
    quarters = find_quarters(base_path)
    print(f"Found quarters: {', '.join(quarters) if quarters else 'none'}")
    print()

    all_stories = []
    all_tasks = []

    for quarter in quarters:
        q_lower = quarter.lower()
        q_path = os.path.join(base_path, "docs", "04-plan", "quarters", q_lower)

        # Parse stories
        stories_path = os.path.join(q_path, "stories.md")
        if os.path.exists(stories_path):
            print(f"Parsing {quarter} stories...")
            stories = parser.parse_stories_md(stories_path)
            print(f"  Found {len(stories)} stories")
            all_stories.extend(stories)

        # Parse sprint files
        sprint_files = sorted(Path(q_path).glob("sprint*.md"))
        for sprint_file in sprint_files:
            print(f"Parsing {sprint_file.name}...")
            tasks = parser.parse_sprint_md(str(sprint_file))
            print(f"  Found {len(tasks)} tasks")
            all_tasks.extend(tasks)

        # Parse individual task files if they exist
        tasks_dir = os.path.join(q_path, "tasks")
        if os.path.isdir(tasks_dir):
            print(f"Parsing {quarter} task files...")
            task_files = list(Path(tasks_dir).glob("T-*.md"))
            for task_file in task_files:
                task = parser.parse_task_file(str(task_file))
                if task:
                    # Check if we already have this task from sprint files
                    existing = [t for t in all_tasks if t["id"] == task["id"]]
                    if not existing:
                        all_tasks.append(task)
            print(f"  Found {len(task_files)} task files")

    print()

    # Try to infer story-task relationships if not explicit
    # Group tasks by ID prefix patterns if storyId is missing
    for task in all_tasks:
        if not task.get("storyId") and all_stories:
            # Simple heuristic: assign to first story in same quarter
            # (this is a fallback, explicit storyId is better)
            pass

    # Add stories and tasks to graph
    print("Building v3 graph...")
    for story in all_stories:
        builder.add_story(story)

    for task in all_tasks:
        builder.add_task(task)

    graph = builder.get_graph()

    # Summary
    print()
    print("Migration Summary")
    print("-" * 40)
    print(f"Epics:   {len(graph['entities']['epics'])}")
    print(f"Stories: {len(graph['entities']['stories'])}")
    print(f"Tasks:   {len(graph['entities']['tasks'])}")

    completed = sum(1 for t in graph["entities"]["tasks"].values() if t["status"] == "completed")
    pending = sum(1 for t in graph["entities"]["tasks"].values() if t["status"] == "pending")
    print(f"  - Completed: {completed}")
    print(f"  - Pending:   {pending}")

    # Count tasks by tag
    tags = {}
    for t in graph["entities"]["tasks"].values():
        tag = t.get("tag", "?")
        tags[tag] = tags.get(tag, 0) + 1
    print(f"  - By tag: {', '.join(f'{k}={v}' for k, v in sorted(tags.items()))}")

    print()

    if dry_run:
        print("DRY RUN - No changes made")
        return {"graph": graph, "state": v2_state}

    # Write v3 graph
    print("Writing .peachflow-graph.json...")
    with open(".peachflow-graph.json", "w") as f:
        json.dump(graph, f, indent=2)

    # Update state to v3
    print("Updating .peachflow-state.json to v3...")
    new_state = {
        "version": "3.0.0",
        "initialized": state.get("initialized", datetime.now(timezone.utc).isoformat()),
        "projectName": v2_state["projectName"],
        "projectType": v2_state["projectType"],
        "testingStrategy": v2_state["testingStrategy"],
        "testingIntensity": v2_state["testingIntensity"],
        "maxParallelTasks": v2_state["maxParallelTasks"],
        "versionControlDocs": True,
        "phases": {
            "discovery": v2_state["phases"].get("discovery", {"status": "pending", "completedAt": None}),
            "design": v2_state["phases"].get("design", {"status": "pending", "completedAt": None}),
            "plan": v2_state["phases"].get("plan", {"status": "pending", "completedAt": None}),
        },
        "currentQuarter": v2_state.get("currentQuarter"),
        "currentSprint": None,
        "lastUpdated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    # Backup old state
    backup_path = ".peachflow-state.json.v2-backup"
    os.rename(".peachflow-state.json", backup_path)
    print(f"  Backed up old state to {backup_path}")

    with open(".peachflow-state.json", "w") as f:
        json.dump(new_state, f, indent=2)

    print()
    print("Migration complete!")
    print()
    print("Next steps:")
    print("  1. Review the migrated data with: /peachflow:graph")
    print("  2. Check statistics with: peachflow-graph.py stats")
    print("  3. Create a sprint: /peachflow:create-sprint")

    return {"graph": graph, "state": new_state}


def main():
    parser = argparse.ArgumentParser(description="Migrate peachflow v2 to v3")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        migrate(dry_run=args.dry_run, verbose=args.verbose)
    except MigrationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
