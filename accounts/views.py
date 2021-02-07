from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from .forms import *


class UsersLoginView(LoginView):
    template_name = 'login.html'
    success_url = 'blog-home'
    success_message = 'Welcome to your profile'
    form_class = UserLoginForm

""" class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html' """
