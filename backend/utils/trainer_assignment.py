"""
Automatic trainer assignment logic
Assigns students to trainers based on track and capacity
"""
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def assign_trainer_to_student(student):
    """
    Automatically assign a trainer to a student based on their track
    
    Logic:
    - First 20 students of each track → trainer1@apranova.com
    - Next 20 students of each track → trainer2@apranova.com
    - Continues with additional trainers if available
    
    Args:
        student: CustomUser instance with role='student' and track set
    
    Returns:
        CustomUser: Assigned trainer or None if no trainer available
    """
    if not student.track:
        logger.warning(f"Student {student.email} has no track assigned")
        return None
    
    # Get all trainers ordered by email (trainer1, trainer2, etc.)
    trainers = User.objects.filter(
        role='trainer',
        is_active=True
    ).order_by('email')
    
    if not trainers.exists():
        logger.error("No trainers available in the system")
        return None
    
    # Count students already assigned to each trainer for this specific track
    track = student.track.upper()
    
    for trainer in trainers:
        # Count students of this track assigned to this trainer
        student_count = User.objects.filter(
            assigned_trainer=trainer,
            track=track,
            role='student'
        ).count()
        
        # Each trainer can handle 20 students per track
        if student_count < 20:
            student.assigned_trainer = trainer
            student.save()
            
            logger.info(
                f"Assigned student {student.email} ({track}) to trainer "
                f"{trainer.email} (now has {student_count + 1} {track} students)"
            )
            
            return trainer
    
    # If all trainers are at capacity, assign to first trainer anyway
    # (in production, you might want to create a waiting list instead)
    first_trainer = trainers.first()
    student.assigned_trainer = first_trainer
    student.save()
    
    logger.warning(
        f"All trainers at capacity for {track}. Assigned {student.email} "
        f"to {first_trainer.email} (over capacity)"
    )
    
    return first_trainer


def get_trainer_capacity_report():
    """
    Get a report of trainer capacity by track
    
    Returns:
        dict: Report with trainer assignments per track
    """
    trainers = User.objects.filter(role='trainer', is_active=True).order_by('email')
    report = {}
    
    for trainer in trainers:
        if trainer.track and trainer.track.strip():
            # Track-specific trainer
            student_count = User.objects.filter(
                assigned_trainer=trainer,
                track=trainer.track,
                role='student'
            ).count()
            
            report[trainer.email] = {
                'name': trainer.name or trainer.username,
                'track': trainer.track,
                'count': student_count,
                'capacity': 20,
                'available': max(0, 20 - student_count)
            }
        else:
            # General trainer (legacy - handles both tracks)
            dp_count = User.objects.filter(
                assigned_trainer=trainer,
                track='DP',
                role='student'
            ).count()
            
            fsd_count = User.objects.filter(
                assigned_trainer=trainer,
                track='FSD',
                role='student'
            ).count()
            
            report[trainer.email] = {
                'name': trainer.name or trainer.username,
                'track': 'ALL',
                'DP': {
                    'count': dp_count,
                    'capacity': 20,
                    'available': max(0, 20 - dp_count)
                },
                'FSD': {
                    'count': fsd_count,
                    'capacity': 20,
                    'available': max(0, 20 - fsd_count)
                },
                'total': dp_count + fsd_count
            }
    
    return report


def reassign_student_trainer(student, new_trainer):
    """
    Manually reassign a student to a different trainer
    
    Args:
        student: CustomUser instance
        new_trainer: CustomUser instance with role='trainer'
    
    Returns:
        bool: Success status
    """
    if new_trainer.role != 'trainer':
        logger.error(f"{new_trainer.email} is not a trainer")
        return False
    
    old_trainer = student.assigned_trainer
    student.assigned_trainer = new_trainer
    student.save()
    
    logger.info(
        f"Reassigned {student.email} from "
        f"{old_trainer.email if old_trainer else 'None'} to {new_trainer.email}"
    )
    
    return True
