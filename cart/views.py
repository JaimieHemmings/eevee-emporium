from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    """
    Render the cart summary page.
    """
    cart = Cart(request)
    cart_products = cart.get_prods()
    return render(request, 'cart_summary.html', {"cart_products": cart_products})


def cart_add(request):
    """
    Add a product to the cart.
    """
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        # Save to session
        cart.add(product=product) 
        # Get Cart Quantity
        cart_quantity = cart.__len__()
        # Return JSON response
        messages.success(request, f'{product.name} has been added to your cart.')
        response = JsonResponse(
            {'qty: ': cart_quantity}
        )      
    return response


def cart_remove(request):
    """
    Remove a product from the cart.
    """
    return render(request, 'cart_remove.html')


def cart_update(request):
    """
    Update the quantity of a product in the cart.
    """
    return render(request, 'cart_update.html')