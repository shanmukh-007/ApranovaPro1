"""
Test complete enrollment flow with automatic trainer assignment
Simulates 45 DP students and 45 FSD students enrolling
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from utils.trainer_assignment import assign_trainer_to_student, get_trainer_capacity_report

User = get_user_model()

def simulate_enrollments():
    print("\n" + "="*60)
    print("SIMULATING ENROLLMENT FLOW")
    print("="*60 + "\n")
    
    # Create test students
    test_students = []
    
    # Create 25 DP students
    print("Creating 25 DP students...")
    for i in range(1, 26):
        email = f"dp_student_{i}@test.com"
        
        # Skip if exists
        if User.objects.filter(email=email).exists():
            student = User.objects.get(email=email)
            test_students.append(student)
            continue
        
        student = User.objects.create_user(
            email=email,
            username=f"dp_student_{i}",
            password="Test@123",
            name=f"DP Student {i}",
            role='student',
            track='DP',
            enrollment_status='ENROLLED',
            payment_verified=True,
            enrolled_at=timezone.now(),
            privacy_accepted=True
        )
        test_students.append(student)
    
    # Create 25 FSD students
    print("Creating 25 FSD students...")
    for i in range(1, 26):
        email = f"fsd_student_{i}@test.com"
        
        # Skip if exists
        if User.objects.filter(email=email).exists():
            student = User.objects.get(email=email)
            test_students.append(student)
            continue
        
        student = User.objects.create_user(
            email=email,
            username=f"fsd_student_{i}",
            password="Test@123",
            name=f"FSD Student {i}",
            role='student',
            track='FSD',
            enrollment_status='ENROLLED',
            payment_verified=True,
            enrolled_at=timezone.now(),
            privacy_accepted=True
        )
        test_students.append(student)
    
    print(f"\n✅ Created/Found {len(test_students)} test students\n")
    
    # Assign trainers
    print("Assigning trainers automatically...\n")
    
    for student in test_students:
        if not student.assigned_trainer:
            trainer = assign_trainer_to_student(student)
            if trainer:
                print(f"✅ {student.email} ({student.track}) → {trainer.email}")
    
    # Show final capacity report
    print("\n" + "="*60)
    print("FINAL CAPACITY REPORT")
    print("="*60 + "\n")
    
    report = get_trainer_capacity_report()
    
    for trainer_email, data in report.items():
        print(f"👨‍🏫 {data['name']} ({trainer_email})")
        print(f"   DP Track:  {data['DP']['count']}/20 students")
        print(f"   FSD Track: {data['FSD']['count']}/20 students")
        print(f"   Total:     {data['total']} students")
        print()
    
    # Verify distribution
    print("\n" + "="*60)
    print("DISTRIBUTION VERIFICATION")
    print("="*60 + "\n")
    
    trainer1 = User.objects.filter(email='trainer1@apranova.com').first()
    trainer2 = User.objects.filter(email='trainer2@apranova.com').first()
    
    if trainer1:
        dp1 = User.objects.filter(assigned_trainer=trainer1, track='DP').count()
        fsd1 = User.objects.filter(assigned_trainer=trainer1, track='FSD').count()
        print(f"✅ Trainer1: {dp1} DP + {fsd1} FSD = {dp1 + fsd1} total")
        
        if dp1 <= 20 and fsd1 <= 20:
            print("   ✅ Within capacity limits")
        else:
            print("   ⚠️  Over capacity!")
    
    if trainer2:
        dp2 = User.objects.filter(assigned_trainer=trainer2, track='DP').count()
        fsd2 = User.objects.filter(assigned_trainer=trainer2, track='FSD').count()
        print(f"✅ Trainer2: {dp2} DP + {fsd2} FSD = {dp2 + fsd2} total")
        
        if dp2 <= 20 and fsd2 <= 20:
            print("   ✅ Within capacity limits")
        else:
            print("   ⚠️  Over capacity!")
    
    print("\n" + "="*60)
    print("Expected Distribution:")
    print("  - First 20 DP students → Trainer1")
    print("  - Next 5 DP students → Trainer2")
    print("  - First 20 FSD students → Trainer1")
    print("  - Next 5 FSD students → Trainer2")
    print("="*60 + "\n")

if __name__ == '__main__':
    simulate_enrollments()
