"""
Support Admin
"""
from django.contrib import admin
from .models import SupportTicket, TicketMessage


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ['sender', 'created_at']
    fields = ['sender', 'message', 'attachment_url', 'is_internal', 'created_at']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number',
        'title',
        'student',
        'category',
        'priority',
        'status',
        'assigned_to',
        'created_at'
    ]
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_number', 'title', 'description', 'student__name', 'student__email']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at', 'resolved_at', 'closed_at']
    inlines = [TicketMessageInline]
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_number', 'title', 'description', 'category', 'priority', 'status')
        }),
        ('Assignment', {
            'fields': ('student', 'assigned_to', 'project')
        }),
        ('Attachments', {
            'fields': ('attachment_url',)
        }),
        ('Discord Integration', {
            'fields': ('discord_thread_id',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at', 'closed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'message_preview', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['ticket__ticket_number', 'message', 'sender__name']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
