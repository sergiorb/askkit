# -*- coding: utf-8 -*-

import random

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import IntegrityError, transaction
from django.core.urlresolvers import reverse
from django.views.generic import View

from allauth.utils import get_form_class, get_request_param, get_current_site
from allauth import app_settings
from allauth.account.forms import *


from questions.models import *
from questions.forms import *

from users.models import *
from users.forms import *

from core.forms import *
from core.lib import *
from core.auto_strings import *

from hashids import Hashids


def get_random_question():
	try:
		return Question.objects.filter(public=True)[random.randint(0,Question.objects.filter(public=True).count()-1)]
	except:
		return None

def get_profile(user):
	try:
		return Profile.objects.get(user=user)
	except:
		return None

def profile_has_voted(requestProfile, question):

		voted = ReplyVotedBy.objects.filter(voter=requestProfile, question=question).count()

		if voted == 1:
			return True
		elif voted == 0:
			return False
		else:
			#Hacked. Implement some alert system.
			return False

def anonymous_has_voted(fromIp, question):

	voted = ReplyVotedBy.objects.filter(fromIp=fromIp, question=question).count()

	if voted == 1:
		return True
	elif voted == 0:
		return False
	else:
		#Hacked. Implement some alert system.
		return False

def is_voted_by(request, question, requestProfile, fromIp):
	if request.user.is_anonymous():
		return anonymous_has_voted(fromIp, question)
	else:
		return profile_has_voted(requestProfile, question)

# http://stackoverflow.com/a/4581997/4922377
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def dashboard(request):
	
	profile = None
	notifications = None
	question = get_random_question()
	
	if not request.user.is_anonymous():
		profile = get_profile(request.user)
		if profile:
			notifications = profile.notifications.exclude(status='RE')
	
	if question:
		replies = question.replies.all()
		#https://wiki.python.org/moin/HowTo/Sorting
		replies_ordered = sorted(replies, key=lambda reply: reply.hits, reverse=True)
		replies = colour_replies(replies)
		ip = get_client_ip(request)
		voted = is_voted_by(request, question, profile, ip)

	form = LoginForm()

	if request.method == 'POST':

		form = LoginForm(request.POST)
		
		if form.is_valid():

			perform_login(request, self.user, email_verification=app_settings.EMAIL_VERIFICATION, redirect_url='/')
			remember = app_settings.SESSION_REMEMBER

			if remember is None:
				remember = self.cleaned_data['remember']
			if remember:
				request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
			else:
				request.session.set_expiry(0)

	template = "core/dashboard.html"
	return render(request, template, locals())


def about(request):
	template = "core/about.html"
	return render(request, template, locals())

def private_policy(request):
	template = "core/private_policy.html"
	return render(request, template, locals())

def contact(request):
	reportForm = ReportForm(prefix='report')
	captchaForm = CaptchaForm(prefix='captcha')

	if request.method == 'POST':

		reportForm = ReportForm(request.POST, prefix='report')
		captchaForm = CaptchaForm(request.POST, prefix='captcha')

		if reportForm.is_valid() and captchaForm.is_valid():
			report_obj = None
			try:
				if not request.user.is_anonymous():
					with transaction.atomic():
						report = reportForm.save(commit=False)
						report.asker = Profile.objects.get(user=request.user)
						report.save()
				else:
					report_obj = reportForm.save()
				reportFormOK = True

			except IntegrityError:
				reportFormERROR = True
			except Exception:
				reportFormERROR = True

			reportForm = ReportForm(prefix='report')
		captchaForm = CaptchaForm(prefix='captcha')
	template = "core/contact.html"
	return render(request, template, locals())


def rand_question(request):

	try:
		question = Question.objects.filter(public=True)[random.randint(0,Question.objects.filter(public=True).count()-1)]
	except:
		raise Http404
	
	url = reverse('question', args=[question.asker or 'anon', question.token])
	return redirect(url)
	

def search(request, string):

	string = string
	template = "core/search_result.html"
	return render(request, template, locals())


def fast_render(request):

	template = "questions/test.html"
	return render(request, template, locals())

def servererror500(request):
	template = "500.html"
	return render(request, template, locals())

def servererror404(request):
	template = "404.html"
	return render(request, template, locals())