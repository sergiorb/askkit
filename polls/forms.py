from django.forms import ModelForm
from .models import Poll, Option, Vote

class PollForm(ModelForm):
	class Meta:
		model = Poll
		fields = ['__all__']

	def validate(self, attrs):
           if len(attrs['items']) > YOUR_MAX:
               raise serializers.ValidationError("Invalid number of items")