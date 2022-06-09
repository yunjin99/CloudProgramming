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
        # tags = Tag.objects.filter(author = Post.author)
        fields = ['link', 'price', 'memo', 'need', 'want']
        widgets = {
        'need': StarWidget,
        'want': StarWidget
        }

    # def __init__(self, *args, **kwargs):
    #     super(PostByLinkForm, self).__init__(*args, **kwargs)
    #     self.fields['tags'] = ModelChoiceField(queryset=Tag.objects.filter(author = ))

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
