from django import forms
from django.forms import ModelForm
#from .models import User



class UserLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'email', 'name':'Username', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password', 'placeholder':'Password'}))

    
