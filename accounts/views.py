from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import render
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


class ChangeUserPassword(View):
    info_sended = False
    template_name = "changepassword.html"
    AUTH_SERVER = config('AUTH_SERVER')
    BASEDN = config('BASEDN')
    #form_class = UserChangePasswordForm
    success_url = reverse_lazy('profile')

    def get(self, request):
        """ current_user = request.user
        context = {'form' : current_user} """
        return render(request, self.template_name)

    def post(self, request):
        PassForm = ""
        #form = PassForm()
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('user_password')
            current_user = 'request.user'
            formdata = {'current_password': current_password, 'new_password': new_password, 'current_user': current_user }
            
            print(formdata)
            return render(formdata)
        else:
            print('error')    


