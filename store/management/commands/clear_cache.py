from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear all cache data'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(
            self.style.SUCCESS('Successfully cleared all cache data')
        )
