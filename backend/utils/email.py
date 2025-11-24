"""
Email utility functions for ApraNova LMS
"""
from django.core.mail import send_mail, EmailMultipleAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_welcome_email(user, password=None):
    """
    Send welcome email to newly enrolled student
    
    Args:
        user: User instance
        password: Plain text password (only for new accounts)
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        track_name = "Data Professional" if user.track == "DP" else "Full Stack Development"
        
        subject = f"Welcome to ApraNova LMS - {track_name} Track"
        
        # Plain text version
        message = f"""
Welcome to ApraNova LMS!

Congratulations on enrolling in the {track_name} track!

Your Account Details:
- Email: {user.email}
- Username: {user.username}
{'- Password: ' + password if password else ''}

Getting Started:
1. Log in at: {settings.FRONTEND_URL or 'http://localhost:3000'}/login
2. Complete your profile
3. Start with Project 1

Your Learning Tools:
"""
        
        if user.track == "DP":
            message += f"""
- Apache Superset (Data Visualization): {user.superset_url or 'Being provisioned...'}
- Prefect (Workflow Orchestration): {user.prefect_url or 'Being provisioned...'}
- Jupyter Notebook: {user.jupyter_url or 'Being provisioned...'}
"""
        else:
            message += f"""
- VS Code Workspace: {user.workspace_url or 'Being provisioned...'}
"""
        
        message += """

Need Help?
- Visit the Support page in your dashboard
- Contact us at support@apranova.com

We're excited to have you on this learning journey!

