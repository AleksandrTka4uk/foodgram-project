from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView

from rest_framework import mixins, viewsets

from apps.recipes.api.serializers import IngredientSerializer, FavoriteSerializer
from apps.recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                                 Subscription, User)


class CreateAndDeleteViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def create(self, request, *args, **kwargs):
        data = {'user': self.request.user.id, 'recipe': request.data['id']}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True}, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'success': True}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class FavoritesViewSet(CreateAndDeleteViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return self.request.user.favorites.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 recipe__pk=self.kwargs['pk'])

# class AddFavorite(APIView):
#     def post(self, request, format=None):
#         obj, created = Favorite.objects.get_or_create(
#             author=request.user,
#             recipe_id=request.data['id']
#         )
#         if created:
#             return Response({'success': created},
#                             status=status.HTTP_200_OK)
#         else:
#             return Response({'success': created},
#                             status=status.HTTP_400_BAD_REQUEST)


# class RemoveFavorite(APIView):
#     def delete(self, request, pk, format=None):
#         obj = get_object_or_404(
#             Favorite,
#             author=request.user,
#             recipe__pk=pk
#         )
#         obj.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)


class AddSubscription(APIView):
    def post(self, request, format=None):
        obj, created = Subscription.objects.get_or_create(
            user=request.user,
            author_id=request.data['id']
        )
        if created:
            return Response({'success': created},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': created},
                            status=status.HTTP_400_BAD_REQUEST)


class AddPurchases(APIView):
    def post(self, request, format=None):
        obj, created = Purchase.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )
        if created:
            return Response({'success': created},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': created},
                            status=status.HTTP_400_BAD_REQUEST)


class RemoveSubscription(APIView):
    def delete(self, request, pk, format=None):
        obj = get_object_or_404(Subscription, user=request.user, author__pk=pk)
        obj.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)



class RemovePurchases(APIView):
    def delete(self, request, recipe_id, format=None):
        obj = get_object_or_404(
            Purchase,
            user=request.user,
            recipe__pk=recipe_id
        )
        obj.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class GetIngredients(APIView):
    def get(self, request, format=None):
        text = request.GET.get('query')
        if text:
            ingredients = Ingredient.objects.filter(title__contains=text)
        else:
            ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
