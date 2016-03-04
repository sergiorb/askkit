from django.views.generic import View
from django.http import JsonResponse

from core.functions import get_task_status

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
		print status
		return JsonResponse({'status':status})