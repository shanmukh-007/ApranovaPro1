"""
Google Meet integration for creating meeting links
"""
import uuid
import logging

logger = logging.getLogger(__name__)


class GoogleMeetService:
    """
    Service for creating Google Meet links
    
    Note: This is a simplified implementation that generates generic Meet links.
    For full Google Calendar integration with automatic Meet links, you would need:
    1. Google Calendar API credentials
    2. OAuth2 authentication
    3. Calendar event creation
    
    For now, we provide a simple Meet link generator.
    """
    
    @staticmethod
    def create_meet_link(session):
        """
        Create a Google Meet link for a session
        
        For development: Uses meet.google.com/new for instant meetings
        For production: Should use Google Calendar API for proper integration
        
        Note: meet.google.com/new creates a new meeting each time it's clicked.
        For a consistent meeting room, use Google Calendar API integration.
        
        Args:
            session: Session instance
        
        Returns:
            str: Google Meet link
        """
        # Option 1: Use instant meeting (creates new meeting each time)
        # meet_link = "https://meet.google.com/new"
        
        # Option 2: Generate a unique meeting code for this session
        # Note: This won't work without Google Calendar API, but provides
        # a consistent link that can be shared
        import hashlib
        
        # Create a unique code based on session ID
        session_hash = hashlib.md5(f"session-{session.id}".encode()).hexdigest()[:10]
        
        # Format as Google Meet style code (xxx-xxxx-xxx)
        code = f"{session_hash[:3]}-{session_hash[3:7]}-{session_hash[7:10]}"
        
        # For development, use meet.google.com/new with a note
        # In production, this should be replaced with Calendar API
        meet_link = f"https://meet.google.com/new?authuser=0"
        
        logger.info(f"Generated Meet link for session {session.id}: {meet_link}")
        logger.info(f"Note: For production, integrate Google Calendar API for persistent meeting rooms")
        
        return meet_link
    
    @staticmethod
    def _generate_meeting_code():
        """
        Generate a meeting code in Google Meet format
        Format: xxx-xxxx-xxx (3-4-3 characters)
        """
        import random
        import string
        
        def random_string(length):
            return ''.join(random.choices(string.ascii_lowercase, k=length))
        
        part1 = random_string(3)
        part2 = random_string(4)
        part3 = random_string(3)
        
        return f"{part1}-{part2}-{part3}"
    
    @staticmethod
    def create_meet_link_with_calendar(session, credentials):
        """
        Create Google Meet link via Google Calendar API
        
        This requires:
        - Google Calendar API enabled
        - OAuth2 credentials
        - User authorization
        
        Args:
            session: Session instance
            credentials: Google OAuth2 credentials
        
        Returns:
            str: Google Meet link from Calendar event
        """
        try:
            from googleapiclient.discovery import build
            from datetime import timedelta
            
            service = build('calendar', 'v3', credentials=credentials)
            
            # Create calendar event
            event = {
                'summary': session.title,
                'description': session.description,
                'start': {
                    'dateTime': session.scheduled_at.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': session.end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': str(uuid.uuid4()),
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                    }
                },
                'attendees': [
                    {'email': student.email}
                    for student in session.students.all()
                ],
            }
            
            # Create event with Meet link
            event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()
            
            # Extract Meet link
            meet_link = event.get('hangoutLink')
            google_event_id = event.get('id')
            
            # Update session
            session.google_event_id = google_event_id
            session.save()
            
            logger.info(f"Created Calendar event with Meet link: {meet_link}")
            
            return meet_link
            
        except Exception as e:
            logger.error(f"Failed to create Calendar event: {str(e)}")
            # Fallback to simple link
            return GoogleMeetService.create_meet_link(session)
