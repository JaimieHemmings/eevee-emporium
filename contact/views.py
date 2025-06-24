from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm

def contact(request):
    """
    Render the contact page and handle form submission.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('contact_success')
    else:
        form = ReviewForm()

    context = {
        'review_form': form,
    }
    return render(request, 'contact/contact.html', context)

def success(request):
    """
    Render the success page after form submission.
    """
    return render(request, 'contact/success.html')