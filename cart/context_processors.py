from .cart import Cart


# Contest processors for the cart application
def cart(request):
    """
    Returns the cart object to be used in templates.
    """
    return {'cart': Cart(request)}
