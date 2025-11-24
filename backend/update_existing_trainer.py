"""
Update existing trainer to be track-specific
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def update_trainer():
    print("\n" + "="*60)
    print("UPDATING EXISTING TRAINER")
    print("="*60 + "\n")
    
    # Update trainer@apranova.com to be trainerdp1
    try:
        trainer = User.objects.get(email='trainer@apranova.com')
        
        print(f"Found trainer: {trainer.email}")
        print(f"Current name: {trainer.name}")
        print(f"Current track: {trainer.track or 'None'}")
        print()
        
        # Update to DP trainer
        trainer.track = 'DP'
        trainer.name = 'TrainerDP1'
        trainer.save()
        
        print("✅ Updated trainer:")
        print(f"   Email: {trainer.email}")
        print(f"   Name: {trainer.name}")
        print(f"   Track: {trainer.track}")
        print(f"   Password: trainer123 (unchanged)")
        print()
        
        # Show current students
        students = User.objects.filter(assigned_trainer=trainer, role='student')
        print(f"   Currently has {students.count()} assigned students")
        
        for student in students:
            print(f"   - {student.email} (Track: {student.track})")
        
    except User.DoesNotExist:
        print("❌ Trainer trainer@apranova.com not found")
        return
    
    print("\n" + "="*60)
    print("UPDATE COMPLETE")
    print("="*60)
    print("\nTrainer credentials:")
    print("Email: trainer@apranova.com")
    print("Password: trainer123")
    print("Track: DP")
    print("Name: TrainerDP1")

if __name__ == '__main__':
    update_trainer()
