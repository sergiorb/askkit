import pytz
from django.apps import apps
from django.conf import settings

def debug(request):
	return {'DEBUG': settings.DEBUG}


def common_timezones(request):
	return {'common_timezones': pytz.common_timezones}


def current_timezone(request):
	
	# ADD function fallback. Sesson > cookie > request > default
	try:
		current_timezone = request.COOKIES.get('askkit_timezone').replace('%2F','/')
	except:
		current_timezone = None
	return {'current_timezone': current_timezone}

def get_adsense_yes(request):
	return { 'ADSENSE_YES': settings.ADSENSE_YES }


def get_adsense_user(request):
	return { 'ADSENSE_USER': settings.ADSENSE_USER }


def get_adsense_main(request):
	return { 'ADSENSE_MAIN': settings.ADSENSE_MAIN }


def get_analytics_id(request):
	return { 'G_ANALYTICS_ID': settings.G_ANALYTICS_ID }
