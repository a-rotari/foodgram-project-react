from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField

    def get_is_subscribed(self, obj):
        pass


    def create(self, validated_data):
        # Use helper function to create user with hashed password
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'password']
        # Ensure there are no empty fields and that the password is hidden
        extra_kwargs = dict.fromkeys(['email', 'first_name', 'last_name'], {'allow_blank': False, 'required': True})
        extra_kwargs['password'] = {'write_only': True}
    
