# Generated by Django 3.1.5 on 2021-02-17 09:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0003_auto_20210211_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('published', 'Опубликована'), ('draft', 'Черновик'), ('hidden', 'Удалено'), ('moderation', 'На модерации')], max_length=50, verbose_name='Статус статьи'),
        ),
    ]
