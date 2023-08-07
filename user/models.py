from django.contrib.auth.models import AbstractUser
from django.db import models

# переменная для полей с нулевым значением
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Создаем пользователя через класс абстрактного пользователя без имени пользователя с авторизаией по почте"""
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='user/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
