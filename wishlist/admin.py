from django.contrib import admin

from wishlist.forms import PostForm
from wishlist.models import Post, Tag


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    form = PostForm

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
