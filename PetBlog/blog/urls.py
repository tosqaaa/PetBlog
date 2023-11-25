from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import PostDetail, CommentDetail, PostCategory, PostHome, PostTag, user_logout, user_login, user_register

urlpatterns = [
    # path('', Home.as_view(), name='home')
    path('', PostHome.as_view(), name='home'),
    path("post/<str:post_slug>", PostDetail.as_view(), name='post'),
    path("comment/<int:pk>", CommentDetail.as_view(), name='comment'),
    path("category/<str:category_slug>", PostCategory.as_view(), name='category'),
    path("tag/<str:tag_slug>", PostTag.as_view(), name='tag'),
    path("logout", user_logout, name='logout'),
    path("login", user_login, name='login'),
    path("register", user_register, name='register'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)