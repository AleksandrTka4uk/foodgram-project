from django.urls import path, include
from apps.recipes.views import RecipeList, RecipeDetailView, AuthorRecipeList, FavoriteRecipeList, SubscriptionList, create_recipe, change_recipe, PurchasesView
from apps.recipes.api.views import AddFavorite, RemoveFavorite, AddSubscription, RemoveSubscription, GetIngredients, AddPurchases, RemovePurchases
from rest_framework.urlpatterns import format_suffix_patterns


view_patterns = [
    path('', RecipeList.as_view(), name="index"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name="recipe"),
    path('recipe/new/', create_recipe, name="create_recipe"),
    path('recipe/change/<int:recipe_id>', change_recipe, name="change_recipe"),
    path('author/<int:pk>/', AuthorRecipeList.as_view(), name="author"),
    path('favorites/', FavoriteRecipeList.as_view(), name="favorites"),
    path('subscriptions/', SubscriptionList.as_view(), name="subscription"),
    path('purchases/', PurchasesView.as_view(), name="purchases"),
]

api_patterns = [
    path('favorites/', AddFavorite.as_view()),
    path('favorites/<int:pk>/', RemoveFavorite.as_view()),
    path('subscriptions/', AddSubscription.as_view()),
    path('subscriptions/<int:pk>', RemoveSubscription.as_view()),
    path('ingredients', GetIngredients.as_view()),
    path('purchases/', AddPurchases.as_view()),
    path('purchases/<int:recipe_id>', RemovePurchases.as_view()),
]

urlpatterns = [
    path('', include(view_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns)))
]
