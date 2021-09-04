from typing import Optional

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (CheckConstraint, Exists, F, OuterRef, Q,
                              UniqueConstraint)
from django.urls import reverse

User = get_user_model()


class TagTitle(models.TextChoices):
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    DINNER = 'Ужин'


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        choices=TagTitle.choices,
        default=TagTitle.BREAKFAST,
        verbose_name='Название'
    )

    color = models.CharField(
        max_length=30,
        default='green',
        verbose_name='Цвет'
    )

    slug = models.SlugField(
        max_length=50,
        default='breakfast'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.title}'


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    dimension = models.CharField(
        max_length=100,
        verbose_name='Мера измерения'
    )

    def __str__(self):
        return f'{self.title}, {self.dimension}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeQuerySet(models.QuerySet):
    def with_is_favorite(self, user_id: Optional[int]):
        return self.annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user_id=user_id,
                    recipe_id=OuterRef('pk'),
                ),
            )
        )

    def with_is_purchase(self, user_id: Optional[int]):
        return self.annotate(
            is_purchase=Exists(
                Purchase.objects.filter(
                    user_id=user_id,
                    recipe_id=OuterRef('pk'),
                ),
            )
        )

    def without_tags(self, tags_off):
        return self.exclude(tag__title__in=tags_off)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Файл с изображением'
    )
    description = models.TextField(
        max_length=2000,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть нулевым')
        ]
    )
    slug = models.SlugField()
    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('recipe', args=[self.id])


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='with_ingredients',
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='in_recipes',
        verbose_name='Ингредиент'
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество не может быть нулевым')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                name='unique_favorite',
                fields=['user', 'recipe']
            )]


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_subscriptions',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                name='unique_subscription',
                fields=['user', 'author']
            ),
            CheckConstraint(
                check=~Q(author=F('user')),
                name='user_and_author_not_equal'
            )
        ]


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_purchases',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            UniqueConstraint(
                name='unique_purchase',
                fields=['user', 'recipe']
            )]
