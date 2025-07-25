from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from store.models import Product, Category, Set
from payment.models import Order, OrderItem
from store.forms import ProductForm, CategoryForm, SetForm
from contact.models import Review


@user_passes_test(lambda u: u.is_superuser)
def control_panel_home(request):
    """
    Render the control panel home page.
    """
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_sets = Set.objects.count()
    total_orders = Order.objects.count()
    latest_orders = Order.objects.order_by('-date_ordered')[:5]
    total_reviews = Review.objects.count()
    return render(request, 'controlpanel/control_panel_home.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_sets': total_sets,
        'total_orders': total_orders,
        'latest_orders': latest_orders,
        'total_reviews': total_reviews,
    })


@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    """
    Render the orders page in the control panel.
    """
    orders = Order.objects.all().order_by('-date_ordered')
    return render(request, 'controlpanel/orders.html', {
        'orders': orders,
    })


@user_passes_test(lambda u: u.is_superuser)
def order_detail(request, order_id):
    """
    Render the details of a specific order in the control panel.
    """
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('control_panel_orders')

    return render(request, 'controlpanel/order_detail.html', {
        'order': order,
        'order_items': order_items,
    })


@user_passes_test(lambda u: u.is_superuser)
def mark_order_shipped(request, order_id):
    """
    Mark an order as shipped in the control panel.
    """
    try:
        order = Order.objects.get(id=order_id)
        order.shipped = True
        order.save()
        messages.success(request, "Order marked as shipped.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")

    return redirect('control_panel_order_detail', order_id=order_id)


@user_passes_test(lambda u: u.is_superuser)
def products(request):
    """
    Render the products page in the control panel.
    """
    products = Product.objects.all().order_by('name')
    return render(request, 'controlpanel/products.html', {
        'products': products,
    })


@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    """
    Add a new product in the control panel.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('control_panel_products')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()

    return render(request, 'controlpanel/control_panel_add_product.html', {
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id):
    """
    Edit a product in the control panel.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('control_panel_products')

    if request.method == 'POST':
        form = ProductForm(
            request.POST, request.FILES or None, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('control_panel_products')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'controlpanel/edit_product.html', {
        'product': product,
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def confirm_delete_product(request, product_id):
    """
    Confirm deletion of a product in the control panel.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('control_panel_products')

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('control_panel_products')

    return render(request, 'controlpanel/confirm_delete_product.html', {
        'product': product,
    })


@user_passes_test(lambda u: u.is_superuser)
def manage_categories(request):
    """
    Render the manage categories page in the control panel.
    """
    categories = Category.objects.all().order_by('name')
    return render(request, 'controlpanel/manage_categories.html', {
        'categories': categories,
    })


@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    """
    Add a new category in the control panel.
    """
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('control_panel_manage_categories')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'controlpanel/add_category.html', {
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, category_id):
    """
    Edit a category in the control panel.
    """
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('control_panel_manage_categories')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('control_panel_manage_categories')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm(instance=category)

    return render(request, 'controlpanel/edit_category.html', {
        'form': form,
        'category': category,
    })


@user_passes_test(lambda u: u.is_superuser)
def confirm_delete_category(request, category_id):
    """
    Confirm deletion of a category in the control panel.
    """
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('control_panel_manage_categories')

    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('control_panel_manage_categories')

    return render(request, 'controlpanel/confirm_delete_category.html', {
        'category': category,
    })


@user_passes_test(lambda u: u.is_superuser)
def manage_sets(request):
    """
    Render the manage sets page in the control panel.
    """
    sets = Set.objects.all().order_by('name')
    return render(request, 'controlpanel/manage_sets.html', {
        'sets': sets,
    })


@user_passes_test(lambda u: u.is_superuser)
def add_set(request):
    """
    Add a new set in the control panel.
    """
    if request.method == 'POST':
        form = SetForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Set added successfully.")
            return redirect('control_panel_manage_sets')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SetForm()

    return render(request, 'controlpanel/add_set.html', {
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def edit_set(request, set_id):
    """
    Edit a set in the control panel.
    """
    try:
        set_instance = Set.objects.get(id=set_id)
    except Set.DoesNotExist:
        messages.error(request, "Set not found.")
        return redirect('control_panel_manage_sets')

    if request.method == 'POST':
        form = SetForm(request.POST, request.FILES or None, instance=set_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Set updated successfully.")
            return redirect('control_panel_manage_sets')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SetForm(instance=set_instance)

    return render(request, 'controlpanel/edit_set.html', {
        'form': form,
        'set': set_instance,
    })


@user_passes_test(lambda u: u.is_superuser)
def confirm_delete_set(request, set_id):
    """
    Confirm deletion of a set in the control panel.
    """
    try:
        set_instance = Set.objects.get(id=set_id)
    except Set.DoesNotExist:
        messages.error(request, "Set not found.")
        return redirect('control_panel_manage_sets')

    if request.method == 'POST':
        set_instance.delete()
        messages.success(request, "Set deleted successfully.")
        return redirect('control_panel_manage_sets')

    return render(request, 'controlpanel/confirm_delete_set.html', {
        'set': set_instance,
    })


@user_passes_test(lambda u: u.is_superuser)
def manage_reviews(request):
    """
    Render the manage reviews page in the control panel.
    """
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'controlpanel/manage_reviews.html', {
        'reviews': reviews,
    })

@user_passes_test(lambda u: u.is_superuser)
def manage_reviews(request):
    """
    Render the manage reviews page in the control panel.
    """
    reviews = Review.objects.all().order_by('-id')
    return render(request, 'controlpanel/manage_reviews.html', {
        'reviews': reviews,
    })

@user_passes_test(lambda u: u.is_superuser)
def toggle_review_status(request, review_id):
    """
    Toggle the featured status of a review in the control panel.
    """
    try:
        review = Review.objects.get(id=review_id)
        review.featured = not review.featured
        review.save()
        messages.success(request, "Review status updated successfully.")
    except Review.DoesNotExist:
        messages.error(request, "Review not found.")

    return redirect('control_panel_manage_reviews')


@user_passes_test(lambda u: u.is_superuser)
def confirm_delete_review(request, review_id):
    """
    Confirm deletion of a review in the control panel.
    """
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        messages.error(request, "Review not found.")
        return redirect('control_panel_manage_reviews')

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect('control_panel_manage_reviews')

    return render(request, 'controlpanel/confirm_delete_review.html', {
        'review': review,
    })
