# views.py
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
    total_price = cart.total()
    return render(
        request,
        'cart_summary.html',
        {
            "cart_products": cart_products,
            "total_price": total_price,
        }
    )


def cart_add(request):
    """
    Add a product to the cart.
    """
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty_str = request.POST.get('product_qty', '1')

        try:
            product_qty = int(product_qty_str)
            if product_qty < 1:
                product_qty = 1
            elif product_qty > 5:
                product_qty = 10
                messages.warning(request, 'Maximum quantity of 5 applied.')
        except ValueError:
            product_qty = 1
            messages.warning(request, 'Invalid quantity provided, defaulting to 1.')

        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product_id=product.id, product_qty=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        messages.success(
            request,
            f'{product.name} has been added to your cart.',
        )
        response = JsonResponse(
            {'cart_quantity': cart_quantity}
        )
    else:
        response = JsonResponse(
            {
                'success': False,
                'error': 'Invalid request method.'
            }
        )
    return response


def cart_remove(request):
    """
    Remove a product from the cart.
    """
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        cart.remove(product_id)
        cart_quantity = cart.__len__()
        messages.success(request, 'Product has been removed from your cart.')
        response = JsonResponse(
            {
                'success': True,
                'cart_quantity': cart_quantity
            }
        )
    else:
        response = JsonResponse(
            {
                'success': False,
                'error': 'Invalid request method.'
            }
        )
    return response


def cart_update(request):
    """
    Update the quantity of a product in the cart.
    """
    if request.POST.get('action') == 'post':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty_str = request.POST.get('product_qty', '1')

        try:
            product_qty = int(product_qty_str)
            if product_qty < 1:
                product_qty = 1
        except ValueError:
            product_qty = 1

        product = get_object_or_404(Product, id=product_id)

        # Update the quantity using the add method, which handles updates
        cart.add(product_id=product.id, product_qty=product_qty)
        cart_quantity = cart.__len__()
        messages.success(
            request, f'{product.name} quantity updated to {product_qty}.'
        )
        response = JsonResponse({
            'success': True,
            'cart_quantity': cart_quantity,
            'product_id': product_id,
            'new_quantity': product_qty,
            'total_price': cart.total(),
        })
    else:
        response = JsonResponse({
            'success': False,
            'error': 'Invalid request method.'
        })
    return response
