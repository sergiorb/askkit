from celery.result import AsyncResult

def get_task_status(pk):
	"""
		Returns task state of given id.
	"""

	res = AsyncResult(pk)
	return res.state