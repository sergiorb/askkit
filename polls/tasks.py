import random, time

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from celery import chord

from askkit.celery import app

from .models import Poll, Option, Vote


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
def option_delete(pk):
	"""
	Deletes given option id and updates its poll votes number.
	"""

	option = Option.objects.get(pk=pk)

	try:
		with transaction.atomic():

			option.poll.total_votes -= option.vote_quantity
			option.poll.save()
			option.delete()

	except IntegrityError as exc:
		raise self.retry(exc=exc)

@app.task
def count_option_votes(pk):
	"""
	Count and updates option votes.
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
	Counts the poll votes (from its options) and update the poll.
	"""

	poll = Poll.objects.get(pk=pk)

	poll.total_votes = sum(options_votes)
	poll.save()


@app.task
def chord_update_poll_votes(pk):
	"""
	Updates poll options votes count.
	"""

	poll = Poll.objects.get(pk=pk)

	callback = update_poll_votes.s(pk)
	header = [count_option_votes.s(option.pk) for option in poll.options.all()]
	result = chord(header)(callback)


@app.task
def reset_poll_votes(pk):
	"""
	Resets poll and its options votes number to 0.
	"""

	try:
		with transaction.atomic():

			poll = Poll.objects.get(pk=pk)
			poll.total_votes = 0
			poll.save()

			for option in poll.options.all():
				option.vote_quantity = 0
				option.save()

	except IntegrityError as exc:
		raise self.retry(exc=exc)


@app.task
def update_votes():
	"""
	Updates polls votes in the db.
	"""
	polls = Poll.objects.all()

	for poll in polls:

		chord_update_poll_votes.delay(poll.pk)


@app.task
def option_random_vote(pk, number=100):
	"""
	Generates given number votes among given poll id.
	"""
	
	poll = Poll.objects.get(pk=pk)
	option = poll.options.all()
	options = option.values_list('pk', flat=True)

	for x in xrange(0, number):
		
		option_add_vote.delay(random.choice(options))


