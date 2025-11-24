"""
Trainer management API views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as http_status
from django.contrib.auth import get_user_model
from utils.trainer_assignment import (
    get_trainer_capacity_report,
    reassign_student_trainer,
    assign_trainer_to_student
)

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trainer_capacity(request):
    """
    Get trainer capacity report
    Only accessible by admin/trainer roles
    """
    if request.user.role not in ['admin', 'superadmin', 'trainer']:
        return Response(
            {"error": "Permission denied"},
            status=http_status.HTTP_403_FORBIDDEN
        )
    
    report = get_trainer_capacity_report()
    
    return Response({
        "success": True,
        "trainers": report
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_students(request):
    """
    Get all students assigned to the current trainer
    """
    if request.user.role != 'trainer':
        return Response(
            {"error": "Only trainers can access this endpoint"},
            status=http_status.HTTP_403_FORBIDDEN
        )
    
    students = User.objects.filter(
        assigned_trainer=request.user,
        role='student'
    ).order_by('-created_at')
    
    student_data = []
    for student in students:
        student_data.append({
            'id': student.id,
            'email': student.email,
            'name': student.name or student.username,
            'track': student.track,
            'enrollment_status': student.enrollment_status,
            'enrolled_at': student.enrolled_at.isoformat() if student.enrolled_at else None,
            'created_at': student.created_at.isoformat(),
        })
    
    return Response({
        "success": True,
        "count": len(student_data),
        "students": student_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reassign_student(request):
    """
    Reassign a student to a different trainer
    Only accessible by admin roles
    
    Body:
    - student_id: ID of the student
    - trainer_id: ID of the new trainer
    """
    if request.user.role not in ['admin', 'superadmin']:
        return Response(
            {"error": "Permission denied"},
            status=http_status.HTTP_403_FORBIDDEN
        )
    
    student_id = request.data.get('student_id')
    trainer_id = request.data.get('trainer_id')
    
    if not student_id or not trainer_id:
        return Response(
            {"error": "student_id and trainer_id are required"},
            status=http_status.HTTP_400_BAD_REQUEST
        )
    
    try:
        student = User.objects.get(id=student_id, role='student')
        trainer = User.objects.get(id=trainer_id, role='trainer')
    except User.DoesNotExist:
        return Response(
            {"error": "Student or trainer not found"},
            status=http_status.HTTP_404_NOT_FOUND
        )
    
    success = reassign_student_trainer(student, trainer)
    
    if success:
        return Response({
            "success": True,
            "message": f"Student {student.email} reassigned to {trainer.email}"
        })
    else:
        return Response(
            {"error": "Failed to reassign student"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_unassigned_students(request):
    """
    Automatically assign all unassigned students to trainers
    Only accessible by admin roles
    """
    if request.user.role not in ['admin', 'superadmin']:
        return Response(
            {"error": "Permission denied"},
            status=http_status.HTTP_403_FORBIDDEN
        )
    
    unassigned = User.objects.filter(
        role='student',
        assigned_trainer__isnull=True,
        track__isnull=False
    )
    
    assigned_count = 0
    failed_count = 0
    
    for student in unassigned:
        trainer = assign_trainer_to_student(student)
        if trainer:
            assigned_count += 1
        else:
            failed_count += 1
    
    return Response({
        "success": True,
        "assigned": assigned_count,
        "failed": failed_count,
        "total": unassigned.count()
    })
