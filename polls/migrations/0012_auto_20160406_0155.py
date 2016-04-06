# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-06 01:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20160323_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 6, 1, 55, 36, 839343, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='option',
            name='added_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vote',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
