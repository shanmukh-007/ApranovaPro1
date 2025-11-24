from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Track, Project, ProjectStep, Deliverable, StudentProgress, Submission
from .serializers import (
    TrackSerializer, ProjectSerializer, ProjectStepSerializer,
    DeliverableSerializer, StudentProgressSerializer, SubmissionSerializer
)


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing learning tracks
    """
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def my_progress(self, request, pk=None):
        """Get student's progress for this track"""
        track = self.get_object()
        progress = StudentProgress.objects.filter(
            student=request.user,
            project__track=track
        ).select_related('project', 'step')
        serializer = StudentProgressSerializer(progress, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing projects
    """
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        track_code = self.request.query_params.get('track', None)
        if track_code:
            queryset = queryset.filter(track__code=track_code)
        return queryset
    
    @action(detail=True, methods=['post'])
    def start_project(self, request, pk=None):
        """
        Start a project - creates GitHub repo from template
        """
        from .github_integration import create_repo_from_template
        
        project = self.get_object()
        student = request.user
        
        # Only students can start projects
        if student.role != 'student':
            return Response(
                {'error': 'Only students can start projects'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create repo
        result = create_repo_from_template(student, project)
        
        if not result['success']:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(result)


class StudentProgressViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing student progress
    """
    serializer_class = StudentProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StudentProgress.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_step_complete(self, request):
        """Mark a step as complete"""
        step_id = request.data.get('step_id')
        project_id = request.data.get('project_id')
        
        if not step_id or not project_id:
            return Response(
                {'error': 'step_id and project_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            step = ProjectStep.objects.get(id=step_id, project_id=project_id)
            project = step.project
        except ProjectStep.DoesNotExist:
            return Response(
                {'error': 'Step not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create or update progress
        progress, created = StudentProgress.objects.update_or_create(
            student=request.user,
            project=project,
            step=step,
            defaults={
                'is_completed': True,
                'completed_at': timezone.now()
            }
        )
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def mark_step_incomplete(self, request):
        """Mark a step as incomplete"""
        step_id = request.data.get('step_id')
        project_id = request.data.get('project_id')
        
        if not step_id or not project_id:
            return Response(
                {'error': 'step_id and project_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            progress = StudentProgress.objects.get(
                student=request.user,
                project_id=project_id,
                step_id=step_id
            )
            progress.is_completed = False
            progress.completed_at = None
            progress.save()
            
            serializer = self.get_serializer(progress)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentProgress.DoesNotExist:
            return Response(
                {'error': 'Progress not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing project submissions
    """
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'trainer':
            # Trainers can see submissions from their students
            return Submission.objects.filter(
                student__assigned_trainer=self.request.user
            ).select_related('student', 'deliverable', 'reviewed_by')
        else:
            # Students can only see their own submissions
            return Submission.objects.filter(
                student=self.request.user
            ).select_related('deliverable', 'reviewed_by')
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Trainer reviews a submission"""
        if request.user.role != 'trainer':
            return Response(
                {'error': 'Only trainers can review submissions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        submission = self.get_object()
        new_status = request.data.get('status')
        feedback = request.data.get('feedback', '')
        
        if new_status not in ['APPROVED', 'REJECTED']:
            return Response(
                {'error': 'Invalid status. Must be APPROVED or REJECTED'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.status = new_status
        submission.feedback = feedback
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)


# Sequential Project Flow Endpoints
from rest_framework.decorators import api_view, permission_classes
from submissions.models import ProjectSubmission

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_project(request):
    """Get current active project for student"""
    user = request.user
    
    if user.role != 'student':
        return Response({'error': 'Only students can access this'}, status=status.HTTP_403_FORBIDDEN)
    
    # Find current project (unlocked but not approved)
    current_progress = StudentProgress.objects.filter(
        student=user,
        step=None,  # Project-level progress
        is_approved=False
    ).select_related('project').order_by('project__number').first()
    
    if not current_progress:
        # All projects completed
        return Response({'current_project': None, 'all_completed': True})
    
    project = current_progress.project
    
    # Check if submitted
    submission = ProjectSubmission.objects.filter(
        student=user,
        project=project
    ).order_by('-submitted_at').first()
    
    # Get completed projects
    completed_projects = StudentProgress.objects.filter(
        student=user,
        step=None,
        is_approved=True
    ).select_related('project').order_by('project__number')
    
    completed_data = [{
        'id': p.project.id,
        'number': p.project.number,
        'title': p.project.title,
        'approved_at': p.approved_at,
    } for p in completed_projects]
    
    return Response({
        'project': {
            'id': project.id,
            'number': project.number,
            'title': project.title,
            'subtitle': project.subtitle,
            'description': project.description,
            'tech_stack': project.tech_stack,
            'estimated_hours': project.estimated_hours,
            'project_type': project.project_type,
        },
        'progress': {
            'is_submitted': bool(submission and submission.status == 'SUBMITTED'),
            'is_approved': current_progress.is_approved,
            'needs_revision': current_progress.needs_revision,
            'trainer_feedback': current_progress.trainer_feedback,
            'started_at': current_progress.started_at,
        },
        'completed_projects': completed_data,
        'total_projects': Project.objects.filter(track=user.track).count()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_project_submission(request, submission_id):
    """Trainer approves submission and unlocks next project"""
    user = request.user
    
    if user.role not in ['trainer', 'admin']:
        return Response({'error': 'Only trainers can approve'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        submission = ProjectSubmission.objects.get(id=submission_id)
    except ProjectSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    feedback = request.data.get('feedback', '')
    
    # Update submission
    submission.status = 'APPROVED'
    submission.reviewed_at = timezone.now()
    submission.reviewed_by = user
    submission.trainer_feedback = feedback
    submission.save()
    
    # Update progress
    progress = StudentProgress.objects.get(
        student=submission.student,
        project=submission.project,
        step=None
    )
    progress.is_approved = True
    progress.approved_at = timezone.now()
    progress.approved_by = user
    progress.trainer_feedback = feedback
    progress.needs_revision = False
    progress.completed_at = timezone.now()
    progress.is_completed = True
    progress.save()
    
    # Unlock next project
    next_project_number = submission.project.number + 1
    next_project = Project.objects.filter(
        track=submission.student.track,
        number=next_project_number
    ).first()
    
    if next_project:
        StudentProgress.objects.get_or_create(
            student=submission.student,
            project=next_project,
            step=None,
            defaults={'started_at': timezone.now()}
        )
        next_unlocked = True
    else:
        next_unlocked = False
    
    return Response({
        'message': 'Project approved successfully',
        'next_project_unlocked': next_unlocked,
        'next_project_number': next_project_number if next_unlocked else None
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_revision(request, submission_id):
    """Trainer requests revision on submission"""
    user = request.user
    
    if user.role not in ['trainer', 'admin']:
        return Response({'error': 'Only trainers can request revisions'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        submission = ProjectSubmission.objects.get(id=submission_id)
    except ProjectSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    feedback = request.data.get('feedback', 'Please revise your submission.')
    
    # Update submission
    submission.status = 'NEEDS_REVISION'
    submission.reviewed_at = timezone.now()
    submission.reviewed_by = user
    submission.trainer_feedback = feedback
    submission.save()
    
    # Update progress
    progress = StudentProgress.objects.get(
        student=submission.student,
        project=submission.project,
        step=None
    )
    progress.needs_revision = True
    progress.trainer_feedback = feedback
    progress.save()
    
    return Response({
        'message': 'Revision requested',
        'feedback': feedback
    })
