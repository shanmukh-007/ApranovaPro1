from django.contrib import admin
from .models import Session, SessionAttendance


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'trainer', 'session_type', 'status',
        'scheduled_at', 'duration_minutes', 'student_count'
    ]
    list_filter = ['status', 'session_type', 'scheduled_at', 'trainer']
    search_fields = ['title', 'description', 'trainer__name', 'trainer__email']
    filter_horizontal = ['students']
    readonly_fields = ['created_at', 'updated_at', 'google_event_id']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'trainer', 'session_type', 'status')
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'duration_minutes', 'ended_at')
        }),
        ('Participants', {
            'fields': ('students',)
        }),
        ('Google Meet', {
            'fields': ('meet_link', 'google_event_id')
        }),
        ('Content', {
            'fields': ('project', 'agenda', 'notes', 'recording_url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'


@admin.register(SessionAttendance)
class SessionAttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'session', 'attended', 'joined_at',
        'duration_minutes', 'student_rating'
    ]
    list_filter = ['attended', 'student_rating', 'session__scheduled_at']
    search_fields = ['student__name', 'student__email', 'session__title']
    readonly_fields = ['created_at', 'updated_at', 'duration_minutes']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('session', 'student')
        }),
        ('Attendance', {
            'fields': ('attended', 'joined_at', 'left_at', 'duration_minutes')
        }),
        ('Feedback', {
            'fields': ('student_rating', 'student_feedback')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
