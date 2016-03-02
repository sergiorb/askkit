from django.conf.urls import url, include

from .views import QuestionListView, AddVote, SubtractVote, RandomVote, RandomVoteAsync

urlpatterns = [
	url(r'^$', QuestionListView.as_view(), name='question_list'),
	url(r'^addvote/$', AddVote.as_view(), name='question_add_vote'),
	url(r'^subtractvote/$', SubtractVote.as_view(), name='question_subtract_vote'),
	url(r'^randomvote/$', RandomVote.as_view(), name='reply_random_vote'),
	url(r'^randomvoteasync/$', RandomVoteAsync.as_view(), name='reply_random_vote_async')
]