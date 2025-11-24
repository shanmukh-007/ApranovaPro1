"""
Fix student progress - ensure FSD student has Project 1 unlocked
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from curriculum.models import Project, StudentProgress, Track
from django.utils import timezone

User = get_user_model()

# Find FSD student
user = User.objects.filter(track='FSD', role='student').first()

if not user:
    print("❌ No FSD student found")
    print("Creating test FSD student...")
    user = User.objects.create_user(
        email='fsd@test.com',
        username='fsd_student',
        password='password123',
        name='FSD Student',
        role='student',
        track='FSD',
        payment_verified=True,
        enrollment_status='ENROLLED',
        privacy_accepted=True
    )
    print(f"✅ Created student: {user.email}")
else:
    print(f"✅ Found student: {user.email}")
    print(f"   Track: {user.track}")
    print(f"   Role: {user.role}")

# Check progress
progress_entries = StudentProgress.objects.filter(student=user, step=None)
print(f"\n📊 Progress entries: {progress_entries.count()}")

for p in progress_entries:
    print(f"   - Project {p.project.number}: {p.project.title}")
    print(f"     Approved: {p.is_approved}")
    print(f"     Started: {p.started_at}")

# Check if Project 1 exists
try:
    track = Track.objects.get(code='FSD')
    project1 = Project.objects.get(track=track, number=1)
    print(f"\n✅ Project 1 exists: {project1.title}")
    
    # Check if student has progress for Project 1
    progress, created = StudentProgress.objects.get_or_create(
        student=user,
        project=project1,
        step=None,
        defaults={'started_at': timezone.now()}
    )
    
    if created:
        print(f"✅ Created progress entry for Project 1")
    else:
        print(f"✅ Progress entry already exists for Project 1")
        
except Track.DoesNotExist:
    print("❌ FSD track not found - run setup_fsd_curriculum.py first")
except Project.DoesNotExist:
    print("❌ Project 1 not found - run setup_fsd_curriculum.py first")

print("\n" + "="*50)
print("Done! Try refreshing the dashboard now.")
