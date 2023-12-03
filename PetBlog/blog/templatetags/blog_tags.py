from django import template
from taggit.models import Tag

from ..models import Category, Comment

register = template.Library()


@register.inclusion_tag(filename='blog/list_categories.html')
def show_categories(category_selected_slug=None):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    if category_selected_slug is None:
        context['is_home_page'] = True
    else:
        context['category_selected_slug'] = category_selected_slug

    return context


@register.inclusion_tag(filename='blog/list_tags.html')
def show_tags():
    tags = Tag.objects.all()
    return {'tags': tags}


# @register.inclusion_tag(filename='blog/list_comments.html')
# def show_comments(post_slug):
#     comments = Comment.objects.filter(post__slug=post_slug)
#     return {'comments': comments}
