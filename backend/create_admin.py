#!/usr/bin/env python
"""
Create an admin/superuser
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin(email, username, password, name):
    """Create an admin superuser"""
    try:
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"❌ User with email {email} already exists")
            return None
        
        if User.objects.filter(username=username).exists():
            print(f"❌ User with username {username} already exists")
            return None
        
        # Create superuser
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
            name=name,
        )
        
        print(f"\n{'='*60}")
        print(f"✅ Admin user created successfully!")
        print(f"{'='*60}")
        print(f"\nLogin Credentials:")
        print(f"  Email: {email}")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Name: {name}")
        print(f"\nAdmin Panel: http://localhost:8000/admin/")
        print(f"Frontend Login: http://localhost:3000/login")
        print(f"{'='*60}\n")
        
        return user
        
    except Exception as e:
        print(f"\n❌ Error creating admin: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Create default admin
    create_admin(
        email='admin@apranova.com',
        username='admin',
        password='admin123',
        name='Admin User'
    )
    
    print("\n💡 You can now:")
    print("  1. Access Django Admin: http://localhost:8000/admin/")
    print("  2. Use email: admin@apranova.com")
    print("  3. Use password: admin123")
    print("  4. Manage users, sessions, payments, etc.")
    print("\n  Or login to frontend:")
    print("  5. Go to: http://localhost:3000/login")
    print("  6. Access admin dashboard\n")
