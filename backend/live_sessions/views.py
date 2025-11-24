from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .models import Session, SessionAttendance
from .serializers import (
    SessionSerializer,
    SessionListSerializer,
    SessionAttendanceSerializer
)
from .google_meet import GoogleMeetService
import logging

logger = logging.getLogger(__name__)


class SessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing live class sessions
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SessionListSerializer
        return SessionSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'trainer':
            # Trainers see their own sessions
            return Session.objects.filter(trainer=user)
        elif user.role == 'student':
            # Students see sessions they're enrolled in
            return Session.objects.filter(students=user)
        else:
            # Admins see all sessions
            return Session.objects.all()
    
    def perform_create(self, serializer):
        """Create session and optionally generate Google Meet link"""
        session = serializer.save(trainer=self.request.user)
        
        # Generate Google Meet link if requested
        if self.request.data.get('create_meet_link'):
            try:
                meet_link = GoogleMeetService.create_meet_link(session)
                session.meet_link = meet_link
                session.save()
            except Exception as e:
                logger.error(f"Failed to create Google Meet link: {str(e)}")
        
        # Send notifications to students
        self._send_session_notifications(session, 'created')
    
    def perform_update(self, serializer):
        """Update session and notify students of changes"""
        session = serializer.save()
        self._send_session_notifications(session, 'updated')
    
    @action(detail=True, methods=['post'])
    def generate_meet_link(self, request, pk=None):
        """Generate Google Meet link for session"""
        session = self.get_object()
        
        try:
            meet_link = GoogleMeetService.create_meet_link(session)
            session.meet_link = meet_link
            session.save()
            
            return Response({
                'meet_link': meet_link,
                'message': 'Google Meet link generated successfully'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def start_session(self, request, pk=None):
        """Mark session as in progress"""
        session = self.get_object()
        
        if session.status != 'SCHEDULED':
            return Response(
                {'error': 'Session is not scheduled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.status = 'IN_PROGRESS'
        session.save()
        
        return Response({
            'message': 'Session started',
            'meet_link': session.meet_link
        })
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """Mark session as completed"""
        session = self.get_object()
        
        if session.status != 'IN_PROGRESS':
            return Response(
                {'error': 'Session is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.status = 'COMPLETED'
        session.ended_at = timezone.now()
        session.notes = request.data.get('notes', session.notes)
        session.save()
        
        return Response({'message': 'Session ended successfully'})
    
    @action(detail=True, methods=['post'])
    def cancel_session(self, request, pk=None):
        """Cancel a scheduled session"""
        session = self.get_object()
        
        if session.status not in ['SCHEDULED', 'IN_PROGRESS']:
            return Response(
                {'error': 'Cannot cancel this session'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.status = 'CANCELLED'
        session.save()
        
        # Notify students
        self._send_session_notifications(session, 'cancelled')
        
        return Response({'message': 'Session cancelled'})
    
    @action(detail=True, methods=['post'])
    def mark_attendance(self, request, pk=None):
        """Mark student attendance (for trainers)"""
        session = self.get_object()
        student_id = request.data.get('student_id')
        attended = request.data.get('attended', True)
        
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            student = User.objects.get(id=student_id, role='student')
            
            attendance, created = SessionAttendance.objects.get_or_create(
                session=session,
                student=student
            )
            attendance.attended = attended
            if attended and not attendance.joined_at:
                attendance.joined_at = timezone.now()
            attendance.save()
            
            return Response({
                'message': 'Attendance marked',
                'attendance': SessionAttendanceSerializer(attendance).data
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def join_session(self, request, pk=None):
        """Student joins session"""
        session = self.get_object()
        student = request.user
        
        if student.role != 'student':
            return Response(
                {'error': 'Only students can join sessions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if student not in session.students.all():
            return Response(
                {'error': 'You are not enrolled in this session'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mark attendance
        attendance, created = SessionAttendance.objects.get_or_create(
            session=session,
            student=student
        )
        attendance.joined_at = timezone.now()
        attendance.attended = True
        attendance.save()
        
        return Response({
            'message': 'Joined session successfully',
            'meet_link': session.meet_link
        })
    
    @action(detail=True, methods=['post'])
    def leave_session(self, request, pk=None):
        """Student leaves session"""
        session = self.get_object()
        student = request.user
        
        try:
            attendance = SessionAttendance.objects.get(
                session=session,
                student=student
            )
            attendance.left_at = timezone.now()
            attendance.save()
            
            return Response({'message': 'Left session'})
        except SessionAttendance.DoesNotExist:
            return Response(
                {'error': 'Attendance record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def submit_feedback(self, request, pk=None):
        """Student submits session feedback"""
        session = self.get_object()
        student = request.user
        
        try:
            attendance = SessionAttendance.objects.get(
                session=session,
                student=student
            )
            attendance.student_rating = request.data.get('rating')
            attendance.student_feedback = request.data.get('feedback', '')
            attendance.save()
            
            return Response({'message': 'Feedback submitted'})
        except SessionAttendance.DoesNotExist:
            return Response(
                {'error': 'Attendance record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming sessions"""
        queryset = self.get_queryset().filter(
            status='SCHEDULED',
            scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')
        
        serializer = SessionListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get past sessions"""
        queryset = self.get_queryset().filter(
            Q(status='COMPLETED') | Q(scheduled_at__lt=timezone.now())
        ).order_by('-scheduled_at')
        
        serializer = SessionListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def _send_session_notifications(self, session, action_type):
        """Send email and Discord notifications for session"""
        try:
            from utils.email import send_session_notification_email
            from utils.discord import send_discord_notification
            
            # Send email to students
            for student in session.students.all():
                send_session_notification_email(student, session, action_type)
            
            # Send Discord notification
            color_map = {
                'created': 0x3b82f6,  # Blue
                'updated': 0xf59e0b,  # Orange
                'cancelled': 0xef4444  # Red
            }
            
            send_discord_notification(
                title=f"📅 Session {action_type.title()}",
                description=f"**{session.title}**",
                fields=[
                    {"name": "Trainer", "value": session.trainer.name, "inline": True},
                    {"name": "Date", "value": session.scheduled_at.strftime('%Y-%m-%d %H:%M'), "inline": True},
                    {"name": "Students", "value": str(session.students.count()), "inline": True},
                ],
                color=color_map.get(action_type, 0x3b82f6)
            )
        except Exception as e:
            logger.error(f"Failed to send session notifications: {str(e)}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_students(request):
    """Get list of students for session enrollment"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    students = User.objects.filter(
        role='student',
        enrollment_status='ENROLLED'
    ).values('id', 'name', 'email', 'track')
    
    return Response(list(students))
