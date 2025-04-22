from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Админка для кастомной модели пользователя.

    Наследуется от стандартного UserAdmin, добавляет:
    - отображение номера телефона и даты рождения;
    - отображение в списке полей: username, email, birth_date, is_staff.
    """
    list_display = ("username", "email", "birth_date", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("phone", "birth_date")}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для модели Post.

    Функционал:
    - отображение заголовка, ссылки на автора, даты создания;
    - фильтрация по дате создания (в т.ч. с календарём);
    - поиск по заголовку и имени автора;
    - сортировка по имени автора.
    """
    list_display = ["title", "author_link", "created_at"]


    list_filter = [
        "created_at",  
        ("created_at", admin.DateFieldListFilter),
    ]


    date_hierarchy = "created_at"

    def author_link(self, obj):
    """
    Возвращает HTML-ссылку на страницу редактирования автора поста.

    Args:
        obj (Post): объект поста.

    Returns:
        str: HTML-ссылка на страницу пользователя в админке.
    """
        url = reverse("admin:appchat_user_change", args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)

    author_link.short_description = "Автор"
    author_link.admin_order_field = "author__username" 


    search_fields = ["title", "author__username"]
