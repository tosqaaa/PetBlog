from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import PostDetail, CommentDetail, PostCategory, PostHome, user_logout, user_login, user_register, \
    edit_profile, UserProfile, create_post, send_mailing, add_comment, share_post, PostTag

urlpatterns = [
    # path('', Home.as_view(), name='home')
    path('', PostHome.as_view(), name='home'),
    path("post/<str:slug>/", PostDetail.as_view(), name='post'),
    path("comment/<int:pk>/", CommentDetail.as_view(), name='comment'),
    path("category/<str:category_slug>/", PostCategory.as_view(), name='category'),
    path("tag/<str:tag_slug>/", PostTag.as_view(), name='tag'),
    path("logout/", user_logout, name='logout'),
    path("login/", user_login, name='login'),
    path("register/", user_register, name='register'),
    path("edit-profile/", edit_profile, name='edit_profile'),
    path("create-post/", create_post, name='create_post'),
    path("profile/<str:username>/", UserProfile.as_view(), name='profile'),
    path("mailing/", send_mailing, name='mailing'),
    path("add_comment/<str:slug>/", add_comment, name='add_comment'),
    path("share_post/<str:slug>/", share_post, name='share_post'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
