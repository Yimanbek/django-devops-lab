"""
URL configuration for django_devops_lab project.

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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django-DevOps-Lab",
        description='Less for up my hard skills, stack: CI/CD, Pytest, RabbitMQ, Celery, Django-DRF and use my SentimentModel for predict reviews',
        default_version='v1'
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
    path('docs/', schema_view.with_ui('swagger'))
]
