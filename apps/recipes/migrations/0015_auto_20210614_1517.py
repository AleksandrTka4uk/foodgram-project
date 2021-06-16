# Generated by Django 3.2.2 on 2021-06-14 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20210614_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterField(
            model_name='purchase',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_purchases', to='recipes.recipe'),
        ),
    ]
