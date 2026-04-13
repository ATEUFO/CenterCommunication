from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework import viewsets, permissions
from .models import User, AuditLog
from .serializers import UserSerializer, UserDetailSerializer
from .forms import UserForm, StudentForm, TeacherForm
from .utils import log_admin_action
from apps.academic.models import Student, Teacher, Classroom


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer


# HTML Views
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['academic_info'] = None
        
        if hasattr(user, 'student_profile'):
            context['academic_info'] = user.student_profile
            context['role_type'] = 'Étudiant'
        elif hasattr(user, 'teacher_profile'):
            context['academic_info'] = user.teacher_profile
            context['role_type'] = 'Enseignant'
            
        return context


# Admin User Management
class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['student_form'] = StudentForm(self.request.POST)
            data['teacher_form'] = TeacherForm(self.request.POST)
        else:
            data['student_form'] = StudentForm()
            data['teacher_form'] = TeacherForm()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        student_form = context['student_form']
        teacher_form = context['teacher_form']
        
        user = form.save()
        
        if user.role == 'STUDENT':
            student = student_form.save(commit=False)
            student.user = user
            student.save()
        elif user.role == 'TEACHER':
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            teacher_form.save_m2m() # For classrooms
            
        log_admin_action(
            self.request.user, 
            'CREATE_USER', 
            f"User: {user.username}", 
            f"Role: {user.role}",
            self.request.META.get('REMOTE_ADDR')
        )
        messages.success(self.request, f"Utilisateur {user.username} créé avec succès.")
        return redirect(self.success_url)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.get_object()
        if self.request.POST:
            if user.role == 'STUDENT':
                data['student_form'] = StudentForm(self.request.POST, instance=getattr(user, 'student_profile', None))
            elif user.role == 'TEACHER':
                data['teacher_form'] = TeacherForm(self.request.POST, instance=getattr(user, 'teacher_profile', None))
        else:
            if user.role == 'STUDENT':
                data['student_form'] = StudentForm(instance=getattr(user, 'student_profile', None))
            elif user.role == 'TEACHER':
                data['teacher_form'] = TeacherForm(instance=getattr(user, 'teacher_profile', None))
        return data

    def form_valid(self, form):
        user = form.save()
        context = self.get_context_data()
        
        if user.role == 'STUDENT' and 'student_form' in context:
            student_form = context['student_form']
            if student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.save()
        elif user.role == 'TEACHER' and 'teacher_form' in context:
            teacher_form = context['teacher_form']
            if teacher_form.is_valid():
                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.save()
                teacher_form.save_m2m()
                
        log_admin_action(
            self.request.user, 
            'UPDATE_USER', 
            f"User: {user.username}", 
            f"Role: {user.role}",
            self.request.META.get('REMOTE_ADDR')
        )
        messages.success(self.request, f"Utilisateur {user.username} mis à jour.")
        return redirect(self.success_url)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        log_admin_action(
            request.user, 
            'DELETE_USER', 
            f"User: {user.username}", 
            "",
            request.META.get('REMOTE_ADDR')
        )
        messages.success(request, f"Utilisateur {user.username} supprimé.")
        return super().delete(request, *args, **kwargs)

