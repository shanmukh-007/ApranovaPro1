"""
Django management command to unlock Project 1 for DP students
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from curriculum.models import Project, StudentProgress


class Command(BaseCommand):
    help = 'Unlock Project 1 for all enrolled DP students'

    def handle(self, *args, **options):
        self.stdout.write('Unlocking DP Project 1 for enrolled students...')
        
        # Get DP Project 1
        try:
            dp_project1 = Project.objects.get(track__code='DP', number=1)
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ DP Project 1 not found. Run setup_dp_track first.'))
            return
        
        # Get all enrolled DP students
        dp_students = CustomUser.objects.filter(
            track='DP',
            enrollment_status='ENROLLED'
        )
        
        if not dp_students.exists():
            self.stdout.write(self.style.WARNING('⚠️  No enrolled DP students found'))
            return
        
        unlocked_count = 0
        for student in dp_students:
            # Create or get progress for Project 1
            progress, created = StudentProgress.objects.get_or_create(
                student=student,
                project=dp_project1,
                step=None,  # Project-level progress
                defaults={
                    'started_at': timezone.now(),
                    'is_completed': False,
                    'is_approved': False
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Unlocked Project 1 for {student.email}'))
                unlocked_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'ℹ️  Project 1 already unlocked for {student.email}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Unlocked Project 1 for {unlocked_count} students'))
        self.stdout.write('='*50)
