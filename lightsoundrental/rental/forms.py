# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class ShopOwnerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)  # Add phone number field
    location = forms.CharField(max_length=255, required=True)  # Add location field

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'location')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price_per_day', 'image', 'total_quantity', 'dimensions', 'installation_instructions', 'compatibility', 'power_rating', 'pincode']


    def clean_total_quantity(self):
        quantity = self.cleaned_data.get('total_quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        return quantity
