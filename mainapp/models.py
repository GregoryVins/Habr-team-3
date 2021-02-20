from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from ckeditor.fields import RichTextField

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
        ('hidden', 'Удалено'),
        ('moderation', 'На модерации'),
    ]

    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(verbose_name='Название статьи', max_length=255, unique=True)
    body = RichTextField(verbose_name='Содержимое статьи', blank=True, null=True)
    image = models.ImageField(upload_to='article_image', blank=True)
    status = models.CharField(verbose_name='Статус статьи', max_length=50, choices=ARTICLE_STATUS)
    slug = models.SlugField(null=False, unique=True)
    is_banned = models.BooleanField(verbose_name='Заблокировать статью', default=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    liked_by = models.ManyToManyField(HabrUser, related_name='liked_articles', blank=True)

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

    def get_piece_body(self):
        return self.body[:500]

    def get_update_article(self):
        return reverse('user_update_article', kwargs={'slug': self.slug})

    def get_remove_article(self):
        return reverse('user_remove_article', kwargs={'slug': self.slug})

    def get_banned_article(self):
        return reverse('ban_article', kwargs={'slug': self.slug})

    def get_like(self):
        return reverse('add_like', kwargs={'pk': self.pk})


class Comment(models.Model):
    """Модель комментария."""
    body = RichTextField(config_name='comment_form', verbose_name='', blank=True, null=True)
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Комментарий активен', default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Пользователь: "{self.user}", статья: "{self.article}", комментарий: "{self.body[:20]}..."'
