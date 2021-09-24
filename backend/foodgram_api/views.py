from rest_framework import viewsets
from rest_framework.response import Response
from core import paginate
from .models import Ingredient, Tag, Recipe
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
