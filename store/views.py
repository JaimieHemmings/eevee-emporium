from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html', {})  # Render the login.html template


def logout_user(request):
    logout(request)  # Log the user out
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home after logout
