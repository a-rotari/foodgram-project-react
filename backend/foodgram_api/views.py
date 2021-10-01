from rest_framework import viewsets, views, permissions, status, renderers
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from core import paginate
from .models import Ingredient, Tag, Recipe, Favorite
from . import serializers


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """ Override queryset to filter by parameter 'name' """
        name = self.request.query_params.get('name')
        if name:
            queryset = Ingredient.objects.filter(name__startswith=name)
        else:
            queryset = self.queryset
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    pagination_class = paginate.CustomPagination


class AddRemoveFavorite(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        favorite = request.user.favorite
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if recipe in favorite.recipes.all():
            return Response({'errors': 'Recipe already in favorites.'}, status=status.HTTP_400_BAD_REQUEST)
        favorite.recipes.add(recipe)
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        favorite = request.user.favorite
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if not recipe in favorite.recipes.all():
            return Response({'errors': 'Recipe not in favorites.'}, status=status.HTTP_400_BAD_REQUEST)
        favorite.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddRemoveShoppingCart(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cart_recipes = request.user.shoppingcart.recipes
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if recipe in cart_recipes.all():
            return Response({'errors': 'Recipe already in shopping cart.'}, status=status.HTTP_400_BAD_REQUEST)
        cart_recipes.add(recipe)
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        cart_recipes = request.user.shoppingcart.recipes
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if not recipe in cart_recipes.all():
            return Response({'errors': 'Recipe not in shopping cart.'}, status=status.HTTP_400_BAD_REQUEST)
        cart_recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        shopping_cart = request.user.shoppingcart
        ingredients = {}
        text = ''
        for recipe in shopping_cart.recipes.all():
            recipe_ingredients = recipe.ingredients.all()
            for ingredient in recipe_ingredients:
                if ingredient.name not in ingredients:
                    ingredients[ingredient.name] = [
                        ingredient.portion_set.get(recipe=recipe).amount,
                        ingredient.measurement_unit]
                else:
                    ingredients[ingredient.name][0] += ingredient.portion_set.get(
                        recipe=recipe).amount
        for name in ingredients.keys():
            amount = str(ingredients[name][0])
            unit = ingredients[name][1]
            text += '* ' + name + ': ' + amount + ' ' + unit + '\r\n'
        file_name = request.user.username + '.txt'
        content = text
        response = HttpResponse(content, content_type='plain/text')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            file_name)
        return response
