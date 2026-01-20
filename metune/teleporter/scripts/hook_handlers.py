#!/usr/bin/env python3
"""
Hook handlers for teleporter plugin.
These are called by the hooks configuration to handle various Claude Code events.
"""

import json
import os
import sys
import time

# Add scripts directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Setup logging for debugging
def log_debug(message: str) -> None:
    """Log debug message to teleporter log file."""
    try:
        home = os.path.expanduser("~")
        log_file = os.path.join(home, ".teleporter", "hook_debug.log")
        with open(log_file, "a") as f:
            from datetime import datetime
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
    except Exception:
        pass

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
    Handles multi-question wizards by showing all questions in Telegram
    and collecting all answers before returning.
    """
    session_id = hook_input.get("session_id", "unknown")
    tool_input = hook_input.get("tool_input", {})

    log_debug(f"AskUserQuestion hook started for session {session_id[:8]}")

    session = get_session(session_id)
    if not session:
        log_debug(f"Session not found: {session_id[:8]}")
        return {"continue": True}

    # Extract all questions
    questions = tool_input.get("questions", [])
    if not questions:
        log_debug("No questions in tool_input")
        return {"continue": True}

    log_debug(f"Wizard with {len(questions)} questions")

    try:
        message_id = session.get("message_id")
        cwd = session.get("cwd", "unknown")

        # Collect answers for all questions
        all_answers = {}
        total_questions = len(questions)

        for q_index, question in enumerate(questions):
            question_text = question.get("question", "")
            question_header = question.get("header", f"Q{q_index + 1}")
            options = question.get("options", [])
            multi_select = question.get("multiSelect", False)

            log_debug(f"Question {q_index + 1}/{total_questions}: {question_text[:40]}... MultiSelect: {multi_select}")

            # Format options for display
            option_labels = [opt.get("label", f"Option {i+1}") for i, opt in enumerate(options)]

            # Build wizard status showing progress
            wizard_status = f"Question {q_index + 1} of {total_questions}"
            if all_answers:
                answered_summary = "\n".join([f"✅ {k}: {v}" for k, v in all_answers.items()])
                wizard_text = f"<b>{wizard_status}</b>\n\n{answered_summary}\n\n<b>Current:</b>\n{question_text}"
            else:
                wizard_text = f"<b>{wizard_status}</b>\n\n{question_text}"

            # Update session with current question
            update_session(
                session_id,
                question=question_text,
                question_options=option_labels
            )

            # Update Telegram message with current question and buttons
            text = format_session_message(session_id, cwd, status="waiting for input", question=wizard_text)
            buttons = create_question_buttons(options, multi_select=multi_select)
            edit_message(message_id, text, reply_markup=buttons)
            log_debug(f"Telegram updated with question {q_index + 1}")

            # Poll for response
            poll_timeout = 115 // total_questions  # Divide timeout among questions
            poll_timeout = max(poll_timeout, 30)  # At least 30s per question
            poll_interval = 0.5
            start_time = time.time()
            poll_count = 0
            got_answer = False

            while time.time() - start_time < poll_timeout:
                poll_count += 1
                pending = get_pending_response(session_id)
                if pending:
                    log_debug(f"Got answer for Q{q_index + 1} after {poll_count} polls: {pending}")

                    # Store answer with both question text and header as keys
                    all_answers[question_text] = pending
                    all_answers[question_header] = pending

                    got_answer = True
                    break

                time.sleep(poll_interval)

            if not got_answer:
                # Timeout on this question - return what we have and let terminal handle rest
                log_debug(f"Timeout on question {q_index + 1}, returning partial answers")

                # Update message to show timeout
                timeout_text = format_session_message(
                    session_id, cwd, status="active",
                    question=f"⏰ Timeout on question {q_index + 1} - continuing in terminal"
                )
                edit_message(message_id, timeout_text, reply_markup=create_session_buttons())
                update_session(session_id, question=None, question_options=None)

                if all_answers:
                    return {
                        "continue": True,
                        "hookSpecificOutput": {"answers": all_answers},
                        "systemMessage": f"Teleporter: Partial answers collected ({len(all_answers)//2} of {total_questions})"
                    }
                return {"continue": True}

        # All questions answered!
        log_debug(f"All {total_questions} questions answered via Telegram")

        # Update message to show completion
        completed_summary = "\n".join([f"✅ {questions[i].get('header', f'Q{i+1}')}: {all_answers.get(questions[i].get('question', ''), '?')}"
                                       for i in range(total_questions)])
        complete_text = format_session_message(
            session_id, cwd, status="active",
            question=f"<b>Wizard Complete</b>\n\n{completed_summary}"
        )
        edit_message(message_id, complete_text, reply_markup=create_session_buttons())

        # Clear session question state
        update_session(session_id, question=None, question_options=None, last_answer=list(all_answers.values())[-1] if all_answers else None)

        log_debug(f"Returning all answers: {list(all_answers.keys())}")

        return {
            "continue": True,
            "hookSpecificOutput": {"answers": all_answers},
            "systemMessage": f"Teleporter: All {total_questions} questions answered via Telegram"
        }

    except Exception as e:
        log_debug(f"Exception in AskUserQuestion handler: {e}")
        import traceback
        log_debug(traceback.format_exc())
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Failed to update Telegram: {e}"
        }


def handle_notification(hook_input: dict) -> dict:
    """
    Handle Notification event.
    Forwards notifications to Telegram.
    Skip if there's an active question waiting for response.
    """
    session_id = hook_input.get("session_id", "unknown")

    session = get_session(session_id)
    if not session:
        return {"continue": True}

    # Don't update message if there's an active question waiting for response
    # This prevents overwriting the question buttons
    current_question = session.get("current_question")
    question_options = session.get("question_options")

    log_debug(f"Notification hook: question={current_question is not None}, options={question_options is not None}")

    if current_question or question_options:
        log_debug("Skipping notification - active question")
        return {"continue": True}

    # Get notification details from the input
    # The notification content varies, so we'll extract what we can
    notification_text = hook_input.get("message", hook_input.get("text", "Notification from Claude"))

    # Skip empty or generic notifications
    if not notification_text or notification_text == "Notification from Claude":
        return {"continue": True}

    try:
        message_id = session.get("message_id")
        cwd = session.get("cwd", "unknown")

        # Check if there was a recent answer - preserve it in the message
        last_answer = session.get("last_answer")
        if last_answer:
            question_display = f"✅ Last answer: {last_answer}\n\n📢 {notification_text}"
        else:
            question_display = f"📢 {notification_text}"

        # Update message with notification
        text = format_session_message(
            session_id,
            cwd,
            status="active",
            question=question_display
        )
        edit_message(message_id, text, reply_markup=create_session_buttons())

        return {"continue": True}

    except Exception as e:
        log_debug(f"Notification error: {e}")
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Failed to send notification: {e}"
        }


def handle_user_prompt_submit(hook_input: dict) -> dict:
    """
    Handle UserPromptSubmit event.
    Checks for pending actions (continue, stop, context) from Telegram buttons.
    """
    session_id = hook_input.get("session_id", "unknown")
    user_prompt = hook_input.get("prompt", "")

    session = get_session(session_id)
    if not session:
        return {"continue": True}

    # Check for pending response from Telegram
    pending = get_pending_response(session_id)
    if not pending:
        return {"continue": True}

    try:
        message_id = session.get("message_id")
        cwd = session.get("cwd", "unknown")

        if pending == "continue":
            # User wants to continue - just proceed
            text = format_session_message(session_id, cwd, status="active", question="▶️ Continuing via Telegram")
            edit_message(message_id, text, reply_markup=create_session_buttons())
            return {"continue": True}

        elif pending == "stop":
            # User wants to stop - inject stop command
            text = format_session_message(session_id, cwd, status="stopping", question="⏹ Stop requested via Telegram")
            edit_message(message_id, text, reply_markup=create_session_buttons())
            return {
                "continue": True,
                "hookSpecificOutput": {
                    "transformedPrompt": "/stop"
                },
                "systemMessage": "Teleporter: Stop requested via Telegram"
            }

        elif pending == "/context":
            # User wants context
            text = format_session_message(session_id, cwd, status="active", question="📊 Context requested via Telegram")
            edit_message(message_id, text, reply_markup=create_session_buttons())
            return {
                "continue": True,
                "hookSpecificOutput": {
                    "transformedPrompt": "/context"
                },
                "systemMessage": "Teleporter: Context requested via Telegram"
            }

        else:
            # Unknown pending response - treat as text input
            text = format_session_message(session_id, cwd, status="active", question=f"💬 Received: {pending}")
            edit_message(message_id, text, reply_markup=create_session_buttons())
            return {
                "continue": True,
                "hookSpecificOutput": {
                    "transformedPrompt": pending
                },
                "systemMessage": f"Teleporter: User input via Telegram: {pending}"
            }

    except Exception as e:
        return {
            "continue": True,
            "systemMessage": f"Teleporter: Error handling prompt submit: {e}"
        }


def main():
    """Main entry point - reads hook input from stdin."""
    if len(sys.argv) < 2:
        print("Usage: hook_handlers.py <handler>", file=sys.stderr)
        print("Handlers: session_start, session_end, ask_user_question, notification, user_prompt_submit", file=sys.stderr)
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
    elif handler == "user_prompt_submit":
        result = handle_user_prompt_submit(hook_input)
    else:
        result = {"continue": True, "systemMessage": f"Unknown handler: {handler}"}

    # Output result as JSON
    print(json.dumps(result))


if __name__ == "__main__":
    main()
