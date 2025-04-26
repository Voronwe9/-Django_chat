"""
URL configuration for projectchat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Chat API",
        default_version="v1",
        description="Документация для API чата",
    ),
    public=True,
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger",
    ),
    """
    Endpoint для доступа к Swagger UI - интерактивной документации API.
    Позволяет тестировать API endpoints прямо из браузера.
    """
    
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    """
    Endpoint для доступа к ReDoc - альтернативному представлению документации API.
    Предоставляет более читабельное, но менее интерактивное отображение API.
    """
    
    path("admin/", admin.site.urls),
    """
    Endpoint для доступа к Django admin панели.
    Используется для управления данными и пользователями администраторами системы.
    """
    
    path("api/", include("appchat.urls")),
    """
    Базовый endpoint для всех API routes чат-приложения.
    Все остальные API endpoints определены в appchat.urls.
    """
    
    path("api-token-auth/", views.obtain_auth_token),
    """
    Endpoint для аутентификации пользователей и получения токена.
    Принимает username и password, возвращает auth token для использования в API.
    """
]
