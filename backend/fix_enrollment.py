#!/usr/bin/env python
"""
Fix enrollment for user after payment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from curriculum.models import Track, Project, StudentProgress

User = get_user_model()

def fix_enrollment(email):
    """Fix enrollment for a user"""
    try:
        user = User.objects.get(email=email)
        print(f"\n{'='*60}")
        print(f"User: {user.username} ({user.email})")
        print(f"{'='*60}")
        
        # Check current status
        print(f"\nCurrent Status:")
        print(f"  Role: {user.role}")
        print(f"  Track: {user.track}")
        print(f"  Enrollment Status: {user.enrollment_status}")
        print(f"  Payment Verified: {user.payment_verified}")
        print(f"  Enrolled At: {user.enrolled_at}")
        
        # Fix enrollment
        print(f"\nFixing enrollment...")
        user.payment_verified = True
        user.enrollment_status = 'ENROLLED'
        if not user.enrolled_at:
            user.enrolled_at = timezone.now()
        user.save()
        print(f"✅ User enrollment fixed")
        
        # Check if track exists
        if not user.track:
            print(f"\n❌ No track assigned to user")
            return
        
        # Get track
        try:
            track = Track.objects.get(code=user.track)
            print(f"\n✅ Track found: {track.name}")
        except Track.DoesNotExist:
            print(f"\n❌ Track {user.track} not found in database")
            return
        
        # Get first project
        first_project = track.projects.filter(number=1).first()
        if not first_project:
            print(f"\n❌ No Project 1 found for track {user.track}")
            return
        
        print(f"\n✅ First project: {first_project.title}")
        
        # Check if progress exists
        progress = StudentProgress.objects.filter(
            student=user,
            project=first_project,
            step=None
        ).first()
        
        if progress:
            print(f"\n✅ Progress already exists for Project 1")
        else:
            print(f"\n📝 Creating progress for Project 1...")
            # Create progress entry for first project (unlocks it)
            progress = StudentProgress.objects.create(
                student=user,
                project=first_project,
                step=None,
                started_at=timezone.now()
            )
            print(f"✅ Project 1 unlocked")
        
        # Create progress entries for all steps
        steps = first_project.steps.all()
        print(f"\n📝 Creating progress for {steps.count()} steps...")
        
        for step in steps:
            step_progress, created = StudentProgress.objects.get_or_create(
                student=user,
                project=first_project,
                step=step
            )
            if created:
                print(f"  ✅ Created progress for: {step.title}")
        
        print(f"\n{'='*60}")
        print(f"✅ Enrollment fixed successfully!")
        print(f"{'='*60}")
        print(f"\nUser should now:")
        print(f"  - See payment verified")
        print(f"  - Have Project 1 unlocked")
        print(f"  - Be able to access all features")
        
    except User.DoesNotExist:
        print(f"\n❌ User with email {email} not found")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Fix for apranova123@gmail.com
    fix_enrollment('apranova123@gmail.com')
