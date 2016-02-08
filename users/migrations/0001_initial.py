# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(default=b'default/default-avatar.jpg', upload_to=users.models.generate_avatar_filename)),
                ('background', models.ImageField(default=b'default/default-background.jpg', upload_to=users.models.generate_background_filename)),
                ('max_replies', models.IntegerField(default=3)),
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
