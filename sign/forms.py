__author__ = 'shinoymm'
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=256, min_length=4)
    password = forms.CharField(max_length=256, min_length=4, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    s_username = forms.CharField(max_length=256, min_length=4)
    s_mail = forms.EmailField()
    s_password = forms.CharField(max_length=256, min_length=4, widget=forms.PasswordInput)
    s_password2 = forms.CharField(max_length=256, min_length=4, widget=forms.PasswordInput)