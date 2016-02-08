# -*- coding: utf-8 -*-

import bleach

from django.shortcuts import render
from django.db import IntegrityError, transaction
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from users.models import *
from users.forms import *



# Create your views here.

def public_profile(request, name):

	###########################################
	# PERFORMACE ##############################
	###########################################
	# Unify db queries to increase performace
	###########################################
		
	votes_num = 0
	pro_owns_pro = False

	try:
		profile = Profile.objects.get(user=User.objects.get(username__iexact=name))
		questions = profile.questions.order_by('date').reverse()
		for question in questions:
			votes_num += question.votes
	except (Profile.DoesNotExist, User.DoesNotExist):
		raise Http404

	#request_profile = Profile.objects.get(user=request.user)

	#if request_profile == profile:
	#	pro_owns_pro = True

	#questions = Question.objects.filter(asker=profile).order_by('date').reverse()

	template = 'users/public_profile.html'
	return render(request, template, locals())


def profile_edit(request):

	name = request.user
	
	if request.user.is_anonymous():
		return HttpResponseRedirect(reverse('dashboard'))

	profile = Profile.objects.filter(user=request.user)

	if len(profile) != 1:
		return HttpResponseRedirect(reverse('dashboard'))

	profile = profile[0]
	votes_num = 0
	
	questions = profile.questions.order_by('date').reverse()
	
	for question in questions:
		votes_num += question.votes
	

	userEditForm = UserEditForm(prefix='user', instance=request.user)
	profileEditForm = ProfileEditForm(prefix='profile', instance=profile)

	if request.method == 'POST':
		userEditForm = UserEditForm(request.POST, prefix='user', instance=request.user)
		profileEditForm = ProfileEditForm(request.POST, request.FILES, prefix='profile', instance=profile)
		if userEditForm.is_valid() and profileEditForm.is_valid():
			try:
				with transaction.atomic():
					userEditForm.save()
					profileEditForm.save()
				return HttpResponseRedirect(reverse('public_profile', args=[name]))
			except IntegrityError:
				pass

	name = profile
	user = profile

	template = "users/profile_edit.html"
	return render(request, template, locals())


class ProfileEdit(UpdateView):
	#model = Question
	form_class = ProfileEditForm
	#fields = [ 'question', 'context', 'date_begin', 'date_end', 'allow_anonymous_voter', 'data_require_vote', 'hide_data', 'public',]
	template_name = 'users/profile_edit.html'

	def dispatch(self, *args, **kwargs):

		if self.request.user.is_anonymous():
			return HttpResponseRedirect(reverse('dashboard'))

		return super(ProfileEdit, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):

		context = super(ProfileEdit, self).get_context_data(**kwargs)
		# Add vars to context. For example, to render it in template.
		context.update({'name': self.kwargs.get('name'), })
		return context

	def get_object(self):
		return Profile.objects.get(user=self.request.user)

	def get_success_url(self):
		return reverse('public_profile', args=[self.object])