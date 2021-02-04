from django.db import models
from django.urls import reverse
from pytils.translit import slugify

from authapp.models import HabrUser


class Category(models.Model):
    """Модель категории."""
    title = models.CharField(verbose_name='Название категории', max_length=50, unique=True)
    description = models.CharField(verbose_name='Описание категории', max_length=255, blank=True)
    slug = models.SlugField(null=False, unique=True)
    is_active = models.BooleanField(verbose_name='Категория активна', default=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_articles', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Article(models.Model):
    """Модель статьи (Хабр)."""
    ARTICLE_STATUS = [
        ('published', 'Опубликована'),
        ('draft', 'Черновик'),
        ('hidden', 'Скрыта'),
    ]

    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название статьи', max_length=255, unique=True)
    body = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='article_image', blank=True)
    status = models.CharField(verbose_name='Статус статьи', max_length=50, choices=ARTICLE_STATUS)
    slug = models.SlugField(null=False, unique=True)
    is_banned = models.BooleanField(verbose_name='Заблокировать статью', default=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
