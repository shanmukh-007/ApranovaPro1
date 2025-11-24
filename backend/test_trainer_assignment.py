"""
Test automatic trainer assignment logic
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from utils.trainer_assignment import assign_trainer_to_student, get_trainer_capacity_report

User = get_user_model()

def test_assignment():
    print("\n" + "="*60)
    print("TESTING AUTOMATIC TRAINER ASSIGNMENT")
    print("="*60 + "\n")
    
    # Check if trainers exist
    trainers = User.objects.filter(role='trainer').order_by('email')
    
    if not trainers.exists():
        print("❌ No trainers found. Please create trainers first:")
        print("   - trainer1@apranova.com")
        print("   - trainer2@apranova.com")
        return
    
    print(f"✅ Found {trainers.count()} trainer(s):")
    for trainer in trainers:
        print(f"   - {trainer.email}")
    print()
    
    # Show current capacity
    print("Current Capacity:")
    report = get_trainer_capacity_report()
    for trainer_email, data in report.items():
        print(f"   {trainer_email}: DP={data['DP']['count']}/20, FSD={data['FSD']['count']}/20")
    print()
    
    # Test with existing unassigned students
    unassigned_students = User.objects.filter(
        role='student',
        assigned_trainer__isnull=True
    ).order_by('created_at')
    
    if unassigned_students.exists():
        print(f"Found {unassigned_students.count()} unassigned student(s)")
        print("\nAssigning trainers to unassigned students...\n")
        
        for student in unassigned_students[:5]:  # Test with first 5
            print(f"Student: {student.email} (Track: {student.track})")
            
            if not student.track:
                print("   ⚠️  No track assigned, skipping")
                continue
            
            trainer = assign_trainer_to_student(student)
            
            if trainer:
                print(f"   ✅ Assigned to: {trainer.email}")
            else:
                print(f"   ❌ Failed to assign trainer")
            print()
    else:
        print("No unassigned students found")
    
    # Show updated capacity
    print("\n" + "="*60)
    print("UPDATED CAPACITY")
    print("="*60 + "\n")
    
    report = get_trainer_capacity_report()
    for trainer_email, data in report.items():
        print(f"👨‍🏫 {data['name']} ({trainer_email})")
        print(f"   DP:  {data['DP']['count']}/20 ({data['DP']['available']} available)")
        print(f"   FSD: {data['FSD']['count']}/20 ({data['FSD']['available']} available)")
        print()

if __name__ == '__main__':
    test_assignment()
