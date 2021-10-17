from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from core import paginate

from . import serializers
from .models import User, UserSubscription


class UserListCreate(generics.ListCreateAPIView):
    """ This APIView provides a list of Users and allows creation
        of new Users. """

    queryset = User.objects.all()
    pagination_class = paginate.CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.UserSerializer
        return serializers.UserSerializerFull

    def get_permissions(self):
        """ Sets permission for the view based on the request method. """
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return [permission() for permission in self.permission_classes]


class CurrentUserView(views.APIView):
    """ This simple view enables the endpoint that shows
        the current user data. """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializerFull(
            request.user, context={'request': request})
        return Response(serializer.data)


class SubscriptionsView(generics.ListAPIView):
    """ This APIView provides the list of followed Users. """

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = paginate.CustomPagination
    serializer_class = serializers.UserRecipeSerializer

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber=self.request.user.id)


class CreateDestroySubscriptionView(views.APIView):
    """ This simple view enables the endpoint that creates or deletes
        User subscriptions. """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user_to_follow = get_object_or_404(User, pk=pk)
        user = request.user
        subscribed = UserSubscription.objects.filter(subscriber=user,
                                                     following=user_to_follow)
        if (user == user_to_follow) or (subscribed):
            return Response(
                {'errors': 'Already subscribed.'},
                status=status.HTTP_400_BAD_REQUEST)
        UserSubscription.objects.create(subscriber=user,
                                        following=user_to_follow)
        serializer = serializers.UserRecipeSerializer(
            user_to_follow,
            context={'request': request}
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        user = request.user
        subscribed = UserSubscription.objects.filter(
            subscriber=user,
            following=user_to_unfollow)
        if (user == user_to_unfollow) or not (subscribed):
            return Response(
                {'errors': 'Not following the user -- can\'t unfollow.'},
                status=status.HTTP_400_BAD_REQUEST)
        subscribed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileView(generics.RetrieveAPIView):
    """ This APIView shows a User profile detail. """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializerFull
    permission_classes = [permissions.IsAuthenticated]


class ChangePasswordView(views.APIView):
    """ This simple view provides an endpoint that enables changing the
        password. """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not request.user.check_password(
                    serializer.data.get('current_password')):
                return Response(
                    {"current_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
