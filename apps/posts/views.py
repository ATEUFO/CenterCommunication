from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Post, ArchivedPost, PostMedia
from .serializers import PostSerializer, PostDetailSerializer, ArchivedPostSerializer
from .forms import PostForm, PostMediaForm
from apps.accounts.views import AdminRequiredMixin
from apps.accounts.utils import log_admin_action


# API ViewSets
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'content', 'author__username']
    filterset_fields = ['post_type', 'classroom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(is_active=True)
        
        # Filter based on user role and post type
        if hasattr(user, 'student_profile') and user.student_profile:
            classroom = user.student_profile.classroom
            queryset = queryset.filter(
                Q(post_type='GLOBAL') |
                Q(post_type='CLASS', classroom=classroom) |
                Q(post_type='PERSONAL', target_user=user)
            )
        elif hasattr(user, 'teacher_profile') and user.teacher_profile:
            classrooms = user.teacher_profile.classrooms.all()
            queryset = queryset.filter(
                Q(post_type='GLOBAL') |
                Q(post_type='CLASS', classroom__in=classrooms) |
                Q(author=user)
            )
        elif user.role == 'ADMIN':
            pass  # Admin sees everything
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArchivedPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedPost.objects.all()
    serializer_class = ArchivedPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'content', 'author__username']
    filterset_fields = ['post_type']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return ArchivedPost.objects.all().order_by('-archived_at')
        return ArchivedPost.objects.none()


# HTML Views
class DashboardView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(is_active=True).select_related('author', 'classroom').prefetch_related('media')
        
        if user.role == 'STUDENT' and hasattr(user, 'student_profile') and user.student_profile:
            classroom = user.student_profile.classroom
            queryset = queryset.filter(
                Q(post_type='GLOBAL') |
                Q(post_type='CLASS', classroom=classroom) |
                Q(post_type='PERSONAL', target_user=user)
            )
        elif user.role == 'TEACHER' and hasattr(user, 'teacher_profile') and user.teacher_profile:
            classrooms = user.teacher_profile.classrooms.all()
            queryset = queryset.filter(
                Q(post_type='GLOBAL') |
                Q(post_type='CLASS', classroom__in=classrooms) |
                Q(author=user)
            )
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.role == 'ADMIN':
            from apps.accounts.models import User
            from apps.academic.models import Classroom
            context['users_count'] = User.objects.count()
            context['classrooms_count'] = Classroom.objects.count()
        
        return context

    def get_template_names(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return ['posts/admin_dashboard.html']
        elif user.role == 'TEACHER':
            return ['posts/teacher_dashboard.html']
        elif user.role == 'STUDENT':
            return ['posts/student_dashboard.html']
        return [self.template_name]



class PostDetailHTMLView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author').order_by('-created_at')
        context['media_list'] = self.object.media.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Handle multiple file uploads
        files = self.request.FILES.getlist('media_files')
        for f in files:
            # Enhanced media type detection
            content_type = f.content_type.lower()
            filename = f.name.lower()
            
            if 'image' in content_type or filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                media_type = 'IMAGE'
            elif 'pdf' in content_type or filename.endswith('.pdf'):
                media_type = 'PDF'
            elif 'video' in content_type or filename.endswith(('.mp4', '.mov', '.avi', '.wmv', '.webm', '.mkv')):
                media_type = 'VIDEO'
            else:
                media_type = 'OTHER'
            
            PostMedia.objects.create(
                post=self.object,
                file=f,
                media_type=media_type
            )

            
        if self.request.user.role == 'ADMIN':
            log_admin_action(
                self.request.user, 
                'CREATE_POST', 
                f"Post: {self.object.title}", 
                f"Type: {self.object.post_type}",
                self.request.META.get('REMOTE_ADDR')
            )
            
        messages.success(self.request, "Publication créée avec succès.")
        return response

