from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    """
    Form for collecting shipping address information.
    """
    shipping_full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    shipping_email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    shipping_address1 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line 1'})
    )
    shipping_address2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line 2 (optional)'})
    )
    shipping_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    shipping_county = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'County'})
    )
    shipping_postcode = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Postcode'})
    )
    shipping_country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Country'}),
        initial='United Kingdom',
        required=False
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name',
            'shipping_email',
            'shipping_address1',
            'shipping_address2',
            'shipping_city',
            'shipping_county',
            'shipping_postcode',
            'shipping_country'
        ]
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with any additional arguments.
        """
        super(ShippingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.label = ''
        self.fields['shipping_country'].widget.attrs['value'] = 'United Kingdom'
        self.fields['shipping_country'].widget.attrs['readonly'] = True
