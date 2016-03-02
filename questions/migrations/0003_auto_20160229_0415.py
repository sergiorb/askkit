# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20160229_0337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vote_quantity', models.PositiveIntegerField(default=0)),
                ('replyText', models.CharField(max_length=140)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='questions.Question'),
        ),
    ]
