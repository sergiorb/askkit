from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.functions import get_task_status
from polls.tasks import update_votes

"""
@api_view(['GET',])
def get_task_status(request):

	status = get_task_status(self.kwargs['pk'])

	return Response({'status':status})


@api_view(['POST',])
def count_all_votes(request):

	task = update_votes.delay()

	return Response({
		'status_code': 200,
		'task_id': task.task_id,
		'detail': 'Your request have been queued.'
		})
"""