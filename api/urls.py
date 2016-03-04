from django.conf.urls import url, include

from rest_framework import routers

from .views_celery import GetTaskStatus
from .views_questions import QuestionViewSet, ReplyViewSet, AddVote
from .views_questions import SubtractVote

router = routers.DefaultRouter()

router.register(r'questions', QuestionViewSet)
router.register(r'replies', ReplyViewSet)

urlpatterns = [
	url(r'^', include(router.urls, namespace='api')),

	url(r'^replies/(?P<pk>[^/]+)/addvote$', AddVote.as_view(), 
		name='reply_add_vote'),

	url(r'^replies/(?P<pk>[^/]+)/subtractvote$', SubtractVote.as_view(), 
		name='reply_subtract_vote'),

	url(r'^core/tasks/(?P<pk>[^/]+)/status$', GetTaskStatus.as_view(), 
		name='core_task_status'),

    url(r'^api-auth/', include('rest_framework.urls', 
    	namespace='rest_framework'))
]