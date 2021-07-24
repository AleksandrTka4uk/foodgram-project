# Generated by Django 3.2.2 on 2021-07-01 19:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20210630_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Время приготовления не может быть нулевым')], verbose_name='Время приготовления'),
        ),
    ]
