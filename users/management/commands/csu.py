from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            phone='8',
            invite_code='000000',
            is_superuser=True,
            is_staff=True,
        )
        Token.objects.get_or_create(
            user=user,
            key='daae7948824525c1b8b59f9d5a75'
        )
        user.set_password('1234')
        user.save()
