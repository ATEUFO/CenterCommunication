from django import forms
from .models import Post, PostMedia
from apps.academic.models import Classroom

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'classroom', 'target_user', 'expires_at']
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.role == 'TEACHER':
                # Teacher can only post in their assigned classes
                self.fields['classroom'].queryset = user.teacher_profile.classrooms.all()
                self.fields['post_type'].choices = [('CLASS', 'Classe')]
                self.fields['post_type'].initial = 'CLASS'


class PostMediaForm(forms.ModelForm):
    class Meta:
        model = PostMedia
        fields = ['file', 'media_type']
