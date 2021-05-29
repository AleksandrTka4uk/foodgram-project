from django.urls import path, include
from apps.recipes.views import RecipeList, RecipeDetailView, AuthorRecipeList
from apps.recipes.api.views import AddFavorite
from rest_framework.urlpatterns import format_suffix_patterns


view_patterns = [
    path('', RecipeList.as_view(), name="index"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name="recipe"),
    path('author/<int:pk>/', AuthorRecipeList.as_view(), name="author"),
]

api_patterns = [
    path('favorites/', AddFavorite.as_view())
]

urlpatterns = [
    path('', include(view_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns)))
]

