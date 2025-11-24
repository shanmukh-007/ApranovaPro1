"""
Check trainer capacity and student assignments
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from utils.trainer_assignment import get_trainer_capacity_report
from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    print("\n" + "="*60)
    print("TRAINER CAPACITY REPORT")
    print("="*60 + "\n")
    
    report = get_trainer_capacity_report()
    
    if not report:
        print("❌ No trainers found in the system")
        return
    
    for trainer_email, data in report.items():
        if 'track' in data and data['track'] != 'ALL':
            # Track-specific trainer
            print(f"👨‍🏫 {data['name']} ({trainer_email}) - {data['track']} Track")
            print(f"   Students: {data['count']}/20 ({data['available']} slots available)")
        else:
            # General trainer (legacy)
            print(f"👨‍🏫 {data['name']} ({trainer_email}) - All Tracks")
            print(f"   DP Track:  {data['DP']['count']}/20 students ({data['DP']['available']} slots available)")
            print(f"   FSD Track: {data['FSD']['count']}/20 students ({data['FSD']['available']} slots available)")
            print(f"   Total:     {data['total']} students")
        print()
    
    # Show recent student assignments
    print("\n" + "="*60)
    print("RECENT STUDENT ASSIGNMENTS")
    print("="*60 + "\n")
    
    recent_students = User.objects.filter(
        role='student',
        assigned_trainer__isnull=False
    ).select_related('assigned_trainer').order_by('-created_at')[:10]
    
    if recent_students:
        for student in recent_students:
            print(f"📚 {student.name or student.username} ({student.email})")
            print(f"   Track: {student.track}")
            print(f"   Trainer: {student.assigned_trainer.name} ({student.assigned_trainer.email})")
            print(f"   Enrolled: {student.enrolled_at.strftime('%Y-%m-%d %H:%M') if student.enrolled_at else 'N/A'}")
            print()
    else:
        print("No students with assigned trainers found")
    
    # Show unassigned students
    unassigned = User.objects.filter(
        role='student',
        assigned_trainer__isnull=True
    ).count()
    
    if unassigned > 0:
        print(f"\n⚠️  {unassigned} students without assigned trainers")

if __name__ == '__main__':
    main()
