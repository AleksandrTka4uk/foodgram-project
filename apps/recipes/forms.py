from django.forms import (CheckboxSelectMultiple, ModelForm,
                          ModelMultipleChoiceField)
from django.shortcuts import get_object_or_404

from apps.recipes.models import Ingredient, Recipe, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'time', 'description', 'image']



