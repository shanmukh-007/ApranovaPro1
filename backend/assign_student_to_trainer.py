#!/usr/bin/env python
"""
Assign student to trainer
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get trainer and student
trainer = User.objects.get(email='trainer@apranova.com')
student = User.objects.get(email='apranova123@gmail.com')

# Assign student to trainer
student.assigned_trainer = trainer
student.save()

print(f"✅ Assigned {student.email} to trainer {trainer.email}")
