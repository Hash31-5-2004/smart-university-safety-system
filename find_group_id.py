#!/usr/bin/env python3
"""
Utility script to help find your Telegram group ID
Run this if you're having trouble finding your group ID
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 60)
    print("🆔 TELEGRAM GROUP ID FINDER")
    print("=" * 60)
    
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        print("\n❌ ERROR: TELEGRAM_BOT_TOKEN not found in .env")
        print("\nPlease set up your .env file first:")
        print("  1. Get your bot token from @BotFather on Telegram")
        print("  2. Copy .env.example to .env")
        print("  3. Add your bot token to TELEGRAM_BOT_TOKEN")
        return 1
    
    print("\n✅ Bot token found")
    print("\nTo find your group ID, follow these steps:\n")
    
    print("📱 METHOD 1: Using Python (Automatic)")
    print("-" * 60)
    print("""
from telegram import Bot
import asyncio

async def find_group_id():
    bot = Bot(token="{token}")
    
    # Get the last 10 updates to the bot
    updates = await bot.get_updates(limit=10)
    
    for update in updates:
        if update.message and update.message.chat.type in ['group', 'supergroup']:
            chat = update.message.chat
            print(f"Found Group: {chat.title}")
            print(f"Group ID: {chat.id}")

asyncio.run(find_group_id())
    """.format(token="YOUR_BOT_TOKEN"))
    
    print("\n\n📱 METHOD 2: Manual (Send a message in group)")
    print("-" * 60)
    print("""
1. In your Telegram group, send a message: /start @your_bot_username
2. Or send any message that mentions the bot
3. Check your Python logs - the group ID will appear in error messages
4. Look for: chat_id or group_id in the output
5. Format: Usually looks like -1001234567890 (negative number with -100 prefix)
    """)
    
    print("\n\n📝 METHOD 3: Edit Group Settings")
    print("-" * 60)
    print("""
1. Open your security group in Telegram
2. Click the group name at the top
3. Edit the group settings
4. Look for "Group ID" or check via the Telegram Web client:
   - Go to https://web.telegram.org
   - Open the group
   - Check the URL or use F12 Developer Tools
   - Look for the chat ID in network requests
    """)
    
    print("\n\n💡 TIPS")
    print("-" * 60)
    print("""
- Group IDs start with -100 followed by digits
- Example: -1001234567890
- Private groups: -1001234567890
- Channels: -1001234567890
- Make sure you get the GROUP ID, not the CHANNEL ID
    """)
    
    print("\n\n✅ ONCE YOU HAVE YOUR GROUP ID:")
    print("-" * 60)
    print("""
1. Edit your .env file
2. Add: TELEGRAM_GROUP_ID=-1001234567890
3. Save the file
4. Run: python test_telegram.py
5. Check your Telegram group for a test alert
    """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
