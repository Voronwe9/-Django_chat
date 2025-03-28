from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Назначает пользователя администратором"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.get(username=options["username"])
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(f"Пользователь {user.username} теперь админ")
