#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import translation
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory
from django.db import IntegrityError, transaction

from askkit import settings

from users.models import *

from questions.models import *
from questions.forms import *

from core.forms import *


# Thanks to: http://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
def get_html_color_code():
	r = lambda: random.randint(0,255)
	return '#%02X%02X%02X' % (r(),r(),r())


# Thanks to: http://stackoverflow.com/a/5976065
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def question(request, name, question_token):

	# ####################################################################
	# ######################### Inner Functions ##########################
	# ####################################################################
	def colour_replies(replies):
		"""
		Generate colours for replies.
		"""

		html_color_obj = [
			
			{'color':"#FDB45C",'highlight':"#FFC870"},
			{'color':"#949FB1",'highlight':"#A8B3C5"},
			{'color':"#4D5360",'highlight':"#616774"},
			{'color':"#F7464A",'highlight':"#FF5A5E"},
			{'color':"#46BFBD",'highlight':"#5AD3D1"},
			{'color':"#4DA519",'highlight':"#5AD3D1"},
			{'color':"#7393E7",'highlight':"#5AD3D1"},
			{'color':"#7537CC",'highlight':"#5AD3D1"},
			{'color':"#A0A42A",'highlight':"#5AD3D1"},
			{'color':"#ACD287",'highlight':"#5AD3D1"},
			{'color':"#275055",'highlight':"#5AD3D1"},
			{'color':"#AF7210",'highlight':"#5AD3D1"},
		]

		# IF remain equal 0, ratings doesn't show.
		total_hits = 0
		for idx, reply in enumerate(replies):
			
			color = None
			total_hits += reply.hits
			try:
				color = html_color_obj[idx]['color']
			except Exception:

				color = get_html_color_code()
			reply.color = color

		return replies

	# ####################################################################
	def profile_has_voted(requestProfile, question):

		voted = ReplyVotedBy.objects.filter(voter=requestProfile, question=question).count()

		if voted == 1:
			return True
		elif voted == 0:
			return False
		else:
			#Hacked
			return False

	# ####################################################################
	def anonymous_has_voted(fromIp, question):

		voted = ReplyVotedBy.objects.filter(fromIp=fromIp, question=question).count()

		if voted == 1:
			return True
		elif voted == 0:
			return False
		else:
			# Hacked. Implement some alert system.
			return False

	# ####################################################################
	def is_voted_by(question, requestProfile, fromIp):
		if request.user.is_anonymous():
			return anonymous_has_voted(fromIp, question)
		else:
			return profile_has_voted(requestProfile, question)

	# ####################################################################
	def show(question, voted):

		show = True
		hide_not_available_msg = False

		if question.data_require_vote and not voted:
			show = False

		if question.hide_data:
			show = False
		return (show, hide_not_available_msg)

	# ####################################################################
	def comment_empy(commentForm):

		return commentForm.cleaned_data['text'].isspace()

	# ####################################################################
	def profile_owns_question(profile, question):
		if profile == question.asker:
			return True
		else:
			return False

	# ####################################################################
	# #################### question request init #########################
	# ####################################################################
	try:

		ip = get_client_ip(request)

		#timezone_cookie = request.COOKIES.get('askkit_timezone').replace('%2F','/')

		request_profile = None
		pro_owns_ques = False

		question = Question.objects.get(token=question_token)
		replies = question.replies.all()

		if not request.user.is_anonymous():
			request_profile = Profile.objects.get(user=request.user)
			pro_owns_ques = profile_owns_question(request_profile, question)

		# Thanks to: https://wiki.python.org/moin/HowTo/Sorting
		replies_ordered = sorted(replies, key=lambda reply: reply.hits, reverse=True)
		replies = colour_replies(replies)
		voted = is_voted_by(question, request_profile, ip)

		makeCommentForm = MakeCommentModelForm()	

		if request.method == 'POST':
			makeCommentForm = MakeCommentModelForm(request.POST)
			if makeCommentForm.is_valid() and request_profile != None and not comment_empy(makeCommentForm):
				valid = True
				comment = makeCommentForm.save(commit=False)
				comment.question = question
				comment.commenter = request_profile
				comment.save()
				makeCommentForm = MakeCommentModelForm()

	except (Profile.DoesNotExist, User.DoesNotExist, Question.DoesNotExist):
		raise Http404
	except Exception, e:
		error = True
	
	template = "questions/question.html"

	return render(request, template, locals())


