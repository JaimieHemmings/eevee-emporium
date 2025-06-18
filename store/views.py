from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

# Function to handle product details view
def product(request, slug):
    product = Product.objects.get(category=slug)  # Fetch the product by name
    if not product:
        messages.error(request, 'Product not found.')  # Show an error message if the product does not exist
        return redirect('home')  # Redirect to home if the product is not found
    return render(request, 'product.html', {'product': product})  # Render the product.html template with the product data


# Function to handle category view
def category(request, slug):
    try:
        # Attempt to fetch the category by slug
        category = Category.objects.get(slug=slug)
        # Get first 5 objects for featured billboard
        products = Product.objects.filter(category=category)  # Fetch products belonging to the category
        featuredProducts = Product.objects.all()[:5]  # Fetch the first 5 products for the featured section
        # Render the category.html template with the category and products data
        return render(
            request,
            'category.html',
            {
                'category': category,
                'products': products,
                'featuredProducts':featuredProducts
                }
        ) 
    except:
        # Show an error message if the category does not exist
        messages.error(request, 'Category does not exist.')  
        return redirect('home')  # Redirect to home if the category does not exist


# Create your views here.
def home(request):
    products = Product.objects.order_by('-created_at')[:5] # Fetch the latest 10 products
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'home.html', {'products':products, 'categories':categories})  # Render the home.html template


def about(request):
    return render(request, 'about.html')  # Render the about.html template


# Function to handle user login
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


# Function to handle user logout
def logout_user(request):
    logout(request)  # Log the user out
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home after logout


# Function to handle user registration
def register_user(request):
    form = SignUpForm()  # Create an instance of the SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Create a form instance with the submitted data
        if form.is_valid():  # Check if the form is valid
            user = form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate the user after registration
            user = authenticate(username=username, password=password)  
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = SignUpForm()
        messages.info(request, 'Please fill out the form to register.')
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})  # Render the register.html template with the form
