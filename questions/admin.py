#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

# Register your models here.

class FullAdmin(admin.ModelAdmin):
    readonly_fields = ('date','id',)


admin.site.register(Question, FullAdmin)
admin.site.register(Reply)
admin.site.register(ReplyVotedBy, FullAdmin)
admin.site.register(Comment)