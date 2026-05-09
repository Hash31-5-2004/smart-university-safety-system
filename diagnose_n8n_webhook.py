#!/usr/bin/env python3
"""
Helper script to diagnose N8N webhook issues
Tests different URL formats to find the correct one
"""

import requests
import sys
from datetime import datetime

def test_webhook_url(url):
    """Test if a webhook URL responds correctly."""
    print(f"\n🔗 Testing: {url}")
    
    test_payload = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "location": "Test Location",
        "confidence": 0.85,
        "caption": "Test alert",
        "alert_text": "Testing webhook connectivity",
        "processing_mode": "Webhook Test"
    }
    
    try:
        response = requests.post(url, json=test_payload, timeout=5)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! This URL works!")
            print(f"   Response: {response.text[:100]}")
            return True
        elif response.status_code == 404:
            print(f"   ❌ 404 Not Found - Webhook URL is incorrect")
            return False
        elif response.status_code == 405:
            print(f"   ❌ 405 Method Not Allowed - Check webhook method (should be POST)")
            return False
        else:
            print(f"   ⚠️  Status {response.status_code}")
            print(f"   Response: {response.text[:100]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout - Server not responding")
        return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error - Cannot reach server")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


def main():
    """Main diagnostic."""
    print("\n" + "="*70)
    print("🔍 N8N WEBHOOK DIAGNOSTIC TOOL")
    print("="*70)
    
    print("\n📋 INSTRUCTIONS:")
    print("1. Go to https://app.n8n.cloud")
    print("2. Open your 'Security Alert Emails' workflow")
    print("3. Click the Webhook node (first one)")
    print("4. In the right panel, find 'Webhook URL'")
    print("5. Copy the complete URL shown there")
    print("6. Run this script with that URL")
    print("\nUsage:")
    print("  python diagnose_n8n_webhook.py <webhook_url>")
    print("\nExample:")
    print("  python diagnose_n8n_webhook.py https://hash314151.app.n8n.cloud/webhook/security-alert-emails")
    
    # If URL provided as argument
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
        
        print(f"\n{'='*70}")
        print(f"Testing your webhook URL...")
        print(f"{'='*70}")
        
        success = test_webhook_url(webhook_url)
        
        if success:
            print(f"\n✅ SOLUTION FOUND!")
            print(f"\nUpdate your dashboard.py with this URL:")
            print(f"\nN8N_WEBHOOK_URL = \"{webhook_url}\"")
            print(f"\nThen restart Streamlit:")
            print(f"  streamlit run dashboard.py")
        else:
            print(f"\n❌ URL doesn't work. Double-check:")
            print(f"  1. URL is copied exactly from N8N Webhook node")
            print(f"  2. Workflow is 'Published' and 'Active'")
            print(f"  3. No extra spaces in URL")
            print(f"\nCommon URL formats:")
            print(f"  https://hash314151.app.n8n.cloud/webhook/security-alert-emails")
            print(f"  https://hash314151.app.n8n.cloud/webhook/campus-safety")
            print(f"  https://hash314151.app.n8n.cloud/webhook/incident-alerts")
    else:
        print(f"\n⚠️  No URL provided!")
        print(f"\nUsage: python diagnose_n8n_webhook.py <your_webhook_url>")
        sys.exit(1)


if __name__ == "__main__":
    main()
