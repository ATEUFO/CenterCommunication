from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, ArchivedPostViewSet, DashboardView, 
    PostDetailHTMLView, PostCreateView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'archived-posts', ArchivedPostViewSet, basename='archived-post')

urlpatterns = [
    # REST API
    path('api/', include(router.urls)),
    
    # HTML Views
    path('', DashboardView.as_view(), name='posts_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', PostDetailHTMLView.as_view(), name='post_detail'),
]

