# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151023_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(default=b'OP', max_length=2, choices=[(b'OP', 'Opened'), (b'IC', 'In curse'), (b'Re', 'Resolved')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='subject',
            field=models.CharField(default=b'Err', max_length=3, choices=[(b'Err', 'Errors'), (b'Sug', 'Sugestions'), (b'Acc', 'Accounts'), (b'Leg', 'Legal'), (b'Otr', 'Others')]),
        ),
    ]
