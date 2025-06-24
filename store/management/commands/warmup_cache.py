from django.core.management.base import BaseCommand
from django.core.cache import cache
from store.models import Category, Set

class Command(BaseCommand):
    help = 'Warm up cache with frequently accessed data'

    def handle(self, *args, **options):
        # Warm up categories cache
        categories = Category.objects.all().order_by('name')
        cache.set('all_categories', categories, 1800)
        self.stdout.write(f'Cached {categories.count()} categories')

        # Warm up sets cache
        sets = Set.objects.all().order_by('name')
        cache.set('all_sets', sets, 1800)
        self.stdout.write(f'Cached {sets.count()} sets')

        self.stdout.write(
            self.style.SUCCESS('Successfully warmed up cache')
        )
