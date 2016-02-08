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

from users.models import *
from users.models import *


# Create your models here.

###########################################################################################################
###########################################################################################################

prominet_num = 10


def generate_token_report(sender, instance, *args, **kwargs):

	min_length = 32

	if 'min_length' in kwargs:
		min_length = kwargs['min_length'] 

	if instance.token == 'default':
		while 1:
			hashids = Hashids(min_length=min_length)
			token =  hashids.encode(instance.pk)
			try:
				Report.objects.get(question_token=token)
			except:
				instance.token = token
				instance.save()
				return token
		

###########################################################################################################
###########################################################################################################

class Report(models.Model):

	asker = models.ForeignKey(Profile, blank = True, null = True, related_name='reports')
	name = models.CharField(max_length=140, blank = True, null = True)
	email = models.EmailField()
	message = models.TextField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	fromIp = models.GenericIPAddressField(blank=True, null=True)
	token = models.TextField(default='default')
	STATUS_CHOICES = (
		('OP', _('Opened')),
		('IC', _('In curse')),
		('Re', _('Resolved')),
	)
	status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='OP')

	SUBJECT_CHOICES = (
		('Err',_("Errors")),
		('Sug',_("Sugestions")),
		('Acc',_("Accounts")),
		('Leg',_("Legal")),
		('Otr',_("Others")),
	)
	subject = models.CharField(choices=SUBJECT_CHOICES, max_length=3, default='Err')


	def __unicode__(self):
		if self.asker:
			return self.subject+" - "+str(self.asker)+" (Account) - "+self.message[0:24]+"..."
		else:
			return self.subject+" - "+str(self.name)+" (Annonymous) - "+self.message[0:24]+"..."

post_save.connect(generate_token_report, sender=Report)
