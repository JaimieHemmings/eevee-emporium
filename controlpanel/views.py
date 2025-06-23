from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from store.models import Product, Category, Set
from payment.models import Order, OrderItem

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
    return render(request, 'controlpanel/control_panel_home.html',{
        'total_products': total_products,
        'total_categories': total_categories,
        'total_sets': total_sets,
        'total_orders': total_orders,
        'latest_orders': latest_orders
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