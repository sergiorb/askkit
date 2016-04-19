# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers

from polls.models import Poll, Option, Vote
from .serializers_users import UserSerializer


class OptionSerializer(serializers.ModelSerializer):
	"""
	General Options serializer.
	"""

	class Meta:
		model = Option
		fields = ('id', 'optionText','votes', 'percentage', 'created', 'modified', 'poll',)


	def validate_poll(self, value):

		request = self.context['request']

		if request.user.is_anonymous():
			raise serializers.ValidationError("You can't add options as an anonymous user.")

		is_owner = Poll.objects.filter(pk=self.initial_data['poll'], owner=request.user)
		
		if not is_owner:
			raise serializers.ValidationError("This poll doesn't belong to you.")

		return value

	def validate_optionText(self, value):

		poll = Poll.objects.get(pk=self.initial_data['poll'])

		###############################################################
		# TODO: use select_related()
		###############################################################
		
		options = poll.options.all()

		for option in options:
			if option.optionText == value:
				raise serializers.ValidationError("Options need to be different.")

		return value


class OptionSerializerPollPost(OptionSerializer):
	"""
	Options serializer when client is creating a new Poll. Due to DRF post
	request process (post->validation->creation), we disable the option poll 
	field requirement, letting Poll creation method run.
	"""

	poll = serializers.UUIDField(required=False)


	def validate_optionText(self, value):

		return value


class PollSerializer(serializers.ModelSerializer):
	"""
	General Polls serializers. Option field setted to 'many' due to the minimum
	requirement of two options per poll.
	"""

	owner = UserSerializer(read_only=True)
	options = OptionSerializerPollPost(many=True)

	class Meta:
		model = Poll
		fields = ('id','owner','title','created','modified', 'context','date_begin',
			'date_end', 'is_active','public','votes', 'anon_allowed', 
			'options',)


	def validate(self, data):
		"""
		Checks that date begin is before the date end.
		"""

		if not 'date_begin' in data:
			data['date_begin'] = timezone.now()

		if 'date_end' in data:
			if data['date_begin'] >= data['date_end']:
				raise serializers.ValidationError("Date end must occur after date begin.")

		return data

	def validate_date_begin(self, value):
		"""
		Checks that date begin is after creation date.
		"""

		if not value:
			raise serializers.ValidationError("This field may not be null.")

		if value <= timezone.now():
			raise serializers.ValidationError("Date begin must occur after creation date.")

		return value

	def validate_date_end(self, value):
		"""
		Checks that date end is after creation date.
		"""

		if not value:
			raise serializers.ValidationError("This field may not be null.")

		if value <= timezone.now():
			raise serializers.ValidationError("Date end must occur after creation date.")

		return value

	def validate_options(self, value):
		"""
		Check that poll has two and different options at minimum.
		"""

		if not len(value) > 1:
			raise serializers.ValidationError("You need to set two options at minimum.")

		options = []
		for option in value:
			if not option in options:
				options.append(option)

		if options != value:
			raise serializers.ValidationError("Options need to be different.")
		return value

	def create(self, validated_data):
		"""
		Allows a full poll/option creation.
		"""	

		user = self.context['request'].user

		if user.is_anonymous():
			user = None

		options_data = validated_data.pop('options')
		poll = Poll.objects.create(owner=user, **validated_data)

		for poll_data in options_data:
			Option.objects.create(poll=poll, **poll_data)
		return poll


class VoteSerializer(serializers.ModelSerializer):
	"""
	General Votes serializes.
	"""

	class Meta:
		model = Vote
		fields = ('id', 'user','option', 'date',)