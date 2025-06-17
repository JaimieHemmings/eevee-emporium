from django.shortcuts import render
from .models import Product, Category

# Create your views here.
def home(request):
    products = Product.objects.order_by('-created_at')[:10] # Fetch the latest 10 products
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'home.html', {'products':products, 'categories':categories})  # Render the home.html template