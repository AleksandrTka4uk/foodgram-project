# Generated by Django 3.2.2 on 2021-06-26 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20210614_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='author',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredients',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='in_recipes',
                to='recipes.ingredient'),
        ),
    ]