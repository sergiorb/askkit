#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from boto.ses import connection

class Command(BaseCommand):

    def handle(self, *args, **options):
    	email = EmailMessage('Hello', 'World', to=['inixtrom@gmail.com'])
        email.send()
        #conn =  connection.SESConnection(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        #conn.send_email('askkit.team@gmail.com', 'subj', 'body', ['askkit.team@gmail.com'])