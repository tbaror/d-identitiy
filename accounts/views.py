from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
import ldap3
from decouple import config


class UsersLoginView(LoginView):
    template_name = 'login.html'
    success_url = 'profile'
    success_message = 'Welcome to your profile'
    form_class = UserLoginForm


class UserProfileView(TemplateView):
    template_name = 'user-profile.html'    


class ChangeUserPassword(TemplateView):
    info_sended = False
    template_name = "changepassword.html"
    #form_class = UserChangePasswordForm
    #success_url = reverse_lazy('loader_success')