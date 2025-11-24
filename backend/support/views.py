"""
Support Ticket Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

from .models import SupportTicket, TicketMessage
from .serializers import (
    SupportTicketSerializer,
    CreateTicketSerializer,
    UpdateTicketSerializer,
    TicketMessageSerializer
)
from utils.discord import (
    notify_new_ticket,
    notify_ticket_assigned,
    notify_ticket_message,
    notify_ticket_resolved
)


class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for support tickets
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students see only their tickets
            return SupportTicket.objects.filter(student=user)
        elif user.role in ['trainer', 'admin', 'superadmin']:
            # Trainers/admins see assigned tickets or all tickets
            if self.request.query_params.get('assigned_to_me'):
                return SupportTicket.objects.filter(assigned_to=user)
            return SupportTicket.objects.all()
        
        return SupportTicket.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTicketSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateTicketSerializer
        return SupportTicketSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new support ticket
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create ticket
        ticket = serializer.save(student=request.user)
        
        # Auto-assign to student's trainer if available
        if hasattr(request.user, 'assigned_trainer') and request.user.assigned_trainer:
            ticket.assigned_to = request.user.assigned_trainer
            ticket.save()
        
        # Send Discord notification
        notify_new_ticket(ticket)
        
        # Return full ticket data
        response_serializer = SupportTicketSerializer(ticket)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Update ticket (status, priority, assignment)
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_status = instance.status
        old_assigned_to = instance.assigned_to
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        
        # Handle status changes
        if ticket.status == 'RESOLVED' and old_status != 'RESOLVED':
            ticket.resolved_at = timezone.now()
            ticket.save()
            notify_ticket_resolved(ticket)
        elif ticket.status == 'CLOSED' and old_status != 'CLOSED':
            ticket.closed_at = timezone.now()
            ticket.save()
        
        # Handle assignment changes
        if ticket.assigned_to and ticket.assigned_to != old_assigned_to:
            notify_ticket_assigned(ticket)
        
        response_serializer = SupportTicketSerializer(ticket)
        return Response(response_serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Add a message/reply to a ticket
        """
        ticket = self.get_object()
        message_text = request.data.get('message')
        attachment_url = request.data.get('attachment_url', '')
        is_internal = request.data.get('is_internal', False)
        
        if not message_text:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create message
        message = TicketMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=message_text,
            attachment_url=attachment_url,
            is_internal=is_internal
        )
        
        # Update ticket status if student replies
        if request.user.role == 'student' and ticket.status == 'WAITING_STUDENT':
            ticket.status = 'IN_PROGRESS'
            ticket.save()
        
        # Send Discord notification
        notify_ticket_message(ticket, message)
        
        serializer = TicketMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign ticket to a trainer/admin
        """
        ticket = self.get_object()
        trainer_id = request.data.get('trainer_id')
        
        if not trainer_id:
            return Response(
                {'error': 'trainer_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from accounts.models import CustomUser
        try:
            trainer = CustomUser.objects.get(id=trainer_id, role__in=['trainer', 'admin', 'superadmin'])
            ticket.assigned_to = trainer
            ticket.status = 'IN_PROGRESS'
            ticket.save()
            
            # Send Discord notification
            notify_ticket_assigned(ticket)
            
            serializer = SupportTicketSerializer(ticket)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Trainer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """
        Mark ticket as resolved
        """
        ticket = self.get_object()
        resolution_message = request.data.get('message', '')
        
        # Add resolution message if provided
        if resolution_message:
            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=resolution_message
            )
        
        ticket.status = 'RESOLVED'
        ticket.resolved_at = timezone.now()
        ticket.save()
        
        # Send Discord notification
        notify_ticket_resolved(ticket)
        
        serializer = SupportTicketSerializer(ticket)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """
        Reopen a resolved/closed ticket
        """
        ticket = self.get_object()
        reason = request.data.get('reason', '')
        
        if reason:
            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=f"Ticket reopened: {reason}"
            )
        
        ticket.status = 'OPEN'
        ticket.resolved_at = None
        ticket.closed_at = None
        ticket.save()
        
        serializer = SupportTicketSerializer(ticket)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        """
        Get current user's tickets
        """
        tickets = self.get_queryset().filter(student=request.user)
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def assigned_to_me(self, request):
        """
        Get tickets assigned to current user (trainer/admin)
        """
        if request.user.role not in ['trainer', 'admin', 'superadmin']:
            return Response(
                {'error': 'Only trainers and admins can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        tickets = self.get_queryset().filter(assigned_to=request.user)
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get ticket statistics
        """
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'open': queryset.filter(status='OPEN').count(),
            'in_progress': queryset.filter(status='IN_PROGRESS').count(),
            'waiting_student': queryset.filter(status='WAITING_STUDENT').count(),
            'resolved': queryset.filter(status='RESOLVED').count(),
            'closed': queryset.filter(status='CLOSED').count(),
            'by_priority': {
                'urgent': queryset.filter(priority='URGENT').count(),
                'high': queryset.filter(priority='HIGH').count(),
                'medium': queryset.filter(priority='MEDIUM').count(),
                'low': queryset.filter(priority='LOW').count(),
            },
            'by_category': {}
        }
        
        # Count by category
        for category, _ in SupportTicket.CATEGORY_CHOICES:
            stats['by_category'][category.lower()] = queryset.filter(category=category).count()
        
        return Response(stats)
