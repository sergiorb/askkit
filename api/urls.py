from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views

from .views_celery import GetTaskStatus, CountVotes
from .views_polls import PollViewSet, OptionViewSet, VoteViewSet
from .views_users import UserViewSet

router = routers.DefaultRouter()

router.register(r'polls', PollViewSet)
router.register(r'options', OptionViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
	url(r'^', include(router.urls, namespace='api')),

	url(r'^core/tasks/(?P<pk>[^/]+)/$', GetTaskStatus.as_view(), 
		name='core_task_status'),

	url(r'^core/count/$', CountVotes.as_view(), 
		name='core_vote_count'),

	# Disable this for production.
    url(r'^api-auth/', include('rest_framework.urls', 
    	namespace='rest_framework')),

    url(r'^request-auth-token/', views.obtain_auth_token)

    #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]