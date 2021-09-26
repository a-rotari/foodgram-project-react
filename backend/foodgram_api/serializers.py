from rest_framework import serializers
from .models import Portion, Tag, Ingredient, Recipe, Favorite
from users_api.serializers import UserSerializer


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
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    
    class Meta:
        model = Portion
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = PortionSerializer(source='portion_set', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        current_user = self.context.get('request').user
        if current_user.is_anonymous:
            return False
        favorites = current_user.favorite.recipes.all()
        if obj in favorites:
            return True
        return False


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'name', 'image', 'text', 'cooking_time')

class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')