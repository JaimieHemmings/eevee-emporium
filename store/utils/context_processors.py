from ..models import Category, Set

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def sets_processor(request):
    sets = Set.objects.all()
    return {'sets': sets}