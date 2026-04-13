from rest_framework import serializers
from .models import Establishment, Classroom, Student, Teacher


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ['id', 'name', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClassroomSerializer(serializers.ModelSerializer):
    establishment_name = serializers.CharField(source='establishment.name', read_only=True)
    
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'establishment', 'establishment_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'classroom', 'classroom_name', 'matricule', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    classrooms = ClassroomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'classrooms', 'speciality', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
