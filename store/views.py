from django.shortcuts import render
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    products = Product.objects.order_by('-created_at')[:10] # Fetch the latest 10 products
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'home.html', {'products':products, 'categories':categories})  # Render the home.html template


def about(request):
    return render(request, 'about.html')  # Render the about.html template


def login_user(request):
    return render(request, 'login.html', {})  # Render the login.html template


def logout_user(request):
    pass  # Placeholder for logout functionality, can be implemented later