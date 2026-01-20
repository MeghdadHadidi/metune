#!/usr/bin/env python3
"""
Hook handlers for teleporter plugin.
These are called by the hooks configuration to handle various Claude Code events.
"""

import json
import os
import sys

# Add scripts directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from telegram_api import (
    send_message,
    edit_message,
    format_session_message,
    create_session_buttons,
    create_question_buttons
)
from session_manager import (
    register_session,
    get_session,
    update_session,
    end_session,
    get_pending_response,
    get_poller_pid
)
from poller import start_poller_daemon, stop_poller


def handle_session_start(hook_input: dict) -> dict:
    """
    Handle SessionStart event.
    Sends initial Telegram message and starts the poller.
    """
    session_id = hook_input.get("session_id", "unknown")
    cwd = hook_input.get("cwd", os.getcwd())

    # Check if Telegram is configured
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return {
            "continue": True,
            "systemMessage": "Teleporter: Telegram not configured. Run /teleporter:configure to set up."
        }

    try:
        # Send initial message
        text = format_session_message(session_id, cwd, status="active")
        buttons = create_session_buttons()

        result = send_message(text, reply_markup=buttons)
        message_id = result.get("message_id")

        # Register the session
        register_session(session_id, message_id, cwd, chat_id)

        # Start the poller if not already running
        poller_pid = get_poller_pid()
        if not poller_pid:
            start_poller_daemon()
            poller_status = "started"
        else:
            poller_status = f"running (PID: {poller_pid})"

        return {
            "continue": True,
            "systemMessage": f"Teleporter: Session registered. Telegram message sent. Poller {poller_status}."
        }

    except Exception as e:
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Failed to send Telegram message: {e}"
        }


def handle_session_end(hook_input: dict) -> dict:
    """
    Handle SessionEnd event.
    Updates Telegram message to show session ended.
    """
    session_id = hook_input.get("session_id", "unknown")

    session = get_session(session_id)
    if not session:
        return {"continue": True}

    try:
        message_id = session.get("message_id")
        cwd = session.get("cwd", "unknown")

        # Update message to show ended
        text = format_session_message(session_id, cwd, status="ended ✓")
        edit_message(message_id, text, reply_markup=None)

        # Mark session as ended
        end_session(session_id)

        return {
            "continue": True,
            "systemMessage": "Teleporter: Session ended, Telegram message updated."
        }

    except Exception as e:
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Failed to update Telegram message: {e}"
        }


def handle_ask_user_question(hook_input: dict) -> dict:
    """
    Handle PreToolUse for AskUserQuestion.
    Updates Telegram message with the question and answer buttons.
    Returns the pending response if available.
    """
    session_id = hook_input.get("session_id", "unknown")
    tool_input = hook_input.get("tool_input", {})

    session = get_session(session_id)
    if not session:
        return {"continue": True}

    # Extract question details
    questions = tool_input.get("questions", [])
    if not questions:
        return {"continue": True}

    # For now, handle the first question
    question = questions[0]
    question_text = question.get("question", "")
    options = question.get("options", [])

    try:
        message_id = session.get("message_id")
        cwd = session.get("cwd", "unknown")

        # Format options for display
        option_labels = [opt.get("label", f"Option {i+1}") for i, opt in enumerate(options)]

        # Update session with current question
        update_session(
            session_id,
            question=question_text,
            question_options=option_labels
        )

        # Update Telegram message with question and buttons
        text = format_session_message(session_id, cwd, status="waiting for input", question=question_text)
        buttons = create_question_buttons(options)
        edit_message(message_id, text, reply_markup=buttons)

        # Check if there's a pending response from Telegram
        pending = get_pending_response(session_id)
        if pending:
            # Find matching option
            for i, opt in enumerate(options):
                if opt.get("label") == pending or opt.get("value") == pending:
                    return {
                        "continue": True,
                        "hookSpecificOutput": {
                            "answers": {question_text: pending}
                        },
                        "systemMessage": f"Teleporter: User responded via Telegram: {pending}"
                    }

            # If no match, treat as custom text
            return {
                "continue": True,
                "hookSpecificOutput": {
                    "answers": {question_text: pending}
                },
                "systemMessage": f"Teleporter: User responded via Telegram: {pending}"
            }

        return {"continue": True}

    except Exception as e:
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Failed to update Telegram: {e}"
        }


def handle_notification(hook_input: dict) -> dict:
    """
    Handle Notification event.
    Forwards notifications to Telegram.
    """
    session_id = hook_input.get("session_id", "unknown")

    session = get_session(session_id)
    if not session:
        return {"continue": True}

    # Get notification details from the input
    # The notification content varies, so we'll extract what we can
    notification_text = hook_input.get("message", hook_input.get("text", "Notification from Claude"))

    try:
        message_id = session.get("message_id")
        cwd = session.get("cwd", "unknown")

        # Update message with notification
        text = format_session_message(
            session_id,
            cwd,
            status="notification",
            question=notification_text
        )
        edit_message(message_id, text, reply_markup=create_session_buttons())

        return {"continue": True}

    except Exception as e:
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Failed to send notification: {e}"
        }


def main():
    """Main entry point - reads hook input from stdin."""
    if len(sys.argv) < 2:
        print("Usage: hook_handlers.py <handler>", file=sys.stderr)
        print("Handlers: session_start, session_end, ask_user_question, notification", file=sys.stderr)
        sys.exit(1)

    handler = sys.argv[1]

    # Read input from stdin
    try:
        input_data = sys.stdin.read()
        hook_input = json.loads(input_data) if input_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    # Route to appropriate handler
    if handler == "session_start":
        result = handle_session_start(hook_input)
    elif handler == "session_end":
        result = handle_session_end(hook_input)
    elif handler == "ask_user_question":
        result = handle_ask_user_question(hook_input)
    elif handler == "notification":
        result = handle_notification(hook_input)
    else:
        result = {"continue": True, "systemMessage": f"Unknown handler: {handler}"}

    # Output result as JSON
    print(json.dumps(result))


if __name__ == "__main__":
    main()
