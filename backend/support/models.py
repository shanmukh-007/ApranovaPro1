"""
Support Ticket System Models
"""
from django.db import models
from django.conf import settings


class SupportTicket(models.Model):
    """
    Support tickets for student doubts and issues
    """
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('WAITING_STUDENT', 'Waiting for Student'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('TECHNICAL', 'Technical Issue'),
        ('PROJECT', 'Project Help'),
        ('CONCEPT', 'Concept Doubt'),
        ('SUBMISSION', 'Submission Issue'),
        ('WORKSPACE', 'Workspace Issue'),
        ('PAYMENT', 'Payment Issue'),
        ('OTHER', 'Other'),
    ]
    
    # Ticket Info
    ticket_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    # Relationships
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_tickets'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        help_text="Trainer or admin assigned to this ticket"
    )
    
    # Related Project (optional)
    project = models.ForeignKey(
        'curriculum.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='support_tickets'
    )
    
    # Attachments
    attachment_url = models.URLField(blank=True, help_text="Screenshot or file URL")
    
    # Discord Integration
    discord_thread_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Discord thread ID for this ticket"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['student', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]
    
    def __str__(self):
        return f"{self.ticket_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Generate ticket number: TKT-YYYYMMDD-XXXX
            from django.utils import timezone
            import random
            date_str = timezone.now().strftime('%Y%m%d')
            random_num = random.randint(1000, 9999)
            self.ticket_number = f"TKT-{date_str}-{random_num}"
        super().save(*args, **kwargs)


class TicketMessage(models.Model):
    """
    Messages/replies in a support ticket
    """
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )
    message = models.TextField()
    attachment_url = models.URLField(blank=True)
    
    # Discord Integration
    discord_message_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Discord message ID"
    )
    
    is_internal = models.BooleanField(
        default=False,
        help_text="Internal note (not visible to student)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message on {self.ticket.ticket_number} by {self.sender.name}"
