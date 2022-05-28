from django.contrib import admin
from wishlist.models import Post, Tag


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag, TagAdmin)
