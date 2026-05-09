#!/usr/bin/env python3
"""
Test script for Telegram integration
Run this to verify your Telegram bot is properly configured
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.integrations.telegram_service import TelegramService


def test_telegram_connection():
    """Test basic Telegram bot connectivity."""
    print("=" * 60)
    print("🤖 TELEGRAM BOT CONNECTION TEST")
    print("=" * 60)
    
    try:
        print("\n📋 Loading environment variables...")
        load_dotenv()
        
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        group_id = os.getenv("TELEGRAM_GROUP_ID")
        
        if not bot_token:
            print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in .env")
            print("   Please set up your environment variables first.")
            print("   See TELEGRAM_SETUP.md for instructions.")
            return False
            
        if not group_id:
            print("❌ ERROR: TELEGRAM_GROUP_ID not found in .env")
            print("   Please set up your environment variables first.")
            print("   See TELEGRAM_SETUP.md for instructions.")
            return False
        
        print("✅ Environment variables loaded")
        print(f"   Token: {bot_token[:20]}...****")
        print(f"   Group ID: {group_id}")
        
        print("\n📱 Initializing Telegram service...")
        service = TelegramService()
        print("✅ Service initialized successfully")
        
        print("\n📤 Sending test alert to Telegram group...")
        success = service.send_alert_sync(
            incident_type="System Test",
            location="Testing Environment",
            confidence=1.0,
            priority="MEDIUM",
            description="This is a test alert to verify Telegram integration is working correctly.",
            recommendations="No action needed - this is a test message"
        )
        
        if success:
            print("✅ Test alert sent successfully!")
            print("\n" + "=" * 60)
            print("🎉 SUCCESS! Telegram integration is working!")
            print("=" * 60)
            return True
        else:
            print("❌ Failed to send test alert")
            print("   Check your bot token and group ID")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Verify bot token is correct (no extra spaces)")
        print("2. Make sure bot is added to the group with Admin permissions")
        print("3. Check that group ID is correct (starts with -100)")
        print("4. Ensure python-telegram-bot is installed: pip install python-telegram-bot")
        return False


def test_status_update():
    """Test status update functionality."""
    print("\n\n📊 TESTING STATUS UPDATE")
    print("=" * 60)
    
    try:
        service = TelegramService()
        
        message = "✅ Campus Safety System is online and monitoring 24/7"
        print(f"Sending: {message}")
        
        success = service.send_status_update_sync(message)
        
        if success:
            print("✅ Status update sent successfully!")
            return True
        else:
            print("❌ Failed to send status update")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_priority_levels():
    """Test different priority levels."""
    print("\n\n🎯 TESTING PRIORITY LEVELS")
    print("=" * 60)
    
    test_cases = [
        {
            "incident_type": "Unauthorized Access",
            "location": "Admin Building - Door 5",
            "confidence": 0.98,
            "priority": "CRITICAL",
            "description": "Detected unauthorized access attempt"
        },
        {
            "incident_type": "Person Falls",
            "location": "Library - 2nd Floor",
            "confidence": 0.85,
            "priority": "HIGH",
            "description": "Person detected falling down stairs"
        },
        {
            "incident_type": "Unusual Activity",
            "location": "Parking Lot B",
            "confidence": 0.65,
            "priority": "MEDIUM",
            "description": "Suspicious movement detected"
        },
    ]
    
    try:
        service = TelegramService()
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing {test_case['priority']} priority...")
            success = service.send_alert_sync(
                incident_type=test_case['incident_type'],
                location=test_case['location'],
                confidence=test_case['confidence'],
                priority=test_case['priority'],
                description=test_case['description'],
                recommendations=f"Test alert for {test_case['priority']} priority level"
            )
            
            if success:
                print(f"   ✅ {test_case['priority']} alert sent")
            else:
                print(f"   ❌ Failed to send {test_case['priority']} alert")
                return False
        
        print("\n✅ All priority level tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "TELEGRAM INTEGRATION TEST SUITE" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    
    # Test 1: Connection
    results.append(("Connection Test", test_telegram_connection()))
    
    # Ask if user wants to run additional tests
    if results[0][1]:
        print("\n\n🔧 Would you like to run additional tests?")
        response = input("Run status update test? (y/n): ").strip().lower()
        if response == 'y':
            results.append(("Status Update Test", test_status_update()))
        
        response = input("Run priority level tests? (y/n): ").strip().lower()
        if response == 'y':
            results.append(("Priority Level Tests", test_priority_levels()))
    
    # Summary
    print("\n\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Your Telegram integration is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("   See TELEGRAM_SETUP.md for troubleshooting.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
