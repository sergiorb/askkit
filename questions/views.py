from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

from .models import Question
from questions.tasks import reply_add_vote, reply_subtract_vote
from questions.tasks import reply_random_vote, reset_question_votes

# Create your views here.

class QuestionListView(ListView):
	"""
		Renders a simple question list with voting methods.
	"""

	model = Question
	template_name = "questions/list.html"


class AddVote(View):
	"""
		Adds a vote to given reply id.
	"""

	def post(self, request, *args, **kwargs):

		reply_add_vote.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('question_list'))
		

class SubtractVote(View):
	"""
		Subtracts a vote from given reply id.
	"""

	def post(self, request, *args, **kwargs):

		reply_subtract_vote.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('question_list'))
		

class RandomVote(View):
	"""
		Makes given number votes to given question id.
	"""

	def post(self, request, *args, **kwargs):

		reply_random_vote.delay(self.request.POST['id'], int(self.request.POST['number']))

		return HttpResponseRedirect(reverse('question_list'))


class ResetQuestionVotes(View):
	"""
		Resets question and its replies to 0 votes.
	"""

	def post(self, request, *args, **kwargs):

		reset_question_votes.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('question_list'))