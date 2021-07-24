# Generated by Django 3.2.2 on 2021-07-13 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0022_alter_tag_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='with_ingredients', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
