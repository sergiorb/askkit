from django.core.management.base import BaseCommand, CommandError

from polls import tasks


class Command(BaseCommand):

	help = 'Updates polls votes in the entire db.'


	def handle(self, *args, **options):

		self.stdout.write(self.style.NOTICE('Launching update task...'))

		task = tasks.update_votes.delay()

		self.stdout.write(self.style.SUCCESS('Task successfully launched. ID: %s' % task.task_id))
