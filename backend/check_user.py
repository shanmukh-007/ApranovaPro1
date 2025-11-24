#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check for apranova123@gmail.com
user = User.objects.filter(email='apranova123@gmail.com').first()

if user:
    print(f"\nUser found: {user.username}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")
    print(f"Track: {user.track}")
    print(f"Payment Verified: {user.payment_verified}")
    print(f"Enrollment Status: {user.enrollment_status}")
else:
    print("\nUser apranova123@gmail.com not found")
    print("\nAll student users:")
    for u in User.objects.filter(role='student'):
        print(f"  - {u.email} (payment_verified={u.payment_verified})")
