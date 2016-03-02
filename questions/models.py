# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.utils import timezone
from django.db import models, IntegrityError, transaction


# Create your models here.

class Question(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
		editable=False)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name='profile')
	
	#allow_anonymous_voter = models.BooleanField(default=True)
	#data_require_vote = models.BooleanField(default=True)
	#fromIp = models.GenericIPAddressField(blank=True, null=True)
	#hide_data = models.BooleanField(default=False)
	added_on = models.DateTimeField(auto_now_add=True)
	context = models.TextField(blank=True, null=True)
	date_begin = models.DateTimeField(default=timezone.now)
	date_end = models.DateTimeField(blank=True, null=True)
	public = models.BooleanField(default=True)
	question = models.CharField(max_length=140)
	total_votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.question

	def short_question(self):
		"""
			Returns a fragment of question string if it's greater than 
			max_length.
		"""
		max_length = 30

		if len(self.question) > max_length:
			return '%s...' % self.question[:max_length]
		else:
			return self.question

	def is_active(self):
		"""
			Returns true when current datetime is greater than its begin date
			and it hasn't end date, or if current daterime is between its
			begin date and end date.
		"""

		now = timezone.now()

		if self.date_begin < now and not self.date_end:
			return True
		elif self.date_begin < now and self.date_end > now:
			return True
		else:
			return False

	def has_end(self):
		"""
			Returns true when question has an end date.
		"""
		if self.date_end:
			return True
		else:
			return False

	def time_to_begin(self):
		"""
			Returns a datetime object with the remaining time to its begin
			date. If current time is above begin date, returns False.
		"""

		now = timezone.now()

		if now < self.date_begin:
			return self.date_begin - now
		else:
			return False

	def time_to_end(self):
		"""
			Returns a datetime object with the remaining time to its end date.
			If current time is aboce end date, returns False.
		"""

		now = timezone.now()

		if self.date_end and self.date_end > now:
			return self.date_end - now
		else:
			return False


	def is_finished(self):
		"""
			Returns True if the question has an end date and current time is
			above end date.
		"""

		now = timezone.now()

		if self.date_end and self.date_end < now:
			return True
		else:
			return False

	def replies_count(self):
		"""
			Returns the count of related replies. 
		"""

		return self.replies.count()


class Reply(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
		editable=False)
	question = models.ForeignKey(Question, related_name='replies')

	#color = models.CharField(max_length=7, blank = True, null = True)
	added_on = models.DateTimeField(auto_now_add=True)
	replyText = models.CharField(max_length=140)
	vote_quantity = models.PositiveIntegerField(default=0)	

	def __unicode__(self):
		return self.replyText
	
	# To TASK
	def delete(self, *args, **kwargs):
		
		try:
			with transaction.atomic():
				self.question.total_votes -= self.vote_quantity
				self.question.save()
				super(Reply, self).delete(*args, **kwargs)
		except IntegrityError:
			pass

	def percentage(self):
		"""
			Returns the reply percentaje based in the question total votes and
			reply votes
		"""

		total_votes = self.question.total_votes
		percentage = (self.hits * 100) / total_votes or 0
			
		return percentage