@csrf_protect
def vote_reply(request):

	# Checks if ID_value is an integer
	def check_token(value):
		return True

	###################
	### ERROR
	error_code = 0
	###################
	### BAD_PARAMS
	bad_params_code = 1
	###################
	### EQUAL_USER
	equal_users_code = 2
	###################
	### ALRY_VOTED
	alry_voted_code = 3
	###################
	### REPLY DOESN'T MACH THE QUESTION
	reply_question_doesnt_match = 4
	###################
	### VOTED 
	voted = 5
	###################
	### USED IP
	used_ip = 6
	###################
	### ANONYMOUS VOTER NOT ALLOWED
	not_anonymous_voter = 7
	###################
	### OUT OF DATE
	out_of_date = 8

	######################################################################
	response = None
	######################################################################

	if request.method == 'POST':
		try:
			# Stores Request IP
			client_ip = get_client_ip(request)

			qtoken = request.POST.get("qtoken") or None
			rtoken = request.POST.get("rtoken")	or None

			# Checks incoming params are valid
			if check_token(qtoken) and check_token(rtoken):

				# DB Search checks that rtoken is a reply of qtoken. If not,
				# return error code
				try:

					reply = Reply.objects.get(token=rtoken, question__token=qtoken)
				except Reply.DoesNotExist:
					reply = None

				# If rtoken is a reply of question. PARAMS OK
				if reply:

					# Retrieves rtoken's question object.
					question = Question.objects.get(token=qtoken)

					# Cheks vote request is on date
					if question.is_active():

						# Retrieves question's replies objects
						replies = question.replies.all()

						# If user is anonymous
						if request.user.is_anonymous():

							# If qustion allow anonnymous votes
							if question.allow_anonymous_voter:
							
								# Search if request IP has voted yet.
								replyVotedBy = ReplyVotedBy.objects.filter(fromIp=client_ip, reply=replies)

								######################### [[REVIEW THIS!!!]] #######################
								# If someone try to make an anonymous vote from an ip that 
								# has been used by an account to vote this resply, the above search
								# will retrieve one or more objects, not allowing (by the "if" below ) 
								# the ip to vote. This could be get over suggesting the ip to make 
								# an account in the service.
								#
								# Its possible get all registered user ip's for this question and compare
								# them with the incoming IP. If any registered user has used the same ip
								# we could let anonymous user to vote, but this translates in a
								# two-votes-per-user scenario, one made anonymously and other made by 
								# the user account. 
								####################################################################

								# If it has voted
								if len(replyVotedBy) > 0:
									# ALREADY_VOTED #####################################################
									response = JsonResponse({'status': used_ip})
								else:
									try:
										with transaction.atomic():
											replyVotedBy = ReplyVotedBy(voter=None, reply=reply, question=question, fromIp=client_ip)
											reply.hits += 1
											question.votes += 1
											replyVotedBy.save()
											reply.save()
											question.save()
									except IntegrityError:
										#messages.error(request, 'There was an error.')
										pass
									
									# ANONYMOUS - VOTED #################################################
									response = JsonResponse({'status': voted})
							else:
								response = JsonResponse({'status': not_anonymous_voter})
						else:

							# Search if request IP has voted yet.
							voter = Profile.objects.get(user=request.user)
							repliesVotedBy = ReplyVotedBy.objects.filter(voter=voter, reply=replies, question=question)

							# QUESTION already answered
							if len(repliesVotedBy) != 0:
								# ALREADY_VOTED #####################################################
								response = JsonResponse({'status': alry_voted_code})
							else:
								#resplies = ReplyVotedBy.objects.filter(voter=voter, reply=reply)
								try:
									with transaction.atomic():
										replyVotedBy = ReplyVotedBy(voter=voter, reply=reply, question=question, fromIp=client_ip)
										reply.hits += 1
										question.votes += 1
										replyVotedBy.save()
										reply.save()
										question.save()
								except IntegrityError:
									#messages.error(request, 'There was an error.')
									pass
								
								# REGISTERED - VOTED ################################################
								response = JsonResponse({'status': voted})
					else:
						# Vote request is out of date
						response = JsonResponse({'status': out_of_date})

				else:
					# REPLY DOESN'T MACHT THE QUESTION ###########################################
					response = JsonResponse({'status': reply_question_doesnt_match})

			else:
				response = JsonResponse({'status': bad_params_code})
		except Exception as e:

			if settings.DEBUG:
				response = JsonResponse({'status': error_code, 'info': str(e)})
			else:
				response = JsonResponse({'status': error_code,})
		
		if settings.DEBUG:	
			time.sleep(1)
		return HttpResponse(response, content_type="application/json")
	else:
		raise Http404


