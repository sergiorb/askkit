from django.http import JsonResponse
from django.views.generic import View

from rest_framework.response import Response
from rest_framework.decorators import api_view


from core.functions import get_task_status
from polls.tasks import update_votes

# Create your views here.


class GetTaskStatus(View):
	"""
		Returns task status from given id.
	"""

	def get(self, request, *args, **kwargs):
		"""
			Executes get_task_status task and returns task state.
		"""

		status = get_task_status(self.kwargs['pk'])

		return JsonResponse({'status':status})


class CountVotes(View):

	def get(self, request, *args, **kwargs):

		task = update_votes.delay()

		return JsonResponse({
			'status_code': 200,
			'task_id': task.task_id,
			'detail': 'Your request have been queued.'
			})