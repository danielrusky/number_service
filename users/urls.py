from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import HomePageView, UserLoginView, UserVerifyView

app_name = UsersConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/verify/', UserVerifyView.as_view(), name='login_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
