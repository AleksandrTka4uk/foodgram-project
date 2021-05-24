from django.views.generic import ListView, DetailView
from apps.recipes.models import Recipe


class RecipeList(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 6


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'