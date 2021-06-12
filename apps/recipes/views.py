from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect, render
from apps.recipes.models import Recipe, User, Favorite, Subscription, Ingredient, RecipeIngredient, Tag
from apps.recipes.forms import CreateRecipeForm


class RecipeList(ListView):
    model = Recipe
    queryset = Recipe.objects.all()
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        tags_off = self.request.GET.getlist('tags_off', '')
        if tags_off:
            return qs.exclude(tag__id__in=tags_off)
        return qs


class FavoriteRecipeList(ListView):
    model = Recipe
    template_name = 'favorite.html'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        tags_off = self.request.GET.getlist('tags_off', '')
        if tags_off:
            return qs.filter(favorite__author=self.request.user).exclude(tag__id__in=tags_off)
        return qs.filter(favorite__author=self.request.user)


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


def get_tags(data):
    tags = []
    if data.get('breakfast'):
        tags.append('Завтрак')
    if data.get('lunch'):
        tags.append('Обед')
    if data.get('dinner'):
        tags.append('Ужин')
    tags = Tag.objects.filter(title__in=tags)
    return tags


def get_ingredients(data):
    ingredients = {}
    for key, value in data.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[value] = data[f'valueIngredient_{num}']
    return ingredients


def create_recipe(request):
    form = CreateRecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        data = request.POST.dict()
        tags = get_tags(data)
        recipe.tag.add(*tags)
        ingredients = get_ingredients(data)
        objs = []
        for title, count in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            objs.append(RecipeIngredient(recipe=recipe, ingredients=ingredient, count=count))
        RecipeIngredient.objects.bulk_create(objs)
        return redirect('index')
    return render(request, 'formRecipe.html', {'form': form})
