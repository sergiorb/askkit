import random, time, string

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from celery import chord

from askkit.celery import app

from .models import Poll, Option, Vote

from .functions import generate_dummy_polls_votes


@app.task(bind=True)
def option_make_vote(self, user_pk, user_ip, option_pk):
	"""
	Stores a vote object.
	"""

	try:
		with transaction.atomic():

			if user_pk != None:
				user_model = get_user_model()
				user = user_model.objects.get(pk=user_pk)
			else:
				user = None
			option = Option.objects.get(pk=option_pk)

			vote = Vote(user=user, option=option, fromIp=user_ip)
			vote.save()

	except IntegrityError as exc:
		raise self.retry(exc=exc)
		

@app.task
def count_option_votes(pk):
	"""
	Count and updates an option votes.
	"""

	try:
		with transaction.atomic():

			option = Option.objects.get(pk=pk)
			votes_count = Vote.objects.filter(option=option).count()
			option.vote_quantity = votes_count
			option.save()
 
			return votes_count

	except IntegrityError as exc:
		raise self.retry(exc=exc)


@app.task
def update_poll_votes(options_votes, pk):
	"""
	Sums poll votes (from its options) and update the poll. 
	( options_votes = [3,0,1] ).
	"""

	poll = Poll.objects.get(pk=pk)

	poll.total_votes = sum(options_votes)
	poll.save()


@app.task
def chord_update_poll_votes(pk):
	"""
	Updates poll options votes count. Using celery chord, executes 
	'count_option_votes()' task (async mode) for every poll option and returns
	 its value to 'update_poll_votes()'.
	"""

	poll = Poll.objects.get(pk=pk)

	callback = update_poll_votes.s(pk)
	header = [count_option_votes.s(option.pk) for option in poll.options.all()]
	result = chord(header)(callback)


@app.task
def update_votes():
	"""
	Updates polls votes in the entire db.
	"""
	polls = Poll.objects.all()

	for poll in polls:

		chord_update_poll_votes.delay(poll.pk)


@app.task
def create_dummy_polls(number=100):

	generate_dummy_polls_votes(number)