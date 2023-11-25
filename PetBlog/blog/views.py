from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .forms import UserLoginForm, UserRegisterForm
from .models import Post, Comment, Category, Tag


class PostHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница'
        context['posts_count'] = Post.objects.filter(is_published=True).count()
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
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['category_slug'])
        context['category_selected_slug'] = self.kwargs['category_slug']
        context['posts_count'] = Post.objects.filter(is_published=True,
                                                     category__slug=self.kwargs['category_slug']).count()
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True, category__slug=self.kwargs['category_slug']).select_related(
            'category')


class PostTag(ListView):
    model = Post
    template_name = 'blog/post_tag.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        context['posts_count'] = Post.objects.filter(is_published=True, tags__slug=self.kwargs['tag_slug']).count()
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True, tags__slug=self.kwargs['tag_slug'])


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, message='Вы успешно вошли в аккаунт.')
            return redirect('home')
        else:
            messages.error(request, message='Произошла ошибка входа.')
    else:
        form = UserLoginForm()
    context = {'title': 'Вход',
               'form': form}
    return render(request, template_name='blog/login.html', context=context)


def user_logout(request):
    logout(request)
    messages.success(request, message='Вы успешно вышли из аккаунта.')
    return redirect('home')


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, message='Вы успешно зарегистрировались.')
            return redirect('home')
        else:
            messages.error(request, message='Ошибка регистрации.')

    else:
        form = UserRegisterForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, template_name='blog/register.html', context=context)
