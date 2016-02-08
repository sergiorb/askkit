#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key


class Command(BaseCommand):

    def handle(self, *args, **options):

    	conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, host=settings.AWS_S3_HOST)
    	bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    	k = Key(bucket)
    	k.key = 'media/default/default.jpg' # for example, 'images/bob/resized_image1.png'
    	
    	file_path = settings.BASE_DIR+'/static/media/default/default.jpg'
    	f = open(file_path, 'r')

    	k.set_contents_from_file(f)
