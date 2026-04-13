from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstablishmentViewSet, ClassroomViewSet, StudentViewSet, TeacherViewSet,
    AcademicOverviewView, ClassroomCreateView, ClassroomUpdateView, ClassroomDeleteView
)

router = DefaultRouter()
router.register(r'establishments', EstablishmentViewSet, basename='establishment')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')

urlpatterns = [
    # REST API
    path('api/', include(router.urls)),
    
    # HTML Views
    path('overview/', AcademicOverviewView.as_view(), name='academic_overview'),
    path('classrooms/create/', ClassroomCreateView.as_view(), name='classroom_create'),
    path('classrooms/<int:pk>/update/', ClassroomUpdateView.as_view(), name='classroom_update'),
    path('classrooms/<int:pk>/delete/', ClassroomDeleteView.as_view(), name='classroom_delete'),
]

