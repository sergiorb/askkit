from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.signals import request_started

from .models import Poll, Option, Vote
from .tasks import chord_update_poll_votes as update_poll_votes


@receiver(post_delete, sender=Vote, dispatch_uid="update_poll_votes_on_delete")
def update_poll_votes_on_delete(sender, instance, **kwargs):
	
	update_poll_votes.delay(instance.option.poll.pk)
