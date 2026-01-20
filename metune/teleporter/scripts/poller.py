#!/usr/bin/env python3
"""
Background poller for teleporter plugin.
Polls Telegram for button clicks and text replies, then stores them for Claude Code to pick up.
"""

import json
import os
import sys
import signal
import time
from typing import Optional

# Add scripts directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from telegram_api import get_updates, answer_callback_query, edit_message, create_session_buttons
from session_manager import (
    get_session_by_message,
    store_pending_response,
    update_session,
    get_active_sessions,
    set_poller_pid,
    clear_poller_pid,
    get_poller_pid
)


# Global flag for graceful shutdown
running = True


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    global running
    running = False
    print("Shutting down poller...")


def process_callback_query(callback: dict) -> None:
    """Process a callback query (button press)."""
    callback_id = callback.get("id")
    data = callback.get("data", "")
    message = callback.get("message", {})
    message_id = message.get("message_id")

    if not message_id:
        answer_callback_query(callback_id, "Invalid callback")
        return

    # Find the session for this message
    result = get_session_by_message(message_id)
    if not result:
        answer_callback_query(callback_id, "Session not found")
        return

    session_id, session = result

    # Handle different callback types
    if data == "get_context":
        # User wants context - acknowledge and inform
        answer_callback_query(callback_id, "Context request sent to Claude")
        store_pending_response(session_id, "/context")

    elif data == "continue":
        answer_callback_query(callback_id, "Continuing...")
        store_pending_response(session_id, "continue")

    elif data == "stop":
        answer_callback_query(callback_id, "Stop requested")
        store_pending_response(session_id, "stop")

    elif data == "text_input":
        answer_callback_query(callback_id, "Reply to this message with your text")
        # Update message to indicate waiting for text
        try:
            text = message.get("text", "")
            if "Waiting for your reply" not in text:
                edit_message(
                    message_id,
                    text + "\n\n<i>💬 Waiting for your reply...</i>",
                    reply_markup=create_session_buttons(include_context=False)
                )
        except Exception:
            pass

    elif data.startswith("answer:"):
        # Multi-choice answer
        answer_value = data[7:]  # Remove "answer:" prefix
        answer_callback_query(callback_id, f"Selected: {answer_value}")
        store_pending_response(session_id, answer_value)

        # Clear the question from the session
        update_session(session_id, question=None, question_options=None)

        # Update message to show selection
        try:
            cwd = session.get("cwd", "unknown")
            from telegram_api import format_session_message
            new_text = format_session_message(
                session_id,
                cwd,
                status="active",
                question=f"✅ Selected: {answer_value}"
            )
            edit_message(message_id, new_text, reply_markup=create_session_buttons())
        except Exception:
            pass

    else:
        answer_callback_query(callback_id, "Unknown action")


def process_message(message: dict) -> None:
    """Process a text message (reply to session message)."""
    text = message.get("text", "").strip()
    reply_to = message.get("reply_to_message", {})
    reply_message_id = reply_to.get("message_id")

    if not reply_message_id or not text:
        return

    # Find the session for the replied-to message
    result = get_session_by_message(reply_message_id)
    if not result:
        return

    session_id, session = result

    # Store the text response
    store_pending_response(session_id, text)

    # Clear question state
    update_session(session_id, question=None, question_options=None)


def poll_loop(poll_interval: int = 30) -> None:
    """Main polling loop."""
    global running

    offset = None
    consecutive_errors = 0
    max_consecutive_errors = 5

    print(f"Poller started (PID: {os.getpid()})")
    set_poller_pid(os.getpid())

    while running:
        try:
            # Check if there are any active sessions
            active = get_active_sessions()
            if not active:
                # No active sessions, wait and check again
                time.sleep(5)
                continue

            # Get updates from Telegram
            updates = get_updates(
                offset=offset,
                timeout=poll_interval,
                allowed_updates=["message", "callback_query"]
            )

            consecutive_errors = 0

            for update in updates:
                update_id = update.get("update_id")
                if update_id:
                    offset = update_id + 1

                # Process callback queries (button presses)
                if "callback_query" in update:
                    try:
                        process_callback_query(update["callback_query"])
                    except Exception as e:
                        print(f"Error processing callback: {e}", file=sys.stderr)

                # Process text messages (replies)
                elif "message" in update:
                    try:
                        process_message(update["message"])
                    except Exception as e:
                        print(f"Error processing message: {e}", file=sys.stderr)

        except KeyboardInterrupt:
            break

        except Exception as e:
            consecutive_errors += 1
            print(f"Poll error ({consecutive_errors}/{max_consecutive_errors}): {e}", file=sys.stderr)

            if consecutive_errors >= max_consecutive_errors:
                print("Too many consecutive errors, stopping poller", file=sys.stderr)
                break

            # Exponential backoff
            time.sleep(min(2 ** consecutive_errors, 60))

    clear_poller_pid()
    print("Poller stopped")


def start_poller_daemon() -> int:
    """Start the poller as a background daemon. Returns the child PID."""
    # Check if already running
    existing_pid = get_poller_pid()
    if existing_pid:
        print(f"Poller already running with PID: {existing_pid}")
        return existing_pid

    # Fork to background
    pid = os.fork()
    if pid > 0:
        # Parent process
        print(f"Started poller daemon with PID: {pid}")
        return pid

    # Child process - become daemon
    os.setsid()

    # Fork again to prevent zombie processes
    pid = os.fork()
    if pid > 0:
        os._exit(0)

    # Redirect standard file descriptors
    sys.stdin.close()

    # Open log file
    home = os.path.expanduser("~")
    log_dir = os.path.join(home, ".teleporter")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "poller.log")

    with open(log_file, "a") as log:
        sys.stdout = log
        sys.stderr = log

        # Set up signal handlers
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Run the poll loop
        poll_loop()

    os._exit(0)


def stop_poller() -> bool:
    """Stop the running poller daemon. Returns True if stopped."""
    pid = get_poller_pid()
    if not pid:
        print("Poller not running")
        return False

    try:
        os.kill(pid, signal.SIGTERM)
        # Wait a moment for graceful shutdown
        time.sleep(1)
        # Check if still running
        try:
            os.kill(pid, 0)
            # Still running, force kill
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        clear_poller_pid()
        print(f"Stopped poller (PID: {pid})")
        return True
    except OSError as e:
        print(f"Error stopping poller: {e}")
        clear_poller_pid()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: poller.py <command>")
        print("Commands: start, stop, status, foreground")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        start_poller_daemon()

    elif command == "stop":
        stop_poller()

    elif command == "status":
        pid = get_poller_pid()
        if pid:
            print(f"Poller running with PID: {pid}")
        else:
            print("Poller not running")

    elif command == "foreground":
        # Run in foreground for debugging
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        poll_loop()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
