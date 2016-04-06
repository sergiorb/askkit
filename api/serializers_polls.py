from django.contrib.auth import get_user_model

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

		# TODO: Executes only when updates.

		request = self.context['request']

		if request.user.is_anonymous():
			raise serializers.ValidationError("You can't add options as an anonymous user.")

		is_owner = Poll.objects.filter(pk=self.initial_data['poll'], owner=request.user)
		
		if not is_owner:
			raise serializers.ValidationError("This poll doesn't belong to you.")

		return value

	def validate_optionText(self, value):

		# TODO: use select_related()
		poll = Poll.objects.get(pk=self.initial_data['poll'])

		# TODO: use select_related()
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
		Check that the date begin is before the date end.
		"""

		if data['date_begin'] >= data['date_end']:
			raise serializers.ValidationError("Date end must occur after date begin.")
		return data

	def validate_options(self, value):
		"""
		Check that the poll has two and different options at minimum.
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

		options_data = validated_data.pop('options')
		poll = Poll.objects.create(**validated_data)

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