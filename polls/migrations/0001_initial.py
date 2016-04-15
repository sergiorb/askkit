# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 02:35
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
            name='Option',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(blank=True, null=True)),
                ('optionText', models.CharField(max_length=140)),
                ('vote_quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(blank=True, null=True)),
                ('context', models.TextField(blank=True, null=True)),
                ('date_begin', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('public', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=140)),
                ('total_votes', models.IntegerField(default=0)),
                ('anon_allowed', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PollAuthToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll', to='polls.Poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_auth_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fromIp', models.GenericIPAddressField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option', to='polls.Option')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='polls.Poll'),
        ),
    ]
