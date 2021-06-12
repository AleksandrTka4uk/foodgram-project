from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.shortcuts import get_object_or_404
from apps.recipes.models import Recipe, Tag, Ingredient


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

