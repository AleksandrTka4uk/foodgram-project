from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from apps.recipes.models import Recipe, User, Favorite, Subscription
from django.db.models import Exists, OuterRef


class RecipeList(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 6


class FavoriteRecipeList(ListView):
    model = Recipe
    template_name = 'favorite.html'
    paginate_by = 6

    def get_queryset(self):
        return Recipe.objects.filter(favorite__author=self.request.user)


class SubscriptionList(ListView):
    model = Recipe
    template_name = 'myFollow.html'
    paginate_by = 6

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'


class AuthorRecipeList(ListView):
    model = Recipe
    template_name = 'authorRecipe.html'
    paginate_by = 6

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        return Recipe.objects.filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        context['author_full_name'] = author.get_full_name
        context['author_id'] = author.id
        return context