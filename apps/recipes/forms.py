from django.forms import (CheckboxSelectMultiple, ModelForm,
                          ModelMultipleChoiceField)
from django.shortcuts import get_object_or_404

from apps.recipes.models import Ingredient, Recipe, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'time', 'description', 'image']

        # fields = ['title', 'tag', 'time', 'description', 'image']

    # tag = ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=CheckboxSelectMultiple(attrs={'class': 'tags__checkbox tags__checkbox_style_orange'}),
    # )

    # def clean_ingredients(self):
    #     # data = self.cleaned_data['ingredients']
    #     data = get_object_or_404(Ingredient, title='авокадо')
    #     if data == "":
    #         raise forms.ValidationError("Заполните поле ингредиенты")
    #     self.cleaned_data['ingredients'] = data
    #     return data

