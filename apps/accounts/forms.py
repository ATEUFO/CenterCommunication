from django import forms
from django.contrib.auth import get_user_model
from .models import User
from apps.academic.models import Student, Teacher, Classroom

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['classroom', 'matricule']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['classrooms', 'speciality']
        widgets = {
            'classrooms': forms.CheckboxSelectMultiple(),
        }
