import json

from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import permissions, renderers, status, views, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from core import paginate

from . import serializers
from .filters import RecipeFilter
from .models import Favorite, Ingredient, Recipe, Tag
from .permissions import RecipePermission


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ This viewset is for displaying Tags. """

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ This viewset is for displaying Ingredients. It also provides
        search by name of the ingredient. """

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """ Override queryset to filter by parameter 'name' """
        name = self.request.query_params.get('name')
        if name:
            return Ingredient.objects.filter(name__startswith=name)
        else:
            return self.queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """ This viewset enables CRUD operations on Recipe objects. """

    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    pagination_class = paginate.CustomPagination
    permission_classes = [RecipePermission]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RecipeFilter
    ordering = ['id']

    def get_object(self):
        """
        The parent method was overriden to avoid the filtering of queryset
        resulting intersection of several querysets during filtering, as it's
        not supported by Django.
        """

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        # Removed filtering from here instead directly getting the object.
        obj = get_object_or_404(Recipe, id=self.kwargs[lookup_url_kwarg])

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        author = self.request.user
        if 'ingredients' not in self.request.data:
            raise ValidationError(
                {'ingredients': ['This field is required.']})
        if 'tags' not in self.request.data:
            raise ValidationError(
                {'tags': ['This field is required.']})
        # print('!!!!!!!!!!!!-!!!!!!!!!!!!!!!!!!!!------!!!!!!!!!!')
        # ing = self.request.data['ingredients']
        # print(ing)
        # print(type(ing))
        # try:
        #     ingredients_data = json.loads(self.request.data['ingredients'])
        #     tags_data = json.loads(self.request.data['tags'])
        # except ValueError:
        #     raise ValidationError(
        #         {'ingredients, tags': ['These fields use JSON format.']})
        ingredients_data = self.request.data['ingredients']
        tags_data = self.request.data['tags']
        serializer.save(author=author,
                        ingredients=ingredients_data,
                        tags=tags_data)

    def perform_update(self, serializer):
        # same as perform_create above, but used for PUT method
        self.perform_create(serializer)


class AddRemoveFavorite(views.APIView):
    """
    This simple view adds or removes the Recipe to favorites
    (which adds/removes a Recipe to/from Favorite's many-to-many field).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        favorite = request.user.favorite
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if recipe in favorite.recipes.all():
            return Response(
                {'errors': 'Recipe already in favorites.'},
                status=status.HTTP_400_BAD_REQUEST)
        favorite.recipes.add(recipe)
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        favorite = request.user.favorite
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if recipe not in favorite.recipes.all():
            return Response(
                {'errors': 'Recipe not in favorites.'},
                status=status.HTTP_400_BAD_REQUEST)
        favorite.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddRemoveShoppingCart(views.APIView):
    """
    This simple view adds or removes the Recipe to shopping list
    (which adds/removes a Recipe to/from ShoppingCart's many-to-many field).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cart_recipes = request.user.shoppingcart.recipes
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if recipe in cart_recipes.all():
            return Response(
                {'errors': 'Recipe already in shopping cart.'},
                status=status.HTTP_400_BAD_REQUEST)
        cart_recipes.add(recipe)
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        cart_recipes = request.user.shoppingcart.recipes
        recipe = get_object_or_404(Recipe.objects.all(), pk=pk)
        if recipe not in cart_recipes.all():
            return Response(
                {'errors': 'Recipe not in shopping cart.'},
                status=status.HTTP_400_BAD_REQUEST)
        cart_recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(views.APIView):
    """
    This simple view provides an endpoint for generating and
    downloading the list of ingredients from ShoppingCart.
    """

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
                    amount = ingredient.portion_set.get(recipe=recipe).amount
                    ingredients[ingredient.name][0] += amount
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
