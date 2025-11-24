from rest_framework import serializers
from .models import ProjectSubmission


class ProjectSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()
    reviewer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectSubmission
        fields = [
            'id',
            'student',
            'student_name',
            'student_email',
            'project_id',
            'deliverable_id',
            'deliverable_type',
            'url',
            'file_path',
            'text_content',
            'status',
            'submitted_at',
            'reviewed_at',
            'reviewed_by',
            'reviewer_name',
            'trainer_feedback',
            'grade',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['student', 'submitted_at', 'reviewed_at', 'reviewed_by']
    
    def get_student_name(self, obj):
        if obj.student:
            return obj.student.name or obj.student.username
        return 'Unknown'
    
    def get_student_email(self, obj):
        return obj.student.email if obj.student else 'N/A'
    
    def get_reviewer_name(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.name or obj.reviewed_by.username
        return None


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSubmission
        fields = [
            'project_id',
            'deliverable_id',
            'deliverable_type',
            'url',
            'file_path',
            'text_content',
        ]
    
    def validate(self, data):
        deliverable_type = data.get('deliverable_type')
        
        # Validate based on type
        if deliverable_type in ['LINK', 'GITHUB']:
            if not data.get('url'):
                raise serializers.ValidationError("URL is required for this deliverable type")
        elif deliverable_type == 'FILE':
            if not data.get('file_path'):
                raise serializers.ValidationError("File is required for this deliverable type")
        elif deliverable_type == 'TEXT':
            if not data.get('text_content'):
                raise serializers.ValidationError("Text content is required for this deliverable type")
        
        return data
