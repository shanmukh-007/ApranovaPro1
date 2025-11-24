"""
Test the submissions endpoint
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from submissions.models import ProjectSubmission
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_endpoint():
    print("\n" + "="*60)
    print("TESTING SUBMISSIONS ENDPOINT")
    print("="*60 + "\n")
    
    # Get a trainer
    trainer = User.objects.filter(role='trainer').first()
    
    if not trainer:
        print("❌ No trainer found")
        return
    
    print(f"✅ Testing with trainer: {trainer.email}")
    print(f"   Role: {trainer.role}")
    print()
    
    # Check assigned students
    students = User.objects.filter(assigned_trainer=trainer, role='student')
    print(f"📚 Assigned students: {students.count()}")
    for student in students[:5]:
        print(f"   - {student.email} (Track: {student.track})")
    print()
    
    # Check submissions
    student_ids = students.values_list('id', flat=True)
    submissions = ProjectSubmission.objects.filter(student_id__in=student_ids)
    print(f"📝 Submissions from assigned students: {submissions.count()}")
    print()
    
    # Test API endpoint
    print("Testing API endpoint...")
    client = APIClient()
    
    # Get JWT token
    refresh = RefreshToken.for_user(trainer)
    token = str(refresh.access_token)
    
    # Make request
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    try:
        response = client.get('/api/submissions/')
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {len(data)} submissions returned")
            print(f"   Data: {data}")
        else:
            print(f"❌ Error Response: {response.content[:500]}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_endpoint()
