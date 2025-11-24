"""
Discord notification utilities
"""
import requests
from django.conf import settings


def send_discord_notification(message, embeds=None):
    """
    Send a message to Discord via webhook
    
    Args:
        message: Plain text message (content)
        embeds: Optional rich formatting embeds (list of embed objects)
        
    Returns:
        bool: Success status
    """
    webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', None)
    
    if not webhook_url:
        print(f"Discord webhook not configured. Message: {message}")
        return False
    
    try:
        payload = {
            "content": message
        }
        
        if embeds:
            payload["embeds"] = embeds
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=5
        )
        
        return response.status_code in [200, 204]
        
    except Exception as e:
        print(f"Discord notification error: {e}")
        return False


def notify_project_started(student, project, repo_url):
    """
    Notify when student starts a project
    """
    message = f"🚀 **{student.name}** started **{project.title}**"
    
    embeds = [{
        "title": "🚀 Project Started",
        "color": 3447003,  # Blue
        "fields": [
            {
                "name": "Student",
                "value": student.name,
                "inline": True
            },
            {
                "name": "Track",
                "value": student.track,
                "inline": True
            },
            {
                "name": "Project",
                "value": project.title,
                "inline": False
            },
            {
                "name": "Repository",
                "value": f"[View on GitHub]({repo_url})",
                "inline": False
            }
        ],
        "timestamp": project.created_at.isoformat() if hasattr(project, 'created_at') else None
    }]
    
    if student.assigned_trainer:
        embeds[0]["fields"].append({
            "name": "Assigned Trainer",
            "value": f"👤 {student.assigned_trainer.name}",
            "inline": False
        })
    
    return send_discord_notification(message, embeds)


def notify_new_submission(submission):
    """
    Notify trainer when student submits a deliverable
    """
    student = submission.student
    project = submission.deliverable.project
    trainer = student.assigned_trainer
    
    message = f"🎉 New submission from **{student.name}**"
    
    embeds = [{
        "title": "🎉 New Submission",
        "color": 5763719,  # Green
        "fields": [
            {
                "name": "Student",
                "value": student.name,
                "inline": True
            },
            {
                "name": "Trainer",
                "value": trainer.name if trainer else "Not assigned",
                "inline": True
            },
            {
                "name": "Project",
                "value": project.title,
                "inline": False
            },
            {
                "name": "Deliverable",
                "value": submission.deliverable.title,
                "inline": False
            }
        ],
        "timestamp": submission.submitted_at.isoformat() if hasattr(submission, 'submitted_at') else None
    }]
    
    # Add submission links
    if submission.submission_url:
        embeds[0]["fields"].append({
            "name": "Submission URL",
            "value": f"[View Submission]({submission.submission_url})",
            "inline": False
        })
    
    if submission.github_pr_url:
        embeds[0]["fields"].append({
            "name": "Pull Request",
            "value": f"[Review PR on GitHub]({submission.github_pr_url})",
            "inline": False
        })
    
    # Add review link
    platform_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    embeds[0]["fields"].append({
        "name": "Action Required",
        "value": f"[Review Now]({platform_url}/trainer/submissions)",
        "inline": False
    })
    
    return send_discord_notification(message, embeds)


def notify_submission_approved(submission):
    """
    Notify student when submission is approved
    """
    student = submission.student
    project = submission.deliverable.project
    reviewer = submission.reviewed_by
    
    message = f"✅ **{student.name}**, your submission was approved!"
    
    embeds = [{
        "title": "✅ Submission Approved",
        "description": f"Congratulations! Your submission for **{project.title}** has been approved.",
        "color": 3066993,  # Green
        "fields": [
            {
                "name": "Project",
                "value": project.title,
                "inline": True
            },
            {
                "name": "Deliverable",
                "value": submission.deliverable.title,
                "inline": True
            },
            {
                "name": "Reviewed by",
                "value": reviewer.name if reviewer else "Unknown",
                "inline": False
            }
        ],
        "timestamp": submission.reviewed_at.isoformat() if hasattr(submission, 'reviewed_at') else None
    }]
    
    if submission.feedback:
        embeds[0]["fields"].append({
            "name": "Feedback",
            "value": submission.feedback[:1024],  # Discord limit
            "inline": False
        })
    
    return send_discord_notification(message, embeds)


