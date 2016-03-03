import random, time

from django.db import IntegrityError, transaction

from askkit.celery import app

from .models import Question, Reply

@app.task
def reply_add_vote(pk):
	"""
		Updates give reply id and its question increasing vote number by 1.
	"""

	reply = Reply.objects.get(pk=pk)

	try:
		with transaction.atomic():

			reply.vote_quantity += 1
			reply.save()
			reply.question.total_votes += 1
			reply.question.save()

	except IntegrityError as exc:
		raise self.retry(exc=exc)

@app.task
def reply_subtract_vote(pk):
	"""
		Updates given reply id and its question decreasing vote number by 1.
	"""

	reply = Reply.objects.get(pk=pk)

	if reply.vote_quantity > 0:
		try:
			with transaction.atomic():

				reply.vote_quantity -= 1
				reply.save()
				reply.question.total_votes -= 1
				reply.question.save()

		except IntegrityError as exc:
			raise self.retry(exc=exc)


@app.task
def reply_delete(pk):
	"""
		Deletes given reply id and updates its question votes number.
	"""

	reply = Reply.objects.get(pk=pk)

	try:
		with transaction.atomic():

			reply.question.total_votes -= reply.vote_quantity
			reply.question.save()
			reply.delete()

	except IntegrityError as exc:
		raise self.retry(exc=exc)


@app.task
def reset_question_votes(pk):
	"""
		Resets question and its replies votes number to 0.
	"""

	try:
		with transaction.atomic():

			question = Question.objects.get(pk=pk)
			question.total_votes = 0
			question.save()

			for reply in question.replies.all():
				reply.vote_quantity = 0
				reply.save()

	except IntegrityError as exc:
		raise self.retry(exc=exc)


@app.task
def reply_random_vote(pk, number=100):
	"""
		Generates given number votes among given question id.
	"""
	
	question = Question.objects.get(pk=pk)
	reply = question.replies.all()
	replies = reply.values_list('pk', flat=True)

	for x in xrange(0, number):
		
		reply_add_vote.delay(random.choice(replies))


