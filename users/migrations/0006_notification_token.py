# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='token',
            field=models.TextField(default=b'default'),
        ),
    ]
