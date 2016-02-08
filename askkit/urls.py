#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin

#from users.views import *

from allauth.account import views

#from django.conf.urls.i18n import i18n_patterns

from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^redactor/', include('redactor.urls')),
]

users_patterns = [
	url(r'^(?P<name>\w+)$', 'users.views.public_profile', name='public_profile'),
    url(r'^settings/profile$', 'users.views.profile_edit', name='profile_edit'),
]

questions_patterns = [
    #url(r'^(?P<name>\w+)/question/(?P<question_token>\w+)$', QuestionDetailView.as_view(), name='question'),
    #url(r'^(?P<name>\w+)/question/(?P<question_token>\w+)/edit$', QuestionEdit.as_view(), name='question_update'),
    url(r'^question/create$', 'questions.views.question_create', name='question_create'),
    url(r'^(?P<name>\w+)/question/(?P<question_token>\w+)$', 'questions.views.question', name='question'),
    url(r'^(?P<name>\w+)/question/(?P<question_token>\w+)/edit$', 'questions.views.question_update', name='question_update'),
    url(r'^question/vote/reply$', 'questions.views.vote_reply', name='vote_reply'),
    url(r'^(?P<name>\w+)/question/(?P<question_token>\w+)/make/anon$', 'questions.views.question_make_anon', name='question_make_anon'),
    url(r'^(?P<name>\w+)/question/(?P<question_token>\w+)/delete$', 'questions.views.question_delete', name='question_delete'),
]

core_patterns = [
    url(r'^$', 'core.views.dashboard', name='dashboard'),
    url(r'^about$', 'core.views.about', name='about'),
    url(r'^private-policy$', 'core.views.private_policy', name='private_policy'),
    url(r'^contact$', 'core.views.contact', name='contact'),
    url(r'^random/question/', 'core.views.rand_question', name='rand_question'),
    url(r'^servererror404/', 'core.views.servererror404', name='servererror404'),
    url(r'^servererror500/', 'core.views.servererror500', name='servererror500'),
]

urlpatterns += core_patterns
urlpatterns += users_patterns
urlpatterns += questions_patterns

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )