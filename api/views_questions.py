from django.views.generic import View
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from questions.models import Question, Reply
from questions.tasks import reply_add_vote, reply_subtract_vote
from .serializers_questions import QuestionSerializer, ReplySerializer

# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer


class ReplyViewSet(viewsets.ModelViewSet):
	queryset = Reply.objects.all()
	serializer_class = ReplySerializer


class AddVote(View):
	"""
		Adds a vote to given reply id.
	"""

	def get(self, request, *args, **kwargs):
		"""
			Executes reply_add_vote task and returns task id.
		"""

		task = reply_add_vote.delay(self.kwargs['pk'])

		return JsonResponse({'task_id':task.task_id})
		

class SubtractVote(View):
	"""
		Subtracts a vote from given reply id.
	"""

	def get(self, request, *args, **kwargs):
		"""
			Executes reply_subtract_vote task and returns task id.
		"""

		task = reply_subtract_vote.delay(self.kwargs['pk'])

		return JsonResponse({'task_id':task.task_id})