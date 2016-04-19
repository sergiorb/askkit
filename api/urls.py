from collections import OrderedDict, namedtuple

from django.conf.urls import url, include
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import routers
from rest_framework.authtoken import views

from .views_celery import GetTaskStatus, CountVotes
from .views_polls import PollViewSet, OptionViewSet, VoteViewSet
from .views_users import UserViewSet

#router = MyCustomRouter()
router = routers.DefaultRouter()
#router = routers.SimpleRouter()

router.register(r'polls', PollViewSet)
router.register(r'options', OptionViewSet)
router.register(r'votes', VoteViewSet)
#router.register(r'core/tasks/', get_task_status.as_view(), base_name='tasks')
#router.register(r'core/processes', count_all_votes, base_name='processes')
#router.register(r'users', UserViewSet)

urlpatterns = [
	url(r'^', include(router.urls, namespace='api')),

	url(r'^users/', include('djoser.urls.authtoken')),

	url(r'^core/tasks/(?P<pk>[^/]+)/$', GetTaskStatus.as_view(), 
		name='core_task_status'),

	#url(r'^auth/session/', include('djoser.urls')),

	#url(r'^core/count/$', CountVotes.as_view(), 
	#	name='core_vote_count'),

	# Disable this for production.
    #url(r'^api-auth/', include('rest_framework.urls', 
    #	namespace='rest_framework')),

    #url(r'^request-auth-token/', views.obtain_auth_token)

    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]