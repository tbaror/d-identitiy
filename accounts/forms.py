from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
#from .models import User



class UserLoginForm(UserCreationForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password', 'placeholder':'Password'}),
    )
    #username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'email', 'name':'Username', 'placeholder':'Username'}))
   # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password', 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control', 'type':'email', 'name':'Username', 'placeholder':'Username'}),
            
        }


class UserChangePasswordForm(forms.Form):
    
    currentpass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'currentpass', 'placeholder':'Current Password'}))
    newpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'currentpass', 'placeholder':'New Password'}))
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'confirmpassword', 'placeholder':'Password Confirm'}))

    """ class Meta:
        fields = ['currentpass',
                'newpassword',
                'confirmpassword',

        ] """
