#!/usr/bin/env python
"""
Test Stripe API keys configuration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import stripe
from django.conf import settings

def test_stripe_keys():
    """Test if Stripe keys are valid"""
    print("\n" + "="*60)
    print("Testing Stripe API Keys")
    print("="*60)
    
    # Check if keys are set
    print("\n1. Checking if keys are configured...")
    
    public_key = settings.STRIPE_PUBLISHABLE_KEY
    secret_key = settings.STRIPE_SECRET_KEY
    
    if not public_key or public_key == 'pk_test_your-stripe-public-key':
        print("❌ STRIPE_PUBLIC_KEY not configured")
        print("   Please update .env with your real Stripe public key")
        print("   Get it from: https://dashboard.stripe.com/test/apikeys")
        return False
    
    if not secret_key or secret_key == 'sk_test_your-stripe-secret-key':
        print("❌ STRIPE_SECRET_KEY not configured")
        print("   Please update .env with your real Stripe secret key")
        print("   Get it from: https://dashboard.stripe.com/test/apikeys")
        return False
    
    print(f"✅ Public key: {public_key[:20]}...")
    print(f"✅ Secret key: {secret_key[:20]}...")
    
    # Test API connection
    print("\n2. Testing Stripe API connection...")
    
    try:
        stripe.api_key = secret_key
        
        # Try to retrieve account balance
        balance = stripe.Balance.retrieve()
        
        print("✅ Stripe API connection successful!")
        print(f"   Account currency: {balance.available[0].currency if balance.available else 'N/A'}")
        print(f"   Available balance: {balance.available[0].amount / 100 if balance.available else 0}")
        
        return True
        
    except stripe.error.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Your secret key is invalid or incorrect")
        print("   Please check: https://dashboard.stripe.com/test/apikeys")
        return False
        
    except stripe.error.StripeError as e:
        print(f"❌ Stripe error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_payment_intent():
    """Test creating a payment intent"""
    print("\n3. Testing payment intent creation...")
    
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Create a test payment intent
        intent = stripe.PaymentIntent.create(
            amount=1000,  # $10.00
            currency='usd',
            payment_method_types=['card'],
            metadata={'test': 'true'}
        )
        
        print("✅ Payment intent created successfully!")
        print(f"   Intent ID: {intent.id}")
        print(f"   Amount: ${intent.amount / 100}")
        print(f"   Status: {intent.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create payment intent: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("Stripe Configuration Test")
    print("="*60)
    
    # Test keys
    keys_valid = test_stripe_keys()
    
    if not keys_valid:
        print("\n" + "="*60)
        print("❌ STRIPE KEYS NOT CONFIGURED")
        print("="*60)
        print("\nTo fix:")
        print("1. Go to: https://dashboard.stripe.com/test/apikeys")
        print("2. Copy your Publishable key (pk_test_...)")
        print("3. Copy your Secret key (sk_test_...)")
        print("4. Update .env file:")
        print("   STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY")
        print("   STRIPE_SECRET_KEY=sk_test_YOUR_KEY")
        print("5. Restart backend server")
        print("="*60 + "\n")
        return
    
    # Test payment intent
    payment_valid = test_payment_intent()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Keys configured: {'✅ PASS' if keys_valid else '❌ FAIL'}")
    print(f"API connection: {'✅ PASS' if keys_valid else '❌ FAIL'}")
    print(f"Payment intent: {'✅ PASS' if payment_valid else '❌ FAIL'}")
    
    if keys_valid and payment_valid:
        print("\n✅ All tests passed! Stripe is configured correctly.")
        print("\nYou can now:")
        print("- Accept payments on /get-started page")
        print("- Use test card: 4242 4242 4242 4242")
        print("- Process enrollments")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
