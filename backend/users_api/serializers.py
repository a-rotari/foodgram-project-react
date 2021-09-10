from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, attrs):
        if attrs == '':
            raise serializers.ValidationError('This field may not be blank.')
        return attrs

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
