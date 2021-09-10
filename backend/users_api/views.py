from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import UserSerializer


class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
