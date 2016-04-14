# -*- coding: utf-8 -*-

import json, random

from ipware.ip import get_ip

from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import detail_route, list_route

from polls.models import Poll, Option, Vote
from polls.tasks import option_make_vote
from .serializers_polls import PollSerializer, OptionSerializer
from .serializers_polls import VoteSerializer
from .permissions_polls import IsOwnerOrReadOnly, OptionIsOwnerOrReadOnly
from .permissions_polls import AnonVotingForOptions, VoterNotOwner, VotingInTime
from .permissions_polls import OnlyOneVote
from .pagination import PollsResultsSetPagination, OptionsResultsSetPagination
from .pagination import VotesResultsSetPagination


# Create your views here.


class PollViewSet(viewsets.ModelViewSet):

	queryset = Poll.objects.all()
	serializer_class = PollSerializer
	permission_classes = [IsOwnerOrReadOnly,]
	pagination_class = OptionsResultsSetPagination

	def get_queryset(self):
		"""
		This view returns a list of public polls.
		"""

		###############################################################
		# TODO: ADD: If request.user in_list(), retrieve object.
		###############################################################
		
		user = self.request.user

		if user.is_anonymous():
			return  Poll.objects.filter(public=True)
		else:
			return Poll.objects.filter(Q(public=True) | Q(owner=user))

	@list_route(methods=['get'])
	def random(self, request):
		"""
		Retieves a single random poll result.
		"""

		count = Poll.objects.all().count()
		

		if count > 0:
			random_index = random.randint(0, count - 1)
			poll = Poll.objects.all()[random_index]
		else:
			return Response({
				'status_code':status.HTTP_404_NOT_FOUND,
				'detail': 'Not found.'
				})

		serializer = PollSerializer(poll)

		return Response(serializer.data)

	@list_route(methods=['get'])
	def randomset(self, request):
		"""
		Retrieves a random** set of polls.
		"""

		n = 5

		count = Poll.objects.all().count()

		if count >= n:
			random_index = random.randint(0, count - n)
			polls = Poll.objects.all()[random_index:random_index + n]
		else:
			polls = Poll.objects.all()

		results = []

		for poll in polls:

			results.append(PollSerializer(poll).data)

		return Response({
			'count': count,
			'results': results
			})


class OptionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, 
	mixins.UpdateModelMixin, mixins.RetrieveModelMixin, 
	mixins.DestroyModelMixin, viewsets.GenericViewSet):

	queryset = Option.objects.all()
	serializer_class = OptionSerializer
	permission_classes = [OptionIsOwnerOrReadOnly,]
	pagination_class = PollsResultsSetPagination

	def get_queryset(self):
		"""
		This view returns a list of public options.
		"""

		###############################################################
		# TODO: ADD: If request.user in_list(), retrieve object.
		###############################################################

		user = self.request.user

		if user.is_anonymous():
			return Option.objects.filter(poll__public=True)
		else:
			return Option.objects.filter(Q(poll__public=True) | Q(poll__owner=user))

		#return  Option.objects.filter(poll__public=True)


	@detail_route(permission_classes=[ VotingInTime, AnonVotingForOptions, 
		VoterNotOwner, OnlyOneVote, ], methods=['post'])
	def vote(self, request, pk=None):
		"""
		Generate a vote object.
		"""

		self.check_object_permissions(self.request, self.get_object())

		task = option_make_vote.delay(user_pk=request.user.pk, 
			user_ip=get_ip(request), option_pk=pk)

		return Response({
			'status_code': 200,
			'task_id': task.task_id,
			'detail': 'Your vote have been queued.'
			})


class VoteViewSet(mixins.ListModelMixin, 
	mixins.RetrieveModelMixin, mixins.DestroyModelMixin, 
	viewsets.GenericViewSet):

	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
	permission_classes = [permissions.IsAuthenticated,]
	pagination_class = VotesResultsSetPagination

	def get_queryset(self):
		"""
		This view returns a list of all the votes made by the currently 
		authenticated user.
		"""

		return  Vote.objects.filter(user=self.request.user)
