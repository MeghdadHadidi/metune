---
name: Telegram Troubleshooting
description: This skill should be used when the user has issues with teleporter, Telegram bot connectivity, message delivery, button responses, or poller problems. Use when user mentions "telegram not working", "bot not responding", "buttons not working", "poller issues", or "teleporter problems".
version: 1.0.0
---

# Telegram Troubleshooting for Teleporter

Help diagnose and fix issues with the teleporter plugin's Telegram integration.

## Common Issues and Solutions

### 1. Bot Not Responding

**Symptoms**: Messages not being sent, bot appears offline

**Diagnostic steps**:
1. Verify environment variables are set:
   ```bash
   echo "Token set: ${TELEGRAM_BOT_TOKEN:+yes}"
   echo "Chat ID set: ${TELEGRAM_CHAT_ID:+yes}"
   ```

2. Test the bot connection:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/telegram_api.py test
   ```

3. Check for API errors in the response

**Solutions**:
- If token not set: Run `/teleporter:configure`
- If token invalid: Regenerate token via @BotFather
- If rate limited: Wait a few minutes and try again

### 2. Messages Not Appearing

**Symptoms**: Claude session starts but no Telegram message received

**Diagnostic steps**:
1. Check if the session was registered:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_manager.py list
   ```

2. Verify chat ID is correct:
   - The chat ID must match where you're looking for messages
   - For groups, chat ID is negative (e.g., -1001234567890)

3. Ensure you've started a conversation with the bot:
   - Open Telegram, find your bot, and send any message first

**Solutions**:
- Update chat ID if incorrect
- Start a conversation with the bot if you haven't
- Check bot privacy settings with @BotFather (`/setprivacy`)

### 3. Buttons Not Working

**Symptoms**: Clicking inline buttons doesn't do anything

**Diagnostic steps**:
1. Check if poller is running:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py status
   ```

2. Check poller logs:
   ```bash
   tail -20 ~/.teleporter/poller.log
   ```

3. Verify the session is active:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_manager.py list
   ```

**Solutions**:
- Start the poller if not running:
  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py start
  ```
- If poller is stuck, restart it:
  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py stop
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py start
  ```

### 4. Poller Crashes

**Symptoms**: Poller stops unexpectedly, buttons stop working

**Diagnostic steps**:
1. Check poller logs for errors:
   ```bash
   cat ~/.teleporter/poller.log
   ```

2. Look for common error patterns:
   - "Too many consecutive errors" - network issues
   - "API error" - Telegram API problems
   - "Invalid token" - credential issues

**Solutions**:
- For network issues: Check internet connection, try again
- For API errors: Wait and retry (could be temporary)
- For credential issues: Run `/teleporter:configure`

### 5. Session Not Updating

**Symptoms**: Question appears but message doesn't update with buttons

**Diagnostic steps**:
1. Check session state:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_manager.py list
   ```

2. Verify message ID is stored correctly

3. Check for Telegram API rate limits

**Solutions**:
- Telegram has rate limits on message editing
- Wait a moment between rapid edits
- If message is too old (>48h), it cannot be edited

### 6. Getting Your Chat ID

If you're unsure of your chat ID:

1. Start a conversation with your bot
2. Send any message
3. Run this curl command (replace YOUR_TOKEN):
   ```bash
   curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | python3 -m json.tool
   ```
4. Look for `"chat": {"id": 123456789}` in the response
5. That number is your chat ID

For groups:
- Add the bot to the group
- Send a message in the group
- The chat ID will be negative (e.g., -1001234567890)

## Telegram API Limits

Be aware of these Telegram Bot API limits:

- **Messages per second**: ~30 messages/second to same chat
- **Message editing**: Same message can be edited frequently but not infinitely
- **Long polling timeout**: Max 50 seconds recommended
- **Message age for editing**: Messages older than 48 hours cannot be edited

## Debug Mode

For detailed debugging, run the poller in foreground mode:

```bash
# Stop any running poller first
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py stop

# Run in foreground to see all output
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py foreground
```

This will show all API calls and responses in real-time.

## Resetting State

If things are completely broken, reset the teleporter state:

```bash
# Stop the poller
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py stop

# Clear session data
rm -rf ~/.teleporter/sessions.json
rm -rf ~/.teleporter/poller.pid
rm -rf ~/.teleporter/poller.log

# Restart Claude Code session
```

This clears all session tracking and starts fresh.
