from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, label="رقم الهاتف")
    email = forms.EmailField(required=True, label="البريد الإلكتروني")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone_number")