from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from .models import Establishment, Classroom, Student, Teacher
from .serializers import EstablishmentSerializer, ClassroomSerializer, StudentSerializer, TeacherSerializer
from apps.accounts.views import AdminRequiredMixin
from apps.accounts.utils import log_admin_action


class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'address']


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    filterset_fields = ['establishment']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['user__username', 'matricule']
    filterset_fields = ['classroom']


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['user__username', 'speciality']


# HTML Views for Admin
class AcademicOverviewView(AdminRequiredMixin, ListView):
    model = Classroom
    template_name = 'academic/overview.html'
    context_object_name = 'classrooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers_count'] = Teacher.objects.count()
        context['students_count'] = Student.objects.count()
        context['establishments'] = Establishment.objects.all()
        return context


class ClassroomCreateView(AdminRequiredMixin, CreateView):
    model = Classroom
    fields = ['name', 'establishment']
    template_name = 'academic/classroom_form.html'
    success_url = reverse_lazy('academic_overview')

    def form_valid(self, form):
        classroom = form.save()
        log_admin_action(
            self.request.user, 
            'CREATE_CLASSROOM', 
            f"Class: {classroom.name}", 
            "",
            self.request.META.get('REMOTE_ADDR')
        )
        messages.success(self.request, f"Classe {classroom.name} créée.")
        return redirect(self.success_url)


class ClassroomUpdateView(AdminRequiredMixin, UpdateView):
    model = Classroom
    fields = ['name', 'establishment']
    template_name = 'academic/classroom_form.html'
    success_url = reverse_lazy('academic_overview')

    def form_valid(self, form):
        classroom = form.save()
        log_admin_action(
            self.request.user, 
            'UPDATE_CLASSROOM', 
            f"Class: {classroom.name}", 
            "",
            self.request.META.get('REMOTE_ADDR')
        )
        messages.success(self.request, f"Classe {classroom.name} mise à jour.")
        return redirect(self.success_url)


class ClassroomDeleteView(AdminRequiredMixin, DeleteView):
    model = Classroom
    template_name = 'academic/classroom_confirm_delete.html'
    success_url = reverse_lazy('academic_overview')

    def delete(self, request, *args, **kwargs):
        classroom = self.get_object()
        log_admin_action(
            request.user, 
            'DELETE_CLASSROOM', 
            f"Class: {classroom.name}", 
            "",
            request.META.get('REMOTE_ADDR')
        )
        messages.success(request, f"Classe {classroom.name} supprimée.")
        return super().delete(request, *args, **kwargs)

