from django.shortcuts import render

def payment_success(request):
    """
    Render the payment success page.
    """
    return render(request, 'payment/payment_success.html')
