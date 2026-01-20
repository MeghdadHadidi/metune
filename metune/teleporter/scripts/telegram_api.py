#!/usr/bin/env python3
"""
Telegram Bot API wrapper for teleporter plugin.
Handles sending messages, updating messages, and managing inline keyboards.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Optional, List, Dict, Any


def get_config() -> tuple[str, str]:
    """Get Telegram bot token and chat ID from environment."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    if not chat_id:
        raise ValueError("TELEGRAM_CHAT_ID environment variable not set")

    return token, chat_id


def api_request(method: str, params: Dict[str, Any], request_timeout: int = 30) -> Dict[str, Any]:
    """Make a request to the Telegram Bot API."""
    token, _ = get_config()
    url = f"https://api.telegram.org/bot{token}/{method}"

    data = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=request_timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
            if not result.get("ok"):
                raise ValueError(f"API error: {result.get('description', 'Unknown error')}")
            return result.get("result", {})
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise ValueError(f"HTTP {e.code}: {error_body}")


def create_inline_keyboard(buttons: List[List[Dict[str, str]]]) -> Dict[str, Any]:
    """
    Create an inline keyboard markup.

    buttons: List of rows, each row is a list of button dicts with 'text' and 'callback_data'
    Example: [[{"text": "Yes", "callback_data": "yes"}, {"text": "No", "callback_data": "no"}]]
    """
    return {"inline_keyboard": buttons}


def send_message(
    text: str,
    chat_id: Optional[str] = None,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> Dict[str, Any]:
    """
    Send a new message to the chat.

    Returns the sent message object (includes message_id).
    """
    _, default_chat_id = get_config()

    params = {
        "chat_id": chat_id or default_chat_id,
        "text": text,
        "parse_mode": parse_mode
    }

    if reply_markup:
        params["reply_markup"] = reply_markup

    return api_request("sendMessage", params)


def edit_message(
    message_id: int,
    text: str,
    chat_id: Optional[str] = None,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> Dict[str, Any]:
    """
    Edit an existing message.

    Returns the edited message object.
    """
    _, default_chat_id = get_config()

    params = {
        "chat_id": chat_id or default_chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }

    if reply_markup:
        params["reply_markup"] = reply_markup

    return api_request("editMessageText", params)


def edit_reply_markup(
    message_id: int,
    reply_markup: Dict[str, Any],
    chat_id: Optional[str] = None
) -> Dict[str, Any]:
    """Edit only the reply markup (buttons) of a message."""
    _, default_chat_id = get_config()

    params = {
        "chat_id": chat_id or default_chat_id,
        "message_id": message_id,
        "reply_markup": reply_markup
    }

    return api_request("editMessageReplyMarkup", params)


def answer_callback_query(
    callback_query_id: str,
    text: Optional[str] = None,
    show_alert: bool = False
) -> bool:
    """
    Answer a callback query (acknowledge button press).

    This must be called after receiving a callback query to stop the loading indicator.
    """
    params = {"callback_query_id": callback_query_id}

    if text:
        params["text"] = text
        params["show_alert"] = show_alert

    return api_request("answerCallbackQuery", params)


def get_updates(
    offset: Optional[int] = None,
    timeout: int = 30,
    allowed_updates: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Get updates (new messages, callback queries, etc.) using long polling.

    offset: Identifier of the first update to be returned (use last update_id + 1)
    timeout: Long polling timeout in seconds
    allowed_updates: List of update types to receive (e.g., ["message", "callback_query"])
    """
    params = {"timeout": timeout}

    if offset is not None:
        params["offset"] = offset

    if allowed_updates:
        params["allowed_updates"] = allowed_updates

    # Use a request timeout slightly longer than the Telegram long-poll timeout
    # to avoid urllib timing out before Telegram responds
    return api_request("getUpdates", params, request_timeout=timeout + 10)


def delete_message(message_id: int, chat_id: Optional[str] = None) -> bool:
    """Delete a message."""
    _, default_chat_id = get_config()

    params = {
        "chat_id": chat_id or default_chat_id,
        "message_id": message_id
    }

    return api_request("deleteMessage", params)


def get_me() -> Dict[str, Any]:
    """Get information about the bot. Useful for testing connection."""
    return api_request("getMe", {})


def format_session_message(
    session_id: str,
    cwd: str,
    status: str = "active",
    question: Optional[str] = None
) -> str:
    """Format the session message text."""
    # Escape HTML special characters
    cwd_escaped = cwd.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    lines = [
        f"<b>Claude Code Session</b>",
        f"<code>{session_id[:8]}</code>",
        f"",
        f"<b>Directory:</b> <code>{cwd_escaped}</code>",
        f"<b>Status:</b> {status}",
    ]

    if question:
        question_escaped = question.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines.extend([
            "",
            f"<b>Question:</b>",
            f"{question_escaped}"
        ])

    return "\n".join(lines)


def create_session_buttons(include_context: bool = True) -> Dict[str, Any]:
    """Create default session action buttons."""
    buttons = []

    if include_context:
        buttons.append([{"text": "📊 Get Context", "callback_data": "get_context"}])

    buttons.append([
        {"text": "✅ Continue", "callback_data": "continue"},
        {"text": "⏹ Stop", "callback_data": "stop"}
    ])

    return create_inline_keyboard(buttons)


def create_question_buttons(options: List[Dict[str, str]], multi_select: bool = False) -> Dict[str, Any]:
    """
    Create buttons for a question.

    options: List of dicts with 'label' and optionally 'value' keys
    multi_select: If True, adds a note that multiple selections are allowed
    """
    buttons = []

    for i, opt in enumerate(options):
        label = opt.get("label", f"Option {i+1}")
        value = opt.get("value", opt.get("label", str(i)))
        # Truncate label if too long for button
        if len(label) > 30:
            label = label[:27] + "..."
        # For multi-select, we'd need more complex state management
        # For now, single-click still works but user can type multiple
        buttons.append([{"text": label, "callback_data": f"answer:{value}"}])

    # Add text input option (especially useful for multi-select)
    if multi_select:
        buttons.append([{"text": "💬 Type multiple (comma-separated)", "callback_data": "text_input"}])
    else:
        buttons.append([{"text": "💬 Type reply...", "callback_data": "text_input"}])

    return create_inline_keyboard(buttons)


if __name__ == "__main__":
    # CLI interface for testing
    if len(sys.argv) < 2:
        print("Usage: telegram_api.py <command> [args...]")
        print("Commands: test, send <message>, get_updates")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "test":
            bot = get_me()
            print(f"Connected to bot: @{bot.get('username')}")

        elif command == "send":
            if len(sys.argv) < 3:
                print("Usage: telegram_api.py send <message>")
                sys.exit(1)
            message = " ".join(sys.argv[2:])
            result = send_message(message)
            print(f"Sent message ID: {result.get('message_id')}")

        elif command == "get_updates":
            updates = get_updates(timeout=1)
            print(json.dumps(updates, indent=2))

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
