from django.urls import path, include
from apps.recipes.views import RecipeList, RecipeDetailView, AuthorRecipeList, FavoriteRecipeList, SubscriptionList
from apps.recipes.api.views import AddFavorite, RemoveFavorite, AddSubscription, RemoveSubscription
from rest_framework.urlpatterns import format_suffix_patterns


view_patterns = [
    path('', RecipeList.as_view(), name="index"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name="recipe"),
    path('author/<int:pk>/', AuthorRecipeList.as_view(), name="author"),
    path('favorites/', FavoriteRecipeList.as_view(), name="favorites"),
    path('subscriptions/', SubscriptionList.as_view(), name="subscription"),
]

api_patterns = [
    path('favorites/', AddFavorite.as_view()),
    path('favorites/<int:pk>/', RemoveFavorite.as_view()),
    path('subscriptions/', AddSubscription.as_view()),
    path('subscriptions/<int:pk>', RemoveSubscription.as_view()),
]

urlpatterns = [
    path('', include(view_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns)))
]
