from django import template
from django.utils.translation import ugettext_lazy as _
from users.models import Profile
register = template.Library()

#@register.filter(name='print_annonymous')
@register.filter
def print_anonymous(user):

		if user.is_anonymous():
			return _('Anonymous')
		else:
			return user

@register.filter
def print_anonymous_profile(profile):

	try:
		if profile.user.is_anonymous():
			return _('Anonymous')
		else:
			return profile
	except:
		return _('Anonymous')

@register.filter
def print_anon_profile(profile):

	try:
		if profile.user.is_anonymous():
			return 'anon'
		else:
			return profile
	except:
		return 'anon'

@register.filter
def print_user_avatar(user):
	
	try:
		obj = Profile.objects.get(user=user)
	except Exception, e:
		return 'default/default.jpg'
	
	return obj.avatar


@register.filter
def get_Profile(user):
	
	try:
		obj = Profile.objects.get(user=user)
	except Exception, e:
		return None	
	return obj
