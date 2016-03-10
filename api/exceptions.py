from django.db.models.deletion import ProtectedError
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.compat import set_rollback
from rest_framework.response import Response


def custom_exception_handler(exc, context):
	"""
	Adds exceptions handlers to api
	"""

	# Executes when django models ProtectedError raise
	if isinstance(exc, ProtectedError):
		msg = _('This object has protected foreign keys.')
		data = {'detail': six.text_type(msg)}

		set_rollback()
		return Response(data, status=status.HTTP_403_FORBIDDEN)

	return None


def status_code_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    if response is None:
    	response = custom_exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response