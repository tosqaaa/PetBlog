from django.views.generic import DetailView, ListView

from .models import Post, Comment, Category, Tag


class PostHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница'
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class CommentDetail(DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'blog/comment_detail.html'


class PostCategory(ListView):
    model = Post
    template_name = 'blog/post_category.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['category_slug'])
        context['category_selected'] = self.kwargs['category_slug']
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True, category__slug=self.kwargs['category_slug']).select_related(
            'category')


class PostTag(ListView):
    model = Post
    template_name = 'blog/post_category.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['tag_slug'])

    def get_queryset(self):
        return Post.objects.filter(is_published=True, tag_slug=self.kwargs['tag_slug']).select_related('tag')

# class Home(ListView):
#     template_name = 'templates/index.html'
