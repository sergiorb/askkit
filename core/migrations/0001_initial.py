# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151022_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140, null=True, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('messages', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('fromIp', models.GenericIPAddressField(null=True, blank=True)),
                ('token', models.TextField(default=b'default')),
                ('status', models.CharField(default=b'Re', max_length=2, choices=[(b'OP', 'Opened'), (b'IC', 'In curse'), (b'Re', 'Resolved')])),
                ('subject', models.CharField(default=b'Re', max_length=3, choices=[(b'Err', 'Errors'), (b'Sug', 'Sugestions'), (b'Acc', 'Accounts'), (b'Leg', 'Legal'), (b'Otr', 'Others')])),
                ('asker', models.ForeignKey(related_name='reports', blank=True, to='users.Profile', null=True)),
            ],
        ),
    ]
