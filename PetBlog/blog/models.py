from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=128, unique=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse(viewname='category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=128, unique=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse(viewname='tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.PROTECT, related_name='post_comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT,
                                       related_name='replies', verbose_name='Родительский комментарий')

    def get_absolute_url(self):
        return reverse(viewname='comment', kwargs={'comment_pk': self.pk})

    def __str__(self):
        return f'{self.author.username} - {self.text[:50]}...'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']


class Post(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=128, unique=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Контент')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True, verbose_name='Изображение')
    author = models.ForeignKey(User, related_name='post_author', on_delete=models.PROTECT, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name='post_comment')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def get_absolute_url(self):
        return reverse(viewname='post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['title']
