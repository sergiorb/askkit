from django.db import IntegrityError, transaction

from askkit.celery import app

from .models import Question, Reply

@app.task
def reply_random_vote(pk, number=100):
	
	question = Question.objects.get(pk=pk)

	for x in xrange(0, number):
		reply = question.replies.order_by('?').first()
		print 'Loop n: %s' % x
		reply_add_vote(reply.pk)

@app.task
def reply_random_vote_async(pk, number=100):

	question = Question.objects.get(pk=pk)
	
	for x in xrange(0, number):
		reply = question.replies.order_by('?').first()
		reply_add_vote.delay(reply.pk)
	
@app.task
def reply_add_vote(pk):

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
	
	reply = Reply.objects.get(pk=pk)

	try:
		with transaction.atomic():
			reply.question.total_votes -= reply.vote_quantity
			reply.question.save()
			reply.delete()
	except IntegrityError as exc:
		raise self.retry(exc=exc)