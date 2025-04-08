from django import forms
from .models import *
import re



class CustomerRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'password', 'location']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_str = str(phone)
        if not re.match(r'^\d{10}$', phone_str):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone


class StafRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Staf
        fields = ['name', 'email', 'password', 'location', 'phone']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone_str = str(phone)
        if not re.match(r'^\d{10}$', phone_str):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone



class AdminRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AdminReg
        fields = ['name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())



from django import forms
from .models import BandTeam

class BandTeamForm(forms.ModelForm):
    class Meta:
        model = BandTeam
        fields = ["name", "genre", "description", "booking_fee", "image"]  # Added booking_fee field


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "image"]
