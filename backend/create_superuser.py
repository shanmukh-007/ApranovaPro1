#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if it doesn't exist
if not User.objects.filter(email='admin@apranova.com').exists():
    User.objects.create_superuser(
        email='admin@apranova.com',
        password='Admin@123456',
        first_name='Admin',
        last_name='User',
        role='SUPERADMIN'
    )
    print('✅ Superuser created successfully!')
    print('Email: admin@apranova.com')
    print('Password: Admin@123456')
else:
    print('⚠️ Superuser already exists')
