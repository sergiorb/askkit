from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from django.contrib.auth import get_user_model
from .serializers_users import UserSerializer
from .permissions_users import IsOwnerOrReadOnly

# Create your views here.


class UserViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, 
	mixins.RetrieveModelMixin, viewsets.GenericViewSet):

	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsOwnerOrReadOnly,]


	@list_route(permission_classes=[], methods=['post'])
	def signup(self, request):
		"""
		Create an account.
		"""

		# TODO #######################################################

		return Response({
			'status_code': 200,
			'account': True,
			})

	@detail_route(permission_classes=[], methods=['post'])
	def close_account(self, request, pk=None):
		"""
		Closes your account.
		"""

		# TODO #######################################################

		return Response({
			'status_code': 200,
			'account': True,
			})