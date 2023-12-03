from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, ListView
from taggit.models import Tag

from .forms import UserLoginForm, UserRegisterForm, ProfileForm, CreatePostForm, MailingForm, CreateCommentForm, \
    SharePostForm
from .models import Post, Comment, Category, Profile


class PostHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница'
        context['tags'] = Post.tags.all()
        context['posts_count'] = Post.objects.filter(is_published=True).count()
        return context

    def get_queryset(self):
        return Post.published.all()


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
        return Post.published.filter(category__slug=self.kwargs['category_slug']).select_related(
            'category')


class PostTag(ListView):
    model = Post
    template_name = 'blog/post_tag.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Посты по тегам'
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        context['posts_count'] = Post.objects.filter(tags__in=[tag]).count()
        return context

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags__in=[tag])


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


def send_mailing(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], from_email="totsamy.t@mail.ru",
                             recipient_list=User.objects.all().values_list('email', flat=True)
                             , fail_silently=False)
            if mail:
                messages.success(request, message="Рассылка произведена успешно")
                return redirect('home')
            else:
                messages.error(request, message="Ошибка рассылки")
        else:
            messages.error(request, message="Ошибка формы")
            return redirect("home")
    else:
        form = MailingForm()
    context = {
        'title': 'Рассылка',
        'form': form
    }

    return render(request, template_name='blog/mailing.html', context=context)


def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    print('Success')
    if request.method == "POST":
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    else:
        form = CreateCommentForm()

    context = {
        'post': post,
        'form': form
    }
    return render(request, template_name='blog/add_comment.html', context=context)


def share_post(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
        form = SharePostForm(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_absolute_url())
            cd = form.cleaned_data
            subject = f"{cd['sender_name']} {cd['sender_email']} рекомендует вам прочитать пост <b>{post.title}</b>"
            message = (f"Советую прочитать пост '{post.title}' {post_url} \n\n"
                       f"Комментарий: {cd['comment']}")
            mail = send_mail(subject=subject, message=message,
                             from_email="totsamy.t@mail.ru",
                             recipient_list=[form.cleaned_data['recipient_email']], fail_silently=False)
            if mail:
                messages.success(request, message="Письмо отправлено успешно")
                return redirect('home')
            else:
                messages.error(request, message="Ошибка отправки")
        else:
            messages.error(request, message="Ошибка формы")
            return redirect("home")
    else:
        form = SharePostForm()
    context = {
        'title': 'Поделиться постом',
        'form': form
    }

    return render(request, template_name='blog/share_email.html', context=context)
