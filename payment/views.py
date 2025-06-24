from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages
from payment.models import Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Set up Stripe
stripe.public_api_key = settings.STRIPE_PUBLIC_KEY
stripe.api_key = settings.STRIPE_PRIVATE_KEY


def process_order(request):
    """
    Process the order and handle payment.
    """
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        total_price = cart.total()
        my_shipping = request.session.get('shipping_info')

        # Combine shipping address parts into a single string
        address_parts = [
            my_shipping.get('shipping_address1'),
            my_shipping.get('shipping_address2'),
            my_shipping.get('shipping_city'),
            my_shipping.get('shipping_county'),
            my_shipping.get('shipping_postcode'),
            my_shipping.get('shipping_country'),
        ]
        shipping_address = ",\n".join(filter(None, address_parts))

        payment_token = request.POST.get('stripeToken')

        try:
            # Create a charge using Stripe
            charge = stripe.Charge.create(
                amount=int(total_price * 100),
                currency='gbp',
                description='Eevee Emporium Order',
                source=payment_token,
            )

            # Create Order
            order_data = {
                'full_name': my_shipping.get('shipping_full_name'),
                'email': my_shipping.get('shipping_email'),
                'shipping_address': shipping_address,
                'amount_paid': total_price,
            }
            if request.user.is_authenticated:
                order_data['user'] = request.user

            create_order = Order.objects.create(**order_data)

            order_items = []

            # Create Order Items
            for product in cart_products:
                order_item_data = {
                    'order': create_order,
                    'product_id': product['id'],
                    'price': product['price'],
                    'quantity': product['quantity'],
                }
                if request.user.is_authenticated:
                    order_item_data['user'] = request.user

                order_item = OrderItem.objects.create(**order_item_data)
                order_items.append(order_item)

                # Reduce product stock
                prod_to_update = Product.objects.get(id=product['id'])
                prod_to_update.stock -= product['quantity']
                prod_to_update.save()

            # Now send the email ONCE, after all items are created
            body = render_to_string('order_confirmation_email.txt', {
                'full_name': my_shipping.get('shipping_full_name'),
                'order_id': create_order.id,
                'items': order_items,
                'total_price': total_price,
            })
            try:
                send_mail(
                    f"Order {create_order.id} Confirmation - Eevee Emporium",
                    body,
                    'noreply@eevee-emporium.com',
                    [my_shipping.get('shipping_email')],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(
                    request,
                    "An error occurred while sending the confirmation email."
                    f" Error: {str(e)}"
                    " Please contact support."
                )
                return redirect('billing_info')

            messages.success(
                request,
                "Order placed successfully! Redirecting to homepage..."
            )
            # Clear the cart
            cart.clear()
            return redirect('home')

        except stripe.error.StripeError as e:
            # Card declined
            messages.error(request, str(e))
            return redirect('billing_info')
        except Exception as e:
            # Other errors
            messages.error(
                request,
                "An error occurred while processing your order."
                "Please try again."
            )
            return redirect('billing_info')
    else:
        messages.error(
            request,
            "Access Denied! Redirecting to homepage..."
        )
        return redirect('home')


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
    shipping_form = ShippingForm()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(
            user=request.user
        ).last()

        shipping_form = ShippingForm(
            request.POST or None,
            instance=shipping_user
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


def billing_info(request):
    """
    Render the billing information page.
    """
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods()
        total_price = cart.total()
        billing_form = PaymentForm()

        # Create session for shipping info
        my_shipping = request.POST
        request.session['shipping_info'] = my_shipping

        context = {
            "cart_products": cart_products,
            "total_price": total_price,
            "shipping_info": request.POST,
            "billing_form": billing_form,
            "stripe_publishable_key": stripe.public_api_key
        }
        return render(request, 'payment/billing_info.html', context)

    else:
        messages.error(
            request,
            "Access Denied! Redirecting to homepage..."
        )
        return redirect('home')
