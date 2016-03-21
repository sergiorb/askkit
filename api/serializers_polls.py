from rest_framework import serializers

from polls.models import Poll, Option, Vote


class UserSerializer(serializers.Serializer):
	
	pk = serializers.CharField(max_length=100)
	username = serializers.CharField(max_length=100)


class PollSerializer(serializers.ModelSerializer):

	#owner = UserSerializer(required=False)

	class Meta:
		model = Poll
		fields = ('id','owner','title','added_on','context','date_begin',
			'date_end', 'is_active','public','total_votes', 'anon_allowed', 'options',)


class PollSerializerShort(serializers.ModelSerializer):

	#owner = UserSerializer()

	class Meta:
		model = Poll
		fields = ('id','owner',)


class OptionSerializer(serializers.ModelSerializer):

	#poll = PollSerializerShort()

	class Meta:
		model = Option
		fields = ('id', 'optionText','vote_quantity', 'percentage','poll',)


class VoteSerializer(serializers.ModelSerializer):

	class Meta:
		model = Vote
		fields = ('id', 'user','option', 'date',)

class VoteSerializerToPost(serializers.ModelSerializer):

	class Meta:
		model = Vote
		fields = ('id', 'user','option',)