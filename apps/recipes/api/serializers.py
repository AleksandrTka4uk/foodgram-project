from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.recipes.models import Ingredient, Favorite


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
