# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from betterforms.multiform import MultiModelForm
from collections import OrderedDict

from datetimewidget.widgets import DateTimeWidget
from redactor.widgets import RedactorEditor

from questions.models import *



class QuestionForm(ModelForm):

	def __init__(self, *args, **kargs):
		# Due we don't want to send to client info about user's request, we have created the below var to store
		# in it this info and validate it.
		self.form_asker = None
		super(QuestionForm, self).__init__(*args)

	class Meta:
		model = Question
		fields = [ 'question', 'context', 'date_begin', 'date_end', 'allow_anonymous_voter', 'data_require_vote', 'hide_data', 'public','asker', 'fromIp',]
		exclude = ['hide_data','asker', 'fromIp']

		labels = {
			'question': _('Question title:'),
			'context': _('Write something more:'),
			'date_begin': _('Open vote in:'),
			'date_end': _('Close vote in:'),
			'allow_anonymous_voter': _('Allow anonymous vote.'),
			'data_require_vote': _('Require vote to show charts.'), 
			'hide_data': _('Hide chart.'),
			'public': _('Shown in \'Random question\'.'),
		}

		widgets = {
			'date_begin': DateTimeWidget(usel10n = True, bootstrap_version=3),
			'date_end': DateTimeWidget(usel10n = True, bootstrap_version=3),
			'context': RedactorEditor(
				allow_file_upload=False, 
				allow_image_upload=False, 
				attrs={'rows': '2', 'cols':'2',}),
			#'asker': forms.HiddenInput(),
			#'fromIp': forms.HiddenInput(),
		}

	def clean(self):
		
		################
		# RECHECK THIS #
		######################################################################################################
		# print self.cleaned_data['date_begin']
		#
		# It seems that date_begin it's a timezone-aware object but doesn't store zone offset. 
		# This makes it imposible to convert it to UTC timezone in order to compare it at level server.
		#
		# if self.cleaned_data['date_begin'] < timezone.now():
		#	self.add_error('date_begin', ValidationError(_('Begin date has to be equal or after current time.'), code='error_date_begin'))
		"""
		print self.cleaned_data
		print "Date_begin: ", self.cleaned_data['date_begin']


		if self.cleaned_data['date_begin']:
			self.add_error('date_begin', ValidationError(_('You need to enter a date to open vote'), code='error_date_begin'))
		"""

		if 'date_begin' in self.cleaned_data and self.cleaned_data['date_begin'] != None: 
			if 'date_end' in self.cleaned_data and self.cleaned_data['date_end'] != None: 
				if self.cleaned_data['date_end'] < self.cleaned_data['date_begin']:
					self.add_error('date_end', ValidationError(_('End date has to be after begin date.'), code='error_date_end'))

		# Here we use form_asker var that we have created before to validate public in anon question.
		if self.form_asker == None and self.cleaned_data['public'] == False:
			self.add_error('public', ValidationError(_('Anon questions have to be public.'), code='error_public'))


# When QuestionEditForm inherit from QuestionForm, update view doesn't load question instance, rendering a new object.
# It seems that overriden init method it's causing this issue.
class QuestionEditForm(ModelForm):

	class Meta:
		model = Question
		fields = [ 'question', 'context', 'date_begin', 'date_end', 'hide_data', 'allow_anonymous_voter', 'data_require_vote', 'public','asker', 'fromIp',]
		exclude = ['asker', 'fromIp']

		labels = {
			'question': _('Question title:'),
			'context': _('Write something more:'),
			'date_begin': _('Open vote in:'),
			'date_end': _('Close vote in:'),
			'allow_anonymous_voter': _('Allow anonymous voter.'),
			'data_require_vote': _('Require vote to show charts.'), 
			'hide_data': _('Hide chart.'),
			'public': _('This question could be shown in \'Random question\'.'),
		}

		widgets = {
			'date_begin': DateTimeWidget(usel10n = True, bootstrap_version=3),
			'date_end': DateTimeWidget(usel10n = True, bootstrap_version=3),
			#'context': forms.Textarea(attrs={'rows': '2'}),
			'context': RedactorEditor(allow_file_upload=False, allow_image_upload=False),
			#'asker': forms.HiddenInput(),
			#'fromIp': forms.HiddenInput(),
		}

	def clean(self):

		######################################################################################################
		# print self.cleaned_data['date_begin']
		#
		# It seems that date_begin it's a timezone-aware object but doesn't store zone offset. 
		# This makes it imposible to convert it to UTC timezone in order to compare it at level server.
		#
		# if self.cleaned_data['date_begin'] < timezone.now():
		#	self.add_error('date_begin', ValidationError(_('Begin date has to be equal or after current time.'), code='error_date_begin'))

		if 'date_begin' in self.cleaned_data and self.cleaned_data['date_begin'] != None: 
			if 'date_end' in self.cleaned_data and self.cleaned_data['date_end'] != None: 
				if self.cleaned_data['date_end'] < self.cleaned_data['date_begin']:
					self.add_error('date_end', ValidationError(_('End date has to be after begin date.'), code='error_date_end'))

		# Here we use form_asker var that we have created before to validate public in anon question.
		if self.instance.asker == None and self.cleaned_data['public'] == False:
			self.add_error('public', ValidationError(_('Anon questions have to be public.'), code='error_public'))

class ReplyForm(ModelForm):

	class Meta:
		model = Reply
		fields = ['replyText', 'question',]
		exclude = ['question',]

		labels = {
			'replyText': _('Reply text'),
		}

		help_texts = {
            #'replyText': _('If you need a long text reply, we recommend you to write here a number/letter reference and make a full description at question level.'),
        }

		widgets = {
          #'question': forms.HiddenInput(),
        }


class QuestionReplyMultiForm(MultiModelForm):
    form_classes = OrderedDict((
        ('question', QuestionForm),
        ('reply', ReplyForm),
    ))

    def save(self, commit=True):
    	objects = super(QuestionReplyMultiForm, self).save(commit=False)

    	if commit:
            question = objects['question']
            question.save()
            reply = objects['reply']
            reply.question = question
            reply.save()

        return objects