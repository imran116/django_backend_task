from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
