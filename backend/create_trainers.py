"""
Create trainer1 and trainer2 accounts
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_trainers():
    trainers_data = [
        {
            'email': 'trainerdp1@apranova.com',
            'username': 'trainerdp1',
            'name': 'TrainerDP1',
            'password': 'TrainerDP1@2024',
            'track': 'DP'
        },
        {
            'email': 'trainerdp2@apranova.com',
            'username': 'trainerdp2',
            'name': 'TrainerDP2',
            'password': 'TrainerDP2@2024',
            'track': 'DP'
        },
        {
            'email': 'trainerfsd1@apranova.com',
            'username': 'trainerfsd1',
            'name': 'TrainerFSD1',
            'password': 'TrainerFSD1@2024',
            'track': 'FSD'
        },
        {
            'email': 'trainerfsd2@apranova.com',
            'username': 'trainerfsd2',
            'name': 'TrainerFSD2',
            'password': 'TrainerFSD2@2024',
            'track': 'FSD'
        }
    ]
    
    for trainer_data in trainers_data:
        email = trainer_data['email']
        username = trainer_data['username']
        
        # Check if trainer already exists
        if User.objects.filter(email=email).exists():
            print(f"✅ Trainer {email} already exists")
            continue
        
        # Check if username exists and generate unique one
        if User.objects.filter(username=username).exists():
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
        
        # Create trainer
        trainer = User.objects.create_user(
            email=email,
            username=username,
            password=trainer_data['password'],
            name=trainer_data['name'],
            role='trainer',
            is_staff=True,
            privacy_accepted=True
        )
        
        print(f"✅ Created trainer: {email}")
        print(f"   Username: {username}")
        print(f"   Password: {trainer_data['password']}")
        print()
    
    # Show all trainers
    print("\n" + "="*60)
    print("ALL TRAINERS")
    print("="*60)
    
    trainers = User.objects.filter(role='trainer').order_by('email')
    for trainer in trainers:
        print(f"👨‍🏫 {trainer.name} ({trainer.email})")
        dp_count = User.objects.filter(assigned_trainer=trainer, track='DP').count()
        fsd_count = User.objects.filter(assigned_trainer=trainer, track='FSD').count()
        print(f"   DP: {dp_count}/20 students")
        print(f"   FSD: {fsd_count}/20 students")
        print()

if __name__ == '__main__':
    create_trainers()
