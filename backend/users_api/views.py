from rest_framework import generics, permissions

from .models import User
from . import serializers, paginate



class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = paginate.UserPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        print(self.request.method)
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        print(self.permission_classes)
        return [permission() for permission in self.permission_classes]