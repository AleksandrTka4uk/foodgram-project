# Generated by Django 3.2.2 on 2021-05-29 16:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_auto_20210529_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='recipes', to=settings.AUTH_USER_MODEL,
                verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(max_length=2000,
                                   verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveSmallIntegerField(verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='author',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='subscriber',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Подписчик')),
            ],
        ),
    ]
