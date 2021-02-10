from django.contrib.auth.models import AbstractUser
from django.db import models


class HabrUser(AbstractUser):
    """
    Модель пользователя.
    Добавлены поля фотографии, возраста и раздела о себе.
    """
    email = models.EmailField(verbose_name='Электронная почта', unique=True, blank=False)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18)
    bio = models.TextField(verbose_name='"О себе"', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