def notify_submission_rejected(submission):
    """
    Notify student when submission needs revision
    """
    student = submission.student
    project = submission.deliverable.project
    reviewer = submission.reviewed_by
    
    message = f"⚠️ **{student.name}**, your submission needs revision"
    
    embeds = [{
        "title": "⚠️ Changes Requested",
        "description": f"Your submission for **{project.title}** needs some revisions.",
        "color": 15105570,  # Orange
        "fields": [
            {
                "name": "Project",
                "value": project.title,
                "inline": True
            },
            {
                "name": "Deliverable",
                "value": submission.deliverable.title,
                "inline": True
            },
            {
                "name": "Reviewed by",
                "value": reviewer.name if reviewer else "Unknown",
                "inline": False
            }
        ],
        "timestamp": submission.reviewed_at.isoformat() if hasattr(submission, 'reviewed_at') else None
    }]
    
    if submission.feedback:
        embeds[0]["fields"].append({
            "name": "Feedback",
            "value": submission.feedback[:1024],  # Discord limit
            "inline": False
        })
    
    # Add action link
    platform_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    embeds[0]["fields"].append({
        "name": "Next Steps",
        "value": f"[View Feedback & Resubmit]({platform_url}/student/submissions)",
        "inline": False
    })
    
    return send_discord_notification(message, embeds)


def notify_pr_created(student, project, pr_url):
    """
    Notify when student creates a PR
    """
    message = f"📝 **{student.name}** created a Pull Request"
    
    embeds = [{
        "title": "📝 Pull Request Created",
        "color": 10181046,  # Purple
        "fields": [
            {
                "name": "Student",
                "value": student.name,
                "inline": True
            },
            {
                "name": "Project",
                "value": project.title,
                "inline": True
            },
            {
                "name": "Pull Request",
                "value": f"[Review on GitHub]({pr_url})",
                "inline": False
            }
        ]
    }]
    
    if student.assigned_trainer:
        embeds[0]["fields"].append({
            "name": "Assigned Trainer",
            "value": f"👤 {student.assigned_trainer.name}",
            "inline": False
        })
    
    return send_discord_notification(message, embeds)


def notify_pr_merged(student, project):
    """
    Notify when PR is merged (project completed)
    """
    message = f"🎊 **{student.name}** completed **{project.title}**!"
    
    embeds = [{
        "title": "🎊 Project Completed",
        "description": "Pull Request has been merged to main branch!",
        "color": 15844367,  # Gold
        "fields": [
            {
                "name": "Student",
                "value": student.name,
                "inline": True
            },
            {
                "name": "Project",
                "value": project.title,
                "inline": True
            }
        ]
    }]
    
    return send_discord_notification(message, embeds)


def notify_payment_received(user, amount, track):
    """
    Notify when a payment is received
    """
    message = f"💰 New payment received from **{user.name}**"
    
    embeds = [{
        "title": "💰 Payment Received",
        "color": 3066993,  # Green
        "fields": [
            {
                "name": "Student",
                "value": user.name,
                "inline": True
            },
            {
                "name": "Email",
                "value": user.email,
                "inline": True
            },
            {
                "name": "Amount",
                "value": f"${amount}",
                "inline": True
            },
            {
                "name": "Track",
                "value": track,
                "inline": True
            }
        ]
    }]
    
    return send_discord_notification(message, embeds)


def notify_new_signup(user, track):
    """
    Notify when a new user signs up
    """
    message = f"👤 New student signed up: **{user.name}**"
    
    embeds = [{
        "title": "👤 New Student Signup",
        "color": 3447003,  # Blue
        "fields": [
            {
                "name": "Name",
                "value": user.name,
                "inline": True
            },
            {
                "name": "Email",
                "value": user.email,
                "inline": True
            },
            {
                "name": "Track",
                "value": track,
                "inline": True
            }
        ]
    }]
    
    return send_discord_notification(message, embeds)


def send_discord_message(message):
    """
    Send a simple test message to Discord
    Used for testing Discord integration
    """
    return send_discord_notification(message)


def send_test_notification():
    """
    Send a test notification to verify Discord webhook is working
    """
    message = "🧪 Test notification from ApraNova LMS"
    
    embeds = [{
        "title": "🧪 Test Notification",
        "description": "Discord webhook is configured correctly!",
        "color": 5763719,  # Green
        "fields": [
            {
                "name": "Status",
                "value": "✅ Working",
                "inline": True
            },
            {
                "name": "Timestamp",
                "value": "Now",
                "inline": True
            }
        ]
    }]
    
    return send_discord_notification(message, embeds)


# ============================================
# Support Ticket Notifications
# ============================================

