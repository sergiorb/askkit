from ipware.ip import get_ip

from django.views.generic import View
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import detail_route, list_route

from polls.models import Poll, Option, OptionVotedByUser
from polls.tasks import option_make_vote
from polls.tasks import option_add_vote, option_subtract_vote
from polls.tasks import reset_poll_votes
from .serializers_polls import PollSerializer, OptionSerializer
from .serializers_polls import OptionVotedByUserSerializer
from .permissions import AnonVotingForOptions, OptionNotOwner
from .permissions import IsOwnerOrReadOnly
from .pagination import PollsResultsSetPagination, OptionsResultsSetPagination
from .pagination import VotesResultsSetPagination


# Create your views here.


class PollViewSet(viewsets.ModelViewSet):

	queryset = Poll.objects.all()
	serializer_class = PollSerializer
	permission_classes = [IsOwnerOrReadOnly]
	pagination_class = OptionsResultsSetPagination


class OptionViewSet(viewsets.ModelViewSet):

	queryset = Option.objects.all()
	serializer_class = OptionSerializer
	pagination_class = PollsResultsSetPagination

	@detail_route(permission_classes=[AnonVotingForOptions, OptionNotOwner], 
		methods=['get'])
	def vote(self, request, pk=None):
		"""
		Stores a vote object.
		"""

		self.check_object_permissions(self.request, self.get_object())

		task = option_make_vote.delay(user_pk=request.user.pk, 
			user_ip=get_ip(request), option_pk=pk)

		return Response({
			'status_code': 200,
			'task_id': task.task_id,
			'task_status_link': task.task_id, 
			'detail': 'Your request have been queued.'
			})

	@detail_route(permission_classes=[AnonVotingForOptions, OptionNotOwner], 
		methods=['get'])
	def unvote(self, request, pk=None):
		"""
		Stores a vote object.
		"""

		self.check_object_permissions(self.request, self.get_object())

		task = option_make_vote.delay(user_pk=request.user.pk, 
			user_ip=get_ip(request), option_pk=pk)

		return Response({
			'status_code': 200,
			'task_id': task.task_id,
			'task_status_link': task.task_id, 
			'detail': 'Your request have been queued.'
			})


	@detail_route(permission_classes=[AnonVotingForOptions], methods=['get'])
	def addvote(self, request, pk=None):
		"""
			Executes option_add_vote task and returns task id.
		"""

		self.check_object_permissions(self.request, self.get_object())

		task = option_add_vote.delay(pk)

		return Response({
			'status_code': 200,
			'task_id': task.task_id,
			'task_status_link': task.task_id, 
			'detail': 'Your request have been queued.'
			})

	@detail_route(permission_classes=[AnonVotingForOptions], methods=['get'])
	def subtractvote(self, request, pk=None):
		"""
			Executes option_subtract_vote task and returns task id.
		"""

		self.check_object_permissions(self.request, self.get_object())

		task = option_subtract_vote.delay(pk)

		return Response({
			'status_code': 200,
			'task_id': task.task_id,
			'task_status_link': task.task_id, 
			'detail': 'Your request have been queued.'
			})


class OptionVotedByUserViewSet(mixins.ListModelMixin, 
	mixins.RetrieveModelMixin, viewsets.GenericViewSet):

	queryset = OptionVotedByUser.objects.all()
	serializer_class = OptionVotedByUserSerializer
	permission_classes = [permissions.IsAuthenticated,]
	pagination_class = VotesResultsSetPagination

	def get_queryset(self):
		"""
		This view returns a list of all the votes made by the currently 
		authenticated user.
		"""

		return  OptionVotedByUser.objects.filter(user=self.request.user)