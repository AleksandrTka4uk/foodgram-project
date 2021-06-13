from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.recipes.models import Recipe, User, Favorite, Subscription, Ingredient, Purchase
from apps.recipes.api.serializers import IngredientSerializer
from django.http import JsonResponse


class AddFavorite(APIView):
    def post(self, request, format=None):
        obj, created = Favorite.objects.get_or_create(
            author=request.user,
            recipe_id=request.data['id']
        )
        return Response({"success": created}, status=status.HTTP_200_OK)


class RemoveFavorite(APIView):
    def delete(self, request, pk, format=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj = get_object_or_404(
            Favorite,
            author=request.user,
            recipe=recipe
        )
        obj.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class AddSubscription(APIView):
    def post(self, request, format=None):
        author = get_object_or_404(User, pk=request.data['id'])
        obj, created = Subscription.objects.get_or_create(
            user=request.user,
            author=author
        )
        return Response({"success": created}, status=status.HTTP_200_OK)


class RemoveSubscription(APIView):
    def delete(self, request, pk, format=None):
        author = get_object_or_404(User, pk=pk)
        obj = get_object_or_404(
            Subscription,
            user=request.user,
            author=author
        )
        obj.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class GetIngredients(APIView):
    def get(self, request, format=None):
        text = request.GET.get('query')
        if text:
            ingredients = Ingredient.objects.filter(title__startswith=text)
        else:
            ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)


class AddPurchases(APIView):
    def post(self, request, format=None):
        recipe = get_object_or_404(Recipe, pk=request.data['id'])
        obj, created = Purchase.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        return Response({"success": created}, status=status.HTTP_200_OK)


class RemovePurchases(APIView):
    def delete(self, request, recipe_id, format=None):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj = get_object_or_404(
            Purchase,
            user=request.user,
            recipe=recipe
        )
        obj.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)