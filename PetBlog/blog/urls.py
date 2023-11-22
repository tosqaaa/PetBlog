from django.urls import path, include

from .views import PostDetail, CommentDetail, PostCategory, PostHome, PostTag

urlpatterns = [
    # path('', Home.as_view(), name='home')
     path('', PostHome.as_view(), name='home'),
     path("post/<str:post_slug>", PostDetail.as_view(), name='post'),
     path("comment/<int:pk>", CommentDetail.as_view(), name='comment'),
     path("category/<str:category_slug>", PostCategory.as_view(), name='category'),
     path("tag/<str:tag_slug>", PostTag.as_view(), name='tag'),
]