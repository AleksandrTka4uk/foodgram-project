from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

User = get_user_model()


class Tag(models.Model):
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    SUPPER = 'Ужин'
    TAG_CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (SUPPER, 'Ужин'),
    ]
    title = models.CharField(
        max_length=50,
        choices=TAG_CHOICES,
        verbose_name='Название'
    )

    color = models.CharField(
        max_length=30,
        default='green',
        verbose_name='Цвет'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


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


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
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
        verbose_name='Время приготовления'
    )
    slug = models.SlugField()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('recipe', args=[self.id])

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='in_recipes',
        verbose_name='Ингредиент'
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


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
        # related_name="author",
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        UniqueConstraint(
            name='unique_subscription',
            fields=['user', 'author']
        )


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        related_name='purchases',
        on_delete=models.CASCADE,
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
