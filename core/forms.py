# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from betterforms.multiform import MultiModelForm
from collections import OrderedDict

from datetimewidget.widgets import DateTimeWidget
from redactor.widgets import RedactorEditor
from captcha.fields import ReCaptchaField

from core.models import *


class CaptchaForm(Form):

	captcha = ReCaptchaField()


class ReportForm(ModelForm):

	class Meta:
		model = Report
		fields = [ 'subject', 'name', 'email', 'message', ]
		exclude = ['status','token','asker', 'date',]

		widgets = {
			'message': RedactorEditor(
				allow_file_upload=False, 
				allow_image_upload=False,
				attrs={'rows': '2', 'cols':'2',}),
		}
		
	def clean_message(self):
		if not self.cleaned_data['message']:
			self.add_error('message', ValidationError(_('This field can\'t be empty.'), code='error_date_end'))
		else:
			return self.cleaned_data['message']