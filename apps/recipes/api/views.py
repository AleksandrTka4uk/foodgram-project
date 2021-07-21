from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework import mixins, viewsets


from apps.recipes.api.serializers import (IngredientSerializer,
                                          FavoriteSerializer,
                                          PurchaseSerializer,
                                          SubscriptionSerializer)
from apps.recipes.models import Ingredient


SUCCESS = JsonResponse({'success': True}, status=status.HTTP_200_OK)
FAIL = JsonResponse({'success': False}, status=status.HTTP_200_OK)


class CreateAndDeleteViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return SUCCESS

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return SUCCESS


class FavoritesViewSet(CreateAndDeleteViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return self.request.user.favorites.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 recipe__pk=self.kwargs['pk'])


class SubscriptionViewSet(CreateAndDeleteViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 author__pk=self.kwargs['pk'])


class PurchaseViewSet(CreateAndDeleteViewSet):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return self.request.user.purchases.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 recipe__pk=self.kwargs['pk'])


class IngredientsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        text = self.request.GET.get('query')
        if text:
            ingredients = Ingredient.objects.filter(title__contains=text)
        else:
            ingredients = Ingredient.objects.all()
        return ingredients
