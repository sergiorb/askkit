from django.utils import timezone
from django.utils.formats import get_language
from django.utils import translation

class LocaleMiddleware(object):
	def process_request(self, request):
		current_timezone = request.COOKIES.get('askkit_timezone', "UTC").replace('%2F','/')
		timezone.activate(current_timezone)

class LanguageMiddleware(object):
	def process_request(self, request):
		current_language = request.COOKIES.get('askkit_language', "en").replace('%2F','/')
		translation.activate(current_language)