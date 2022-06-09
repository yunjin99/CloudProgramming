import requests
from django import forms
from django.forms import ModelChoiceField

from .models import Post, Tag
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
        fields = ['link', 'price', 'memo', 'need', 'want']
        widgets = {
        'need': StarWidget,
        'want': StarWidget
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['price', 'memo', 'need', 'want']
        widgets = {
        'need': StarWidget,
        'want': StarWidget
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
