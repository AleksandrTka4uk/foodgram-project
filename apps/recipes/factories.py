from random import choice

import factory
from factory import fuzzy

from apps.users.factories import UserFactory

from . import models


class BaseRecipeFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    image = factory.django.ImageField(width=1000)
    description = factory.Faker('text')
    time = fuzzy.FuzzyInteger(10, 120)

    class Meta:
        model = models.Recipe

    @factory.post_generation
    def tag(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tag.add(*extracted)


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory(BaseRecipeFactory)
    count = fuzzy.FuzzyInteger(50, 500)

    class Meta:
        model = models.RecipeIngredient

    @factory.lazy_attribute
    def ingredients(self):
        return choice(models.Ingredient.objects.all())


class RecipeFactory(BaseRecipeFactory):

    ingredients_1 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredients_2 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredients_3 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredients_4 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )

