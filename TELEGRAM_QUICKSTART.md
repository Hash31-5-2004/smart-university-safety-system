# Quick Start: Telegram Integration

**Get your security team chatting in < 10 minutes** 🚀

## 1️⃣ Create a Telegram Bot (2 min)

1. Open Telegram → Search `@BotFather`
2. Send `/newbot`
3. Follow the prompts → **Save your TOKEN**

```
Example: 123456789:ABCDEfghIjklmnopQRSTuvwxyz1234567890
```

## 2️⃣ Create Security Group (2 min)

1. In Telegram → New Group
2. Add security staff members
3. Group name: "Campus Security - Real Time Alerts"
4. Add your bot with **Admin permissions**

## 3️⃣ Get Group ID (2 min)

Easiest way: Run this Python code:

```python
from telegram import Bot
import asyncio

async def get_id():
    bot = Bot(token="YOUR_BOT_TOKEN")
    # Group ID appears in error logs or API responses
    # Usually looks like: -1001234567890
    
asyncio.run(get_id())
```

Or check your Python logs when bot joins the group.

## 4️⃣ Configure Environment (1 min)

```bash
# Copy template
cp .env.example .env

# Edit .env
nano .env
```

Add these lines:
```
TELEGRAM_BOT_TOKEN=123456789:ABCDEfghIjklmnopQRSTuvwxyz1234567890
TELEGRAM_GROUP_ID=-1001234567890
```

## 5️⃣ Install & Test (2 min)

```bash
# Install packages
pip install python-telegram-bot aiohttp

# Run test
python test_telegram.py
```

**Done!** 🎉 Check your Telegram group for a test alert.

---

## Alert Format Example

When an incident is detected:

```
🚨 CAMPUS SAFETY ALERT

Priority: CRITICAL
Incident Type: Unauthorized Access
Location: Building A - Main Entrance
Confidence: 95.5%
Timestamp: 2026-04-29 14:23:45

Description: Detected unauthorized access attempt

Recommended Actions:
1. Alert security immediately
2. Review access logs
3. Check camera footage

Security Team - Immediate Action Required
```

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| ❌ "Bot token not found" | Check `.env` file exists with correct token |
| ❌ "Chat not found" | Verify group ID is correct (starts with -100) |
| ❌ "User not member" | Make sure bot is added to group with Admin permissions |
| ❌ "ModuleNotFoundError" | Run `pip install python-telegram-bot aiohttp` |

---

## Verify It Works

1. ✅ Bot joins your group successfully
2. ✅ Test alert appears in group
3. ✅ Emoji indicators show (🚨 ⚠️ ⏱️ ℹ️)
4. ✅ Timestamps are correct
5. ✅ All security staff can see alerts

---

## Key Commands

```bash
# Test the integration
python test_telegram.py

# Check logs
tail -f output.log

# View environment variables (safe, masked)
grep TELEGRAM .env
```

---

## Features

- ✅ Real-time alerts to group
- ✅ Priority-based emoji indicators
- ✅ Detailed incident information
- ✅ Confidence scores
- ✅ Safety recommendations
- ✅ Works alongside n8n automation
- ✅ Easy to test and debug

---

## Full Documentation

See `TELEGRAM_SETUP.md` for detailed instructions and troubleshooting.

**Questions?** Check the logs or run `python test_telegram.py` with verbose output.

Happy alerting! 🛡️
