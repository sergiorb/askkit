from rest_framework import serializers

from polls.models import Poll, Option

class UserSerializer(serializers.Serializer):
	
	pk = serializers.CharField(max_length=100)
	username = serializers.CharField(max_length=100)

class PollSerializer(serializers.ModelSerializer):

	owner = UserSerializer(required=False)

	class Meta:
		model = Poll
		fields = ('id','owner','title','added_on','context','date_begin',
			'date_end','public','total_votes','options',)

class PollSerializerShort(serializers.ModelSerializer):

	owner = UserSerializer()

	class Meta:
		model = Poll
		fields = ('id','owner',)

class OptionSerializer(serializers.ModelSerializer):

	poll = PollSerializerShort()

	class Meta:
		model = Option
		fields = ('id', 'optionText','vote_quantity',
			'percentage','poll',)