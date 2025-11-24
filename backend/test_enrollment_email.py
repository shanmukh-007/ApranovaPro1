#!/usr/bin/env python
"""
Test script for enrollment email functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from utils.email import send_welcome_email, send_payment_confirmation_email
from payments.models import Payment

User = get_user_model()

def test_welcome_email():
    """Test welcome email for new enrollment"""
    print("\n" + "="*60)
    print("Testing Welcome Email")
    print("="*60)
    
    # Find a test user or create one
    user = User.objects.filter(role='student').first()
    
    if not user:
        print("❌ No student user found. Create a test user first.")
        return False
    
    print(f"📧 Sending welcome email to: {user.email}")
    print(f"   Username: {user.username}")
    print(f"   Track: {user.track}")
    
    # Send welcome email with a test password
    success = send_welcome_email(user, password="TestPassword123!")
    
    if success:
        print("✅ Welcome email sent successfully!")
        print(f"   Check inbox: {user.email}")
        return True
    else:
        print("❌ Failed to send welcome email")
        return False


def test_payment_confirmation_email():
    """Test payment confirmation email"""
    print("\n" + "="*60)
    print("Testing Payment Confirmation Email")
    print("="*60)
    
    # Find a payment record
    payment = Payment.objects.filter(status='SUCCEEDED').first()
    
    if not payment:
        print("❌ No successful payment found. Make a test payment first.")
        return False
    
    user = payment.user
    if not user:
        print("❌ Payment has no associated user")
        return False
    
    print(f"📧 Sending payment confirmation to: {user.email}")
    print(f"   Amount: ${payment.amount}")
    print(f"   Track: {payment.track}")
    
    success = send_payment_confirmation_email(user, payment)
    
    if success:
        print("✅ Payment confirmation email sent successfully!")
        print(f"   Check inbox: {user.email}")
        return True
    else:
        print("❌ Failed to send payment confirmation email")
        return False


def main():
    print("\n" + "="*60)
    print("ApraNova LMS - Enrollment Email Test")
    print("="*60)
    
    # Test welcome email
    welcome_success = test_welcome_email()
    
    # Test payment confirmation
    payment_success = test_payment_confirmation_email()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Welcome Email: {'✅ PASS' if welcome_success else '❌ FAIL'}")
    print(f"Payment Confirmation: {'✅ PASS' if payment_success else '❌ FAIL'}")
    print("\n💡 Check your email inbox (and spam folder)")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
