import json

from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import permissions, renderers, status, views, viewsets
from rest_framework.exceptions import APIException
#import rest_framework
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from core import paginate

from . import serializers
from .filters import RecipeFilter
from .models import Favorite, Ingredient, Recipe, Tag
from .permissions import RecipePermission


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
    permission_classes = [RecipePermission]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RecipeFilter
    ordering = ['id']

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        obj = get_object_or_404(Recipe, id=self.kwargs[lookup_url_kwarg])

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    # def get_queryset(self):
    #     """ Override queryset to filter by parameter 'name' """
    #     is_favorited = self.request.query_params.get('is_favorited')
    #     is_in_shopping_cart = self.request.query_params.get(
    #         'is_in_shopping_cart')
    #     tags = self.request.query_params.getlist('tags')
    #     if is_favorited and (int(is_favorited) == 1):
    #         favorite = self.request.user.favorite.recipes.all()
    #     else:
    #         favorite = self.queryset
    #     if is_in_shopping_cart and (int(is_in_shopping_cart) == 1):
    #         shopping = self.request.user.shoppingcart.recipes.all()
    #     else:
    #         shopping = self.queryset
    #     if tags:
    #         tags_id = []
    #         for tag in tags:
    #             tags_id.append(Tag.objects.get(slug=tag).id)
    #         tags_queryset = Recipe.objects.filter(tags__in=tags_id)
    #     else:
    #         tags_queryset = self.queryset
    #     queryset = self.queryset.intersection(
    #         favorite, shopping, tags_queryset)
    #     print(queryset)
    #     input()
    #     return queryset

    def perform_create(self, serializer):
        author = self.request.user
        if 'ingredients' not in self.request.data:
            raise ValidationError(
                {'ingredients': ['This field is required.']})
        if 'tags' not in self.request.data:
            raise ValidationError(
                {'tags': ['This field is required.']})
        try:
            ingredients_data = json.loads(self.request.data['ingredients'])
            tags_data = json.loads(self.request.data['tags'])
        except ValueError:
            raise ValidationError(
                {'ingredients, tags': ['These fields use JSON format.']})

        serializer.save(author=author,
                        ingredients=ingredients_data,
                        tags=tags_data)

    def perform_update(self, serializer):
        # author = self.request.user
        # if 'ingredients' not in self.request.data:
        #     raise ValidationError(
        #         {'ingredients': ['This field is required.']})
        # if 'tags' not in self.request.data:
        #     raise ValidationError(
        #         {'tags': ['This field is required.']})
        # ingredients = self.request.data['ingredients']
        # tags = self.request.data['tags']
        # serializer.save(author=author,
        #                 ingredients=ingredients,
        #                 tags=tags)
        self.perform_create(serializer)


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
