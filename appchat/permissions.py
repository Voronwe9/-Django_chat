from rest_framework import permissions
from django.utils import timezone


class IsAdult(permissions.BasePermission):
    """Проверяет, что пользователю есть 18+ лет"""

    message = "Только для пользователей старше 18 лет"

    def has_permission(self, request, view):
        if not request.user.birth_date:
            return False
        age = (timezone.now().date() - request.user.birth_date).days // 365
        return age >= 18


class IsAuthorOrAdmin(permissions.BasePermission):
    """Разрешает доступ только автору или администратору"""

    message = "Только автор или администратор могут выполнять это действие"

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff


class CanEditUser(permissions.BasePermission):
    """Пользователь может редактировать только свой профиль (или админ)"""

    message = "Вы можете редактировать только свой профиль"

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """Только админ может удалять/создавать, остальные — read-only"""

    message = "Только администратор может выполнять это действие"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class CanEditPost(permissions.BasePermission):
    message = ""

    def has_permission(self, request, view):
        # Проверка возраста
        age = (timezone.now().date() - request.user.birth_date).days // 365
        if age < 18:
            self.message = "Только для пользователей старше 18 лет"
            return False

        return True

    def has_object_permission(self, request, view, obj):
        # Проверка авторства/админки
        if obj.author != request.user and not request.user.is_staff:
            self.message = "Только автор или администратор могут редактировать"
            return False

        return True
