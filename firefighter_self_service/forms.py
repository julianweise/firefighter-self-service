from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail'}))
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
