from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Кастомная команда управления для назначения пользователя администратором.

    Позволяет назначить указанного пользователя администратором системы,
    устанавливая флаги is_staff и is_superuser в True.

    Пример использования:
        python manage.py make_admin username
    """
    help = "Назначает пользователя администратором"

    def add_arguments(self, parser):
        """
        Добавляет аргументы для команды.

        Args:
            parser: Парсер аргументов командной строки.
        """
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        """
        Основная логика команды.

        Получает пользователя по имени, устанавливает права администратора
        и сохраняет изменения.

        Args:
            *args: Дополнительные позиционные аргументы.
            **options: Аргументы командной строки.
        """
        User = get_user_model()
        user = User.objects.get(username=options["username"])
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(f"Пользователь {user.username} теперь админ")
