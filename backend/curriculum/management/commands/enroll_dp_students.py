"""
Django management command to enroll all DP students
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Enroll all DP students and verify their payment'

    def handle(self, *args, **options):
        self.stdout.write('Enrolling DP students...')
        
        # Get all DP students
        dp_students = CustomUser.objects.filter(track='DP')
        
        if not dp_students.exists():
            self.stdout.write(self.style.WARNING('⚠️  No DP students found'))
            return
        
        enrolled_count = 0
        for student in dp_students:
            # Update enrollment status
            if student.enrollment_status != 'ENROLLED':
                student.enrollment_status = 'ENROLLED'
                student.enrolled_at = timezone.now()
                enrolled_count += 1
            
            # Verify payment
            if not student.payment_verified:
                student.payment_verified = True
            
            # Accept privacy if not already
            if not student.privacy_accepted:
                student.privacy_accepted = True
                student.privacy_accepted_at = timezone.now()
            
            student.save()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Enrolled: {student.email}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Enrolled {enrolled_count} DP students'))
        self.stdout.write('='*50)