def question_create(request):

	fake_get = False
	replies = 2

	if request.user.is_anonymous():
		request_user = None
		# Move to settings files or db.
		max_replies = 2
		warnings = ['anon']
	else:
		request_user = Profile.objects.get(user=request.user)
		# Better move to settings to db.
		max_replies = settings.MAX_REPLIES_REGISTERED
	

	# Due we make a post request to add/delete replies, we search on post params its key.
	for key in request.POST:
		if key.startswith('add_reply'):
			replies = int(key[len('add_reply')+1:])
			replies += 1
			fake_get = True
			break

		if key.startswith('delete_reply'):
			replies = int(key[len('delete_reply')+1:])
			replies -= 1
			fake_get = True
			break

	MakeReplyFormSet = modelformset_factory(Reply, ReplyForm, extra=replies, max_num=max_replies, validate_max=True)
	captchaForm = CaptchaForm()

	if request.method == 'POST':

		makeQuestionForm = QuestionForm(request.POST, prefix='question')
		makeReplyFormSet = MakeReplyFormSet(request.POST, prefix='replies')
		captchaForm = CaptchaForm(request.POST, prefix='captcha')

		makeQuestionForm.form_asker = request_user
			
		# Its avoid form reset on post_save call. STRANGE.
		if fake_get:
			request.POST['replies-TOTAL_FORMS'] = replies

		# First logic operator avoid form save on add/delete reply call.
		if not fake_get and makeQuestionForm.is_valid() and makeReplyFormSet.is_valid() and captchaForm.is_valid():

			question = makeQuestionForm.save(commit=False)
			question.asker = request_user
			question.fromIp = get_client_ip(request)
			question.save()
			makeQuestionForm.save_m2m()

			replies = makeReplyFormSet.save(commit=False)

			for reply in replies:
				reply.question = question
				reply.save()

			return HttpResponseRedirect(reverse('question', args=[question.asker or 'anon', question.token]))
	
	if request.method == 'GET':

		makeQuestionForm = QuestionForm(prefix='question')
		makeReplyFormSet = MakeReplyFormSet(queryset=Reply.objects.filter(question__id=None), prefix='replies')

	template = 'questions/create.html'
	return render(request,template,locals())


