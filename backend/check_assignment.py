import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

student = User.objects.get(email='apranova123@gmail.com')
print(f'Student: {student.email}')
print(f'Assigned Trainer: {student.assigned_trainer.email if student.assigned_trainer else "None"}')
