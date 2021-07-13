from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, CreateView

from apps.recipes.forms import RecipeForm
from apps.recipes.models import (Ingredient, Recipe, RecipeIngredient,
                                 Subscription, Tag, User)
from foodgram.settings import PAGINATE_BY


class IsFavoriteMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs


class IsPurchaseMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_purchase(user_id=self.request.user.id)
        )

        return qs


class BaseRecipeList(IsFavoriteMixin, IsPurchaseMixin, ListView):
    model = Recipe
    queryset = Recipe.objects.all()
    paginate_by = PAGINATE_BY


class RecipeList(BaseRecipeList):
    template_name = 'index.html'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     tags_off = self.request.GET.getlist('tags_off', '')
    #     if tags_off:
    #         return qs.exclude(tag__id__in=tags_off)
    #     return qs


class FavoriteRecipeList(LoginRequiredMixin, BaseRecipeList):
    template_name = 'favorite.html'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     tags_off = self.request.GET.getlist('tags_off', '')
    #     if tags_off:
    #         return qs.filter(favorite__user=self.request.user).exclude(
    #             tag__id__in=tags_off)
    #     return qs.filter(favorite__user=self.request.user)


class PurchasesView(LoginRequiredMixin, BaseRecipeList):
    template_name = 'purchases.html'


class SubscriptionList(LoginRequiredMixin, BaseRecipeList):
    template_name = 'myFollow.html'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class RecipeDetailView(IsFavoriteMixin, IsPurchaseMixin, DetailView):
    model = Recipe
    template_name = 'recipe_page.html'


class AuthorRecipeList(BaseRecipeList):
    template_name = 'authors_recipes.html'

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        return Recipe.objects.filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        context['author_full_name'] = author.get_full_name
        context['author_username'] = author.username
        context['author_id'] = author.id
        return context


@login_required
def create_recipe(request):
    form = RecipeForm(
        request.POST or None,
        request=request,
        files=request.FILES or None
    )
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'create_new_recipe.html', {'form': form})


@login_required
def change_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('change_recipe', recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        request=request,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        return redirect('recipe', pk=recipe_id)
    form = RecipeForm(instance=recipe)
    return render(request,
                  'change_recipe.html',
                  {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required
def remove_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    request.user.purchases.filter(recipe=recipe).delete()
    return redirect('purchases')


@login_required
def download_purchases(request):
    recipes_in_purchases = Recipe.objects.filter(
        in_purchases__user=request.user
    )
    ingredients = Ingredient.objects.filter(
        in_recipes__recipe__in=recipes_in_purchases).annotate(
        Sum('in_recipes__count')
    )
    file_data = ''
    for ingredient in ingredients:
        file_data += (f'{ingredient.title} '
                      f'({ingredient.dimension}) - '
                      f'{ingredient.in_recipes__count__sum} \n'
                      )
    response = HttpResponse(file_data,
                            content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="cart.txt"'
    return response


def page_not_found(request, exception):
    return render(
        request,
        '404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, '500.html', status=500)