def question_update(request, name, question_token):

	# if anon user try to edit a question, redirect to dashboard
	if request.user.is_anonymous():
		return HttpResponseRedirect(reverse('dashboard'))
	else:

		# Searchs if question to edit belongs to request user...
		question = Question.objects.filter(asker=Profile.objects.filter(user=request.user), token=question_token)
		
		if len(question) == 0:
			# Does not belongs
			return HttpResponseRedirect(reverse('question', args=[name, question_token]))
		elif len(question) > 1:
			# ###########################################################################
			# THIS SHOULD NEVER HAPPEND #################################################
			# ###########################################################################
			# There is two or more quetions token asociated to the same user and token.
			# This should stores and notify the incident.
			return HttpResponseRedirect(reverse('question', args=[name, question_token]))
		else:
			# Question belongs to request's user
			question = question[0]
			replies = question.replies.all()
			replies_count = len(replies)
			fake_get = False

			if request.user.is_anonymous():
				request_user = None
				max_replies = 2
			else:
				request_user = Profile.objects.get(user=request.user)
				max_replies = settings.MAX_REPLIES_REGISTERED

			# Due we make a post request to add/delete replies, we search on post params its key.
			for key in request.POST:
				if key.startswith('add_reply'):
					replies_count = int(key[len('add_reply')+1:])
					replies_count += 1
					fake_get = True
					break

				if key.startswith('delete_reply'):
					replies_count = int(key[len('delete_reply')+1:])
					replies_count -= 1
					fake_get = True
					break

			updateQuestionForm = QuestionEditForm(request.POST or None, instance=question, prefix='question')

			UpdateReplyFormSet = inlineformset_factory(Question, Reply, form=ReplyForm, extra=0, can_delete=True)
			updateReplyFormSet = UpdateReplyFormSet(instance=question)
			#captchaForm = CaptchaForm()
			
			if request.method == 'POST':

				if fake_get:
					request.POST['replies-TOTAL_FORMS'] = replies_count

				updateReplyFormSet = UpdateReplyFormSet(request.POST, instance=question)
				#captchaForm = CaptchaForm(request.POST, prefix='captcha')

				# First logic operator avoid form save on add/delete reply call.
				#if not fake_get and updateQuestionForm.is_valid() and updateReplyFormSet.is_valid() and captchaForm.is_valid():
				if not fake_get and updateQuestionForm.is_valid() and updateReplyFormSet.is_valid():
					try:
						with transaction.atomic():
							updateQuestionForm.save()
							updateReplyFormSet.save()
					except IntegrityError:
						#messages.error(request, 'There was an error.')
						pass

					return HttpResponseRedirect(reverse('question', args=[name, question_token]))	

			template = 'questions/update.html'
			return render(request,template,locals())


def question_make_anon(request, name, question_token):

	# if anon user try to edit a question, redirect to dashboard
	if request.user.is_anonymous():
		return HttpResponseRedirect(reverse('dashboard'))
	else:

		# Searchs if question to anon belongs to request user...
		question = Question.objects.filter(asker=Profile.objects.filter(user=request.user), token=question_token)
		
		if len(question) == 0:
			# Does not belongs
			return HttpResponseRedirect(reverse('question', args=[name, question_token]))
		elif len(question) > 1:
			# ###########################################################################
			# THIS SHOULD NEVER HAPPEND #################################################
			# ###########################################################################
			# There is two or more quetions token asociated to the same user and token.
			# This should stores and notify the incident.
			return HttpResponseRedirect(reverse('question', args=[name, question_token]))
		else:
			try:
				with transaction.atomic():
					question = question[0]
					question.asker = None
					question.fromIp = None
					question.data_require_vote = True
					question.hide_data = False
					question.public = True
					######################################
					# Think about this ###################
					question.allow_anonymous_voter = True
					######################################
					# Should we generate a new token?
					######################################
					question.save()

					return HttpResponseRedirect(reverse('question', args=['anon', question_token]))
			except IntegrityError:
				#messages.error(request, 'There was an error.')
				pass

			return HttpResponseRedirect(reverse('question', args=[name, question_token]))


def question_delete(request, name, question_token):

	# if anon user try to edit a question, redirect to dashboard
	if request.user.is_anonymous():
		return HttpResponseRedirect(reverse('dashboard'))
	else:

		# Searchs if question to anon belongs to request user...
		question = Question.objects.filter(asker=Profile.objects.filter(user=request.user), token=question_token)
		
		if len(question) == 0:
			# Does not belongs
			return HttpResponseRedirect(reverse('question', args=[name, question_token]))
		elif len(question) > 1:
			# ###########################################################################
			# THIS SHOULD NEVER HAPPEND #################################################
			# ###########################################################################
			# There is two or more quetions token asociated to the same user and token.
			# This should stores and notify the incident.
			return HttpResponseRedirect(reverse('question', args=[name, question_token]))
		else:
			try:
				with transaction.atomic():

					question = question[0]
					# Implement anon copy.
					"""	
					question.id = None
					question.asker = None
					question.fromIp = None
					question.token = 'default'
					#question_copied = question.save(commit=False)
					# Copy question
					question_copied = Question(
						asker=None, 
						fromIp=None,
						allow_anonymous_voter = question.allow_anonymous_voter,
						context = question.context,
						data_require_vote = question.data_require_vote,
						date = question.date,
						date_begin = question.date_begin,
						date_end = question.date_end,
						hide_data = question.hide_data,
						public = question.public,
						question = question.question,
						votes = question.votes
					)
					
					question_copied.save()
					"""
					question.delete()

				return HttpResponseRedirect(reverse('dashboard'))
			except IntegrityError as err:
				#messages.error(request, 'There was an error.')
				pass

			return HttpResponseRedirect(reverse('question', args=[name, question_token]))



