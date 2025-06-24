from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Set up database cache table if needed'

    def handle(self, *args, **options):
        try:
            call_command('createcachetable', 'cache_table')
            self.stdout.write(
                self.style.SUCCESS('Successfully created cache table')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Cache table may already exist: {e}')
            )
