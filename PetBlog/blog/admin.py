from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Profile, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'views',  'get_photo', 'status')
    list_editable = ('status',)
    list_display_links = ('title',)
    list_filter = ('title', 'category', 'tags')
    fields = (
        'title', 'slug', 'content', 'author', 'image', 'category', 'tags', 'comments', 'likes', 'views',
        'status')
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


# class TagAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     list_display_links = ('title',)
#     fields = ('title', 'slug')
#     prepopulated_fields = {'slug': ('title',)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_avatar', 'get_user_posts')
    list_display_links = ('user',)
    fields = ('user', 'about_me', 'avatar', 'get_user_posts')
    readonly_fields = ('get_user_posts',)

    def get_avatar(self, obj):

        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width = "50"')
        else:
            return "нет аватара"

    get_avatar.short_description = "Аватар"


class CommentAdmin(admin.ModelAdmin):
    fields = ('post', 'author', 'text', 'created_at', 'parent_comment')
    list_display = ('post', 'author')
    readonly_fields = ('created_at', )
    list_display_links = ('post', 'author')


admin.site.register(Post, PostAdmin)
# admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)
