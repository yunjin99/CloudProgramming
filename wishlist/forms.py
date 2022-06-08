from django import forms

from .models import Post
from .widgets import StarWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'need': StarWidget,
            'want': StarWidget
        }


class PostByLinkForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['link', 'price', 'memo', 'need', 'want', 'tags']
        widgets = {
        'need': StarWidget,
        'want': StarWidget
    }
