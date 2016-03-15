from django.conf.urls import url, include

from rest_framework import routers

from .views_celery import GetTaskStatus
from .views_polls import PollViewSet, OptionViewSet

router = routers.DefaultRouter()

router.register(r'polls', PollViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = [
	url(r'^', include(router.urls, namespace='api')),

	url(r'^core/tasks/(?P<pk>[^/]+)/status$', GetTaskStatus.as_view(), 
		name='core_task_status'),

    url(r'^api-auth/', include('rest_framework.urls', 
    	namespace='rest_framework'))
]