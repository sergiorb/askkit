# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151022_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default=b'default/default-avatar.jpg', upload_to=users.models.generate_avatar_filename),
        ),
        migrations.AlterField(
            model_name='profile',
            name='background',
            field=imagekit.models.fields.ProcessedImageField(default=b'default/default-background.jpg', upload_to=users.models.generate_background_filename),
        ),
    ]
