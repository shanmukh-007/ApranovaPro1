from rest_framework import serializers
from .models import Track, Project, ProjectStep, Deliverable, StudentProgress, Submission


class DeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverable
        fields = ['id', 'title', 'description', 'deliverable_type', 'is_required', 'order']


class ProjectStepSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectStep
        fields = ['id', 'step_number', 'title', 'description', 'estimated_minutes', 
                  'resources', 'order', 'is_completed']
    
    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return StudentProgress.objects.filter(
                student=request.user,
                step=obj,
                is_completed=True
            ).exists()
        return False


class ProjectSerializer(serializers.ModelSerializer):
    steps = ProjectStepSerializer(many=True, read_only=True)
    deliverables = DeliverableSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()
    github_repo_url = serializers.SerializerMethodField()
    github_repo_name = serializers.SerializerMethodField()
    github_repo_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'number', 'title', 'subtitle', 'description', 'project_type',
                  'tech_stack', 'estimated_hours', 'steps', 'deliverables', 
                  'progress_percentage', 'is_unlocked', 'github_repo_url', 
                  'github_repo_name', 'github_repo_created']
    
    def get_progress_percentage(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            total_steps = obj.steps.count()
            if total_steps == 0:
                return 0
            completed_steps = StudentProgress.objects.filter(
                student=request.user,
                project=obj,
                step__isnull=False,
                is_completed=True
            ).count()
            return int((completed_steps / total_steps) * 100)
        return 0
    
    def get_is_unlocked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if student has progress record for this project (means it's unlocked)
            has_progress = StudentProgress.objects.filter(
                student=request.user,
                project=obj,
                step=None  # Project-level progress
            ).exists()
            
            if has_progress:
                return True
            
            # For Project 1, auto-unlock for all students (regardless of payment status)
            if obj.number == 1:
                # Auto-create progress for all authenticated students
                from django.utils import timezone
                StudentProgress.objects.get_or_create(
                    student=request.user,
                    project=obj,
                    step=None,
                    defaults={'started_at': timezone.now()}
                )
                return True
            
            # Check if previous project is approved
            previous_project = Project.objects.filter(
                track=obj.track,
                number=obj.number - 1
            ).first()
            
            if previous_project:
                previous_progress = StudentProgress.objects.filter(
                    student=request.user,
                    project=previous_project,
                    step=None,
                    is_approved=True
                ).exists()
                return previous_progress
        return False
    
    def get_github_repo_url(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = StudentProgress.objects.filter(
                student=request.user,
                project=obj,
                github_repo_created=True
            ).first()
            return progress.github_repo_url if progress else None
        return None
    
    def get_github_repo_name(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = StudentProgress.objects.filter(
                student=request.user,
                project=obj,
                github_repo_created=True
            ).first()
            return progress.github_repo_name if progress else None
        return None
    
    def get_github_repo_created(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return StudentProgress.objects.filter(
                student=request.user,
                project=obj,
                github_repo_created=True
            ).exists()
        return False


class TrackSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    overall_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Track
        fields = ['id', 'code', 'name', 'description', 'icon', 'duration_weeks', 
                  'projects', 'overall_progress']
    
    def get_overall_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            total_steps = ProjectStep.objects.filter(project__track=obj).count()
            if total_steps == 0:
                return 0
            completed_steps = StudentProgress.objects.filter(
                student=request.user,
                project__track=obj,
                step__isnull=False,
                is_completed=True
            ).count()
            return int((completed_steps / total_steps) * 100)
        return 0


class StudentProgressSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    step_title = serializers.CharField(source='step.title', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = ['id', 'project', 'project_title', 'step', 'step_title', 
                  'is_completed', 'completed_at', 'notes', 'created_at',
                  'github_repo_url', 'github_repo_name', 'github_repo_created',
                  'github_pr_url', 'github_pr_number', 'github_pr_merged', 'started_at']
        read_only_fields = ['completed_at', 'created_at', 'github_repo_created', 
                           'github_pr_merged', 'started_at']


class SubmissionSerializer(serializers.ModelSerializer):
    deliverable_title = serializers.SerializerMethodField()
    deliverable_type = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()
    reviewer_name = serializers.SerializerMethodField()
    url = serializers.CharField(source='submission_url', read_only=True)
    text_content = serializers.CharField(source='submission_text', read_only=True)
    trainer_feedback = serializers.CharField(source='feedback', read_only=True)
    grade = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Submission
        fields = ['id', 'deliverable', 'deliverable_title', 'deliverable_type', 'project_title', 
                  'project_id', 'submission_url', 'url', 'submission_text', 'text_content', 
                  'submission_file', 'github_pr_url', 'status', 'feedback', 'trainer_feedback',
                  'student_name', 'student_email', 'reviewer_name', 'grade',
                  'reviewed_at', 'submitted_at', 'updated_at']
        read_only_fields = ['student', 'reviewed_by', 'reviewed_at', 'submitted_at', 'updated_at']
    
    def get_deliverable_title(self, obj):
        return obj.deliverable.title if obj.deliverable else 'N/A'
    
    def get_deliverable_type(self, obj):
        return obj.deliverable.deliverable_type if obj.deliverable else 'N/A'
    
    def get_project_title(self, obj):
        if obj.deliverable and obj.deliverable.project:
            return obj.deliverable.project.title
        return 'N/A'
    
    def get_project_id(self, obj):
        if obj.deliverable and obj.deliverable.project:
            return obj.deliverable.project.id
        return None
    
    def get_student_name(self, obj):
        return obj.student.name or obj.student.username if obj.student else 'Unknown'
    
    def get_student_email(self, obj):
        return obj.student.email if obj.student else 'N/A'
    
    def get_reviewer_name(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.name or obj.reviewed_by.username
        return None
