# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151022_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='token',
            field=models.TextField(default=b'default'),
        ),
    ]
