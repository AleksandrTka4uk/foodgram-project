from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.recipes.api.views import (AddFavorite, AddPurchases, AddSubscription,
                                    GetIngredients, RemoveFavorite,
                                    RemovePurchases, RemoveSubscription)
from apps.recipes.views import (AuthorRecipeList, FavoriteRecipeList,
                                PurchasesView, RecipeDetailView, RecipeList,
                                SubscriptionList, change_recipe, create_recipe,
                                delete_recipe, download_purchases,
                                remove_purchase)

view_patterns = [
    path('', RecipeList.as_view(), name='index'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe'),
    path('recipe/new/', create_recipe, name='create_recipe'),
    path('recipe/change/<int:recipe_id>', change_recipe, name='change_recipe'),
    path('recipe/delete/<int:recipe_id>', delete_recipe, name='delete_recipe'),
    path('author/<int:pk>/', AuthorRecipeList.as_view(), name='author'),
    path('favorites/', FavoriteRecipeList.as_view(), name='favorites'),
    path('subscriptions/', SubscriptionList.as_view(), name='subscription'),
    path('purchases/', PurchasesView.as_view(), name='purchases'),
    path('purchases/download', download_purchases, name='download_purchases'),
    path('purchases/<int:recipe_id>',
         remove_purchase, name='remove_purchases'),
]

api_patterns = [
    path('favorites/', AddFavorite.as_view()),
    path('favorites/<int:pk>/', RemoveFavorite.as_view()),
    path('subscriptions/', AddSubscription.as_view()),
    path('subscriptions/<int:pk>', RemoveSubscription.as_view()),
    path('ingredients', GetIngredients.as_view()),
    path('purchases/', AddPurchases.as_view()),
    path('purchases/<int:recipe_id>',
         RemovePurchases.as_view(), name='remove_purchase'),
]

urlpatterns = [
    path('', include(view_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns)))
]
