from rest_framework.serializers import ModelSerializer

from apps.recipes.models import Ingredient, Favorite, Subscription, Purchase


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['recipe']

    def to_internal_value(self, data):
        data = {'recipe': data['id']}
        return super().to_internal_value(data)


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['author']

    def to_internal_value(self, data):
        data = {'author': data['id']}
        return super().to_internal_value(data)


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['recipe']

    def to_internal_value(self, data):
        data = {'recipe': data['id']}
        return super().to_internal_value(data)