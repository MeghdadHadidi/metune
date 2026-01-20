---
name: teleporter:configure
description: Set up Telegram bot credentials for teleporter
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
argument-hint: "[token] [chat_id]"
---

# Configure Teleporter

Help the user configure their Telegram bot credentials for the teleporter plugin.

## Steps

1. **Check current configuration**:
   - Check if `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` environment variables are set
   - Run: `echo "Token: ${TELEGRAM_BOT_TOKEN:+[SET]}" && echo "Chat ID: ${TELEGRAM_CHAT_ID:+[SET]}"`

2. **If credentials provided as arguments**:
   - If both token and chat_id were passed, validate and save them
   - Test the connection using the telegram_api.py script

3. **If credentials not provided**, guide the user:

   First, ask if they already have a Telegram bot:
   - If yes: Ask for the bot token
   - If no: Explain how to create one:
     1. Open Telegram and search for @BotFather
     2. Send `/newbot` and follow the prompts
     3. Copy the bot token provided

   Then, ask for the chat ID:
   - Explain how to get it:
     1. Start a conversation with the bot
     2. Send any message to the bot
     3. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
     4. Find the `chat.id` in the response

4. **Save credentials**:
   - Create or update the user's shell profile with exports
   - Determine which shell profile to use:
     - If `~/.zshrc` exists, use that (macOS default)
     - Otherwise use `~/.bashrc`

   Add these lines to the profile:
   ```bash
   # Teleporter - Telegram integration for Claude Code
   export TELEGRAM_BOT_TOKEN="<token>"
   export TELEGRAM_CHAT_ID="<chat_id>"
   ```

5. **Test the connection**:
   - Run: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/telegram_api.py test`
   - If successful, send a test message
   - Run: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/telegram_api.py send "Teleporter configured successfully! 🚀"`

6. **Inform the user**:
   - Credentials have been saved
   - They need to restart their terminal or run `source ~/.zshrc` (or appropriate file)
   - The plugin will work automatically on next Claude Code session

## Tips

- Never display the full bot token in output - it's sensitive
- The chat ID is a number (can be negative for groups)
- If the user wants to use a group chat, they need to add the bot to the group first
