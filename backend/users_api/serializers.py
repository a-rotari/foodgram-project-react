from rest_framework import serializers

from foodgram_api.models import Favorite, Recipe, ShoppingCart

from .models import User, UserSubscription


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User model. """

    def create(self, validated_data):
        # Using the 'create_user' function to create user with hashed password
        user = User.objects.create_user(**validated_data)
        Favorite.objects.create(user=user)
        ShoppingCart.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = ['email', 'id', 'username',
                  'first_name', 'last_name', 'password']
        # Ensure there are no empty fields and that the password is hidden
        extra_kwargs = dict.fromkeys(['email', 'first_name', 'last_name'], {
                                     'allow_blank': False, 'required': True})
        extra_kwargs['password'] = {'write_only': True}


class UserSerializerFull(UserSerializer):
    """ Serializer for User model that adds a method-field displaying user
        subscription status.  """
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        if current_user.is_anonymous:
            return False
        subscribed = UserSubscription.objects.filter(
            subscriber=current_user,
            following=obj
        )
        if (subscribed) or (current_user == obj):
            return True
        return False

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['is_subscribed']


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer that handles the change of password. """
    new_password = serializers.CharField(required=True, max_length=150)
    current_password = serializers.CharField(required=True, max_length=150)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """ Short serializer for Recipes that has only 4 fields:
        id, name, image, cooking_time. """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserRecipeSerializer(UserSerializerFull):
    """ Serializer for User model that adds a read-only recipes field and a
        query parameter 'recipes_limit' to limit the number of recipes shown.
        Also shows the total number of recipes for each displayed User. """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, user):
        int_limit = None
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit or (limit == ''):
            try:
                int_limit = int(limit)
            except ValueError:
                raise serializers.ValidationError(
                    '\'recipes_limit\' query parameter must be an integer.')
        queryset = Recipe.objects.filter(author=user)[:int_limit]
        serializer = ShortRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, user):
        return Recipe.objects.filter(author=user).count()

    class Meta(UserSerializerFull.Meta):
        fields = UserSerializerFull.Meta.fields + ['recipes', 'recipes_count']
