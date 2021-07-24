from django_filters import rest_framework as filters

from apps.recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = Ingredient
        fields = ['title']
