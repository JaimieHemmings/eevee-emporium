from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    """
    Render the cart summary page.
    """
    return render(request, 'cart_summary.html', {})


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
        # Return JSON response
        response = JsonResponse(
            {'product Name: ': product.name,'success': True}
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