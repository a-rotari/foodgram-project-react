import json

from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users_api.serializers import UserSerializerFull

from .fields import Base64ImageField
from .models import Favorite, Ingredient, Portion, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """ This simple serializer is for handling Tag objects. """
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """ This simple serializer is for handling Ingredient objects. """
    class Meta:
        model = Ingredient
        fields = '__all__'


class PortionSerializer(serializers.ModelSerializer):
    """
    This serializer is for handling Portion objects from
    the intermediate table between Recipe and Ingredient.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField(validators=[MinValueValidator(
        0, message='Количество ингредиентов не может быть отрицательным.'), ])

    class Meta:
        model = Portion
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """ This serializer is for handling the Recipe objects. """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializerFull(read_only=True)
    ingredients = PortionSerializer(
        source='portion_set', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(validators=[MinValueValidator(
        1, message='Время приготовления не может быть меньше минуты.'), ])

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

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError(
                    {'ingredients': ['Количество ингредиентов не должно '
                                     'быть отрицательным.']})
            existing_portion = Portion.objects.filter(
                recipe=recipe,
                ingredient__id=ingredient['id'])
            if existing_portion:
                existing_portion.delete()
                recipe.delete()
                raise serializers.ValidationError(
                    {'ingredients': ['Ингредиенты должны быть уникальными.']})
            else:
                Portion.objects.create(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    amount=ingredient['amount'])
        for tag_id in tags_data:
            tag = Tag.objects.get(id=tag_id)
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        for ingredient in ingredients_data:
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError(
                    {'ingredients': ['Количество ингредиентов не должно '
                                     'быть отрицательным.']})
            existing_portion = Portion.objects.filter(
                recipe=instance,
                ingredient__id=ingredient['id'])
            if existing_portion:
                raise serializers.ValidationError(
                    {'ingredients': ['Ингредиенты должны быть уникальными.']})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.ingredients.clear()
        for ingredient in ingredients_data:
            Portion.objects.create(
                recipe=instance,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount'])

        instance.tags.clear()

        try:
            for tag_id in tags_data:
                tag = Tag.objects.get(id=tag_id)
                instance.tags.add(tag)
        except TypeError:
            instance.tags.add(Tag.objects.get(id=tags_data))
        return instance

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    This serializer provides less complete serialization of
    Recipe objects for shorter output.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
