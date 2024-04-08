from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """ Это модель пользователя """
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    invite_code = models.CharField(max_length=6, unique=True, verbose_name='Инвайт код')
    referrals = models.ManyToManyField(
        'self',
        verbose_name='Мои рефералы'
    )
    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        db_table = 'users'
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Code(models.Model):
    """ ? """
    code = models.CharField(max_length=4, unique=True, verbose_name='Кода авторизации')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='codes',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f"{self.code} - {self.user}"

    class Meta:
        db_table = 'codes'
        ordering = ['-id']
        verbose_name = 'Код авторизации'
        verbose_name_plural = 'Коды авторизации'