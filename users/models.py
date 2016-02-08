#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db import IntegrityError, transaction
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


from allauth.account.signals import user_signed_up
from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.signals import pre_social_login, social_account_added


from core.auto_strings import *


from hashids import Hashids
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


###################################################################
###################################################################

def generate_token_profile(sender, instance, created, *args, **kwargs):
	min_length = 32

	if 'min_length' in kwargs:
		min_length = kwargs['min_length'] 

	if instance.token == 'default':
		while 1:
			hashids = Hashids(min_length=min_length)
			token =  hashids.encode(instance.pk)
			try:
				Profile.objects.get(token=token)
			except:
				instance.token = token
				instance.save()
				#############################
				# THIS SHOULD NOT BE HERE
				notification = Notification(profile = instance, tittle = WELCOME_HEAD_STR, message = WELCOME_BODY_STR, style="SU")
				notification.save()
				##############################
				return token

def generate_avatar_filename(self, filename):
		url = "users/%s/avatar/%s" % (self.user.id, filename)
		return url

def generate_background_filename(self, filename):
		url = "users/%s/background/%s" % (self.user.id, filename)
		return url

class Profile(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile')
	avatar = ProcessedImageField(
		upload_to=generate_avatar_filename,
		processors=[ResizeToFill(250, 250)],
		format='JPEG',
		options={'quality': 90},
		default='default/default-avatar.jpg')
	background = ProcessedImageField(
		upload_to=generate_background_filename,
		#processors=[ResizeToFill(1920, 600)],
		format='JPEG',
		options={'quality': 90},
		default='default/default-background.jpg')
	max_replies = models.IntegerField(default=3)
	token = models.TextField(default='default')

	def __unicode__(self):
		return str(self.user.username)

post_save.connect(generate_token_profile, sender=Profile, dispatch_uid="generate_token_profile")

###################################################################
###################################################################
def generate_token_notification(sender, instance, *args, **kwargs):

	min_length = 32

	if 'min_length' in kwargs:
		min_length = kwargs['min_length'] 

	if instance.token == 'default':
		while 1:
			hashids = Hashids(min_length=min_length)
			token =  hashids.encode(instance.pk)
			try:
				Notification.objects.get(token=token)
			except:
				instance.token = token
				instance.save()
				return token

STYLE_CHOICES = (
	('DE', _('Default')),
	('PR', _('Primary')),
	('SU', _('Success')),
	('IN', _('Info')),
	('WA', _('Warning')),
	('DA', _('Danger')),
)
STATUS_CHOICES = (
	('CR', _('Created')),
	('RE', _('Readed')),
)

class Notification(models.Model):
	profile = models.ForeignKey(Profile, related_name='notifications')
	token = models.TextField(default='default')
	date = models.DateTimeField(auto_now_add=True)
	tittle = models.CharField(max_length=140)
	message = models.TextField(blank=True, null=True)
	style = models.CharField(choices=STYLE_CHOICES, max_length=2, default='DE')
	status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='CR')

	def __unicode__(self):
		return str(self.profile) + ' - ' +str(self.tittle)

post_save.connect(generate_token_notification, sender=Notification, dispatch_uid="generate_token_notification")

###################################################################
###################################################################

"""
def sociallogin(request, sociallogin, *args, **kwargs):
	print "####################################################"
	print sociallogin.user.__dict__
	return HttpResponseRedirect(reverse('dashboard'))

pre_social_login.connect(sociallogin)


def what(request, sociallogin, *args, **kwargs):
	print "####################################################"
	print sociallogin.user.__dict__
	return HttpResponseRedirect('http://localhost/')


social_account_added.connect(what)
"""

###################################################################
###################################################################

def profile_create(sender, request, user, *args, **kwargs):

	try:
		with transaction.atomic():
			profile = Profile(user=user)
			profile.save()
	except IntegrityError:
		user.delete()
	except:
		user.delete()

user_signed_up.connect(profile_create, dispatch_uid="profile_create")


"""
def generate_welcome_notification(sender, instance, created, *args, **kwargs):
	print "##########################################"
	print "##########################################"
	print "##########################################"
	print sender
	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	print instance
	print "##########################################"
	print created

	if created:
		notification = Notification(profile = None, tittle = WELCOME_HEAD_STR, message = WELCOME_BODY_STR)
		print notification
		notification.save()

pre_save.connect(generate_welcome_notification, sender=Profile, dispatch_uid="generate_welcome_notification")
"""
#####################################################################
#####################################################################