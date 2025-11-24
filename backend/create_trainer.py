#!/usr/bin/env python
"""
Create a trainer user
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def create_trainer(email, username, password, name):
    """Create a trainer user"""
    try:
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"❌ User with email {email} already exists")
            return None
        
        if User.objects.filter(username=username).exists():
            print(f"❌ User with username {username} already exists")
            return None
        
        # Create trainer user
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            name=name,
            role='trainer',
            enrollment_status='ENROLLED',
            payment_verified=True,
            enrolled_at=timezone.now(),
            privacy_accepted=True,
            privacy_accepted_at=timezone.now(),
            privacy_version='1.0',
        )
        
        print(f"\n{'='*60}")
        print(f"✅ Trainer user created successfully!")
        print(f"{'='*60}")
        print(f"\nLogin Credentials:")
        print(f"  Email: {email}")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Name: {name}")
        print(f"\nLogin URL: http://localhost:3000/login")
        print(f"{'='*60}\n")
        
        return user
        
    except Exception as e:
        print(f"\n❌ Error creating trainer: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Create default trainer
    create_trainer(
        email='trainer@apranova.com',
        username='trainer1',
        password='trainer123',
        name='John Trainer'
    )
    
    print("\n💡 You can now:")
    print("  1. Log in at: http://localhost:3000/login")
    print("  2. Use email: trainer@apranova.com")
    print("  3. Use password: trainer123")
    print("  4. Go to: /trainer/sessions")
    print("  5. Schedule sessions for students\n")
