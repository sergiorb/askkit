# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('tittle', models.CharField(max_length=140)),
                ('message', models.TextField(null=True, blank=True)),
                ('style', models.CharField(default=b'DE', max_length=2, choices=[(b'DE', 'Default'), (b'PR', 'Primary'), (b'SU', 'Success'), (b'IN', 'Info'), (b'WA', 'Warning'), (b'DA', 'Danger')])),
                ('status', models.CharField(default=b'CR', max_length=2, choices=[(b'CR', 'Created'), (b'RE', 'Readed')])),
                ('user', models.ForeignKey(related_name='notifications', to='users.Profile')),
            ],
        ),
    ]
