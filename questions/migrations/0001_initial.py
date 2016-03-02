# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 03:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('context', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('date_begin', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('public', models.BooleanField(default=True)),
                ('question', models.CharField(max_length=140)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
