"""
Support Serializers
"""
from rest_framework import serializers
from .models import SupportTicket, TicketMessage
from accounts.serializers import UserSerializer


class TicketMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    
    class Meta:
        model = TicketMessage
        fields = [
            'id',
            'ticket',
            'sender',
            'sender_name',
            'sender_role',
            'message',
            'attachment_url',
            'is_internal',
            'created_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True, allow_null=True)
    project_title = serializers.CharField(source='project.title', read_only=True, allow_null=True)
    messages = TicketMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'ticket_number',
            'title',
            'description',
            'category',
            'priority',
            'status',
            'student',
            'student_name',
            'assigned_to',
            'assigned_to_name',
            'project',
            'project_title',
            'attachment_url',
            'discord_thread_id',
            'messages',
            'message_count',
            'created_at',
            'updated_at',
            'resolved_at',
            'closed_at'
        ]
        read_only_fields = [
            'id',
            'ticket_number',
            'student',
            'discord_thread_id',
            'created_at',
            'updated_at',
            'resolved_at',
            'closed_at'
        ]
    
    def get_message_count(self, obj):
        return obj.messages.count()


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = [
            'title',
            'description',
            'category',
            'priority',
            'project',
            'attachment_url'
        ]


class UpdateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = [
            'status',
            'priority',
            'assigned_to'
        ]
