# авторизация по номеру телефона, а не по логину с паролем
from django.contrib.auth.backends import ModelBackend

from users.models import User


class PhoneBackend(ModelBackend):
    # происходит аутентификация
    def authenticate(self, request, phone=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
        return user

    # код, который получает пользоваткль по id
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
