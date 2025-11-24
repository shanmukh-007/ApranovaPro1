"""
Custom middleware for ApraNova LMS
"""
from django.http import HttpResponsePermanentRedirect


class TrailingSlashMiddleware:
    """
    Middleware to handle trailing slashes for API endpoints
    Automatically adds trailing slash to API requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only handle API endpoints
        if request.path.startswith('/api/'):
            # If path doesn't end with slash, add it
            if not request.path.endswith('/'):
                new_path = request.path + '/'
                # Preserve query string
                if request.META.get('QUERY_STRING'):
                    new_path = new_path + '?' + request.META['QUERY_STRING']
                # Don't redirect, just modify the path
                request.path = new_path.split('?')[0]
                request.path_info = new_path.split('?')[0]
        
        response = self.get_response(request)
        return response
