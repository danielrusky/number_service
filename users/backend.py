from django.contrib.auth.backends import ModelBackend

from users.models import User


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
