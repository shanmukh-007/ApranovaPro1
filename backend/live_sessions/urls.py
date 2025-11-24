from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sessions', views.SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
    path('students/available/', views.get_available_students, name='available-students'),
]
