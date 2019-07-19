from django import forms
from .models import Post, Like


class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ('title', 'text', 'date')

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['user','post']