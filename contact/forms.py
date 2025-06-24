from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """
    Form for submitting a review.
    """
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    review = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Review
        fields = ['name', 'email', 'review']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Name'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Email'}
            ),
            'review': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Your Review'}
            ),
        }
        labels = {
            'name': '',
            'email': '',
            'review': '',
        }
    def clean_email(self):
        """
        Validate the email field to ensure it is not empty.
        """
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email
