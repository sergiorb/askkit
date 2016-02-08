# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('commenter', models.ForeignKey(related_name='profileComments', to='users.Profile')),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='questions.Comment', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow_anonymous_voter', models.BooleanField(default=True)),
                ('context', models.TextField(null=True, blank=True)),
                ('data_require_vote', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('date_begin', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_end', models.DateTimeField(null=True, blank=True)),
                ('fromIp', models.GenericIPAddressField()),
                ('hide_data', models.BooleanField(default=False)),
                ('question', models.CharField(max_length=140)),
                ('token', models.TextField(default=b'default')),
                ('votes', models.IntegerField(default=0)),
                ('public', models.BooleanField(default=True)),
                ('asker', models.ForeignKey(related_name='questions', blank=True, to='users.Profile', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=7, null=True, blank=True)),
                ('hits', models.BigIntegerField(default=0)),
                ('replyText', models.CharField(max_length=50)),
                ('token', models.TextField(default=b'default')),
                ('question', models.ForeignKey(related_name='replies', to='questions.Question')),
            ],
        ),
        migrations.CreateModel(
            name='ReplyVotedBy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fromIp', models.GenericIPAddressField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(related_name='questionVotes', to='questions.Question')),
                ('reply', models.ForeignKey(related_name='replyVote', to='questions.Reply')),
                ('voter', models.ForeignKey(blank=True, to='users.Profile', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(related_name='comments', to='questions.Question'),
        ),
    ]
