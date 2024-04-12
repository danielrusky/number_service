import os
from functools import lru_cache

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, NotFound

from users.tasks import send_verify_code_for_number
from users.models import User, Code
from users.validators import generate_unique_invite_code


class UserLoginService:

    def __init__(self, phone=None):
        self.__phone = phone
        self.validate()

    def validate(self):
        if not self.__phone:
            raise ValidationError({
                'error': 'Укажите номер телефона (phone)!'
            })

    def execute(self):
        self.login()
        self.send_mail()

    @property
    def _user(self):
        try:
            return User.objects.get(phone=self.__phone)
        except User.DoesNotExist:
            return None

    def login(self):
        user = self._user
        if user:
            return
        User.objects.create(
            phone=self.__phone,
            invite_code=generate_unique_invite_code(6),
            is_active=False
        )

    def send_mail(self):
        send_verify_code_for_number.apply_async(
            (self._user.id,),
            countdown=os.getenv(
                'COUNTDOWN_SEND_CODE',
                default=5
            )
        )


class UserVerifyService:

    def __init__(self, phone=None, code=None):
        self.__phone = phone
        self.__code = code
        self.validate()

    def validate(self):
        if not self.__phone:
            raise ValidationError({
                'error': 'Укажите номер телефона (phone)!'
            })
        if not self.__code:
            raise ValidationError({
                'error': 'Укажите код подтверждения (code)!'
            })

    def execute(self):
        self.verify()

    @property
    @lru_cache
    def _user(self):
        try:
            return User.objects.get(phone=self.__phone)
        except User.DoesNotExist:
            raise NotFound({
                'detail': 'Такого пользователя не существует!'
            })

    @property
    def _code(self):
        try:
            return Code.objects.get(
                user=self._user,
                code=self.__code
            )
        except Code.DoesNotExist:
            raise NotFound({
                'detail': 'Вы ввели не правильный код!'
            })

    def verify(self):
        code = self._code
        user = self._user
        user.is_active = True
        user.save()
        Token.objects.get_or_create(user=user)
        code.delete()
