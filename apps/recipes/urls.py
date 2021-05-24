from django.urls import path
from apps.recipes.views import RecipeList,RecipeDetailView


urlpatterns = [
    path('', RecipeList.as_view(), name="index"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name="recipe"),
]