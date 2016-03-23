# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.utils import timezone
from django.db import models, IntegrityError, transaction

# Create your models here.

class Poll(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
		editable=False)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name='polls', blank=True, null=True)
	
	added_on = models.DateTimeField(default=timezone.now)
	context = models.TextField(blank=True, null=True)
	date_begin = models.DateTimeField(default=timezone.now)
	date_end = models.DateTimeField(blank=True, null=True)
	public = models.BooleanField(default=True)
	title = models.CharField(max_length=140)
	total_votes = models.IntegerField(default=0)
	anon_allowed = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

	def short_title(self):
		"""
			Returns a fragment of title string if it's greater than 
			max_length.
		"""
		max_length = 30

		if len(self.title) > max_length:
			return '%s...' % self.title[:max_length]
		else:
			return self.title

	def is_active(self):
		"""
			Returns true when current datetime is greater than its begin date
			and it hasn't end date, or if current datetime is between its
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
			Returns true when poll has an end date.
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
			Returns True if the poll has an end date and current time is
			above end date.
		"""

		now = timezone.now()

		if self.date_end and self.date_end < now:
			return True
		else:
			return False

	def options_count(self):
		"""
			Returns the count of related options. 
		"""

		return self.options.count()


class Option(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
		editable=False)

	poll = models.ForeignKey(Poll, related_name='options')

	added_on = models.DateTimeField(auto_now_add=True)
	optionText = models.CharField(max_length=140)
	vote_quantity = models.PositiveIntegerField(default=0)	

	def __unicode__(self):
		return self.optionText
	
	# To TASK
	def delete(self, *args, **kwargs):
		
		try:
			with transaction.atomic():
				self.poll.total_votes -= self.vote_quantity
				self.poll.save()
				super(Option, self).delete(*args, **kwargs)
		except IntegrityError:
			pass

	def percentage(self):
		"""
			Returns the option percentaje based in the poll total votes and
			option votes
		"""

		total_votes = self.poll.total_votes

		if total_votes != 0:
			percentage = (self.vote_quantity * 100.0) / total_votes
		else:
			percentage = 0

		return round(percentage,2)


class Vote(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
		editable=False)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes',
		blank = True, null = True)

	option = models.ForeignKey(Option, related_name='option')

	fromIp = models.GenericIPAddressField(blank = True, null = True)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s - %s' % (self.user, self.option)


class PollAuthToken(models.Model):
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
		editable=False)
	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_auth_token',)
	
	poll = models.ForeignKey(Poll, related_name='poll')
