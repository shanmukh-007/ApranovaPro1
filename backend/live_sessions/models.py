from django.db import models
from django.conf import settings
from django.utils import timezone


class Session(models.Model):
    """Live class sessions between trainers and students"""
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    SESSION_TYPE_CHOICES = [
        ('ONE_ON_ONE', 'One-on-One'),
        ('GROUP', 'Group Session'),
        ('WORKSHOP', 'Workshop'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trainer_sessions',
        limit_choices_to={'role': 'trainer'}
    )
    
    # Participants
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student_sessions',
        limit_choices_to={'role': 'student'}
    )
    
    # Session Details
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default='ONE_ON_ONE'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )
    
    # Scheduling
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # Google Meet Integration
    meet_link = models.URLField(blank=True)
    google_event_id = models.CharField(max_length=255, blank=True)
    
    # Related Content
    project = models.ForeignKey(
        'curriculum.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    
    # Notes and Recording
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    recording_url = models.URLField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['-scheduled_at']),
            models.Index(fields=['trainer', '-scheduled_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_upcoming(self):
        """Check if session is upcoming"""
        return self.status == 'SCHEDULED' and self.scheduled_at > timezone.now()
    
    @property
    def is_past(self):
        """Check if session is in the past"""
        return self.scheduled_at < timezone.now()
    
    @property
    def end_time(self):
        """Calculate session end time"""
        from datetime import timedelta
        return self.scheduled_at + timedelta(minutes=self.duration_minutes)


class SessionAttendance(models.Model):
    """Track student attendance for sessions"""
    
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='session_attendance'
    )
    
    # Attendance
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    attended = models.BooleanField(default=False)
    
    # Feedback
    student_rating = models.IntegerField(null=True, blank=True)  # 1-5
    student_feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.session.title}"
    
    @property
    def duration_minutes(self):
        """Calculate attendance duration"""
        if self.joined_at and self.left_at:
            delta = self.left_at - self.joined_at
            return int(delta.total_seconds() / 60)
        return 0
