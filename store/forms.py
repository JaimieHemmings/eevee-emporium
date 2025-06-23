from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile, Product, Category, Set


class ChangePasswordForm(SetPasswordForm):
    """
    Form for changing the user's password.
    Inherits from SetPasswordForm to handle password change functionality.
    """

    class meta:
        model = User
        fields = ('new_password1', 'new_password2')

    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password'
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm New Password'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your'
            'other personal information.</li><li>'
            'Your password must contain at least 8 characters.'
            '</li><li>Your password can\'t be a commonly used password.'
            '</li><li>Your password can\'t be entirely numeric.</li></ul>'
        )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }
        )
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = (
        forms.CharField(
            label="",
            max_length=100,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last Name'
                }
            )
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Required. 150 characters or fewer.'
            ' Letters, digits and @/./+/-/_ only.'
            '</small></span>'
        )

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your'
            'other personal information.</li><li>'
            'Your password must contain at least 8 characters.'
            '</li><li>Your password can\'t be a commonly used password.'
            '</li><li>Your password can\'t be entirely numeric.</li></ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = (
            'Confirm Password'
        )
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Enter the same password as before, for verification.'
            '</small></span>'
        )


class UpdateUserForm(UserChangeForm):
    # Prevents password field from being displayed
    password = None
    # Customizing the fields to use TextInput widgets
    email = (
        forms.EmailField(
            label="",
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email Address'
                }
            )
        )
    )
    first_name = (
        forms.CharField(
            label="",
            max_length=100,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First Name'
                }
            )
        )
    )
    last_name = (
        forms.CharField(
            label="",
            max_length=100,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last Name'
                }
            )
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Required. 150 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
            '</small></span>'
        )


class UserInfoForm(forms.ModelForm):
    """
    Form for updating user information.
    This form is used to update additional user details.
    """
    phone = forms.CharField(
        label="",
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )
    )
    address1 = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Address Line 1'
            }
        )
    )
    address2 = forms.CharField(
        label="",
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Address Line 2 (optional)'
            }
        )
    )
    city = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }
        )
    )
    county = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'County'
            }
        )
    )
    postcode = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Post Code'
            }
        )
    )
    country = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Country',
                'value': 'United Kingdom',
            }
        ),
        initial='United Kingdom'
    )

    class Meta:
        model = Profile
        fields = [
            'phone',
            'address1',
            'address2',
            'city',
            'county',
            'postcode',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)

        # Customizing the form fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = ''
            self.fields[field].help_text = ''


class ProductForm(forms.ModelForm):
    """
    Form for creating or updating a product.
    This form is used in the control panel to manage products.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'set', 'stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Product Description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'set': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"
        self.fields['set'].empty_label = "Select Set"

