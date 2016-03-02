from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

from .models import Question
from questions.tasks import reply_add_vote, reply_subtract_vote, reply_random_vote, reply_random_vote_async

# Create your views here.

class QuestionListView(ListView):

	model = Question
	template_name = "questions/list.html"


class AddVote(View):

	def post(self, request, *args, **kwargs):

		reply_add_vote.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('question_list'))
		

class SubtractVote(View):
	def post(self, request, *args, **kwargs):

		reply_subtract_vote.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('question_list'))
		

class RandomVote(View):
	def post(self, request, *args, **kwargs):

		reply_random_vote.delay(self.request.POST['id'], int(self.request.POST['number']))

		return HttpResponseRedirect(reverse('question_list'))


class RandomVoteAsync(View):
	def post(self, request, *args, **kwargs):

		reply_random_vote_async.delay(self.request.POST['id'], int(self.request.POST['number']))

		return HttpResponseRedirect(reverse('question_list'))