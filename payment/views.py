from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def payment_success(request):
    """
    Render the payment success page.
    """
    return render(request, 'payment/payment_success.html')


def checkout(request):
    """
    Render the checkout page.
    """
    cart = Cart(request)
    cart_products = cart.get_prods()
    total_price = cart.total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(
            user__id = request.user.id
        )

        shipping_form = ShippingForm(
            request.POST or None,
            instance = shipping_user
        )
        return render(
            request,
            'payment/checkout.html',
            {
                "cart_products": cart_products,
                "total_price": total_price,
                "shipping_form": shipping_form,
            }
        )
    else:
        return render(
            request,
            'payment/checkout.html',
            {
                "cart_products": cart_products,
                "total_price": total_price,
                "shipping_form": shipping_form,
            }
        )
