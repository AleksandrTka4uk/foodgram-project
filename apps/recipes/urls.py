from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.recipes.api.views import (FavoritesViewSet, IngredientsViewSet,
                                    PurchaseViewSet, SubscriptionViewSet)
from apps.recipes.views import (AuthorRecipeList, FavoriteRecipeList,
                                PurchasesView, RecipeDetailView, RecipeList,
                                SubscriptionList, change_recipe, create_recipe,
                                delete_recipe, download_purchases,
                                remove_purchase)

api_v1_router = DefaultRouter()
api_v1_router.register('favorites', FavoritesViewSet, basename='favorites')
api_v1_router.register('subscriptions', SubscriptionViewSet,
                       basename='subscriptions')
api_v1_router.register('purchases', PurchaseViewSet, basename='purchases')
api_v1_router.register('ingredients', IngredientsViewSet,
                       basename='ingredients')


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


urlpatterns = [
    path('', include(view_patterns)),
    path('api/', include(api_v1_router.urls))
]
