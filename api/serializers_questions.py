from rest_framework import serializers

from questions.models import Question, Reply

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ('id','owner','question','added_on','context','date_begin',
			'date_end','public','total_votes','replies',)

class ReplySerializer(serializers.ModelSerializer):
	class Meta:
		model = Reply