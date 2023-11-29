from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, FormView

from .forms import UserLoginForm, UserRegisterForm, ProfileForm, CreatePostForm
from .models import Post, Comment, Category, Tag, Profile


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
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пост'
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class CommentDetail(DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'blog/comment_detail.html'
    slug_field = 'slug'


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


def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, message="Профиль успешно отредактирован")
            return redirect('home')
        else:
            messages.error(request, message="Ошибка редактирования профиля")
    else:
        form = ProfileForm()

    context = {
        'title': 'Редактирование профиля',
        'form': form
    }
    return render(request, template_name='blog/edit_profile.html', context=context)


class UserProfile(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'blog/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['user_posts'] = self.object.get_user_posts()
        return context

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        return profile


class CreatePost(FormView):
    form_class = CreatePostForm
    template_name = 'blog/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            messages.success(request, message='Пост успешно создан')
            return redirect('home')

        else:
            messages.error(request, message='Ошибка создания поста')
    form = CreatePostForm()
    context = {
        'title': 'Создание поста',
        'form': form
    }
    return render(request, template_name='blog/create_post.html', context=context)
