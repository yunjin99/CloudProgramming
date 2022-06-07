import os.path

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
# from markdown import markdown
# from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/wishlist/tag/{self.slug}"



class Post(models.Model):
    title = models.CharField(max_length=30)
    price = models.CharField(max_length=30) # int 값 입력

    # hook_msg = models.TextField(blank=True)

    head_image = models.ImageField(upload_to='wishlist/images/%Y/%m/%d/', blank=True)
    link = models.TextField()
    memo = models.TextField()
    need = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    want = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # methods
    # 기본으로 있는 __str__ 메소드를 오버라이드
    def __str__(self):
        return f'[{self.pk}] [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f"/wishlist/{self.pk}/"



