from django.core.exceptions import ValidationError
from datetime import date
import re


def validate_password_complexity(value):
    if len(value) < 8:
        raise ValidationError("Пароль должен содержать минимум 8 символов")
    if not re.search(r"\d", value):
        raise ValidationError("Пароль должен содержать хотя бы 1 цифру")


def validate_email_domain(value):
    allowed_domains = ["mail.ru", "yandex.ru"]
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(
            f"Разрешены только домены: {', '.join(allowed_domains)}"
        )


def validate_adult(birth_date):
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    if age < 18:
        raise ValidationError(
            "Для создания постов необходимо быть старше 18 лет"
        )


def validate_title_words(value):
    forbidden_words = ["ерунда", "глупость", "чепуха"]
    for word in forbidden_words:
        if word in value.lower():
            raise ValidationError(f"Запрещённое слово в заголовке: {word}")
