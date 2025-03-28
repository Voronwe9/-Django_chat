from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, User
from django.contrib.auth.admin import UserAdmin


# 1. Регистрируем кастомную модель User с UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "birth_date", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("phone", "birth_date")}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author_link", "created_at"]

    # Фильтрация по дате создания
    list_filter = [
        "created_at",  # Простой фильтр по дате
        ("created_at", admin.DateFieldListFilter),
    ]

    # Навигация по датам (календарь над списком)
    date_hierarchy = "created_at"

    # Кликабельная ссылка на автора
    def author_link(self, obj):
        url = reverse("admin:appchat_user_change", args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)

    author_link.short_description = "Автор"
    author_link.admin_order_field = "author__username"  # Сортировка по автору

    # Поиск по заголовку и автору
    search_fields = ["title", "author__username"]
