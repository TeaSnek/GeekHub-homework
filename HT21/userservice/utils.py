from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        required_fields = ['username', 'password']
        fields = ['username', 'password']
