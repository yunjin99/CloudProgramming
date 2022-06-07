from django import forms

from .models import Post
from .widgets import StarWidget

# 생략

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['link', 'price', 'memo', 'need', 'want', 'tags']
        widgets = {
            'need': StarWidget,
            'want': StarWidget
        }