from ..models import Category, Set
from django.core.cache import cache

def categories_processor(request):
    categories = cache.get('all_categories')
    if not categories:
        categories = Category.objects.all().order_by('name')
        cache.set('all_categories', categories, 1800)  # Cache for 30 minutes
    return {'categories': categories}

def sets_processor(request):
    sets = cache.get('all_sets')
    if not sets:
        sets = Set.objects.all().order_by('name')
        cache.set('all_sets', sets, 1800)  # Cache for 30 minutes
    return {'sets': sets}