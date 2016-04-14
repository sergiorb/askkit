import random, string

from django.contrib.auth import get_user_model

from .models import Poll, Option, Vote


def generate_dummy_polls_votes(number=100):
	"""
	Generates 100 polls (by default) with x3 and x10 multiplier for options and
	votes respectively.
	"""

	def string_generator(size=6, chars=string.ascii_uppercase + string.digits + ' '):
		return ''.join(random.choice(chars) for _ in range(size))

	user_model = get_user_model()

	users = user_model.objects.filter(is_superuser=False)


	polls = Poll.objects.bulk_create([Poll(owner=random.choice(users), 
		title=string_generator(size=48)) for i in range(number)])

	options = Option.objects.bulk_create([Option(poll=random.choice(polls), 
		optionText=string_generator()) for i in range(number*3)])

	votes = Vote.objects.bulk_create([Vote(option=random.choice(options), 
		user=random.choice(users)) for i in range(number*10)])

