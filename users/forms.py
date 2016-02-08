# -*- coding: utf-8 -*-

import bleach

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from betterforms.multiform import MultiModelForm
from collections import OrderedDict

from datetimewidget.widgets import DateTimeWidget
from redactor.widgets import RedactorEditor

from django.contrib.auth.models import User
from users.models import *

from passwords.fields import PasswordField

from sanitizer.forms import SanitizedCharField


class SignupUserFrom(forms.ModelForm):

	password = PasswordField()
	repassword = forms.CharField(widget=forms.PasswordInput(), label=_('Password (again)'))

	class Meta:
		model = User
		fields = ['username', 'email', 'password',]

		labels = {
			'username': _('User name'),
		}


	def clean(self):
		if 'password' in self.cleaned_data and 'repassword' in self.cleaned_data:
			if self.cleaned_data["password"] != self.cleaned_data["repassword"]:
				self.add_error('repassword', forms.ValidationError(_("You must type the same password each time,"), code='error_password'))

class SignupProfileForm(ModelForm):

	class Meta:
		model = Profile
		exclude = ['user', 'avatar', 'background', 'max_replies', 'token',]


class ProfileEditForm(ModelForm):

	class Meta:
		model = Profile
		fields = [ 'avatar', 'background', ]
		exclude = ['user', 'max_replies']

		labels = {
			'avatar': _('Profile picture'),
			'background': _('Profile background picture'),
		}


class UserEditForm(ModelForm):

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email',]
		
		labels = {
			'username': _('User name'),
		}