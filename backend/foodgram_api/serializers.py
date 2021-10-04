import base64
from unittest.mock import Base
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Portion, Tag, Ingredient, Recipe, Favorite
from users_api.serializers import UserSerializer


class Base64ImageField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr),
                               name=id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        #fields = ['name', 'measurement_unit']
        fields = '__all__'


class PortionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Portion
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = PortionSerializer(
        source='portion_set', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        current_user = self.context.get('request').user
        if current_user.is_anonymous:
            return False
        favorites = current_user.favorite.recipes.all()
        if obj in favorites:
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context.get('request').user
        if current_user.is_anonymous:
            return False
        if obj in current_user.shoppingcart.recipes.all():
            return True
        return False

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
