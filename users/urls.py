from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import (
    HomePageView,
    UserLoginView,
    UserVerifyView,
    UserInviteCodeView
)

app_name = UsersConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('users/login/verify/', UserVerifyView.as_view(), name='login_verify'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/invite_code/', UserInviteCodeView.as_view(), name='invite_code'),
]
