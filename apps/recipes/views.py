from django.views.generic import ListView
from apps.recipes.models import Recipe


class RecipeList(ListView):
    model = Recipe
    template_name = 'indexNotAuth.html'