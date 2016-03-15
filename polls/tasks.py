import random, time

from django.db import IntegrityError, transaction

from askkit.celery import app

from .models import Poll, Option

@app.task
def option_add_vote(pk):
	"""
		Updates give option id and its poll increasing vote number by 1.
	"""

	option = Option.objects.get(pk=pk)

	try:
		with transaction.atomic():

			option.vote_quantity += 1
			option.save()
			option.poll.total_votes += 1
			option.poll.save()

	except IntegrityError as exc:
		raise self.retry(exc=exc)

@app.task
def option_subtract_vote(pk):
	"""
		Updates given option id and its poll decreasing vote number by 1.
	"""

	option = Option.objects.get(pk=pk)

	if option.vote_quantity > 0:
		try:
			with transaction.atomic():

				option.vote_quantity -= 1
				option.save()
				option.poll.total_votes -= 1
				option.poll.save()

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
def option_random_vote(pk, number=100):
	"""
		Generates given number votes among given poll id.
	"""
	
	poll = Poll.objects.get(pk=pk)
	option = poll.options.all()
	options = option.values_list('pk', flat=True)

	for x in xrange(0, number):
		
		option_add_vote.delay(random.choice(options))


