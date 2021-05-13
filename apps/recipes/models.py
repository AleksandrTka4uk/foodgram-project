from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200
    )
    measure = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f'{self.title}, {self.measure}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=100
    )
    image = models.ImageField()
    description = models.TextField(
        max_length=2000
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tag = models.ManyToManyField(Tag)
    time = models.PositiveSmallIntegerField()
    slug = models.SlugField()

    def __str__(self):
        return f'{self.title}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