def notify_new_ticket(ticket):
    """
    Notify when a new support ticket is created
    """
    student = ticket.student
    trainer = ticket.assigned_to
    
    # Priority colors
    priority_colors = {
        'URGENT': 15158332,  # Red
        'HIGH': 15105570,    # Orange
        'MEDIUM': 3447003,   # Blue
        'LOW': 10070709,     # Gray
    }
    
    message = f"🎫 New support ticket from **{student.name}**"
    
    embeds = [{
        "title": f"🎫 New Support Ticket - {ticket.ticket_number}",
        "description": ticket.description[:500],  # Limit description
        "color": priority_colors.get(ticket.priority, 3447003),
        "fields": [
            {
                "name": "Student",
                "value": f"{student.name} ({student.email})",
                "inline": True
            },
            {
                "name": "Category",
                "value": ticket.get_category_display(),
                "inline": True
            },
            {
                "name": "Priority",
                "value": f"{'🔴' if ticket.priority == 'URGENT' else '🟠' if ticket.priority == 'HIGH' else '🟡' if ticket.priority == 'MEDIUM' else '⚪'} {ticket.get_priority_display()}",
                "inline": True
            },
            {
                "name": "Status",
                "value": ticket.get_status_display(),
                "inline": True
            }
        ],
        "timestamp": ticket.created_at.isoformat()
    }]
    
    if ticket.project:
        embeds[0]["fields"].append({
            "name": "Related Project",
            "value": ticket.project.title,
            "inline": False
        })
    
    if trainer:
        embeds[0]["fields"].append({
            "name": "Assigned To",
            "value": f"👤 {trainer.name}",
            "inline": False
        })
    
    if ticket.attachment_url:
        embeds[0]["fields"].append({
            "name": "Attachment",
            "value": f"[View Attachment]({ticket.attachment_url})",
            "inline": False
        })
    
    # Add action link
    platform_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    embeds[0]["fields"].append({
        "name": "Action",
        "value": f"[View Ticket]({platform_url}/trainer/support/{ticket.id})",
        "inline": False
    })
    
    return send_discord_notification(message, embeds)


def notify_ticket_assigned(ticket):
    """
    Notify when a ticket is assigned to a trainer
    """
    trainer = ticket.assigned_to
    student = ticket.student
    
    message = f"👤 Ticket **{ticket.ticket_number}** assigned to **{trainer.name}**"
    
    embeds = [{
        "title": f"👤 Ticket Assigned - {ticket.ticket_number}",
        "description": ticket.title,
        "color": 3447003,  # Blue
        "fields": [
            {
                "name": "Student",
                "value": student.name,
                "inline": True
            },
            {
                "name": "Assigned To",
                "value": trainer.name,
                "inline": True
            },
            {
                "name": "Category",
                "value": ticket.get_category_display(),
                "inline": True
            },
            {
                "name": "Priority",
                "value": ticket.get_priority_display(),
                "inline": True
            }
        ]
    }]
    
    # Add action link
    platform_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    embeds[0]["fields"].append({
        "name": "Action",
        "value": f"[View Ticket]({platform_url}/trainer/support/{ticket.id})",
        "inline": False
    })
    
    return send_discord_notification(message, embeds)


def notify_ticket_message(ticket, message_obj):
    """
    Notify when a new message is added to a ticket
    """
    sender = message_obj.sender
    is_student = sender.role == 'student'
    
    # Don't notify for internal messages
    if message_obj.is_internal:
        return False
    
    msg = f"💬 New message on ticket **{ticket.ticket_number}**"
    
    embeds = [{
        "title": f"💬 New Message - {ticket.ticket_number}",
        "description": message_obj.message[:1000],  # Limit message length
        "color": 5763719 if is_student else 3447003,  # Green for student, Blue for trainer
        "fields": [
            {
                "name": "From",
                "value": f"{sender.name} ({sender.get_role_display()})",
                "inline": True
            },
            {
                "name": "Ticket",
                "value": ticket.title,
                "inline": True
            }
        ],
        "timestamp": message_obj.created_at.isoformat()
    }]
    
    if message_obj.attachment_url:
        embeds[0]["fields"].append({
            "name": "Attachment",
            "value": f"[View Attachment]({message_obj.attachment_url})",
            "inline": False
        })
    
    # Add action link
    platform_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    role_path = 'student' if is_student else 'trainer'
    embeds[0]["fields"].append({
        "name": "Action",
        "value": f"[View & Reply]({platform_url}/{role_path}/support/{ticket.id})",
        "inline": False
    })
    
    return send_discord_notification(msg, embeds)


def notify_ticket_resolved(ticket):
    """
    Notify when a ticket is resolved
    """
    student = ticket.student
    resolver = ticket.assigned_to
    
    message = f"✅ Ticket **{ticket.ticket_number}** has been resolved"
    
    embeds = [{
        "title": f"✅ Ticket Resolved - {ticket.ticket_number}",
        "description": ticket.title,
        "color": 3066993,  # Green
        "fields": [
            {
                "name": "Student",
                "value": student.name,
                "inline": True
            },
            {
                "name": "Resolved By",
                "value": resolver.name if resolver else "Unknown",
                "inline": True
            },
            {
                "name": "Category",
                "value": ticket.get_category_display(),
                "inline": True
            }
        ],
        "timestamp": ticket.resolved_at.isoformat() if ticket.resolved_at else None
    }]
    
    return send_discord_notification(message, embeds)