Best regards,
The ApraNova Team
"""
        
        # HTML version (optional, can be enhanced later)
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .credentials {{ background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }}
        .tools {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to ApraNova LMS! 🎉</h1>
            <p>You're enrolled in the {track_name} track</p>
        </div>
        <div class="content">
            <p>Congratulations on taking the first step in your learning journey!</p>
            
            <div class="credentials">
                <h3>Your Account Details</h3>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Username:</strong> {user.username}</p>
                {'<p><strong>Password:</strong> ' + password + '</p>' if password else '<p><em>Use your existing password to log in</em></p>'}
            </div>
            
            <a href="{settings.FRONTEND_URL or 'http://localhost:3000'}/login" class="button">Log In Now</a>
            
            <h3>Getting Started</h3>
            <ol>
                <li>Log in to your account</li>
                <li>Complete your profile</li>
                <li>Start with Project 1</li>
            </ol>
            
            <div class="tools">
                <h3>Your Learning Tools</h3>
"""
        
        if user.track == "DP":
            html_message += f"""
                <p><strong>Apache Superset</strong> (Data Visualization)<br>
                {user.superset_url or '<em>Being provisioned...</em>'}</p>
                
                <p><strong>Prefect</strong> (Workflow Orchestration)<br>
                {user.prefect_url or '<em>Being provisioned...</em>'}</p>
                
                <p><strong>Jupyter Notebook</strong><br>
                {user.jupyter_url or '<em>Being provisioned...</em>'}</p>
"""
        else:
            html_message += f"""
                <p><strong>VS Code Workspace</strong><br>
                {user.workspace_url or '<em>Being provisioned...</em>'}</p>
"""
        
        html_message += """
            </div>
            
            <h3>Need Help?</h3>
            <p>Visit the Support page in your dashboard or contact us at <a href="mailto:support@apranova.com">support@apranova.com</a></p>
            
            <div class="footer">
                <p>We're excited to have you on this learning journey!</p>
                <p><strong>The ApraNova Team</strong></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        # Send email
        email = EmailMultipleAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Welcome email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False


def send_payment_confirmation_email(user, payment):
    """
    Send payment confirmation email
    
    Args:
        user: User instance
        payment: Payment instance
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        track_name = "Data Professional" if payment.track == "DP" else "Full Stack Development"
        
        subject = "Payment Confirmation - ApraNova LMS"
        
        message = f"""
Payment Confirmation

Dear {user.name or user.username},

Thank you for your payment! Your enrollment in the {track_name} track is now confirmed.

Payment Details:
- Amount: ${payment.amount} {payment.currency.upper()}
- Payment ID: {payment.stripe_payment_intent}
- Date: {payment.created_at.strftime('%B %d, %Y at %I:%M %p')}
- Track: {track_name}

Your account is now active and you can start learning immediately!

Log in at: {settings.FRONTEND_URL or 'http://localhost:3000'}/login

If you have any questions about your payment, please contact us at support@apranova.com

Best regards,
The ApraNova Team
"""
        
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #10b981; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .payment-details {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Payment Confirmed</h1>
        </div>
        <div class="content">
            <p>Dear {user.name or user.username},</p>
            <p>Thank you for your payment! Your enrollment in the <strong>{track_name}</strong> track is now confirmed.</p>
            
            <div class="payment-details">
                <h3>Payment Details</h3>
                <p><strong>Amount:</strong> ${payment.amount} {payment.currency.upper()}</p>
                <p><strong>Payment ID:</strong> {payment.stripe_payment_intent}</p>
                <p><strong>Date:</strong> {payment.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                <p><strong>Track:</strong> {track_name}</p>
            </div>
            
            <p>Your account is now active and you can start learning immediately!</p>
            
            <a href="{settings.FRONTEND_URL or 'http://localhost:3000'}/login" class="button">Start Learning</a>
            
            <div class="footer">
                <p>If you have any questions about your payment, please contact us at <a href="mailto:support@apranova.com">support@apranova.com</a></p>
                <p><strong>The ApraNova Team</strong></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        email = EmailMultipleAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Payment confirmation email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send payment confirmation to {user.email}: {str(e)}")
        return False


def send_payment_failed_email(email, amount, track):
    """
    Send payment failed notification
    
    Args:
        email: Customer email
        amount: Payment amount
        track: Track code (DP or FSD)
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        track_name = "Data Professional" if track == "DP" else "Full Stack Development"
        
        subject = "Payment Failed - ApraNova LMS"
        
        message = f"""
Payment Failed

We're sorry, but your payment for the {track_name} track could not be processed.

Amount: ${amount}
Track: {track_name}

This could be due to:
- Insufficient funds
- Card declined by your bank
- Incorrect card details
- Security restrictions

What to do next:
1. Check your payment method details
2. Contact your bank if needed
3. Try again at: {settings.FRONTEND_URL or 'http://localhost:3000'}/payment

If you continue to experience issues, please contact us at support@apranova.com

Best regards,
The ApraNova Team
"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        
        logger.info(f"Payment failed email sent to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send payment failed email to {email}: {str(e)}")
        return False


def send_session_notification_email(user, session, action_type):
    """
    Send session notification email to student
    
    Args:
        user: User instance (student)
        session: Session instance
        action_type: 'created', 'updated', 'cancelled'
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        action_titles = {
            'created': 'New Class Session Scheduled',
            'updated': 'Class Session Updated',
            'cancelled': 'Class Session Cancelled'
        }
        
        subject = f"{action_titles.get(action_type, 'Class Session')} - ApraNova LMS"
        
        message = f"""
{action_titles.get(action_type, 'Class Session')}

Dear {user.name or user.username},

"""
        
        if action_type == 'cancelled':
            message += f"""
The following class session has been cancelled:

Session: {session.title}
Trainer: {session.trainer.name}
Originally Scheduled: {session.scheduled_at.strftime('%B %d, %Y at %I:%M %p')}

We apologize for any inconvenience. Your trainer will reschedule soon.
"""
        else:
            message += f"""
Session Details:
- Title: {session.title}
- Trainer: {session.trainer.name}
- Date & Time: {session.scheduled_at.strftime('%B %d, %Y at %I:%M %p')}
- Duration: {session.duration_minutes} minutes
- Type: {session.get_session_type_display()}

"""
            if session.description:
                message += f"Description:\n{session.description}\n\n"
            
            if session.agenda:
                message += f"Agenda:\n{session.agenda}\n\n"
            
            if session.meet_link:
                message += f"Google Meet Link: {session.meet_link}\n\n"
            
            message += f"""
To join the session:
1. Log in to your dashboard at {settings.FRONTEND_URL or 'http://localhost:3000'}
2. Go to "Sessions" or "Classes"
3. Click "Join Session" at the scheduled time
"""
        
        message += """

If you have any questions, please contact your trainer or support@apranova.com

Best regards,
The ApraNova Team
"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        
        logger.info(f"Session notification email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send session notification to {user.email}: {str(e)}")
        return False


def send_refund_notification_email(user, payment):
    """
    Send refund notification email
    
    Args:
        user: User instance
        payment: Payment instance
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        subject = "Refund Processed - ApraNova LMS"
        
        message = f"""
Refund Processed

Dear {user.name or user.username},

Your refund has been processed successfully.

Refund Details:
- Amount: ${payment.refund_amount} {payment.currency.upper()}
- Original Payment ID: {payment.stripe_payment_intent}
- Refund Date: {payment.refunded_at.strftime('%B %d, %Y at %I:%M %p')}

The refund will appear in your account within 5-10 business days, depending on your bank.

Your enrollment has been withdrawn. If you'd like to re-enroll in the future, you're always welcome back!

If you have any questions, please contact us at support@apranova.com

Best regards,
The ApraNova Team
"""
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        
        logger.info(f"Refund notification email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send refund notification to {user.email}: {str(e)}")
        return False
