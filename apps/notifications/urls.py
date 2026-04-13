from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationListView

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # REST API
    path('api/', include(router.urls)),
    
    # HTML Views
    path('', NotificationListView.as_view(), name='notifications'),
]
