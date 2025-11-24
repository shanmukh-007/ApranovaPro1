#!/usr/bin/env python
"""
Test Discord webhook integration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from utils.discord import send_test_notification, send_discord_message

print("🧪 Testing Discord Webhook Integration...")
print("=" * 50)

# Test 1: Simple message
print("\n1. Sending simple message...")
result1 = send_discord_message("Hello from ApraNova LMS! 👋")
if result1:
    print("   ✅ Simple message sent successfully")
else:
    print("   ❌ Failed to send simple message")

# Test 2: Rich embed notification
print("\n2. Sending test notification with embed...")
result2 = send_test_notification()
if result2:
    print("   ✅ Test notification sent successfully")
else:
    print("   ❌ Failed to send test notification")

print("\n" + "=" * 50)
if result1 or result2:
    print("✅ Discord webhook is working!")
    print("\nCheck your Discord channel for the messages.")
else:
    print("❌ Discord webhook failed")
    print("\nPlease check:")
    print("  1. DISCORD_WEBHOOK_URL is set in .env")
    print("  2. Webhook URL is correct")
    print("  3. Discord server is accessible")
