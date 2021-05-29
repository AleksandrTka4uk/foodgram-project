from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.recipes.models import Recipe, User, Favorite


class AddFavorite(APIView):
    def post(self, request, format=None):
        obj, created = Favorite.objects.get_or_create(
            author=request.user,
            recipe_id=request.data['id']
        )
        return Response({"success": created}, status=status.HTTP_200_OK)


class RemoveFavorite(APIView):
    def post(self, request, format=None):
        recipe = get_object_or_404(Recipe, pk=request.data['id'])
        obj = get_object_or_404(
            Favorite,
            author=request.user,
            recipe=recipe
        )
        obj.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)