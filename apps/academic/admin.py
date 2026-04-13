from django.contrib import admin
from .models import Establishment, Classroom, Student, Teacher


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at']
    search_fields = ['name', 'address']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Établissement', {'fields': ('name', 'address')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'establishment', 'created_at']
    list_filter = ['establishment', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Classe', {'fields': ('name', 'establishment')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'matricule', 'classroom', 'created_at']
    list_filter = ['classroom', 'created_at']
    search_fields = ['user__username', 'user__email', 'matricule']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Étudiant', {'fields': ('user', 'classroom', 'matricule')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_student_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_student_name.short_description = 'Nom'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_teacher_name', 'speciality', 'get_classrooms_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'speciality']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Enseignant', {'fields': ('user', 'speciality', 'classrooms')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    filter_horizontal = ('classrooms',)
    
    def get_teacher_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_teacher_name.short_description = 'Nom'
    
    def get_classrooms_count(self, obj):
        return obj.classrooms.count()
    get_classrooms_count.short_description = 'Nombre de classes'
