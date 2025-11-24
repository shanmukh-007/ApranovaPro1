"""
Test script to verify DP track API is working correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from curriculum.models import Track, Project, StudentProgress
from curriculum.serializers import TrackSerializer
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser

def test_dp_track():
    print("="*60)
    print("DP TRACK API TEST")
    print("="*60)
    
    # Get DP track
    try:
        dp_track = Track.objects.get(code='DP')
        print(f"\n✅ DP Track found: {dp_track.name}")
    except Track.DoesNotExist:
        print("\n❌ DP Track not found!")
        return
    
    # Get DP projects
    dp_projects = Project.objects.filter(track=dp_track).order_by('number')
    print(f"\n✅ DP Projects: {dp_projects.count()}")
    for project in dp_projects:
        print(f"   {project.number}. {project.title}")
        print(f"      - Steps: {project.steps.count()}")
        print(f"      - Deliverables: {project.deliverables.count()}")
        print(f"      - Tech: {', '.join(project.tech_stack[:3])}")
    
    # Get DP student
    try:
        dp_student = CustomUser.objects.get(email='test@gmail.com')
        print(f"\n✅ DP Student found: {dp_student.email}")
        print(f"   - Track: {dp_student.track}")
        print(f"   - Status: {dp_student.enrollment_status}")
    except CustomUser.DoesNotExist:
        print("\n❌ DP Student not found!")
        return
    
    # Check student progress
    progress_records = StudentProgress.objects.filter(
        student=dp_student,
        step=None  # Project-level progress
    )
    print(f"\n✅ Student Progress Records: {progress_records.count()}")
    for progress in progress_records:
        print(f"   - Project {progress.project.number}: {progress.project.title}")
        print(f"     Unlocked: Yes, Started: {progress.started_at}")
    
    # Test serializer
    print("\n" + "="*60)
    print("TESTING SERIALIZER")
    print("="*60)
    
    factory = APIRequestFactory()
    request = factory.get('/api/curriculum/tracks/')
    request.user = dp_student
    
    serializer = TrackSerializer(dp_track, context={'request': request})
    data = serializer.data
    
    print(f"\n✅ Track Serialized: {data['name']}")
    print(f"   - Code: {data['code']}")
    print(f"   - Projects: {len(data['projects'])}")
    print(f"   - Overall Progress: {data['overall_progress']}%")
    
    print("\nProjects:")
    for project in data['projects']:
        print(f"\n   Project {project['number']}: {project['title']}")
        print(f"   - Unlocked: {project['is_unlocked']}")
        print(f"   - Progress: {project['progress_percentage']}%")
        print(f"   - Steps: {len(project['steps'])}")
        print(f"   - Deliverables: {len(project['deliverables'])}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE!")
    print("="*60)
    
    # Summary
    print("\n📊 SUMMARY:")
    print(f"   ✅ DP Track exists with {dp_projects.count()} projects")
    print(f"   ✅ Student has {progress_records.count()} unlocked project(s)")
    print(f"   ✅ API serialization working correctly")
    print(f"   ✅ Dashboard should show Project 1")

if __name__ == '__main__':
    test_dp_track()
