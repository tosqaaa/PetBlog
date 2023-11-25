from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'views', 'is_published', 'get_photo',)
    list_editable = ('is_published',)
    list_display_links = ('title',)
    list_filter = ('title', 'category', 'tags')
    fields = (
        'title', 'slug', 'content', 'author', 'image', 'category', 'tags', 'comments', 'likes', 'views',
        'is_published')
    prepopulated_fields = {'slug': ('title',)}

    def get_photo(self, obj):

        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width = "50"')
        else:
            return "нет фото"

    get_photo.short_description = "Фото"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
