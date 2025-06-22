from django.shortcuts import render, redirect
from .models import Product, Category, Set, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm


# Function to handle product details view
def product(request, slug):
    product = Product.objects.get(slug=slug)  # Fetch the product by name
    if not product:
        # Show an error message if the product does not exist
        messages.error(request, 'Product not found.')
        # Redirect to home if the product is not found
        return redirect('home')
    # Render the product.html template with the product data
    return render(request, 'product.html', {'product': product})


# Function to handle category view
def category(request, slug):
    try:
        # Attempt to fetch the category by slug
        searchCategory = Category.objects.get(slug=slug)
        # Fetch products belonging to the category
        products = Product.objects.filter(category=searchCategory)
        # Fetch the first 5 products for the featured section
        featuredProducts = Product.objects.filter(category=searchCategory)[:5]
        # Render the category.html template with the category and products data
        return render(
            request,
            'category.html',
            {
                'searchCategory': searchCategory,
                'products': products,
                'featuredProducts': featuredProducts
            }
        )
    except Exception as e:
        # Show an error message if the category does not exist
        messages.error(request, f'Category does not exist - {e}')
        # Redirect to home if the category does not exist
        return redirect('home')


# Function to handle category view
def set(request, slug):
    try:
        # Attempt to fetch the category by slug
        searchCategory = Set.objects.get(slug=slug)
        # Fetch products belonging to the category
        products = Product.objects.filter(set=searchCategory)
        # Fetch the first 5 products for the featured section
        featuredProducts = Product.objects.filter(set=searchCategory)[:5]
        # Render the category.html template with the category and products data
        return render(
            request,
            'category.html',
            {
                'searchCategory': searchCategory,
                'products': products,
                'featuredProducts': featuredProducts
            }
        )
    except Exception as e:
        # Show an error message if the category does not exist
        messages.error(request, f'Set does not exist - {e}')
        # Redirect to home if the category does not exist
        return redirect('home')


# Create your views here.
def home(request):
    # Fetch the latest 10 products
    products = Product.objects.order_by('-created_at')[:5]
    # Fetch all categories from the database
    categories = Category.objects.all()
    # Fetch the latest 5 sets
    featuredSets = Set.objects.all()[:3]
    # Render the home.html template
    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'featuredSets': featuredSets
    })


def about(request):
    return render(request, 'about.html')


# Function to handle user login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html', {})


# Function to handle user logout
def logout_user(request):
    logout(request)  # Log the user out
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home after logout


# Function to handle user registration
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate the user after registration
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            # Redirect to home after successful registration
            return redirect('home')
    else:
        form = SignUpForm()
        messages.info(request, 'Please fill out the form to register.')
        return render(request, 'register.html', {'form': form})
    # Render the register.html template with the form
    return render(request, 'register.html', {'form': form})


# Function to handle user profile update
def update_user(request):
    """
    This function checks if the user is authenticated
    and allows them to update their profile information.
    """
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(
            request.POST or None,
            instance=current_user
        )

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(
                request, 'Profile updated successfully!'
            )

        return render(
            request, 'update_user.html', {'user_form': user_form}
        )
    else:
        messages.error(
            request,
            'You need to be logged in to update your profile.'
        )
        return redirect('login')


def update_password(request):
    """
    This view allows authenticated users to change their password.
    """
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(
                user=current_user,
                data=request.POST
            )
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Your password has been changed successfully!'
                    'Please log in again.'
                )
                return redirect('login')
            else:
                # If the form is not valid, display the errors
                for error in list(form.errors.values()):
                    messages.error(
                        request,
                        f'Error: {error}'
                    )
                return render(request, 'update_password.html', {
                    'password_form': form
                })
        else:
            form = ChangePasswordForm(
                current_user
            )
            return render(request, 'update_password.html', {
                'password_form': form
            })

    else:
        messages.error(
            request,
            'You need to be logged in to change your password.'
        )
        return redirect('login')


def update_info(request):
    if request.user.is_authenticated:
        # Account for potential mismatch between User and Profile IDs
        # Ensure that the Profile instance is fetched correctly
        current_user = Profile.objects.get(user__id=request.user.id)
        user_info_form = UserInfoForm(
            request.POST or None,
            instance=current_user
        )
        if user_info_form.is_valid():
            user_info_form.save()
            messages.success(
                request, 'Your information has been updated successfully!'
            )
        else:
            # If the form is not valid, display the errors
            for error in list(user_info_form.errors.values()):
                messages.error(
                    request,
                    f'Error: {error}'
                )
        return render(request, 'update_info.html', {
            'user_form': user_info_form
        })
    else:
        messages.error(
            request,
            'You need to be logged in to update your information.'
        )
        return redirect('login')
