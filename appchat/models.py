from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .validators import (
    validate_password_complexity,
    validate_email_domain,
    validate_adult,
    validate_title_words,
)


class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями.
    """
    phone = models.CharField(
        max_length=20, verbose_name="Номер телефона", blank=True, null=True
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        help_text="Обязательное поле. Формат: ГГГГ-ММ-ДД",
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата редактирования"
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email_domain],
        help_text="Только адреса @mail.ru или @yandex.ru",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        """
        Сохраняет пользователя, предварительно проверяя сложность пароля.
        """
        if self.password:
            validate_password_complexity(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращает имя пользователя.
        """
        return self.username


class Post(models.Model):
    """
    Модель поста с заголовком, текстом, изображением и автором.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        validators=[validate_title_words],
    )
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(
        upload_to="posts/", verbose_name="Изображение", blank=True, null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата редактирования"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def clean(self):
        """
        Проверяет, что автор поста является совершеннолетним.
        """
        if self.author.birth_date:
            validate_adult(self.author.birth_date)

    def __str__(self):
        """
        Возвращает заголовок поста.
        """
        return self.title


class Comment(models.Model):
    """
    Модель комментария к посту.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата редактирования"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self):
        """
        Возвращает строковое представление комментария.
        """
        return f'Комментарий от {self.author.username} к посту "{self.post.title}"'  # noqa: E501
