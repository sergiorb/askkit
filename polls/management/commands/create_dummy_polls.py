from django.core.management.base import BaseCommand, CommandError

from polls import functions


class Command(BaseCommand):

	help = 'Creates dummy polls, options and votes. By default, it creates \
		100, 300, 10000 respectively.'

	def add_arguments(self, parser):

		parser.add_argument('--pollsNumber',
			dest='pollsNumber',
			default=False,
			help='Set the number of polls to be created.')

	def handle(self, *args, **options):

		number = 100

		if options['pollsNumber']:

			number = int(options['pollsNumber'])

		self.stdout.write(self.style.NOTICE('Generating %s polls...' % number ))

		functions.generate_dummy_polls_votes(number)

		self.stdout.write(self.style.SUCCESS('%s polls successfully created' % number))
