from rest_framework import serializers

from polls.models import Poll, Option, Vote


class OptionSerializer(serializers.ModelSerializer):

	#poll = PollSerializerShort()

	class Meta:
		model = Option
		fields = ('id', 'optionText','vote_quantity', 'percentage','poll',)


class PollSerializer(serializers.ModelSerializer):

	#owner = UserSerializer(required=False)
	options = OptionSerializer(many=True)

	class Meta:
		model = Poll
		fields = ('id','owner','title','added_on','context','date_begin',
			'date_end', 'is_active','public','total_votes', 'anon_allowed', 
			'options',)

	def create(self, validate_data):

		options_data = validate_data.pop('options')
		poll = Poll.objects.create(**validate_data)

		for option_data in options_data:
			Option.objects.create(poll=poll **options_data)

		return poll

	def validate_options(self, value):
		"""
		Check that the poll has two options at minimum.
		"""
		print value
		if not len(value) > 1:
			raise serializers.ValidationError("You need to set two options at minimum.")
		return value


class PollSerializerShort(serializers.ModelSerializer):

	#owner = UserSerializer()

	class Meta:
		model = Poll
		fields = ('id','owner',)


class VoteSerializer(serializers.ModelSerializer):

	class Meta:
		model = Vote
		fields = ('id', 'user','option', 'date',)

class VoteSerializerToPost(serializers.ModelSerializer):

	class Meta:
		model = Vote
		fields = ('id', 'user','option',)