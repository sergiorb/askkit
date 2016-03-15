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

from polls.models import Poll, Option
from polls.tasks import option_add_vote, option_subtract_vote
from polls.tasks import reset_poll_votes
from .serializers_polls import PollSerializer, OptionSerializer


# Create your views here.


class PollViewSet(viewsets.ModelViewSet):

	queryset = Poll.objects.all()
	serializer_class = PollSerializer

	@detail_route(methods=['get'])
	def reset(self, request, pk=None):
		"""
			Resets poll and its replies votes number to 0.
		"""

		task = reset_poll_votes.delay(pk)

		return JsonResponse({'task_id':task.task_id})


class OptionViewSet(viewsets.ModelViewSet):

	queryset = Option.objects.all()
	serializer_class = OptionSerializer

	@detail_route(methods=['get'])
	def addvote(self, request, pk=None):
		"""
			Executes option_add_vote task and returns task id.
		"""

		task = option_add_vote.delay(pk)

		return JsonResponse({'task_id':task.task_id})

	@detail_route(methods=['get'])
	def subtractvote(self, request, pk=None):
		"""
			Executes option_subtract_vote task and returns task id.
		"""

		task = option_subtract_vote.delay(pk)

		return JsonResponse({'task_id':task.task_id})