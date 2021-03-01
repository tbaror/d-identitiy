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
#import ldap3
from ldap3 import *
from decouple import config
import ssl


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
    AUTH_SRV = config('AUTH_SRV')
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
                user_attrb = ""
                tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
                s = Server(self.AUTH_SRV, get_info=ALL, use_ssl=True, tls=tls_configuration)
                c = Connection(s, user=USER, password=CURREENTPWD)
                c.open()
                c.bind()


                c.search(search_base = self.BASEDN,
                search_filter = SEARCHFILTER,
                    search_scope = SUBTREE,
                    attributes = ['cn', 'givenName'],
                    paged_size = 5)

                for entry in c.response:
                    if entry.get("dn") and entry.get("attributes"):
        
                        if entry.get("attributes").get("cn"):
                            USER_DN=entry.get("dn")
                
                print (c.extend.microsoft.modify_password(USER_DN, NEWPWD, CURREENTPWD))
                messages.success(self.request, 'Password has been changed successfully.')
                
            except Exception as e:
                messages.warning(self.request, e)
                print(e)
                        
            print(formdata)
            return render(request, self.template_name, formdata)
        else:
            print('error')    


class ResetPass(View):

    BASEDN= config('BASEDN')
    AUTH_SRV = config('AUTH_SRV')
    SVCUSER = config('SVCUSER')
    SVCPASS = config('SVCPASS')

    def get(self, request):
        template_name = "resetform.html"
        return render(request, template_name)


    def post(self, request):
        template_name = "resetform.html"
        if request.method == 'POST':
            first_name = request.POST.get('first-name')
            last_name  = request.POST.get('last-name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(email)
#Get User & validate info from AD
            try:
                #Try to connect
                USER_DN = ""
                user_attrib = []
                tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
                s = Server(self.AUTH_SRV, get_info=ALL, use_ssl=True, tls=tls_configuration)
                c = Connection(s, user=self.SVCUSER, password=self.SVCPASS)
                c.open()
                c.bind()
                #defien search filter for user account
                SEARCHFILTER='(&(|(userPrincipalName='+email+')(samaccountname='+email+')(mail='+email+'))(objectClass=person))'
                #Get user DN
                c.search(search_base = self.BASEDN,
                    search_filter = SEARCHFILTER,
                    search_scope = SUBTREE,
                    attributes = ['cn', 'givenName'],
                    paged_size = 5)

                for entry in c.response:
                    if entry.get("dn") and entry.get("attributes"):
        
                        if entry.get("attributes").get("cn"):
                            USER_DN=entry.get("dn")
                #retrieve User attributes
                c.search(
                    search_base=USER_DN,
                    search_filter= '(objectClass=*)', # required
                    search_scope=BASE,
                    attributes='*'
                    )

                user_attrib[0] = c.entries[0].mail.values
                user_attrib[1] = c.entries[0].givenName.values
                user_attrib[2] = c.entries[0].sn.values
                print(user_attrib[2])
                c.unbind()
                if email == user_attrib[0] and first_name == user_attrib[1] and last_name == user_attrib[2]:
                    print("match")
                else:
                    print('not match')
                return render(request, template_name)
            except Exception as e:
                print(e)        