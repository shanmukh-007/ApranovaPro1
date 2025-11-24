"""
Fix trainer track assignments
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def fix_tracks():
    print("\n" + "="*60)
    print("FIXING TRAINER TRACKS")
    print("="*60 + "\n")
    
    updates = [
        ('trainerdp1@apranova.com', 'DP', 'TrainerDP1'),
        ('trainerdp2@apranova.com', 'DP', 'TrainerDP2'),
        ('trainerfsd1@apranova.com', 'FSD', 'TrainerFSD1'),
        ('trainerfsd2@apranova.com', 'FSD', 'TrainerFSD2'),
    ]
    
    for email, track, name in updates:
        try:
            trainer = User.objects.get(email=email)
            trainer.track = track
            trainer.name = name
            trainer.save()
            print(f"✅ Updated {email}")
            print(f"   Name: {name}")
            print(f"   Track: {track}")
            print()
        except User.DoesNotExist:
            print(f"❌ Trainer {email} not found")
            print()
    
    print("\n" + "="*60)
    print("ALL TRAINERS")
    print("="*60 + "\n")
    
    trainers = User.objects.filter(role='trainer').order_by('email')
    for trainer in trainers:
        print(f"👨‍🏫 {trainer.name} ({trainer.email})")
        print(f"   Track: {trainer.track or 'ALL'}")
        print()

if __name__ == '__main__':
    fix_tracks()