# ##########################################################################################
# #################### Class bases views test ##############################################
# ################ ONLY FOR DEVELOPMENT PURPOSES ###########################################

class QuestionDetailView(DetailView):

    model = Question
    
    """
    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    """
    def get_object(self):
    	return Question.objects.get(token=self.kwargs.get("question_token"))
    	#return Question.objects.get(name=self.kwargs.get("name"))


class QuestionCreate(CreateView):

    form_class = QuestionReplyMultiForm
    template_name = 'questions/question_form.html'

    """
    def get_context_data(self, **kwargs):
    	context = super(QuestionCreate, self).get_context_data(**kwargs)
    	# Add vars to context. For example, to render it in template.
    	return context
    """

    """
    def get_form_kwargs(self):
    	kwargs = super(QuestionCreate, self).get_form_kwargs()
    	
    	if self.request.method in ('POST', 'PUT'):
    		
    		profile = None
    		if not self.request.user.is_anonymous():
    			profile = Profile.objects.get(user=self.request.user)

			kwargs['initial']['asker'] = profile
			kwargs['initial']['fromIp'] = get_client_ip(self.request)
    		print kwargs

        return kwargs
    """

    
    # Changes this method to avoid sendind profile and ip data to the client ASAP.
    # It should be added to the form in the clean and save method.
    def get_initial(self):
    	profile = None
    	if not self.request.user.is_anonymous():
    		profile = Profile.objects.get(user=self.request.user)

    	return {
    		'question': {
    			'asker': profile, 
    			'fromIp': get_client_ip(self.request),
    		},
    		'reply': {
    			# Profile's initial data
    		},
    	}
    	#return {'asker': profile, 'fromIp': get_client_ip(self.request)}
    


    def form_valid(self, form):
    	
    	
    	# Form is validated and ready to save. Then do the following below.
    	profile = None
    	if not self.request.user.is_anonymous():
    		profile = Profile.objects.get(user=self.request.user)
    	form.instance.asker = profile
    	
    	form.instance.fromIp = get_client_ip(self.request)
    	
    	return super(QuestionCreate, self).form_valid(form)


    def get_success_url(self):
    	return reverse('question', args=[self.object.asker or 'anon', self.object.token])


class QuestionEdit(UpdateView):
	#model = Question
	form_class = QuestionEditForm
	#fields = [ 'question', 'context', 'date_begin', 'date_end', 'allow_anonymous_voter', 'data_require_vote', 'hide_data', 'public',]
	template_name = 'questions/update.html'

	def dispatch(self, *args, **kwargs):

		if self.request.user.is_anonymous():
			return HttpResponseRedirect(reverse('dashboard'))
		else:

			question = Question.objects.filter(asker=Profile.objects.filter(user=self.request.user), token=self.kwargs.get("question_token"))
			
			if len(question) == 0:
				return HttpResponseRedirect(reverse('question', args=[self.kwargs.get("name"), self.kwargs.get("question_token")]))
			elif len(question) > 1:
				# ###########################################################################
				# THIS SHOULD NEVER HAPPEND #################################################
				# ###########################################################################
				# There is two or more quetions token asociated to the same user and token.
				# This should stores and notify the incident.
				return HttpResponseRedirect(reverse('question', args=[self.kwargs.get("name"), self.kwargs.get("question_token")]))
			else:
				# Question belongs to request's user
				pass

		return super(QuestionEdit, self).dispatch(*args, **kwargs)


	def get_object(self):
		return Question.objects.get(token=self.kwargs.get("question_token"))
		#return Question.objects.get(name=self.kwargs.get("name"))

	def get_success_url(self):
		return reverse('question', args=[self.kwargs.get("name"), self.kwargs.get("question_token")])
