from django.urls import path
from api.apps import ApiConfig
from api.views import (
    UserProfileAPIView,
    UserLoginAPIView,
    UserVerifyAPIView
)

app_name = ApiConfig.name

urlpatterns = [
    path(
        'users/<int:user_id>/profile/',
        UserProfileAPIView.as_view(),
        name='user_profile'
    ),
    path(
        'users/login/',
        UserLoginAPIView.as_view(),
        name='user_login'
    ),
    path(
        'users/verify/',
        UserVerifyAPIView.as_view(),
        name='user_verify'
    )
]
