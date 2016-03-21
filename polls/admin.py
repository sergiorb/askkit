from django.contrib import admin

from .models import Poll, Option, Vote

# Register your models here.

class OptionInline(admin.TabularInline):
	model = Option


class PollAdmin(admin.ModelAdmin):

	def is_active(self, obj):
		return obj.is_active()

	def short_title(self, obj):
		return obj.short_title()

	def options_count(self, obj):
		return obj.options_count()

	fields = (
		'title', 
		'context',
		'added_on',
		'date_begin',
		'date_end',
		'public',
		'anon_allowed',
		'owner',
		'total_votes',
	)

	readonly_fields = (
		'added_on',
	)

	list_display = (
		'short_title',
		'added_on',
		'date_begin',
		'date_end',
		'is_active',
		'options_count',
		'total_votes',
		'public',
	)
	
	list_filter = (
		'public',
	)

	search_fields = (
		'added_on',
		'date_begin',
		'date_end',
	)

	inlines = [
		OptionInline,
	]


class OptionAdmin(admin.ModelAdmin):

	def percentage(self, obj):
		return obj.percentage()

	fields = (
		'optionText',
		'vote_quantity',
		'added_on',
		'poll', 
	)

	readonly_fields = (
		'added_on',
	)

	list_display = (
		'optionText',
		'vote_quantity',
		'added_on',
		'poll', 
	)

	list_filter = (
		'vote_quantity',
	)

	search_fields = (
		'added_on',
	)

class VoteAdmin(admin.ModelAdmin):

	fields = (
		'id',
		'user', 
		'option',
		'fromIp',
		'date',
	)

	readonly_fields = (
		'id',
		'date',
	)

	list_display = (
		'user',
		'option',
		'fromIp',
		'date',
	)
	
	search_fields = (
		'fromIp',
	)


admin.site.register(Poll, PollAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Vote, VoteAdmin)