# Telegram Integration Guide

This guide will help you set up Telegram integration for the Smart University Safety System. The system will send real-time alerts to a Telegram group where your security staff can monitor campus incidents.

## Prerequisites

- Telegram app installed (desktop or mobile)
- A Telegram account
- Access to create a Telegram group

## Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a conversation with BotFather
3. Send the command: `/newbot`
4. Follow the prompts to create a new bot:
   - Give it a name (e.g., "Campus Safety Bot")
   - Give it a username (must end with `bot`, e.g., `campus_safety_bot`)
5. BotFather will provide you with a **BOT TOKEN** that looks like:
   ```
   123456789:ABCDEfghIjklmnopQRSTuvwxyz1234567890
   ```
6. **Save this token** - you'll need it in Step 4

## Step 2: Create a Telegram Group for Security Staff

1. Open Telegram
2. Click the menu (three lines) → New Group
3. Add security staff members to the group
4. Give the group a name (e.g., "x  ")
5. Keep the group settings to default (or customize as needed)

## Step 3: Add the Bot to Your Security Group

1. Open your security group chat
2. Click the group name at the top → Edit Group
3. Click "Add Members"
4. Search for your bot (use the username you created in Step 1)
5. Add the bot to the group
6. Give the bot **Admin permissions** (required to send messages):
   - Click the bot name
   - Click "Promote to Admin"
   - Give it permission to "Post Messages"

## Step 4: Get Your Group ID

There are two ways to get your group ID:

### Method A: Using a Bot Helper (Easiest)
1. In your security group, send the command: `/start` to your bot
2. Send a message in the group
3. Check your Python logs or use a test script to see the group ID

### Method B: Programmatic Way
Create a temporary Python script to find the group ID:

```python
from telegram import Bot
import asyncio

async def get_group_id():
    bot = Bot(token="YOUR_BOT_TOKEN_HERE")
    
    # Send a test message to the group
    # The group ID will be displayed in error messages or logs
    updates = await bot.get_updates()
    
    for update in updates:
        if update.message and update.message.chat.type == "group":
            print(f"Group ID: {update.message.chat_id}")

asyncio.run(get_group_id())
```

The group ID typically looks like: `-1001234567890` (note the negative sign and initial -100)

## Step 5: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCDEfghIjklmnopQRSTuvwxyz1234567890
   TELEGRAM_GROUP_ID=-1001234567890
   GROQ_API_KEY=your_groq_key_here
   ```

3. **Never commit `.env` to version control** - add it to `.gitignore`

## Step 6: Install Dependencies

Install the new Telegram dependencies:

```bash
pip install -r requirements.txt
```

Or if you already have dependencies installed, just add:

```bash
pip install python-telegram-bot aiohttp
```

## Step 7: Test the Integration

Create a test script to verify everything works:

```python
from src.integrations.telegram_service import TelegramService

# Create service instance
service = TelegramService()

# Send a test alert
success = service.send_alert_sync(
    incident_type="Test Alert",
    location="Main Campus Gate",
    confidence=0.95,
    priority="HIGH",
    description="This is a test alert to verify Telegram integration",
    recommendations="Verify bot is working correctly"
)

if success:
    print("✅ Telegram bot is working!")
else:
    print("❌ Failed to send message. Check your configuration.")
```

## Troubleshooting

### Bot Token Error
- **Error**: "Unauthorized" or "404 Not Found"
- **Solution**: Double-check your BOT_TOKEN in `.env` - it should not have extra spaces

### Group ID Error
- **Error**: "Chat not found" or "User not member"
- **Solution**: 
  - Verify the group ID is correct (should start with -100)
  - Make sure the bot is added to the group
  - Check that the bot has Admin permissions

### Messages Not Appearing
- **Solution**: 
  - Verify the group ID in `.env`
  - Check that bot has "Post Messages" permission
  - Look for error messages in the logs

### Import Errors
- **Error**: `ModuleNotFoundError: No module named 'telegram'`
- **Solution**: Run `pip install python-telegram-bot aiohttp`

## How Alerts Are Sent

When the system detects an incident:

1. **Computer Vision Agent** analyzes the image and detects anomalies
2. **RAG Agent** retrieves relevant safety protocols from the knowledge base
3. **Alert Agent** formats the alert and sends it via:
   - **Telegram**: Real-time group notification with formatted details
   - **n8n**: Webhook for additional automation

## Message Format

Telegram alerts appear in the group with this format:

```
🚨 CAMPUS SAFETY ALERT

Priority: CRITICAL
Incident Type: Unauthorized Access
Location: Building A - Floor 3
Confidence: 95.0%
Timestamp: 2026-04-29 14:23:45

Description:
Detected unauthorized access attempt at restricted area

Recommended Actions:
1. Alert campus security immediately
2. Review security footage
3. Check access logs

Security Team - Immediate Action Required
```

## Features

### Priority Levels with Emoji Indicators
- 🚨 **CRITICAL**: Immediate response required (fight, assault, weapon, high confidence)
- ⚠️ **HIGH**: Urgent response (fall, injury, medical, confidence > 0.7)
- ⏱️ **MEDIUM**: Standard response (confidence > 0.5)
- ℹ️ **LOW**: Informational (low confidence)

### Status Updates
Send status updates to the group:

```python
from src.integrations.telegram_service import TelegramService

service = TelegramService()
service.send_status_update_sync(
    "✅ System online and monitoring. 5 incidents detected today."
)
```

## Best Practices

1. **Keep Bot Token Secure**: Never share your bot token or commit it to version control
2. **Use Group Admin Cautiously**: Only add trusted administrators
3. **Monitor Alerts**: Regularly check that alerts are being sent properly
4. **Test New Features**: Always test with a test group before deploying to production
5. **Document Changes**: Keep your security group informed of system updates

## Next Steps

- Set up notification rules in your security group (mute certain times, etc.)
- Configure additional security responses in your organization
- Integrate Telegram bot commands for security staff to query system status
- Add webhook forwarding from Telegram to your security operations center

## Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all credentials in `.env`
3. Ensure the bot has proper admin permissions
4. Test with the provided test script
5. Check the Telegram Bot API documentation: https://core.telegram.org/bots/api

Happy monitoring! 🛡️
