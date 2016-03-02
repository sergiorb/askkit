from django.contrib import admin

from .models import Question, Reply

# Register your models here.

class ReplyInline(admin.TabularInline):
	model = Reply


class QuestionAdmin(admin.ModelAdmin):

	def is_active(self, obj):
		return obj.is_active()

	def short_question(self, obj):
		return obj.short_question()

	def replies_count(self, obj):
		return obj.replies_count()

	fields = (
		'question', 
		'context',
		'added_on',
		'date_begin',
		'date_end',
		'public',
		'owner',
		'total_votes',
	)

	readonly_fields = (
		'added_on',
	)

	list_display = (
		'short_question',
		'added_on',
		'date_begin',
		'date_end',
		'is_active',
		'replies_count',
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
		ReplyInline,
	]


class ReplyAdmin(admin.ModelAdmin):

	def percentage(self, obj):
		return obj.percentage()

	fields = (
		'replyText',
		'vote_quantity',
		'added_on',
		'question', 
	)

	readonly_fields = (
		'added_on',
	)

	list_display = (
		'replyText',
		'vote_quantity',
		'added_on',
		'question', 
	)

	list_filter = (
		'vote_quantity',
	)

	search_fields = (
		'added_on',
	)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Reply, ReplyAdmin)