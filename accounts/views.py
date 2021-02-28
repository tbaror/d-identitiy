from django.contrib import messages
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
            current_user = request.user
            USER = current_user.username + '@dalet.com'
            CURREENTPWD = current_password
            NEWPWD = new_password
            formdata = {'current_password': current_password, 'new_password': new_password, 'current_user': current_user.username }
            
            try:
                SEARCHFILTER='(&(|(userPrincipalName='+USER+')(samaccountname='+USER+')(mail='+USER+'))(objectClass=person))'

                USER_DN=""

                ldap_server = ldap3.Server(self.AUTH_SERVER, get_info=ldap3.ALL)
                conn = ldap3.Connection(ldap_server, USER, CURREENTPWD, auto_bind=True)
                conn.start_tls()

                print(conn)

                conn.search(search_base = self.BASEDN,
                search_filter = SEARCHFILTER,
                search_scope = ldap3.SUBTREE,
                attributes = ['cn', 'givenName'],
                paged_size = 5)

                for entry in conn.response:
                    if entry.get("dn") and entry.get("attributes"):
                        if entry.get("attributes").get("cn"):
                            USER_DN=entry.get("dn")
                messages.success(self.request, 'Password has been changed successfully.')
                print (USER_DN)
                print (ldap3.extend.microsoft.modifyPassword.ad_modify_password(conn, USER_DN, NEWPWD, CURREENTPWD,  controls=None))
            except Exception as e:
                messages.warning(self.request, e)
                print(e)
                        
            print(formdata)
            return render(request, self.template_name, formdata)
        else:
            print('error')    


class ResetPass(View):
    def get(self, request):
        template_name = "resetform.html"
        return render(request, template_name)


    def post(self, request):
        pass    
