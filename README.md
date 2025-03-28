# Django Chat Project

Проект чата на Django с REST API и системой модерации.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
python manage.py makemigrations  # Создаем миграции на основе моделей
python manage.py migrate        # Применяем миграции к БД
```

### 3. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите логин, email и пароль для доступа к админке (`/admin`).

### 4. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

---

## 🔧 Администрирование

### Назначение администраторов

```bash
python manage.py promote_to_admin username
```

### Снятие прав админа

```bash
python manage.py demote_from_admin username
```

### Создание тестовых данных

```bash
python manage.py loaddata fixtures/initial_data.json
```

---

## 🌐 API Endpoints

| Метод | Эндпоинт         | Описание                                         |
| ----- | ---------------- | ------------------------------------------------ |
| GET   | `/api/posts/`    | Список всех постов                               |
| POST  | `/api/posts/`    | Создание нового поста (требуется аутентификация) |
| GET   | `/api/users/me/` | Профиль текущего пользователя                    |

---

## ⚙️ Настройки окружения

Создайте файл `.env` в корне проекта:

```ini
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
DB_NAME=chat_db
DB_USER=user
DB_PASSWORD=password
```

---

## 🛠️ Development

### Pre-commit хуки

Перед коммитом автоматически проверяются:

- Форматирование кода (Black)
- Стиль (flake8)
- Валидность миграций

Установка:

```bash
pre-commit install
```

---

## 📌 Важно

- Для доступа к админ-панели пользователь должен иметь флаги `is_staff=True` и `is_superuser=True`
- Все POST/PUT/DELETE запросы требуют аутентификации
- Логины/пароли тестовых пользователей: `moderator:qwerty123`
