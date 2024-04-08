from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='8',
            invite_code='000000',
            is_superuser=True,
            is_staff=True,
        )
        user.set_password('1234')
        user.save()
