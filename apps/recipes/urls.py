from django.urls import path
from apps.recipes.views import RecipeList


urlpatterns = [
    path('', RecipeList.as_view(), name="index"),
]