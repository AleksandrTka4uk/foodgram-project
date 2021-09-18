from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, ValidationError

from apps.recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'time',
            'description',
            'image',
            'ingredients',
            'tag'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['ingredients'].required = False
        self.fields['tag'].required = False

    def clean_ingredients(self):
        data = self.data.dict()
        ingredients = {}
        for key, value in data.items():
            if key.startswith('nameIngredient'):
                try:
                    ingredient = Ingredient.objects.get(title=value)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        f'Ингредиента {value} не существует. '
                        f'Выберите ингредиенты из выпадающего списка.'
                    )
                num = key.split('_')[1]
                ingredients[ingredient] = data[f'valueIngredient_{num}']
        if not ingredients:
            raise ValidationError('Укажите ингредиенты для рецепта')
        return ingredients

    def clean_tag(self):
        data = self.data.keys()
        tags = Tag.objects.filter(title__in=data)
        if not tags:
            raise ValidationError('Укажите теги для рецепта')
        return tags

    def _save_m2m(self):
        tags = self.cleaned_data['tag']
        if self.instance.tag is None:
            self.instance.tag.add(*tags)
        else:
            self.instance.tag.set(tags)
        ingredients = self.cleaned_data['ingredients']
        objs = []
        for ingredient, count in ingredients.items():
            objs.append(
                RecipeIngredient(
                    recipe=self.instance,
                    ingredients=ingredient,
                    count=count
                )
            )
        if self.instance.with_ingredients is not None:
            self.instance.with_ingredients.all().delete()
        RecipeIngredient.objects.bulk_create(objs)
