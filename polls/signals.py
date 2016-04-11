from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.signals import request_started
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

from .models import Poll, Option, Vote
from .tasks import chord_update_poll_votes as update_poll_votes



@receiver(post_delete, sender=Vote, dispatch_uid="update_poll_votes_on_delete")
def update_poll_votes_on_delete(sender, instance, **kwargs):
	"""
	Updates votes count on vote deletion. 
	"""
	
	update_poll_votes.delay(instance.option.poll.pk)


@receiver(post_save, sender=Vote, dispatch_uid="update_poll_votes_on_create")
def update_poll_votes_on_create(sender, instance, **kwargs):
	"""
	Updates votes count on vote creation.

	This aproach works in a VERY LOW scale environment because it not overload 
	the system. TODO: IMPROVE VOTE COUNT TRIGGER SYSTEM. 
	"""

	update_poll_votes.delay(instance.option.poll.pk)


@receiver(post_save, sender=get_user_model(), dispatch_uid="create_auth_token_on_user_creation")
def create_auth_token_on_user_creation(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)