import os
from functools import lru_cache

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, NotFound

from users.tasks import send_verify_code_for_number
from users.models import User, Code, Referrals
from users.validators import generate_unique_invite_code


# сервис для логина пользователя и для отправки кода подтверждения
class UserLoginService:

    # определение локальных свойств для класса
    def __init__(self, phone=None):
        self.__phone = phone
        self.validate()

    # валидация данных
    def validate(self):
        if not self.__phone:
            raise ValidationError({
                'error': 'Укажите номер телефона (phone)!'
            })

    # метод для запуска класса
    def execute(self):
        self.login()
        self.send_mail()

    # позволяет обращться к функции, как к свойству класса
    @property
    def _user(self):
        try:
            return User.objects.get(phone=self.__phone)
        except User.DoesNotExist:
            return None

    # функция, которая отвечает за создания пользователя, если его нет
    def login(self):
        user = self._user
        if user:
            return
        User.objects.create(
            phone=self.__phone,
            invite_code=generate_unique_invite_code(6),
            is_active=False
        )

    # функция, которая отправляет код верификации
    def send_mail(self):
        send_verify_code_for_number.apply_async(
            (self._user.id,),
            countdown=os.getenv(
                'COUNTDOWN_SEND_CODE',
                default=5
            )
        )


# сервис для верификации пользователя
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
        return self.verify()

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
        code.delete()
        token, _ = Token.objects.get_or_create(user=user)
        return token


# сервис для подписки на другого пользователя
class UserInviteCodeService:

    def __init__(self, user: User, invite_code: str):
        self.__user = user
        self.__invite_code = invite_code
        self.validate()

    def validate(self):
        if not self.__invite_code:
            raise ValidationError({
                'error': 'Укажите код приглашения (invite_code)!'
            })
        if Referrals.objects.filter(user=self.__user):
            raise ValidationError({
                "error": "Вы уже являетесь рефералом этого пользователя!"
            })
        if self._author == self.__user:
            raise ValidationError({
                "error": "Вы не можете подписаться на самого себя!"
            })
        if Referrals.objects.filter(
                user=self.__user,
                author=self._author
        ):
            raise ValidationError({
                "error": "Вы уже являетесь рефералом этого пользователя!"
            })

    @property
    @lru_cache # кэширует результат выполняемой функции
    def _author(self):
        try:
            return User.objects.get(invite_code=self.__invite_code)
        except User.DoesNotExist:
            raise NotFound({
                "error": "Такого пользователя не существует!"
            })

    def execute(self):
        self.referral()

    def referral(self):
        Referrals.objects.create(
            user=self.__user,
            author=self._author
        )
