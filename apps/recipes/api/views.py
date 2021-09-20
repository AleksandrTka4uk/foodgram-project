from django.db import DatabaseError, IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError

from apps.recipes.api.filters import IngredientFilter
from apps.recipes.api.serializers import (FavoriteSerializer,
                                          IngredientSerializer,
                                          PurchaseSerializer,
                                          SubscriptionSerializer)
from apps.recipes.models import Ingredient

SUCCESS = JsonResponse({'success': True}, status=status.HTTP_200_OK)
FAIL = JsonResponse({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class CreateAndDeleteViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True, )
            self.perform_create(serializer)
        except (ValidationError, DatabaseError, IntegrityError):
            return FAIL
        return SUCCESS

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except (IntegrityError, DatabaseError):
            return FAIL
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
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
