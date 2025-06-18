from django.shortcuts import render

def cart_summary(request):
    """
    Render the cart summary page.
    """
    return render(request, 'cart_summary.html', {})


def cart_add(request, product_id):
    """
    Add a product to the cart.
    """
    return render(request, 'cart_add.html', {'product_id': product_id})


def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    return render(request, 'cart_remove.html', {'product_id': product_id})


def cart_update(request, product_id):
    """
    Update the quantity of a product in the cart.
    """
    return render(request, 'cart_update.html', {'product_id': product_id})