#!/usr/bin/env python3
"""
peachflow-graph.py - Graph-based work item management for Peachflow v3

A unified CLI tool for managing epics, stories, tasks, clarifications, ADRs,
and sprints in a JSON graph structure.

Usage:
    peachflow-graph.py <command> [options]

Commands:
    init                    Initialize empty graph
    create <type>           Create entity (epic, story, task, clarification, adr, sprint)
    get <type> <id>         Get entity by ID
    update <type> <id>      Update entity
    delete <type> <id>      Delete entity (soft delete)
    list <type>             List entities with filters
    depends                 Manage task dependencies
    ready-tasks             Find tasks ready for work
    chain <id>              Get full chain (task->story->epic->quarter)
    descendants <type> <id> Get all children of entity
    stats                   Show statistics
    sprint-create           Auto-create sprint from ready tasks
    sprint-active           Get current active sprint
    sprint-complete <id>    Complete a sprint
    next-id <type>          Get next available ID
    export                  Export graph
    serve                   Start visualization server
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
import http.server
import socketserver
import webbrowser
import threading


# === Constants ===

DEFAULT_GRAPH_PATH = ".peachflow-graph.json"
VERSION = "3.0.0"

ENTITY_TYPES = ["epic", "story", "task", "clarification", "adr", "sprint", "quarter"]
TASK_TAGS = ["FE", "BE", "DevOps", "Full"]
ENTITY_STATUSES = {
    "quarter": ["planned", "active", "completed"],
    "epic": ["draft", "ready", "in_progress", "completed", "blocked"],
    "story": ["draft", "ready", "in_progress", "completed", "blocked"],
    "task": ["pending", "in_progress", "completed", "blocked", "skipped"],
    "clarification": ["pending", "clarified"],
    "adr": ["proposed", "accepted", "deprecated", "superseded"],
    "sprint": ["planned", "active", "completed"],
}

ID_PATTERNS = {
    "quarter": "Q",
    "epic": "E-",
    "story": "US-",
    "task": "T-",
    "clarification": "CL-",
    "adr": "ADR-",
    "sprint": "S-",
}


# === Color Output ===

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"

    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith("_") and attr != "disable":
                setattr(cls, attr, "")


if os.environ.get("PEACHFLOW_NO_COLOR") or not sys.stdout.isatty():
    Colors.disable()


# === Graph Class ===

class PeachflowGraph:
    def __init__(self, path: str = None):
        self.path = Path(path or os.environ.get("PEACHFLOW_GRAPH_PATH", DEFAULT_GRAPH_PATH))
        self.data = None
        self._load()

    def _load(self):
        """Load graph from file or create empty."""
        if self.path.exists():
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = None

    def _save(self):
        """Save graph to file."""
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def _now(self) -> str:
        """Get current ISO timestamp."""
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def init(self) -> dict:
        """Initialize empty graph."""
        self.data = {
            "version": VERSION,
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
        self._save()
        return {"status": "initialized", "path": str(self.path)}

    def _ensure_loaded(self):
        """Ensure graph is loaded."""
        if self.data is None:
            raise ValueError("Graph not initialized. Run 'peachflow-graph init' first.")

    def next_id(self, entity_type: str) -> str:
        """Generate next ID for entity type."""
        self._ensure_loaded()
        if entity_type not in self.data["counters"]:
            raise ValueError(f"Unknown entity type: {entity_type}")

        self.data["counters"][entity_type] += 1
        counter = self.data["counters"][entity_type]
        prefix = ID_PATTERNS.get(entity_type, "")

        if entity_type == "adr":
            return f"{prefix}{counter:04d}"
        else:
            return f"{prefix}{counter:03d}"

    # === Create Operations ===

    def create_epic(self, title: str, quarter: str, priority: int = 5,
                    description: str = "", deliverables: list = None) -> dict:
        """Create a new epic."""
        self._ensure_loaded()
        if quarter not in ["Q1", "Q2", "Q3", "Q4"]:
            raise ValueError(f"Invalid quarter: {quarter}")

        epic_id = self.next_id("epic")
        epic = {
            "id": epic_id,
            "title": title,
            "description": description,
            "status": "draft",
            "quarter": quarter,
            "priority": priority,
            "deliverables": deliverables or [],
            "createdAt": self._now(),
            "updatedAt": self._now(),
        }

        self.data["entities"]["epics"][epic_id] = epic
        self.data["relationships"]["quarter_epics"][quarter].append(epic_id)
        self.data["relationships"]["epic_stories"][epic_id] = []
        self._save()
        return epic

    def create_story(self, epic_id: str, title: str, description: str = "",
                     acceptance_criteria: list = None) -> dict:
        """Create a new user story under an epic."""
        self._ensure_loaded()
        if epic_id not in self.data["entities"]["epics"]:
            raise ValueError(f"Epic not found: {epic_id}")

        story_id = self.next_id("story")
        story = {
            "id": story_id,
            "title": title,
            "description": description,
            "status": "draft",
            "epicId": epic_id,
            "acceptanceCriteria": acceptance_criteria or [],
            "createdAt": self._now(),
            "updatedAt": self._now(),
        }

        self.data["entities"]["stories"][story_id] = story
        self.data["relationships"]["epic_stories"][epic_id].append(story_id)
        self.data["relationships"]["story_tasks"][story_id] = []
        self._save()
        return story

    def create_task(self, story_id: str, title: str, tag: str,
                    description: str = "", depends_on: list = None) -> dict:
        """Create a new task under a story."""
        self._ensure_loaded()
        if story_id not in self.data["entities"]["stories"]:
            raise ValueError(f"Story not found: {story_id}")
        if tag not in TASK_TAGS:
            raise ValueError(f"Invalid tag: {tag}. Must be one of {TASK_TAGS}")

        task_id = self.next_id("task")
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": "pending",
            "storyId": story_id,
            "tag": tag,
            "sprintId": None,
            "createdAt": self._now(),
            "updatedAt": self._now(),
            "completedAt": None,
        }

        self.data["entities"]["tasks"][task_id] = task
        self.data["relationships"]["story_tasks"][story_id].append(task_id)
        self.data["relationships"]["task_dependencies"][task_id] = depends_on or []
        self._save()
        return task

    def create_clarification(self, entity_id: str, question: str,
                             entity_type: str = "general") -> dict:
        """Create a clarification request for an entity."""
        self._ensure_loaded()
        cl_id = self.next_id("clarification")
        clarification = {
            "id": cl_id,
            "question": question,
            "answer": None,
            "status": "pending",
            "entityId": entity_id,
            "entityType": entity_type,
            "createdAt": self._now(),
            "clarifiedAt": None,
        }

        self.data["entities"]["clarifications"][cl_id] = clarification
        if entity_id not in self.data["relationships"]["entity_clarifications"]:
            self.data["relationships"]["entity_clarifications"][entity_id] = []
        self.data["relationships"]["entity_clarifications"][entity_id].append(cl_id)
        self._save()
        return clarification

    def create_adr(self, title: str, context: str = "", decision: str = "",
                   consequences: str = "", entity_id: str = None) -> dict:
        """Create an Architecture Decision Record."""
        self._ensure_loaded()
        adr_id = self.next_id("adr")
        adr = {
            "id": adr_id,
            "title": title,
            "status": "proposed",
            "context": context,
            "decision": decision,
            "consequences": consequences,
            "entityId": entity_id,
            "filePath": f"docs/architecture/adr/{adr_id.lower()}-{title.lower().replace(' ', '-')[:30]}.md",
            "createdAt": self._now(),
            "updatedAt": self._now(),
        }

        self.data["entities"]["adrs"][adr_id] = adr
        if entity_id:
            if entity_id not in self.data["relationships"]["entity_adrs"]:
                self.data["relationships"]["entity_adrs"][entity_id] = []
            self.data["relationships"]["entity_adrs"][entity_id].append(adr_id)
        self._save()
        return adr

    def create_sprint(self, quarter: str, task_ids: list = None, name: str = "") -> dict:
        """Create a new sprint."""
        self._ensure_loaded()
        if quarter not in ["Q1", "Q2", "Q3", "Q4"]:
            raise ValueError(f"Invalid quarter: {quarter}")

        sprint_id = self.next_id("sprint")
        sprint = {
            "id": sprint_id,
            "quarterId": quarter,
            "name": name,
            "status": "planned",
            "taskIds": task_ids or [],
            "worktreePath": None,
            "createdAt": self._now(),
            "startedAt": None,
            "completedAt": None,
        }

        # Assign tasks to this sprint
        for task_id in task_ids or []:
            if task_id in self.data["entities"]["tasks"]:
                self.data["entities"]["tasks"][task_id]["sprintId"] = sprint_id

        self.data["entities"]["sprints"][sprint_id] = sprint
        self._save()
        return sprint

    # === Get Operations ===

    def get(self, entity_type: str, entity_id: str) -> dict:
        """Get entity by type and ID."""
        self._ensure_loaded()
        type_map = {
            "quarter": "quarters",
            "epic": "epics",
            "story": "stories",
            "task": "tasks",
            "clarification": "clarifications",
            "adr": "adrs",
            "sprint": "sprints",
        }
        collection = type_map.get(entity_type)
        if not collection:
            raise ValueError(f"Unknown entity type: {entity_type}")

        entity = self.data["entities"][collection].get(entity_id)
        if not entity:
            raise ValueError(f"{entity_type} not found: {entity_id}")
        return entity

    # === Update Operations ===

    def update(self, entity_type: str, entity_id: str, cascade: bool = True, **kwargs) -> dict:
        """Update entity fields. Optionally cascade status changes to parents."""
        self._ensure_loaded()
        entity = self.get(entity_type, entity_id)

        # Validate status if provided
        if "status" in kwargs:
            valid_statuses = ENTITY_STATUSES.get(entity_type, [])
            if valid_statuses and kwargs["status"] not in valid_statuses:
                raise ValueError(f"Invalid status: {kwargs['status']}. Must be one of {valid_statuses}")

        # Track if status changed
        status_changed = "status" in kwargs and entity.get("status") != kwargs["status"]

        # Update fields
        for key, value in kwargs.items():
            if key in entity:
                entity[key] = value

        entity["updatedAt"] = self._now()

        # Special handling for task completion
        if entity_type == "task" and kwargs.get("status") == "completed":
            entity["completedAt"] = self._now()

        # Special handling for clarification
        if entity_type == "clarification" and kwargs.get("status") == "clarified":
            entity["clarifiedAt"] = self._now()

        self._save()

        # Cascade status check if status changed and cascade is enabled
        cascade_changes = {}
        if cascade and status_changed:
            cascade_changes = self.cascade_status_check(entity_type, entity_id)

        # Return entity with cascade info
        result = entity.copy()
        if cascade_changes:
            result["_cascaded"] = cascade_changes

        return result

    # === Delete Operations ===

    def delete(self, entity_type: str, entity_id: str) -> dict:
        """Soft delete an entity (marks as deleted/skipped)."""
        self._ensure_loaded()
        if entity_type == "task":
            return self.update("task", entity_id, status="skipped")
        else:
            # For other types, actually remove
            entity = self.get(entity_type, entity_id)
            type_map = {
                "epic": "epics",
                "story": "stories",
                "clarification": "clarifications",
                "adr": "adrs",
                "sprint": "sprints",
            }
            collection = type_map.get(entity_type)
            if collection:
                del self.data["entities"][collection][entity_id]
                self._save()
            return {"deleted": entity_id}

    # === List Operations ===

    def list_entities(self, entity_type: str, **filters) -> list:
        """List entities with optional filters."""
        self._ensure_loaded()
        type_map = {
            "quarter": "quarters",
            "epic": "epics",
            "story": "stories",
            "task": "tasks",
            "clarification": "clarifications",
            "adr": "adrs",
            "sprint": "sprints",
        }
        collection = type_map.get(entity_type)
        if not collection:
            raise ValueError(f"Unknown entity type: {entity_type}")

        entities = list(self.data["entities"][collection].values())

        # Apply filters
        if "quarter" in filters and filters["quarter"]:
            if entity_type == "epic":
                entities = [e for e in entities if e.get("quarter") == filters["quarter"]]
            elif entity_type == "story":
                # Get stories via epics in quarter
                epic_ids = self.data["relationships"]["quarter_epics"].get(filters["quarter"], [])
                story_ids = []
                for epic_id in epic_ids:
                    story_ids.extend(self.data["relationships"]["epic_stories"].get(epic_id, []))
                entities = [e for e in entities if e["id"] in story_ids]
            elif entity_type == "task":
                # Get tasks via stories via epics in quarter
                epic_ids = self.data["relationships"]["quarter_epics"].get(filters["quarter"], [])
                task_ids = []
                for epic_id in epic_ids:
                    for story_id in self.data["relationships"]["epic_stories"].get(epic_id, []):
                        task_ids.extend(self.data["relationships"]["story_tasks"].get(story_id, []))
                entities = [e for e in entities if e["id"] in task_ids]
            elif entity_type == "sprint":
                entities = [e for e in entities if e.get("quarterId") == filters["quarter"]]

        if "epic" in filters and filters["epic"]:
            if entity_type == "story":
                entities = [e for e in entities if e.get("epicId") == filters["epic"]]
            elif entity_type == "task":
                story_ids = self.data["relationships"]["epic_stories"].get(filters["epic"], [])
                task_ids = []
                for story_id in story_ids:
                    task_ids.extend(self.data["relationships"]["story_tasks"].get(story_id, []))
                entities = [e for e in entities if e["id"] in task_ids]

        if "story" in filters and filters["story"]:
            if entity_type == "task":
                entities = [e for e in entities if e.get("storyId") == filters["story"]]

        if "status" in filters and filters["status"]:
            entities = [e for e in entities if e.get("status") == filters["status"]]

        if "tag" in filters and filters["tag"]:
            entities = [e for e in entities if e.get("tag") == filters["tag"]]

        if "sprint" in filters and filters["sprint"]:
            entities = [e for e in entities if e.get("sprintId") == filters["sprint"]]

        if filters.get("unassigned"):
            entities = [e for e in entities if not e.get("sprintId")]

        if filters.get("pending"):
            entities = [e for e in entities if e.get("status") == "pending"]

        if "entity" in filters and filters["entity"]:
            # For clarifications/ADRs linked to specific entity
            if entity_type == "clarification":
                entities = [e for e in entities if e.get("entityId") == filters["entity"]]
            elif entity_type == "adr":
                entities = [e for e in entities if e.get("entityId") == filters["entity"]]

        # Sort by priority for epics, by ID otherwise
        if entity_type == "epic":
            entities.sort(key=lambda x: (x.get("priority", 99), x["id"]))
        else:
            entities.sort(key=lambda x: x["id"])

        return entities

    # === Dependency Operations ===

    def add_dependency(self, task_id: str, depends_on: str) -> dict:
        """Add a dependency: task_id depends on depends_on."""
        self._ensure_loaded()
        if task_id not in self.data["entities"]["tasks"]:
            raise ValueError(f"Task not found: {task_id}")
        if depends_on not in self.data["entities"]["tasks"]:
            raise ValueError(f"Dependency task not found: {depends_on}")

        deps = self.data["relationships"]["task_dependencies"].get(task_id, [])
        if depends_on not in deps:
            deps.append(depends_on)
            self.data["relationships"]["task_dependencies"][task_id] = deps
            self._save()
        return {"task": task_id, "depends_on": deps}

    def remove_dependency(self, task_id: str, depends_on: str) -> dict:
        """Remove a dependency."""
        self._ensure_loaded()
        deps = self.data["relationships"]["task_dependencies"].get(task_id, [])
        if depends_on in deps:
            deps.remove(depends_on)
            self.data["relationships"]["task_dependencies"][task_id] = deps
            self._save()
        return {"task": task_id, "depends_on": deps}

    def get_dependencies(self, task_id: str) -> list:
        """Get tasks that task_id depends on."""
        self._ensure_loaded()
        return self.data["relationships"]["task_dependencies"].get(task_id, [])

    def get_blockers(self, task_id: str) -> list:
        """Get unresolved blocking tasks."""
        self._ensure_loaded()
        deps = self.get_dependencies(task_id)
        blockers = []
        for dep_id in deps:
            task = self.data["entities"]["tasks"].get(dep_id)
            if task and task["status"] not in ["completed", "skipped"]:
                blockers.append(task)
        return blockers

    # === Traversal Operations ===

    def get_ready_tasks(self, quarter: str = None, epic: str = None, limit: int = None) -> list:
        """Find tasks ready for work (pending + no blockers)."""
        self._ensure_loaded()
        tasks = self.list_entities("task", quarter=quarter, epic=epic, status="pending", unassigned=True)
        ready = []
        for task in tasks:
            blockers = self.get_blockers(task["id"])
            if not blockers:
                ready.append(task)
                if limit and len(ready) >= limit:
                    break
        return ready

    def get_chain(self, task_id: str) -> dict:
        """Get full chain: task -> story -> epic -> quarter."""
        self._ensure_loaded()
        task = self.get("task", task_id)
        story = self.get("story", task["storyId"])
        epic = self.get("epic", story["epicId"])

        return {
            "quarter": epic["quarter"],
            "epic": epic,
            "story": story,
            "task": task,
            "path": f"{epic['quarter']}/{epic['id']}/{story['id']}/{task['id']}",
        }

    def get_descendants(self, entity_type: str, entity_id: str) -> dict:
        """Get all children of an entity."""
        self._ensure_loaded()
        result = {"epics": [], "stories": [], "tasks": []}

        if entity_type == "quarter":
            epic_ids = self.data["relationships"]["quarter_epics"].get(entity_id, [])
            for epic_id in epic_ids:
                result["epics"].append(self.get("epic", epic_id))
                story_ids = self.data["relationships"]["epic_stories"].get(epic_id, [])
                for story_id in story_ids:
                    result["stories"].append(self.get("story", story_id))
                    task_ids = self.data["relationships"]["story_tasks"].get(story_id, [])
                    for task_id in task_ids:
                        result["tasks"].append(self.get("task", task_id))

        elif entity_type == "epic":
            story_ids = self.data["relationships"]["epic_stories"].get(entity_id, [])
            for story_id in story_ids:
                result["stories"].append(self.get("story", story_id))
                task_ids = self.data["relationships"]["story_tasks"].get(story_id, [])
                for task_id in task_ids:
                    result["tasks"].append(self.get("task", task_id))

        elif entity_type == "story":
            task_ids = self.data["relationships"]["story_tasks"].get(entity_id, [])
            for task_id in task_ids:
                result["tasks"].append(self.get("task", task_id))

        return result

    # -------------------------------------------------------------------------
    # Status Aggregation Helpers
    # -------------------------------------------------------------------------

    def _get_story_tasks_status(self, story_id: str) -> dict:
        """Get aggregated status counts for all tasks in a story."""
        task_ids = self.data["relationships"]["story_tasks"].get(story_id, [])
        tasks = [self.data["entities"]["tasks"].get(tid) for tid in task_ids
                 if self.data["entities"]["tasks"].get(tid)]

        return {
            "total": len(tasks),
            "completed": sum(1 for t in tasks if t["status"] == "completed"),
            "skipped": sum(1 for t in tasks if t["status"] == "skipped"),
            "in_progress": sum(1 for t in tasks if t["status"] == "in_progress"),
            "blocked": sum(1 for t in tasks if t["status"] == "blocked"),
            "pending": sum(1 for t in tasks if t["status"] == "pending"),
        }

    def _get_epic_stories_status(self, epic_id: str) -> dict:
        """Get aggregated status counts for all stories in an epic."""
        story_ids = self.data["relationships"]["epic_stories"].get(epic_id, [])
        stories = [self.data["entities"]["stories"].get(sid) for sid in story_ids
                   if self.data["entities"]["stories"].get(sid)]

        return {
            "total": len(stories),
            "completed": sum(1 for s in stories if s["status"] == "completed"),
            "in_progress": sum(1 for s in stories if s["status"] == "in_progress"),
            "blocked": sum(1 for s in stories if s["status"] == "blocked"),
            "ready": sum(1 for s in stories if s["status"] == "ready"),
            "draft": sum(1 for s in stories if s["status"] == "draft"),
        }

    def _get_quarter_epics_status(self, quarter_id: str) -> dict:
        """Get aggregated status counts for all epics in a quarter."""
        epic_ids = self.data["relationships"]["quarter_epics"].get(quarter_id, [])
        epics = [self.data["entities"]["epics"].get(eid) for eid in epic_ids
                 if self.data["entities"]["epics"].get(eid)]

        return {
            "total": len(epics),
            "completed": sum(1 for e in epics if e["status"] == "completed"),
            "in_progress": sum(1 for e in epics if e["status"] == "in_progress"),
            "blocked": sum(1 for e in epics if e["status"] == "blocked"),
            "ready": sum(1 for e in epics if e["status"] == "ready"),
            "draft": sum(1 for e in epics if e["status"] == "draft"),
        }

    # -------------------------------------------------------------------------
    # Status Computation Methods
    # -------------------------------------------------------------------------

    def _compute_story_status(self, story_id: str) -> str:
        """Compute what a story's status should be based on its tasks."""
        stats = self._get_story_tasks_status(story_id)

        if stats["total"] == 0:
            return None  # No change - story has no tasks

        # All done (completed or skipped)
        if stats["completed"] + stats["skipped"] == stats["total"]:
            return "completed"

        # All remaining are blocked
        remaining = stats["total"] - stats["completed"] - stats["skipped"]
        if remaining > 0 and stats["blocked"] == remaining:
            return "blocked"

        # Some work started
        if stats["in_progress"] > 0 or stats["completed"] > 0:
            return "in_progress"

        return None  # No status change needed

    def _compute_epic_status(self, epic_id: str) -> str:
        """Compute what an epic's status should be based on its stories."""
        stats = self._get_epic_stories_status(epic_id)

        if stats["total"] == 0:
            return None

        if stats["completed"] == stats["total"]:
            return "completed"

        remaining = stats["total"] - stats["completed"]
        if remaining > 0 and stats["blocked"] == remaining:
            return "blocked"

        if stats["in_progress"] > 0 or stats["completed"] > 0:
            return "in_progress"

        return None

    def _compute_quarter_status(self, quarter_id: str) -> str:
        """Compute what a quarter's status should be based on its epics."""
        stats = self._get_quarter_epics_status(quarter_id)

        if stats["total"] == 0:
            return None

        if stats["completed"] == stats["total"]:
            return "completed"

        if stats["in_progress"] > 0 or stats["completed"] > 0:
            return "active"

        return None

    def _compute_sprint_status(self, sprint_id: str) -> str:
        """Compute what a sprint's status should be based on its tasks."""
        sprint = self.data["entities"]["sprints"].get(sprint_id)
        if not sprint:
            return None

        task_ids = sprint.get("taskIds", [])
        if not task_ids:
            return None

        tasks = [self.data["entities"]["tasks"].get(tid) for tid in task_ids
                 if self.data["entities"]["tasks"].get(tid)]

        if not tasks:
            return None

        completed_or_skipped = sum(1 for t in tasks if t["status"] in ["completed", "skipped"])

        if completed_or_skipped == len(tasks):
            return "completed"

        return None  # Sprint stays active until all tasks done

    # -------------------------------------------------------------------------
    # Cascade Status Methods
    # -------------------------------------------------------------------------

    def _unblock_dependents(self, task_id: str) -> list:
        """Re-evaluate tasks that depend on the completed task."""
        unblocked = []

        # Find tasks that depend on this one
        for tid, deps in self.data["relationships"]["task_dependencies"].items():
            if task_id in deps:
                task = self.data["entities"]["tasks"].get(tid)
                if task and task["status"] == "blocked":
                    # Check if all dependencies are now resolved
                    blockers = self.get_blockers(tid)
                    if not blockers:
                        task["status"] = "pending"
                        task["updatedAt"] = self._now()
                        unblocked.append(tid)

        return unblocked

    def cascade_status_check(self, entity_type: str, entity_id: str) -> dict:
        """
        Check and update parent statuses after an entity status change.

        Returns dict of all status changes made: {entity_id: new_status}
        """
        self._ensure_loaded()
        changes = {}

        if entity_type == "task":
            task = self.data["entities"]["tasks"].get(entity_id)
            if not task:
                return changes

            # If task is completed, unblock any dependents
            if task["status"] == "completed":
                unblocked = self._unblock_dependents(entity_id)
                for uid in unblocked:
                    changes[uid] = "pending (unblocked)"

            # Get task's story
            story_id = task.get("storyId")
            if story_id:
                # Check story status
                new_story_status = self._compute_story_status(story_id)
                if new_story_status:
                    story = self.data["entities"]["stories"].get(story_id)
                    if story and story["status"] != new_story_status:
                        story["status"] = new_story_status
                        story["updatedAt"] = self._now()
                        if new_story_status == "completed":
                            story["completedAt"] = self._now()
                        changes[story_id] = new_story_status

                # Get story's epic
                story = self.data["entities"]["stories"].get(story_id)
                if story:
                    epic_id = story.get("epicId")
                    if epic_id:
                        # Check epic status
                        new_epic_status = self._compute_epic_status(epic_id)
                        if new_epic_status:
                            epic = self.data["entities"]["epics"].get(epic_id)
                            if epic and epic["status"] != new_epic_status:
                                epic["status"] = new_epic_status
                                epic["updatedAt"] = self._now()
                                if new_epic_status == "completed":
                                    epic["completedAt"] = self._now()
                                changes[epic_id] = new_epic_status

                        # Get epic's quarter
                        epic = self.data["entities"]["epics"].get(epic_id)
                        if epic:
                            quarter_id = epic.get("quarter")
                            if quarter_id:
                                new_quarter_status = self._compute_quarter_status(quarter_id)
                                if new_quarter_status:
                                    quarter = self.data["entities"]["quarters"].get(quarter_id)
                                    if quarter and quarter["status"] != new_quarter_status:
                                        quarter["status"] = new_quarter_status
                                        quarter["updatedAt"] = self._now()
                                        if new_quarter_status == "completed":
                                            quarter["completedAt"] = self._now()
                                        changes[quarter_id] = new_quarter_status

            # Check sprint status if task is in a sprint
            sprint_id = task.get("sprintId")
            if sprint_id:
                new_sprint_status = self._compute_sprint_status(sprint_id)
                if new_sprint_status:
                    sprint = self.data["entities"]["sprints"].get(sprint_id)
                    if sprint and sprint["status"] != new_sprint_status:
                        sprint["status"] = new_sprint_status
                        sprint["completedAt"] = self._now()
                        sprint["updatedAt"] = self._now()
                        changes[sprint_id] = new_sprint_status

        elif entity_type == "story":
            # Cascade up from story
            story = self.data["entities"]["stories"].get(entity_id)
            if story:
                epic_id = story.get("epicId")
                if epic_id:
                    new_epic_status = self._compute_epic_status(epic_id)
                    if new_epic_status:
                        epic = self.data["entities"]["epics"].get(epic_id)
                        if epic and epic["status"] != new_epic_status:
                            epic["status"] = new_epic_status
                            epic["updatedAt"] = self._now()
                            if new_epic_status == "completed":
                                epic["completedAt"] = self._now()
                            changes[epic_id] = new_epic_status

                    epic = self.data["entities"]["epics"].get(epic_id)
                    if epic:
                        quarter_id = epic.get("quarter")
                        if quarter_id:
                            new_quarter_status = self._compute_quarter_status(quarter_id)
                            if new_quarter_status:
                                quarter = self.data["entities"]["quarters"].get(quarter_id)
                                if quarter and quarter["status"] != new_quarter_status:
                                    quarter["status"] = new_quarter_status
                                    quarter["updatedAt"] = self._now()
                                    if new_quarter_status == "completed":
                                        quarter["completedAt"] = self._now()
                                    changes[quarter_id] = new_quarter_status

        elif entity_type == "epic":
            epic = self.data["entities"]["epics"].get(entity_id)
            if epic:
                quarter_id = epic.get("quarter")
                if quarter_id:
                    new_quarter_status = self._compute_quarter_status(quarter_id)
                    if new_quarter_status:
                        quarter = self.data["entities"]["quarters"].get(quarter_id)
                        if quarter and quarter["status"] != new_quarter_status:
                            quarter["status"] = new_quarter_status
                            quarter["updatedAt"] = self._now()
                            if new_quarter_status == "completed":
                                quarter["completedAt"] = self._now()
                            changes[quarter_id] = new_quarter_status

        if changes:
            self._save()

        return changes

    # -------------------------------------------------------------------------
    # Acceptance Criteria Methods
    # -------------------------------------------------------------------------

    def update_acceptance_criterion(self, story_id: str, criterion_index: int, done: bool) -> dict:
        """Update a specific acceptance criterion's done status."""
        self._ensure_loaded()
        story = self.get("story", story_id)

        criteria = story.get("acceptanceCriteria", [])
        if criterion_index < 0 or criterion_index >= len(criteria):
            raise ValueError(f"Invalid criterion index: {criterion_index}. Story has {len(criteria)} criteria.")

        # Handle both old format (string) and new format ({title, done})
        if isinstance(criteria[criterion_index], str):
            criteria[criterion_index] = {"title": criteria[criterion_index], "done": done}
        else:
            criteria[criterion_index]["done"] = done

        story["acceptanceCriteria"] = criteria
        story["updatedAt"] = self._now()
        self._save()

        return story

    def get_acceptance_progress(self, story_id: str) -> dict:
        """Get acceptance criteria completion status for a story."""
        self._ensure_loaded()
        story = self.get("story", story_id)

        criteria = story.get("acceptanceCriteria", [])
        total = len(criteria)
        done = sum(1 for c in criteria if isinstance(c, dict) and c.get("done", False))

        return {
            "story_id": story_id,
            "total": total,
            "done": done,
            "remaining": total - done,
            "progress": done / total if total > 0 else 0,
            "criteria": criteria
        }

    def get_stats(self, quarter: str = None, epic: str = None) -> dict:
        """Get statistics."""
        self._ensure_loaded()

        if epic:
            stories = self.list_entities("story", epic=epic)
            tasks = self.list_entities("task", epic=epic)
        elif quarter:
            stories = self.list_entities("story", quarter=quarter)
            tasks = self.list_entities("task", quarter=quarter)
        else:
            stories = self.list_entities("story")
            tasks = self.list_entities("task")

        epics = self.list_entities("epic", quarter=quarter) if not epic else [self.get("epic", epic)]

        completed_tasks = [t for t in tasks if t["status"] == "completed"]
        pending_tasks = [t for t in tasks if t["status"] == "pending"]
        blocked_tasks = [t for t in tasks if self.get_blockers(t["id"])]

        return {
            "epics": {
                "total": len(epics),
                "by_status": self._count_by_status(epics),
            },
            "stories": {
                "total": len(stories),
                "by_status": self._count_by_status(stories),
            },
            "tasks": {
                "total": len(tasks),
                "completed": len(completed_tasks),
                "pending": len(pending_tasks),
                "blocked": len(blocked_tasks),
                "by_tag": self._count_by_field(tasks, "tag"),
                "by_status": self._count_by_status(tasks),
            },
            "progress": len(completed_tasks) / len(tasks) if tasks else 0,
            "clarifications": {
                "pending": len(self.list_entities("clarification", pending=True)),
                "total": len(self.list_entities("clarification")),
            },
        }

    def _count_by_status(self, entities: list) -> dict:
        counts = {}
        for e in entities:
            status = e.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts

    def _count_by_field(self, entities: list, field: str) -> dict:
        counts = {}
        for e in entities:
            value = e.get(field, "unknown")
            counts[value] = counts.get(value, 0) + 1
        return counts

    # === Sprint Operations ===

    def auto_create_sprint(self, quarter: str, max_tasks: int = 10, name: str = "") -> dict:
        """Auto-create sprint from ready tasks."""
        self._ensure_loaded()
        ready_tasks = self.get_ready_tasks(quarter=quarter, limit=max_tasks)

        if not ready_tasks:
            return {"error": "No ready tasks found", "sprint": None}

        task_ids = [t["id"] for t in ready_tasks]
        sprint = self.create_sprint(quarter, task_ids, name)
        return {"sprint": sprint, "tasks": ready_tasks}

    def get_active_sprint(self) -> Optional[dict]:
        """Get current active sprint."""
        self._ensure_loaded()
        sprints = self.list_entities("sprint", status="active")
        return sprints[0] if sprints else None

    def complete_sprint(self, sprint_id: str) -> dict:
        """Complete a sprint."""
        return self.update("sprint", sprint_id, status="completed", completedAt=self._now())

    # === Export ===

    def export(self, format: str = "json") -> str:
        """Export graph in specified format."""
        self._ensure_loaded()
        if format == "json":
            return json.dumps(self.data, indent=2)
        elif format == "markdown":
            return self._export_markdown()
        else:
            raise ValueError(f"Unknown format: {format}")

    def _export_markdown(self) -> str:
        """Export as markdown overview."""
        self._ensure_loaded()
        lines = ["# Peachflow Project Overview\n"]

        for quarter in ["Q1", "Q2", "Q3", "Q4"]:
            q_data = self.data["entities"]["quarters"].get(quarter, {})
            epic_ids = self.data["relationships"]["quarter_epics"].get(quarter, [])
            if not epic_ids:
                continue

            lines.append(f"\n## {quarter}: {q_data.get('theme', 'Untitled')}\n")

            for epic_id in epic_ids:
                epic = self.data["entities"]["epics"].get(epic_id, {})
                lines.append(f"\n### {epic_id}: {epic.get('title', 'Untitled')}")
                lines.append(f"Status: {epic.get('status', 'unknown')} | Priority: {epic.get('priority', '-')}\n")

                story_ids = self.data["relationships"]["epic_stories"].get(epic_id, [])
                for story_id in story_ids:
                    story = self.data["entities"]["stories"].get(story_id, {})
                    lines.append(f"\n#### {story_id}: {story.get('title', 'Untitled')}")

                    task_ids = self.data["relationships"]["story_tasks"].get(story_id, [])
                    for task_id in task_ids:
                        task = self.data["entities"]["tasks"].get(task_id, {})
                        status_icon = "✅" if task.get("status") == "completed" else "⬜"
                        lines.append(f"- {status_icon} [{task.get('tag', '?')}] {task_id}: {task.get('title', 'Untitled')}")

        return "\n".join(lines)


