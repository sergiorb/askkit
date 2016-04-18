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

class MyCustomRouter(routers.DefaultRouter):

	def get_api_root_view(self):
		"""
		Return a view to use as the API root.
		"""
		api_root_dict = OrderedDict()
		list_name = self.routes[0].name
		for prefix, viewset, basename in self.registry:
			api_root_dict[prefix] = list_name.format(basename=basename)

		class APIRoot(views.APIView):
			_ignore_model_permissions = True

			def get(self, request, *args, **kwargs):
				ret = OrderedDict()
				namespace = request.resolver_match.namespace
				for key, url_name in api_root_dict.items():
					if namespace:
						url_name = namespace + ':' + url_name
					try:
						ret[key] = reverse(
						url_name,
						args=args,
						kwargs=kwargs,
						request=request,
						format=kwargs.get('format', None)
						)
					except NoReverseMatch:
						# Don't bail out if eg. no list routes exist, only detail routes.
						continue

				return Response(ret)

		return APIRoot.as_view()

router = MyCustomRouter()
#router = routers.DefaultRouter()
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