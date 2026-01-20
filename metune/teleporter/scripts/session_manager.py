#!/usr/bin/env python3
"""
Session manager for teleporter plugin.
Tracks Claude Code sessions and their associated Telegram messages.
Uses a JSON file for persistence across script invocations.
"""

import json
import os
import sys
import fcntl
from typing import Optional, Dict, Any
from datetime import datetime


def get_sessions_file() -> str:
    """Get the path to the sessions file."""
    # Store in user's home directory under .teleporter
    home = os.path.expanduser("~")
    teleporter_dir = os.path.join(home, ".teleporter")
    os.makedirs(teleporter_dir, exist_ok=True)
    return os.path.join(teleporter_dir, "sessions.json")


def get_poller_pid_file() -> str:
    """Get the path to the poller PID file."""
    home = os.path.expanduser("~")
    teleporter_dir = os.path.join(home, ".teleporter")
    os.makedirs(teleporter_dir, exist_ok=True)
    return os.path.join(teleporter_dir, "poller.pid")


def load_sessions() -> Dict[str, Any]:
    """Load sessions from the JSON file."""
    sessions_file = get_sessions_file()

    if not os.path.exists(sessions_file):
        return {"sessions": {}, "pending_responses": {}}

    try:
        with open(sessions_file, "r") as f:
            # Use file locking for concurrent access safety
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return data
    except (json.JSONDecodeError, IOError):
        return {"sessions": {}, "pending_responses": {}}


def save_sessions(data: Dict[str, Any]) -> None:
    """Save sessions to the JSON file."""
    sessions_file = get_sessions_file()

    with open(sessions_file, "w") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(data, f, indent=2)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def register_session(
    session_id: str,
    message_id: int,
    cwd: str,
    chat_id: str
) -> None:
    """Register a new Claude Code session with its Telegram message."""
    data = load_sessions()

    data["sessions"][session_id] = {
        "message_id": message_id,
        "chat_id": chat_id,
        "cwd": cwd,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "current_question": None,
        "question_options": None
    }

    save_sessions(data)


def update_session(
    session_id: str,
    status: Optional[str] = None,
    question: Optional[str] = None,
    question_options: Optional[list] = None,
    message_id: Optional[int] = None
) -> None:
    """Update a session's state."""
    data = load_sessions()

    if session_id not in data["sessions"]:
        return

    session = data["sessions"][session_id]
    session["last_updated"] = datetime.now().isoformat()

    if status is not None:
        session["status"] = status
    if question is not None:
        session["current_question"] = question
    if question_options is not None:
        session["question_options"] = question_options
    if message_id is not None:
        session["message_id"] = message_id

    save_sessions(data)


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get a session by ID."""
    data = load_sessions()
    return data["sessions"].get(session_id)


def get_session_by_message(message_id: int) -> Optional[tuple[str, Dict[str, Any]]]:
    """Get a session by its Telegram message ID."""
    data = load_sessions()

    for sid, session in data["sessions"].items():
        if session.get("message_id") == message_id:
            return sid, session

    return None


def end_session(session_id: str) -> None:
    """Mark a session as ended."""
    update_session(session_id, status="ended")


def remove_session(session_id: str) -> None:
    """Remove a session entirely."""
    data = load_sessions()

    if session_id in data["sessions"]:
        del data["sessions"][session_id]
        save_sessions(data)


def get_active_sessions() -> Dict[str, Dict[str, Any]]:
    """Get all active sessions."""
    data = load_sessions()
    return {
        sid: session
        for sid, session in data["sessions"].items()
        if session.get("status") == "active"
    }


def store_pending_response(session_id: str, response: str) -> None:
    """Store a response from Telegram for a session to pick up."""
    data = load_sessions()
    data["pending_responses"][session_id] = {
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    save_sessions(data)


def get_pending_response(session_id: str) -> Optional[str]:
    """Get and remove a pending response for a session."""
    data = load_sessions()

    if session_id in data["pending_responses"]:
        response = data["pending_responses"][session_id]["response"]
        del data["pending_responses"][session_id]
        save_sessions(data)
        return response

    return None


def clear_pending_response(session_id: str) -> None:
    """Clear a pending response without returning it."""
    data = load_sessions()

    if session_id in data["pending_responses"]:
        del data["pending_responses"][session_id]
        save_sessions(data)


def set_poller_pid(pid: int) -> None:
    """Store the poller process PID."""
    pid_file = get_poller_pid_file()
    with open(pid_file, "w") as f:
        f.write(str(pid))


def get_poller_pid() -> Optional[int]:
    """Get the poller process PID if running."""
    pid_file = get_poller_pid_file()

    if not os.path.exists(pid_file):
        return None

    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        # Check if process is actually running
        try:
            os.kill(pid, 0)
            return pid
        except OSError:
            # Process not running, clean up PID file
            os.remove(pid_file)
            return None

    except (ValueError, IOError):
        return None


def clear_poller_pid() -> None:
    """Remove the poller PID file."""
    pid_file = get_poller_pid_file()
    if os.path.exists(pid_file):
        os.remove(pid_file)


def cleanup_stale_sessions(max_age_hours: int = 24) -> int:
    """Remove sessions older than max_age_hours. Returns count of removed sessions."""
    data = load_sessions()
    now = datetime.now()
    removed = 0

    sessions_to_remove = []
    for sid, session in data["sessions"].items():
        try:
            created = datetime.fromisoformat(session.get("created_at", ""))
            age = (now - created).total_seconds() / 3600
            if age > max_age_hours:
                sessions_to_remove.append(sid)
        except (ValueError, TypeError):
            sessions_to_remove.append(sid)

    for sid in sessions_to_remove:
        del data["sessions"][sid]
        removed += 1

    if removed > 0:
        save_sessions(data)

    return removed


if __name__ == "__main__":
    # CLI interface for testing and management
    if len(sys.argv) < 2:
        print("Usage: session_manager.py <command> [args...]")
        print("Commands: list, get <session_id>, cleanup")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        sessions = get_active_sessions()
        if not sessions:
            print("No active sessions")
        else:
            for sid, session in sessions.items():
                print(f"{sid[:8]}: {session.get('cwd')} (msg: {session.get('message_id')})")

    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py get <session_id>")
            sys.exit(1)
        session = get_session(sys.argv[2])
        if session:
            print(json.dumps(session, indent=2))
        else:
            print("Session not found")

    elif command == "cleanup":
        removed = cleanup_stale_sessions()
        print(f"Removed {removed} stale sessions")

    elif command == "poller_pid":
        pid = get_poller_pid()
        if pid:
            print(f"Poller running with PID: {pid}")
        else:
            print("Poller not running")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
