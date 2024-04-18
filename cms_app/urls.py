from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, PostView, PublicPost, PostUpdateDelete, UserInfoView, LikeView

urlpatterns = [
    path('accounts', RegisterView.as_view()),   # create account
    path('accounts/login', LoginView.as_view()),   # Perform login and return a token for user authentication
    path('me/', UserInfoView.as_view()),
    path('blog/', PostView.as_view()),   # user blog
    path('blog/<uuid:uid>', PostUpdateDelete.as_view()), # blog update delete
    path('g/blog/', PublicPost.as_view()),   # user blog
    path('like/<uuid:uid>', LikeView.as_view(), name='like_post')
]