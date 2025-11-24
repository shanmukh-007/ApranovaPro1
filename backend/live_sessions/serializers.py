from rest_framework import serializers
from .models import Session, SessionAttendance
from accounts.serializers import UserSerializer


class SessionSerializer(serializers.ModelSerializer):
    trainer = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    is_upcoming = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Session
        fields = [
            'id', 'title', 'description', 'trainer', 'students', 'student_ids',
            'session_type', 'status', 'scheduled_at', 'duration_minutes',
            'ended_at', 'meet_link', 'google_event_id', 'project',
            'agenda', 'notes', 'recording_url', 'created_at', 'updated_at',
            'is_upcoming', 'is_past', 'end_time', 'student_count'
        ]
        read_only_fields = ['trainer', 'google_event_id', 'created_at', 'updated_at']
    
    def get_student_count(self, obj):
        return obj.students.count()
    
    def create(self, validated_data):
        student_ids = validated_data.pop('student_ids', [])
        session = Session.objects.create(**validated_data)
        
        if student_ids:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            students = User.objects.filter(id__in=student_ids, role='student')
            session.students.set(students)
        
        return session
    
    def update(self, instance, validated_data):
        student_ids = validated_data.pop('student_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if student_ids is not None:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            students = User.objects.filter(id__in=student_ids, role='student')
            instance.students.set(students)
        
        return instance


class SessionAttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    session = SessionSerializer(read_only=True)
    duration_minutes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = SessionAttendance
        fields = [
            'id', 'session', 'student', 'joined_at', 'left_at',
            'attended', 'student_rating', 'student_feedback',
            'duration_minutes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SessionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing sessions"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    student_count = serializers.SerializerMethodField()
    is_upcoming = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Session
        fields = [
            'id', 'title', 'trainer_name', 'session_type', 'status',
            'scheduled_at', 'duration_minutes', 'meet_link',
            'student_count', 'is_upcoming'
        ]
    
    def get_student_count(self, obj):
        return obj.students.count()
