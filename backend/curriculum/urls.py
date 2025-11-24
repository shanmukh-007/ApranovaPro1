from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrackViewSet, ProjectViewSet, StudentProgressViewSet, SubmissionViewSet,
    get_current_project, approve_project_submission, request_revision
)
from .webhook_views import github_webhook

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'progress', StudentProgressViewSet, basename='progress')
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/github/', github_webhook, name='github-webhook'),
    path('webhooks/github', github_webhook, name='github-webhook-no-slash'),
    # Sequential project flow endpoints
    path('current-project/', get_current_project, name='current-project'),
    path('submissions/<int:submission_id>/approve/', approve_project_submission, name='approve-submission'),
    path('submissions/<int:submission_id>/request-revision/', request_revision, name='request-revision'),
]
