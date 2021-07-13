from django.forms import ModelForm, ValidationError
from django.shortcuts import get_object_or_404
from apps.recipes.models import Ingredient, Recipe, Tag, RecipeIngredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'time', 'description', 'image', 'ingredients', 'tag']

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
                num = key.split('_')[1]
                ingredients[value] = data[f'valueIngredient_{num}']
        if len(ingredients) == 0:
            raise ValidationError('Укажите ингредиенты для рецепта')
        return ingredients

    def clean_tag(self):
        data = self.data.keys()
        tags = Tag.objects.filter(title__in=data)
        if not tags:
            raise ValidationError('Укажите теги для рецепта')
        return tags

    def save(self, force_insert=False, force_update=False, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        ingredients = self.cleaned_data['ingredients']
        objs = []
        for title, count in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            objs.append(RecipeIngredient(recipe=recipe,
                                         ingredients=ingredient,
                                         count=count))
        RecipeIngredient.objects.bulk_create(objs)
        return recipe