from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

from .models import Poll
from polls.tasks import option_add_vote, option_subtract_vote
from polls.tasks import option_random_vote, reset_poll_votes

# Create your views here.

class PollListView(ListView):
	"""
		Renders a simple poll list with voting methods.
	"""

	model = Poll
	template_name = "polls/list.html"


class AddVote(View):
	"""
		Adds a vote to given option id.
	"""

	def post(self, request, *args, **kwargs):

		option_add_vote.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('poll_list'))
		

class SubtractVote(View):
	"""
		Subtracts a vote from given option id.
	"""

	def post(self, request, *args, **kwargs):

		option_subtract_vote.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('poll_list'))
		

class RandomVote(View):
	"""
		Makes given number votes to given poll id.
	"""

	def post(self, request, *args, **kwargs):

		option_random_vote.delay(self.request.POST['id'], int(self.request.POST['number']))

		return HttpResponseRedirect(reverse('poll_list'))


class ResetPollVotes(View):
	"""
		Resets poll and its replies to 0 votes.
	"""

	def post(self, request, *args, **kwargs):

		reset_poll_votes.delay(self.request.POST['id'])

		return HttpResponseRedirect(reverse('poll_list'))