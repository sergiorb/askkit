#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from datetime import datetime

from hashids import Hashids
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError, transaction
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import user_signed_up
from allauth.account.utils import send_email_confirmation

from users.models import *


###########################################################################################################
###########################################################################################################

prominet_num = 10

# Merge this function with generate_token_reply.
def generate_token_question(sender, instance, *args, **kwargs):

	min_length = 32

	if 'min_length' in kwargs:
		min_length = kwargs['min_length'] 

	if instance.token == 'default':
		while 1:
			hashids = Hashids(min_length=min_length)
			token =  hashids.encode(instance.pk)
			try:
				Question.objects.get(token=token)
			except:
				instance.token = token
				instance.save()
				return token

# Merge this function with generate_token_question.
def generate_token_reply(sender, instance, *args, **kwargs):

	min_length = 32

	if 'min_length' in kwargs:
		min_length = kwargs['min_length'] 

	if instance.token == 'default':
		while 1:
			hashids = Hashids(min_length=min_length)
			token =  hashids.encode(instance.pk)
			try:
				Reply.objects.get(token=token)
			except:
				instance.token = token
				instance.save()
				return token
		

###########################################################################################################
###########################################################################################################

class Question(models.Model):

	asker = models.ForeignKey(Profile, blank = True, null = True, related_name='questions')

	allow_anonymous_voter = models.BooleanField(default=True)
	context = models.TextField(blank=True, null=True)
	data_require_vote = models.BooleanField(default=True)
	date = models.DateTimeField(auto_now_add=True)
	date_begin = models.DateTimeField(default=timezone.now)
	date_end = models.DateTimeField(blank=True, null=True)
	fromIp = models.GenericIPAddressField(blank=True, null=True)
	hide_data = models.BooleanField(default=False)
	public = models.BooleanField(default=True)
	question = models.CharField(max_length=140)
	token = models.TextField(default='default')
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.question

	def get_active_carousel(self):
		return self.carousels.filter(show=True).first()
		### EQUIVALENT TO ###############################
		#################################################
		# try:
		# 	carousel = self.carousels.filter(show=True)[0]
		# except IndexError:
		#	carousel = None
		#################################################

	def get_comments_by_date(self):
		return self.comments.order_by('-date')

	def get_prominets_comments(self):
		return self.comments.filter(rank__gte=prominet_num).order_by('-rank')

	def is_active(self):

		now = timezone.now()

		if self.date_begin < now and not self.date_end:
			return True
		elif self.date_begin < now and  self.date_end > now:
			return True
		else:
			return False

	def has_end(self):
		if self.date_end:
			return True
		else:
			return False

	def time_to_begin(self):

		now = timezone.now()

		if now < self.date_begin:
			return self.date_begin - now
		else:
			return False

	def time_to_end(self):

		now = timezone.now()

		if self.date_end and self.date_end > now:
			return self.date_end - now
		else:
			return False


	def is_finished(self):

		now = timezone.now()

		if self.date_end and self.date_end < now:
			return True
		else:
			return False


post_save.connect(generate_token_question, sender=Question)


###########################################################################################################
###########################################################################################################


class Reply(models.Model):
	color = models.CharField(max_length=7, blank = True, null = True)
	hits = models.BigIntegerField(default=0)
	question = models.ForeignKey(Question, related_name='replies')
	replyText = models.CharField(max_length=50)
	token = models.TextField(default='default')
	

	def delete(self, *args, **kwargs):
		try:
			with transaction.atomic():
				self.question.votes = self.question.votes - self.hits
				self.question.save()
				super(Reply, self).delete(*args, **kwargs)
		except IntegrityError:
			pass
	

	def __unicode__(self):
		return self.replyText

	def percentage(self):
		total_votes = self.question.votes
		try:
			percentage = (self.hits * 100) / total_votes
		except:
			percentage = 0
		return percentage

post_save.connect(generate_token_reply, sender=Reply)

###########################################################################################################
###########################################################################################################

class ReplyVotedBy(models.Model):
	voter = models.ForeignKey(Profile, blank = True, null = True)
	reply = models.ForeignKey(Reply, related_name='replyVote')
	question = models.ForeignKey(Question, related_name='questionVotes')
	fromIp = models.GenericIPAddressField()
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.voter) + " - " + str(self.reply).decode('utf-8') + " : " + self.fromIp


###########################################################################################################
###########################################################################################################

class Comment(models.Model):
	question = models.ForeignKey(Question, related_name='comments')
	commenter = models.ForeignKey(Profile, related_name='profileComments')
	parent = models.ForeignKey("self", blank=True, null = True, related_name="children")
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)
	rank = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.rank = self.likes - self.dislikes
		super(Comment, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.text[0:12]+"..."

	def hits(self):
		return self.likes + self.dislikes

	def is_prominet(self):
		if self.rank >= prominet_num:
			return True
		return False

###############################################################################################
class MakeCommentModelForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text',]
		labels = {
			'text': _('Leave your comment'),
		}
		error_messages = {
			'text': {
				'required': _('You cant leave a blank comment'.decode('utf-8')),
			}
		}
		widgets = {
          'text': forms.Textarea(attrs={'rows':2, 'cols':20}),
        }

###########################################################################################################
###########################################################################################################

def senMailOnSingUp(sender, request, user, **kwargs):

	send_email_confirmation(request, user, signup=True)

#user_signed_up.connect(senMailOnSingUp)


