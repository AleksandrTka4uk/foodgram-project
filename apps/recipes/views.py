from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from apps.recipes.forms import RecipeForm
from apps.recipes.models import Ingredient, Recipe, Tag, User
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


class TagsFilterMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        tags_on = []
        for tag in Tag.objects.all():
            if self.request.GET.get(tag.slug, 'active') == 'active':
                tags_on.append(tag.slug)
        if tags_on:
            qs = (
                qs
                .select_related('author')
                .with_tags(tags_on=tags_on)
            )
        return qs


class BaseRecipeList(IsFavoriteMixin,
                     IsPurchaseMixin,
                     TagsFilterMixin,
                     ListView):
    model = Recipe
    queryset = Recipe.objects.all()
    paginate_by = PAGINATE_BY

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Http404:
            request_params = self.request.GET.copy()
            request_params['page'] = 'last'
            query_params = request_params.urlencode()
            return redirect(self.request.path + '?' + query_params)


class RecipeList(BaseRecipeList):
    template_name = 'recipes/index.html'


class RecipeDetailView(IsFavoriteMixin, IsPurchaseMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_page.html'


class FavoriteRecipeList(LoginRequiredMixin, BaseRecipeList):
    template_name = 'recipes/favorites.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(in_favorites__user=self.request.user)


class PurchasesView(LoginRequiredMixin, BaseRecipeList):
    template_name = 'recipes/purchases.html'

    def get_queryset(self):
        return self.request.user.purchases.all()


class SubscriptionList(LoginRequiredMixin, BaseRecipeList):
    template_name = 'recipes/subscriptions.html'
    paginate_by = 3

    def get_queryset(self):
        return self.request.user.subscriptions.all()


class AuthorRecipeList(BaseRecipeList):
    template_name = 'recipes/authors_recipes.html'

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        qs = super().get_queryset()
        return qs.filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, pk=self.kwargs['pk'])
        context['author'] = author
        return context


@login_required
def create_recipe(request):
    form = RecipeForm(
        request.POST or None,
        request=request,
        files=request.FILES or None
    )
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'recipes/recipe_form.html', {'form': form})


@login_required
def change_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('create_recipe')
    form = RecipeForm(
        request.POST or None,
        request=request,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('recipe', pk=recipe_id)
    form = RecipeForm(instance=recipe)
    return render(
        request,
        'recipes/recipe_form.html',
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
    ingredients = Ingredient.objects.filter(
        in_recipes__recipe__in_purchases__user=request.user).annotate(
        sum_ingredients=Sum('in_recipes__count')
    )
    file_data = ''
    for ingredient in ingredients:
        file_data += (f'{ingredient.title} '
                      f'({ingredient.dimension}) - '
                      f'{ingredient.sum_ingredients} \r\n'
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
