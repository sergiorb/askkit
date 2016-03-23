from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins

from django.contrib.auth import get_user_model
from .serializers_users import UserSerializer
from .permissions_users import IsOwnerOrReadOnly

# Create your views here.


class UserViewSet(mixins.ListModelMixin, 
	mixins.RetrieveModelMixin, viewsets.GenericViewSet):

	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]