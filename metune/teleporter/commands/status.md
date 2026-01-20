---
name: teleporter:status
description: Check teleporter connection status and current session
allowed-tools:
  - Bash
  - Read
---

# Teleporter Status

Show the current status of the teleporter plugin, including Telegram connection and session information.

## Check and Display

1. **Check Telegram configuration**:
   ```bash
   echo "=== Telegram Configuration ==="
   if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
     echo "Bot Token: [SET] (${#TELEGRAM_BOT_TOKEN} chars)"
   else
     echo "Bot Token: [NOT SET]"
   fi

   if [ -n "$TELEGRAM_CHAT_ID" ]; then
     echo "Chat ID: $TELEGRAM_CHAT_ID"
   else
     echo "Chat ID: [NOT SET]"
   fi
   ```

2. **Test Telegram connection** (if configured):
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/telegram_api.py test
   ```

3. **Check poller status**:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/poller.py status
   ```

4. **List active sessions**:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_manager.py list
   ```

5. **Show summary**:
   - Configuration status (configured/not configured)
   - Connection status (connected/disconnected/error)
   - Poller status (running/stopped)
   - Active sessions count

## Output Format

Present the information in a clear, readable format:

```
Teleporter Status
─────────────────
Configuration: ✓ Configured
Connection:    ✓ Connected to @YourBotName
Poller:        ✓ Running (PID: 12345)
Sessions:      1 active

Current Session:
  ID: abc12345
  Directory: /path/to/project
  Message ID: 67890
```

If not configured, show:
```
Teleporter Status
─────────────────
Configuration: ✗ Not configured
Run /teleporter:configure to set up Telegram credentials
```
