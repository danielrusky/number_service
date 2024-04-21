import string

from config.celery import app
from users.models import Code, User
from utils.generate_string import generate_string


# задача в Celery, которая создает в админ панели код
@app.task
def send_verify_code_for_number(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return 'User with this id not found'

    # удаление предыдущего кода для подтверждения
    Code.objects.filter(user=user).delete()

    # создание нового кода для подтверждения
    Code.objects.create(
        user=user,
        code=generate_string(
            length=4,
            symbols=string.digits
        )
    )
