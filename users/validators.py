from django.core.exceptions import ValidationError

from users.models import User
from utils.generate_string import generate_string


def generate_unique_invite_code(length):
    for i in range(10):
        invite_code = generate_string(length)
        if not User.objects.filter(invite_code=invite_code):
            return invite_code
    raise ValidationError("Что-то пошло не так, попробуйте еще раз")
