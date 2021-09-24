from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request


class CustomAuthTokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    email = serializers.EmailField(
        label='Email',
        write_only=True
    )

    token = serializers.CharField(
        label='Token',
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        print('VALIDATE: EMAIL: ', email)
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