# === Visualization Server ===

def create_visualization_html(graph: PeachflowGraph) -> str:
    """Create HTML visualization of the graph."""
    data = graph.data

    # Build nodes and edges for visualization
    nodes = []
    edges = []

    # Add quarters
    for q_id, quarter in data["entities"]["quarters"].items():
        nodes.append({
            "id": q_id,
            "label": q_id,
            "type": "quarter",
            "status": quarter.get("status", "planned"),
            "theme": quarter.get("theme", ""),
        })

    # Add epics
    for epic_id, epic in data["entities"]["epics"].items():
        nodes.append({
            "id": epic_id,
            "label": f"{epic_id}\\n{epic.get('title', '')[:30]}",
            "type": "epic",
            "status": epic.get("status", "draft"),
            "priority": epic.get("priority", 5),
        })
        edges.append({"from": epic.get("quarter"), "to": epic_id})

    # Add stories
    for story_id, story in data["entities"]["stories"].items():
        nodes.append({
            "id": story_id,
            "label": f"{story_id}\\n{story.get('title', '')[:25]}",
            "type": "story",
            "status": story.get("status", "draft"),
        })
        edges.append({"from": story.get("epicId"), "to": story_id})

    # Add tasks
    for task_id, task in data["entities"]["tasks"].items():
        nodes.append({
            "id": task_id,
            "label": f"[{task.get('tag', '?')}] {task_id}",
            "type": "task",
            "status": task.get("status", "pending"),
            "tag": task.get("tag", ""),
        })
        edges.append({"from": task.get("storyId"), "to": task_id})

        # Add dependency edges
        deps = data["relationships"]["task_dependencies"].get(task_id, [])
        for dep_id in deps:
            edges.append({"from": dep_id, "to": task_id, "type": "dependency"})

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Peachflow Graph Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.6/vis-network.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #eee; }}
        #header {{ padding: 16px 24px; background: #16213e; border-bottom: 1px solid #0f3460; display: flex; justify-content: space-between; align-items: center; }}
        #header h1 {{ font-size: 20px; font-weight: 500; }}
        #stats {{ display: flex; gap: 24px; }}
        .stat {{ text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: 600; color: #e94560; }}
        .stat-label {{ font-size: 11px; color: #888; text-transform: uppercase; }}
        #container {{ display: flex; height: calc(100vh - 60px); }}
        #graph {{ flex: 1; background: #1a1a2e; }}
        #sidebar {{ width: 320px; background: #16213e; border-left: 1px solid #0f3460; overflow-y: auto; }}
        #sidebar h2 {{ padding: 16px; font-size: 14px; border-bottom: 1px solid #0f3460; }}
        .entity-list {{ padding: 8px; }}
        .entity-item {{ padding: 10px 12px; margin: 4px 0; background: #1a1a2e; border-radius: 6px; cursor: pointer; transition: all 0.2s; }}
        .entity-item:hover {{ background: #0f3460; }}
        .entity-id {{ font-weight: 600; color: #e94560; }}
        .entity-title {{ font-size: 13px; color: #ccc; margin-top: 4px; }}
        .entity-meta {{ font-size: 11px; color: #666; margin-top: 4px; }}
        .status-badge {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 10px; text-transform: uppercase; }}
        .status-completed {{ background: #10b981; color: #fff; }}
        .status-in_progress {{ background: #f59e0b; color: #000; }}
        .status-pending, .status-draft, .status-planned {{ background: #6b7280; color: #fff; }}
        .status-blocked {{ background: #ef4444; color: #fff; }}
        .legend {{ padding: 16px; border-top: 1px solid #0f3460; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; margin: 6px 0; font-size: 12px; }}
        .legend-color {{ width: 16px; height: 16px; border-radius: 4px; }}
        .tab-buttons {{ display: flex; border-bottom: 1px solid #0f3460; }}
        .tab-btn {{ flex: 1; padding: 12px; background: none; border: none; color: #888; cursor: pointer; font-size: 12px; text-transform: uppercase; }}
        .tab-btn.active {{ color: #e94560; border-bottom: 2px solid #e94560; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
    </style>
</head>
<body>
    <div id="header">
        <h1>Peachflow Project Graph</h1>
        <div id="stats">
            <div class="stat">
                <div class="stat-value">{len(data['entities']['epics'])}</div>
                <div class="stat-label">Epics</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(data['entities']['stories'])}</div>
                <div class="stat-label">Stories</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(data['entities']['tasks'])}</div>
                <div class="stat-label">Tasks</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len([t for t in data['entities']['tasks'].values() if t.get('status') == 'completed'])}</div>
                <div class="stat-label">Done</div>
            </div>
        </div>
    </div>
    <div id="container">
        <div id="graph"></div>
        <div id="sidebar">
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="showTab('epics')">Epics</button>
                <button class="tab-btn" onclick="showTab('tasks')">Tasks</button>
                <button class="tab-btn" onclick="showTab('legend')">Legend</button>
            </div>
            <div id="epics-tab" class="tab-content active">
                <div class="entity-list" id="epic-list"></div>
            </div>
            <div id="tasks-tab" class="tab-content">
                <div class="entity-list" id="task-list"></div>
            </div>
            <div id="legend-tab" class="tab-content">
                <div class="legend">
                    <div class="legend-item"><div class="legend-color" style="background: #e94560"></div> Quarter</div>
                    <div class="legend-item"><div class="legend-color" style="background: #0f3460"></div> Epic</div>
                    <div class="legend-item"><div class="legend-color" style="background: #533483"></div> Story</div>
                    <div class="legend-item"><div class="legend-color" style="background: #3498db"></div> Task [FE]</div>
                    <div class="legend-item"><div class="legend-color" style="background: #2ecc71"></div> Task [BE]</div>
                    <div class="legend-item"><div class="legend-color" style="background: #e67e22"></div> Task [DevOps]</div>
                    <div class="legend-item"><div class="legend-color" style="background: #9b59b6"></div> Task [Full]</div>
                    <hr style="margin: 16px 0; border-color: #0f3460;">
                    <div class="legend-item"><span style="color: #888">→</span> Hierarchy</div>
                    <div class="legend-item"><span style="color: #ef4444">⟶</span> Dependency</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        const graphData = {json.dumps({"nodes": nodes, "edges": edges})};
        const rawData = {json.dumps(data)};

        const colorMap = {{
            quarter: '#e94560',
            epic: '#0f3460',
            story: '#533483',
            task: '#6b7280'
        }};
        const tagColors = {{
            FE: '#3498db',
            BE: '#2ecc71',
            DevOps: '#e67e22',
            Full: '#9b59b6'
        }};

        const nodes = new vis.DataSet(graphData.nodes.map(n => ({{
            id: n.id,
            label: n.label,
            color: {{
                background: n.type === 'task' ? (tagColors[n.tag] || colorMap.task) : colorMap[n.type],
                border: n.status === 'completed' ? '#10b981' : (n.status === 'blocked' ? '#ef4444' : '#444'),
                highlight: {{ background: '#e94560', border: '#fff' }}
            }},
            shape: n.type === 'quarter' ? 'diamond' : (n.type === 'epic' ? 'box' : (n.type === 'story' ? 'ellipse' : 'box')),
            font: {{ color: '#fff', size: n.type === 'quarter' ? 14 : 11 }},
            borderWidth: n.status === 'completed' ? 3 : 1,
            size: n.type === 'quarter' ? 30 : (n.type === 'epic' ? 25 : (n.type === 'story' ? 20 : 15))
        }})));

        const edges = new vis.DataSet(graphData.edges.map((e, i) => ({{
            id: i,
            from: e.from,
            to: e.to,
            arrows: 'to',
            color: {{ color: e.type === 'dependency' ? '#ef4444' : '#444', opacity: 0.6 }},
            dashes: e.type === 'dependency',
            smooth: {{ type: 'cubicBezier' }}
        }})));

        const container = document.getElementById('graph');
        const network = new vis.Network(container, {{ nodes, edges }}, {{
            layout: {{
                hierarchical: {{
                    direction: 'LR',
                    sortMethod: 'directed',
                    levelSeparation: 200,
                    nodeSpacing: 80
                }}
            }},
            physics: false,
            interaction: {{ hover: true, zoomView: true }}
        }});

        // Populate sidebar
        const epicList = document.getElementById('epic-list');
        Object.values(rawData.entities.epics).sort((a,b) => a.priority - b.priority).forEach(epic => {{
            const stories = rawData.relationships.epic_stories[epic.id] || [];
            let taskCount = 0, doneCount = 0;
            stories.forEach(sId => {{
                const tasks = rawData.relationships.story_tasks[sId] || [];
                taskCount += tasks.length;
                tasks.forEach(tId => {{
                    if (rawData.entities.tasks[tId]?.status === 'completed') doneCount++;
                }});
            }});
            epicList.innerHTML += `
                <div class="entity-item" onclick="network.focus('${{epic.id}}', {{scale: 1.5, animation: true}})">
                    <span class="entity-id">${{epic.id}}</span>
                    <span class="status-badge status-${{epic.status}}">${{epic.status}}</span>
                    <div class="entity-title">${{epic.title}}</div>
                    <div class="entity-meta">${{stories.length}} stories · ${{doneCount}}/${{taskCount}} tasks</div>
                </div>
            `;
        }});

        const taskList = document.getElementById('task-list');
        Object.values(rawData.entities.tasks).filter(t => t.status !== 'completed').forEach(task => {{
            taskList.innerHTML += `
                <div class="entity-item" onclick="network.focus('${{task.id}}', {{scale: 2, animation: true}})">
                    <span class="entity-id">[${{task.tag}}] ${{task.id}}</span>
                    <span class="status-badge status-${{task.status}}">${{task.status}}</span>
                    <div class="entity-title">${{task.title}}</div>
                    <div class="entity-meta">Story: ${{task.storyId}}</div>
                </div>
            `;
        }});

        function showTab(name) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelector(`[onclick="showTab('${{name}}')"]`).classList.add('active');
            document.getElementById(`${{name}}-tab`).classList.add('active');
        }}
    </script>
</body>
</html>"""
    return html


def serve_visualization(graph: PeachflowGraph, port: int = 9876):
    """Start visualization server."""
    html_content = create_visualization_html(graph)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode())

        def log_message(self, format, *args):
            pass  # Suppress logging

    with socketserver.TCPServer(("", port), Handler) as httpd:
        url = f"http://localhost:{port}"
        print(f"{Colors.GREEN}Peachflow Graph Visualization{Colors.RESET}")
        print(f"Server running at: {Colors.CYAN}{url}{Colors.RESET}")
        print(f"Press {Colors.YELLOW}Ctrl+C{Colors.RESET} to stop\n")

        # Open browser in background
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n{Colors.GRAY}Server stopped.{Colors.RESET}")


# === CLI Interface ===

def format_output(data: Any, format: str = "human") -> str:
    """Format output for display."""
    if format == "json":
        return json.dumps(data, indent=2)
    elif format == "yaml":
        # Simple YAML-like output
        def to_yaml(obj, indent=0):
            lines = []
            prefix = "  " * indent
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        lines.append(f"{prefix}{k}:")
                        lines.append(to_yaml(v, indent + 1))
                    else:
                        lines.append(f"{prefix}{k}: {v}")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        lines.append(f"{prefix}-")
                        lines.append(to_yaml(item, indent + 1))
                    else:
                        lines.append(f"{prefix}- {item}")
            else:
                lines.append(f"{prefix}{obj}")
            return "\n".join(lines)
        return to_yaml(data)
    else:
        return str(data)


def print_entity(entity: dict, entity_type: str):
    """Print entity in human-readable format."""
    status_colors = {
        "completed": Colors.GREEN,
        "in_progress": Colors.YELLOW,
        "pending": Colors.GRAY,
        "draft": Colors.GRAY,
        "planned": Colors.GRAY,
        "blocked": Colors.RED,
        "active": Colors.CYAN,
    }

    id_str = f"{Colors.BOLD}{entity['id']}{Colors.RESET}"
    status = entity.get("status", "unknown")
    status_str = f"{status_colors.get(status, '')}{status}{Colors.RESET}"

    if entity_type == "epic":
        print(f"{id_str}: {entity.get('title', 'Untitled')}")
        print(f"  Status: {status_str} | Priority: {entity.get('priority', '-')} | Quarter: {entity.get('quarter', '-')}")
        if entity.get("description"):
            print(f"  {Colors.GRAY}{entity['description'][:100]}...{Colors.RESET}")
        if entity.get("deliverables"):
            print(f"  Deliverables: {', '.join(entity['deliverables'][:5])}")

    elif entity_type == "story":
        print(f"{id_str}: {entity.get('title', 'Untitled')}")
        print(f"  Status: {status_str} | Epic: {entity.get('epicId', '-')}")
        if entity.get("acceptanceCriteria"):
            print(f"  Acceptance Criteria: {len(entity['acceptanceCriteria'])} items")

    elif entity_type == "task":
        tag = entity.get("tag", "?")
        tag_colors = {"FE": Colors.BLUE, "BE": Colors.GREEN, "DevOps": Colors.YELLOW, "Full": Colors.MAGENTA}
        tag_str = f"{tag_colors.get(tag, '')}{tag}{Colors.RESET}"
        print(f"[{tag_str}] {id_str}: {entity.get('title', 'Untitled')}")
        print(f"  Status: {status_str} | Story: {entity.get('storyId', '-')} | Sprint: {entity.get('sprintId', '-')}")

    elif entity_type == "clarification":
        print(f"{id_str}: {entity.get('question', '')[:80]}")
        print(f"  Status: {status_str} | Entity: {entity.get('entityId', '-')}")
        if entity.get("answer"):
            print(f"  Answer: {entity['answer'][:80]}...")

    elif entity_type == "sprint":
        print(f"{id_str}: {entity.get('name', 'Unnamed')} ({entity.get('quarterId', '-')})")
        print(f"  Status: {status_str} | Tasks: {len(entity.get('taskIds', []))}")
        if entity.get("worktreePath"):
            print(f"  Worktree: {entity['worktreePath']}")

    print()


def print_list(entities: list, entity_type: str):
    """Print list of entities."""
    if not entities:
        print(f"{Colors.GRAY}No {entity_type}s found.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}{entity_type.title()}s ({len(entities)} total){Colors.RESET}")
    print("─" * 60)

    for entity in entities:
        print_entity(entity, entity_type)


def print_stats(stats: dict):
    """Print statistics."""
    print(f"\n{Colors.BOLD}Project Statistics{Colors.RESET}")
    print("─" * 40)

    progress = stats.get("progress", 0) * 100
    bar_len = 20
    filled = int(bar_len * stats.get("progress", 0))
    bar = f"{'█' * filled}{'░' * (bar_len - filled)}"

    print(f"Progress: {Colors.GREEN}{bar}{Colors.RESET} {progress:.1f}%\n")

    print(f"Epics:    {stats['epics']['total']:3d} total")
    for status, count in stats['epics']['by_status'].items():
        print(f"          {count:3d} {status}")

    print(f"\nStories:  {stats['stories']['total']:3d} total")
    for status, count in stats['stories']['by_status'].items():
        print(f"          {count:3d} {status}")

    print(f"\nTasks:    {stats['tasks']['total']:3d} total")
    print(f"          {Colors.GREEN}{stats['tasks']['completed']:3d} completed{Colors.RESET}")
    print(f"          {stats['tasks']['pending']:3d} pending")
    print(f"          {Colors.RED}{stats['tasks']['blocked']:3d} blocked{Colors.RESET}")
    print(f"\n  By tag:")
    for tag, count in stats['tasks']['by_tag'].items():
        print(f"          {count:3d} [{tag}]")

    print(f"\nClarifications: {stats['clarifications']['pending']} pending / {stats['clarifications']['total']} total")


def main():
    parser = argparse.ArgumentParser(description="Peachflow Graph Management")
    parser.add_argument("--format", "-f", choices=["human", "json", "yaml"], default="human")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # init
    subparsers.add_parser("init", help="Initialize empty graph")

    # create
    create_parser = subparsers.add_parser("create", help="Create entity")
    create_sub = create_parser.add_subparsers(dest="entity_type")

    epic_p = create_sub.add_parser("epic")
    epic_p.add_argument("--title", required=True)
    epic_p.add_argument("--quarter", required=True, choices=["Q1", "Q2", "Q3", "Q4"])
    epic_p.add_argument("--priority", type=int, default=5)
    epic_p.add_argument("--description", default="")
    epic_p.add_argument("--deliverables", help="Comma-separated deliverables")

    story_p = create_sub.add_parser("story")
    story_p.add_argument("--epic", required=True, dest="epic_id")
    story_p.add_argument("--title", required=True)
    story_p.add_argument("--description", default="")
    story_p.add_argument("--acceptance", help="Comma-separated acceptance criteria")

    task_p = create_sub.add_parser("task")
    task_p.add_argument("--story", required=True, dest="story_id")
    task_p.add_argument("--title", required=True)
    task_p.add_argument("--tag", required=True, choices=TASK_TAGS)
    task_p.add_argument("--description", default="")
    task_p.add_argument("--depends-on", help="Comma-separated task IDs")

    cl_p = create_sub.add_parser("clarification")
    cl_p.add_argument("--entity", required=True, dest="entity_id")
    cl_p.add_argument("--question", required=True)
    cl_p.add_argument("--type", default="general", dest="entity_type_cl")

    adr_p = create_sub.add_parser("adr")
    adr_p.add_argument("--title", required=True)
    adr_p.add_argument("--context", default="")
    adr_p.add_argument("--decision", default="")
    adr_p.add_argument("--consequences", default="")
    adr_p.add_argument("--entity", dest="entity_id")

    sprint_p = create_sub.add_parser("sprint")
    sprint_p.add_argument("--quarter", required=True, choices=["Q1", "Q2", "Q3", "Q4"])
    sprint_p.add_argument("--tasks", help="Comma-separated task IDs")
    sprint_p.add_argument("--name", default="")

    # get
    get_parser = subparsers.add_parser("get", help="Get entity by ID")
    get_parser.add_argument("entity_type", choices=["epic", "story", "task", "clarification", "adr", "sprint", "quarter"])
    get_parser.add_argument("entity_id")

    # update
    update_parser = subparsers.add_parser("update", help="Update entity")
    update_parser.add_argument("entity_type", choices=["epic", "story", "task", "clarification", "adr", "sprint"])
    update_parser.add_argument("entity_id")
    update_parser.add_argument("--status")
    update_parser.add_argument("--title")
    update_parser.add_argument("--description")
    update_parser.add_argument("--priority", type=int)
    update_parser.add_argument("--answer")  # For clarifications
    update_parser.add_argument("--worktree")  # For sprints
    update_parser.add_argument("--no-cascade", action="store_true", help="Disable automatic status cascading")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete entity")
    delete_parser.add_argument("entity_type", choices=["epic", "story", "task", "clarification", "adr", "sprint"])
    delete_parser.add_argument("entity_id")

    # cascade
    cascade_parser = subparsers.add_parser("cascade", help="Manually trigger cascade status check")
    cascade_parser.add_argument("entity_type", choices=["task", "story", "epic"])
    cascade_parser.add_argument("entity_id")

    # acceptance
    acceptance_parser = subparsers.add_parser("acceptance", help="Manage acceptance criteria")
    acceptance_sub = acceptance_parser.add_subparsers(dest="acceptance_action")

    acc_update = acceptance_sub.add_parser("update", help="Update acceptance criterion status")
    acc_update.add_argument("story_id")
    acc_update.add_argument("--index", type=int, required=True, help="Criterion index (0-based)")
    acc_update.add_argument("--done", action="store_true", help="Mark as done")
    acc_update.add_argument("--not-done", action="store_true", help="Mark as not done")

    acc_progress = acceptance_sub.add_parser("progress", help="Show acceptance criteria progress")
    acc_progress.add_argument("story_id")

    # list
    list_parser = subparsers.add_parser("list", help="List entities")
    list_parser.add_argument("entity_type", choices=["epics", "stories", "tasks", "clarifications", "adrs", "sprints"])
    list_parser.add_argument("--quarter", choices=["Q1", "Q2", "Q3", "Q4"])
    list_parser.add_argument("--epic")
    list_parser.add_argument("--story")
    list_parser.add_argument("--status")
    list_parser.add_argument("--tag", choices=TASK_TAGS)
    list_parser.add_argument("--sprint")
    list_parser.add_argument("--unassigned", action="store_true")
    list_parser.add_argument("--pending", action="store_true")
    list_parser.add_argument("--entity")

    # depends
    depends_parser = subparsers.add_parser("depends", help="Manage dependencies")
    depends_sub = depends_parser.add_subparsers(dest="depends_action")

    dep_add = depends_sub.add_parser("add")
    dep_add.add_argument("task_id")
    dep_add.add_argument("--on", required=True, dest="depends_on")

    dep_remove = depends_sub.add_parser("remove")
    dep_remove.add_argument("task_id")
    dep_remove.add_argument("--on", required=True, dest="depends_on")

    dep_list = depends_sub.add_parser("list")
    dep_list.add_argument("task_id")

    dep_blockers = depends_sub.add_parser("blockers")
    dep_blockers.add_argument("task_id")

    # ready-tasks
    ready_parser = subparsers.add_parser("ready-tasks", help="Find ready tasks")
    ready_parser.add_argument("--quarter", choices=["Q1", "Q2", "Q3", "Q4"])
    ready_parser.add_argument("--epic")
    ready_parser.add_argument("--limit", type=int)

    # chain
    chain_parser = subparsers.add_parser("chain", help="Get task chain")
    chain_parser.add_argument("task_id")

    # descendants
    desc_parser = subparsers.add_parser("descendants", help="Get descendants")
    desc_parser.add_argument("entity_type", choices=["quarter", "epic", "story"])
    desc_parser.add_argument("entity_id")

    # stats
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument("--quarter", choices=["Q1", "Q2", "Q3", "Q4"])
    stats_parser.add_argument("--epic")

    # sprint operations
    sprint_create_parser = subparsers.add_parser("sprint-create", help="Auto-create sprint")
    sprint_create_parser.add_argument("--quarter", required=True, choices=["Q1", "Q2", "Q3", "Q4"])
    sprint_create_parser.add_argument("--max-tasks", type=int, default=10)
    sprint_create_parser.add_argument("--name", default="")

    subparsers.add_parser("sprint-active", help="Get active sprint")

    sprint_complete_parser = subparsers.add_parser("sprint-complete", help="Complete sprint")
    sprint_complete_parser.add_argument("sprint_id")

    # next-id
    next_id_parser = subparsers.add_parser("next-id", help="Get next ID")
    next_id_parser.add_argument("entity_type", choices=["epic", "story", "task", "clarification", "adr", "sprint"])

    # export
    export_parser = subparsers.add_parser("export", help="Export graph")
    export_parser.add_argument("--format", choices=["json", "markdown"], default="json")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Start visualization server")
    serve_parser.add_argument("--port", type=int, default=9876)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    graph = PeachflowGraph()

    try:
        if args.command == "init":
            result = graph.init()
            if args.format == "json":
                print(json.dumps(result))
            else:
                print(f"{Colors.GREEN}✓ Graph initialized at {result['path']}{Colors.RESET}")

        elif args.command == "create":
            if args.entity_type == "epic":
                deliverables = args.deliverables.split(",") if args.deliverables else []
                result = graph.create_epic(args.title, args.quarter, args.priority, args.description, deliverables)
            elif args.entity_type == "story":
                acceptance = args.acceptance.split(",") if args.acceptance else []
                result = graph.create_story(args.epic_id, args.title, args.description, acceptance)
            elif args.entity_type == "task":
                depends = args.depends_on.split(",") if args.depends_on else []
                result = graph.create_task(args.story_id, args.title, args.tag, args.description, depends)
            elif args.entity_type == "clarification":
                result = graph.create_clarification(args.entity_id, args.question, args.entity_type_cl)
            elif args.entity_type == "adr":
                result = graph.create_adr(args.title, args.context, args.decision, args.consequences, args.entity_id)
            elif args.entity_type == "sprint":
                tasks = args.tasks.split(",") if args.tasks else []
                result = graph.create_sprint(args.quarter, tasks, args.name)

            if args.format == "json":
                print(json.dumps(result))
            else:
                print(f"{Colors.GREEN}✓ Created {args.entity_type}: {result['id']}{Colors.RESET}")

        elif args.command == "get":
            result = graph.get(args.entity_type, args.entity_id)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print_entity(result, args.entity_type)

        elif args.command == "update":
            updates = {}
            for field in ["status", "title", "description", "priority", "answer", "worktree"]:
                val = getattr(args, field, None)
                if val is not None:
                    if field == "worktree":
                        updates["worktreePath"] = val
                    else:
                        updates[field] = val

            cascade = not getattr(args, 'no_cascade', False)
            result = graph.update(args.entity_type, args.entity_id, cascade=cascade, **updates)
            if args.format == "json":
                print(json.dumps(result))
            else:
                print(f"{Colors.GREEN}✓ Updated {args.entity_id}{Colors.RESET}")
                if result.get("_cascaded"):
                    print(f"  Cascaded status changes:")
                    for eid, status in result["_cascaded"].items():
                        print(f"    {eid} → {status}")

        elif args.command == "cascade":
            result = graph.cascade_status_check(args.entity_type, args.entity_id)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                if result:
                    print(f"{Colors.GREEN}Status changes cascaded:{Colors.RESET}")
                    for entity_id, new_status in result.items():
                        print(f"  {entity_id} → {new_status}")
                else:
                    print(f"{Colors.GRAY}No status changes needed.{Colors.RESET}")

        elif args.command == "acceptance":
            if args.acceptance_action == "update":
                if args.done and args.not_done:
                    print(f"{Colors.RED}Error: Cannot specify both --done and --not-done{Colors.RESET}")
                    sys.exit(1)
                done = args.done if args.done else not args.not_done
                result = graph.update_acceptance_criterion(args.story_id, args.index, done)
                if args.format == "json":
                    print(json.dumps(result))
                else:
                    status = "done" if done else "not done"
                    print(f"{Colors.GREEN}✓ Updated criterion {args.index} for {args.story_id} → {status}{Colors.RESET}")

            elif args.acceptance_action == "progress":
                result = graph.get_acceptance_progress(args.story_id)
                if args.format == "json":
                    print(json.dumps(result, indent=2))
                else:
                    progress_pct = result["progress"] * 100
                    print(f"\n{Colors.BOLD}Acceptance Criteria: {args.story_id}{Colors.RESET}")
                    print(f"Progress: {result['done']}/{result['total']} ({progress_pct:.0f}%)")
                    for i, c in enumerate(result["criteria"]):
                        if isinstance(c, dict):
                            icon = f"{Colors.GREEN}✓{Colors.RESET}" if c.get("done") else "○"
                            print(f"  [{i}] {icon} {c.get('title', c)}")
                        else:
                            print(f"  [{i}] ○ {c}")
            else:
                print(f"{Colors.RED}Error: acceptance action required (update or progress){Colors.RESET}")
                sys.exit(1)

        elif args.command == "delete":
            result = graph.delete(args.entity_type, args.entity_id)
            if args.format == "json":
                print(json.dumps(result))
            else:
                print(f"{Colors.YELLOW}✓ Deleted {args.entity_id}{Colors.RESET}")

        elif args.command == "list":
            entity_type = args.entity_type.rstrip("s")  # Remove plural
            filters = {
                "quarter": args.quarter,
                "epic": args.epic,
                "story": args.story,
                "status": args.status,
                "tag": args.tag,
                "sprint": args.sprint,
                "unassigned": args.unassigned,
                "pending": args.pending,
                "entity": args.entity,
            }
            result = graph.list_entities(entity_type, **{k: v for k, v in filters.items() if v})
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print_list(result, entity_type)

        elif args.command == "depends":
            if args.depends_action == "add":
                result = graph.add_dependency(args.task_id, args.depends_on)
            elif args.depends_action == "remove":
                result = graph.remove_dependency(args.task_id, args.depends_on)
            elif args.depends_action == "list":
                result = graph.get_dependencies(args.task_id)
            elif args.depends_action == "blockers":
                result = graph.get_blockers(args.task_id)

            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print(result)

        elif args.command == "ready-tasks":
            result = graph.get_ready_tasks(args.quarter, args.epic, args.limit)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print_list(result, "task")

        elif args.command == "chain":
            result = graph.get_chain(args.task_id)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print(f"\n{Colors.BOLD}Task Chain{Colors.RESET}")
                print(f"Path: {Colors.CYAN}{result['path']}{Colors.RESET}")
                print(f"\nQuarter: {result['quarter']}")
                print(f"Epic: {result['epic']['id']} - {result['epic']['title']}")
                print(f"Story: {result['story']['id']} - {result['story']['title']}")
                print(f"Task: {result['task']['id']} - {result['task']['title']}")

        elif args.command == "descendants":
            result = graph.get_descendants(args.entity_type, args.entity_id)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print(f"\n{Colors.BOLD}Descendants of {args.entity_id}{Colors.RESET}")
                if result["epics"]:
                    print(f"\nEpics: {len(result['epics'])}")
                if result["stories"]:
                    print(f"Stories: {len(result['stories'])}")
                if result["tasks"]:
                    print(f"Tasks: {len(result['tasks'])}")

        elif args.command == "stats":
            result = graph.get_stats(args.quarter, args.epic)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print_stats(result)

        elif args.command == "sprint-create":
            result = graph.auto_create_sprint(args.quarter, args.max_tasks, args.name)
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                if result.get("error"):
                    print(f"{Colors.YELLOW}{result['error']}{Colors.RESET}")
                else:
                    sprint = result["sprint"]
                    print(f"{Colors.GREEN}✓ Created {sprint['id']}: {sprint['name']}{Colors.RESET}")
                    print(f"  Tasks: {', '.join(sprint['taskIds'])}")

        elif args.command == "sprint-active":
            result = graph.get_active_sprint()
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                if result:
                    print_entity(result, "sprint")
                else:
                    print(f"{Colors.GRAY}No active sprint.{Colors.RESET}")

        elif args.command == "sprint-complete":
            result = graph.complete_sprint(args.sprint_id)
            if args.format == "json":
                print(json.dumps(result))
            else:
                print(f"{Colors.GREEN}✓ Completed {args.sprint_id}{Colors.RESET}")

        elif args.command == "next-id":
            # Don't actually increment, just show what would be next
            graph._ensure_loaded()
            current = graph.data["counters"].get(args.entity_type, 0)
            prefix = ID_PATTERNS.get(args.entity_type, "")
            if args.entity_type == "adr":
                next_id = f"{prefix}{current + 1:04d}"
            else:
                next_id = f"{prefix}{current + 1:03d}"
            print(next_id)

        elif args.command == "export":
            result = graph.export(args.format)
            print(result)

        elif args.command == "serve":
            serve_visualization(graph, args.port)

    except ValueError as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
