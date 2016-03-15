from django.conf.urls import url, include

from .views import PollListView, AddVote, SubtractVote, RandomVote
from .views import ResetPollVotes

urlpatterns = [
	url(r'^$', PollListView.as_view(), 
		name='poll_list'),
	
	url(r'^addvote/$', AddVote.as_view(), 
		name='poll_add_vote'),

	url(r'^subtractvote/$', SubtractVote.as_view(), 
		name='poll_subtract_vote'),

	url(r'^randomvote/$', RandomVote.as_view(), 
		name='option_random_vote'),

	url(r'^resetpollvotes/$', ResetPollVotes.as_view(), 
		name='reset_poll_votes')
]