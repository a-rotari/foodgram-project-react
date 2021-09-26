from rest_framework import serializers
from foodgram_api.models import Favorite, ShoppingCart
from .models import User, UserSubscription


class UserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        # Use helper function to create user with hashed password
        user = User.objects.create_user(**validated_data)
        Favorite.objects.create(user=user)
        ShoppingCart.objects.create(user=user)
        return user 

    class Meta:
        model = User
        fields = ['email', 'id', 'username',
                  'first_name', 'last_name', 'password', 'is_subscribed']
        # Ensure there are no empty fields and that the password is hidden
        extra_kwargs = dict.fromkeys(['email', 'first_name', 'last_name'], {
                                     'allow_blank': False, 'required': True})
        extra_kwargs['password'] = {'write_only': True}


class ChangePasswordSerializer(serializers.Serializer):
    #model = User
    new_password = serializers.CharField(required=True, max_length=150)
    current_password = serializers.CharField(required=True, max_length=150)
