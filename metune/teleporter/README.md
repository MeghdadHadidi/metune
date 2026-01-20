# Teleporter

Control Claude Code remotely via Telegram. Get notifications, answer questions, and interact with your Claude sessions from anywhere.

## Features

- **Session notifications**: Each Claude Code session sends a Telegram message with action buttons
- **Interactive questions**: When Claude asks you something, the message updates with answer buttons
- **Multi-session support**: Track multiple concurrent Claude Code sessions
- **Bidirectional communication**: Send responses back to Claude via Telegram

## Prerequisites

- Python 3.8+
- A Telegram bot (create one via [@BotFather](https://t.me/BotFather))
- Your Telegram chat ID

## Installation

1. Copy this plugin to your Claude Code plugins directory or use `--plugin-dir`:
   ```bash
   claude --plugin-dir /path/to/teleporter
   ```

2. Configure your Telegram credentials:
   ```bash
   # Run the configure command in Claude Code
   /teleporter:configure
   ```

   Or set environment variables directly:
   ```bash
   export TELEGRAM_BOT_TOKEN="your-bot-token"
   export TELEGRAM_CHAT_ID="your-chat-id"
   ```

## Usage

Once configured, the plugin works automatically:

1. **Session Start**: When you start a Claude Code session, you'll receive a Telegram message with:
   - Session ID and working directory
   - "Get Context" button for current status

2. **Questions**: When Claude asks a question (framework choice, yes/no, etc.):
   - The message updates with the question
   - Answer buttons appear as inline keyboard
   - Tap a button or reply with text

3. **Notifications**: Build completions, errors, and other notifications are forwarded

## Commands

- `/teleporter:configure` - Set up or update Telegram credentials
- `/teleporter:status` - Check current session status and connection

## How It Works

1. **SessionStart hook** sends initial Telegram message and starts background poller
2. **PreToolUse hook** intercepts AskUserQuestion to display options as buttons
3. **Background poller** watches for button clicks and text replies
4. **Response injector** sends your Telegram response to Claude Code's input

## Troubleshooting

### Bot not responding?
- Verify your bot token with `/teleporter:status`
- Make sure you've started a conversation with your bot first
- Check that your chat ID is correct

### Not receiving messages?
- Ensure the poller is running (check with `/teleporter:status`)
- Verify environment variables are set correctly

### Getting your Chat ID
1. Start a conversation with your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find your chat ID in the response

## License

MIT
