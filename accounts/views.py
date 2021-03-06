from pyotp.totp import TOTP
from . models import *
from .user_ops import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
import time
import pyotp
from ldap3 import *
from decouple import config
import ssl
#from django_user_agents.utils import get_user_agent


class UsersLoginView(LoginView):
    template_name = 'login.html'
    success_url = 'profile'
    success_message = 'Welcome to your profile'
    form_class = UserLoginForm


class UsersLogoutView(LogoutView):
    template_name = "login.html"

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user-profile.html'
    login_url = '/'
    AUTH_SRV = config('AUTH_SRV')
    BASEDN = config('BASEDN')
    SVCUSER = config('SVCUSER')
    SVCPASS = config('SVCPASS')
    DOMAIN_NAME = config('DOMAIN_NAME')

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        
        profileuser = str(self.request.user) + self.DOMAIN_NAME
        current_user = self.request.user
        UserProfileData  = LdapOpertions(self.AUTH_SRV, self.BASEDN, self.SVCUSER, self.SVCPASS, profileuser)
        context['profile_info'] = UserProfileData.query_user_attrib()
        #print(context)
        context['usr_reevts'] = PassEvents.objects.filter(user_related_event__exact=profileuser)
        context['otp_obj'] = OtpProfile.objects.filter(user__exact=current_user)
        print(context)
        return context


class ChangeUserPassword(LoginRequiredMixin, View):
    
    
    info_sended = False
    template_name = "changepassword.html"
    AUTH_SERVER = config('AUTH_SERVER')
    AUTH_SRV = config('AUTH_SRV')
    BASEDN = config('BASEDN')
    #form_class = UserChangePasswordForm
    #success_url = reverse_lazy('profile')
    login_url = '/'

    def get(self, request):
        context = {}
        current_user = request.user
        
        context['current_user'] = current_user
        return render(request, self.template_name, context)

    def post(self, request):
        model = PassEvents()
        PassForm = ""

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
                ip = request.META.get('REMOTE_ADDR')
                #print(ip)
                messages.success(self.request, 'Password has been changed successfully.')
                request.session['stat_msg'] = "Change Password completed Successfully."
                request.session['email'] = USER
                #event writing 
                model.user_related_event = USER
                model.ip_source = ip
                model.pass_event_type = 'change password'
                #agent details
                model.user_browser = request.user_agent.browser.family
                model.user_os = request.user_agent.os.family
                model.user_agent = request.user_agent.device.family
            
                model.save()


                #self.model.
                return redirect('opschange')
                
            except Exception as e:
                messages.warning(self.request, e)
                print(e)
                        
            print(formdata)
            return render(request, self.template_name, formdata)
        else:
            print('error')    


class ResetRequestForm(View):

    BASEDN= config('BASEDN')
    AUTH_SRV = config('AUTH_SRV')
    SVCUSER = config('SVCUSER')
    SVCPASS = config('SVCPASS')
    OTP_NUMLEN = config('OTP_NUMLEN')
    FROM_EMAIL = config('FROM_EMAIL')

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

                user_email = c.entries[0].mail.values
                user_givenname = c.entries[0].givenName.values
                user_sn = c.entries[0].sn.values
                sAMAccountName = c.entries[0].sAMAccountName.values
                
                c.unbind()
                #Comparing reset form to AD details
                if email == user_email[0] and first_name == user_givenname[0] and last_name == user_sn[0]:
                    user_id = User.objects.filter(username__exact=sAMAccountName[0]).values_list('id',flat=True)
                    
                    opt_method = OtpProfile.objects.filter(user__exact=int(user_id[0])).values_list('otp_method',flat=True)
                    user_key = OtpProfile.objects.filter(user__exact=int(user_id[0])).values_list('otp_code',flat=True)
                    request.session['email'] = user_email[0]
                    print(opt_method)
                    
                    if opt_method[0] == 'EM':

                    #print("match")
                        #email reset method
                        request.session['ms_method'] = 'Email just been sent with Token valid for  <strong> 5min</strong>, Please check your mailbox, including the spam folder'
                        secret = user_key[0]
                        totp = pyotp.TOTP(secret, interval=int(self.OTP_NUMLEN))
                        now = time.time()
                        totp.at(now)
                        
                        request.session['otp'] = otp = totp.now()
                        request.session['secret'] = secret
                            
                        #print('OTP code:', totp.now())
                        
                        #messages.warning(self.request, 'Sending OTP MAIL')
                        messege_subject = 'OTP Code for {0}'.format(user_email[0])
                        message_contact = 'Hello \n That’s your OTP Code Valid for next 5min : {0}'.format(totp.now())
                        mail_from = self.FROM_EMAIL
                        recipient_list = [user_email[0],]
                            #fail_silently = False,
                        try:    
                            send_mail(
                                messege_subject,
                                message_contact,
                                mail_from,
                                recipient_list,
                            )
                        except Exception as e:
                            messages.warning(self.request, e)
                            time.sleep(3)
                            return redirect('/')
                            print(e)

                        return redirect('tokenchalenge')

                    elif opt_method[0] == 'GO':
                        request.session['user_id'] = user_id[0]
                        request.session['ms_method'] = 'Please Use your scanned QR code In GoogleAuthentication App'
                        return redirect('googlechalenge')
                        
                else:
                    print('not match')
                    #print( email , user_email[0], first_name, user_givenname[0], last_name, user_sn[0])
                return render(request, template_name)
            except Exception as e:
                print(e)
                return render(request, template_name)   



class TokenChalengeView(View):
    
    template_name = "token_chalenge.html"
    OTP_NUMLEN = config('OTP_NUMLEN')


    def get(self, request):

        context = {}
        
        user_email = request.session.get('email')
        if user_email == None:
           return redirect('resetpass')
        context['email']= user_email
        context['ms_method'] = request.session.get('ms_method')

        return render(request, self.template_name, context)



    def post(self, request):
        context = {}
        token_resp = ""

        if request.method == 'POST':
            totp = pyotp.TOTP(request.session.get('secret'), interval=int(self.OTP_NUMLEN))

            token_resp = str(request.POST.get('token_input'))
            otp = totp.verify(token_resp)
            if otp == True:
                print('bingo')
                request.session['otp_resualt'] = True

                return redirect('resetaction')
            else:
                print('try again')
                request.session['otp_resualt'] = False     

            context['token_resp' ]= token_resp

        return render(request, self.template_name, context)

class GoogleAuthChalengeView(View):
    
    template_name = "token_chalenge.html"
    GO_OTP_NUMLEN = config('GO_OTP_NUMLEN')


    def get(self, request):

        context = {}
        print(request.session.get('email'))
        
        user_email = request.session.get('email')
        if user_email == None:
            #redirect back to reset request form
            return redirect('resetpass')
        print(user_email)
        context['email']= user_email
        context['ms_method'] = request.session.get('ms_method')

        return render(request, self.template_name, context)



    def post(self, request):
        context = {}
        token_resp = ""

        if request.method == 'POST':
            user_key = OtpProfile.objects.filter(user__exact=int(request.session.get('user_id'))).values_list('otp_code',flat=True)
            print(user_key)
            totp = pyotp.TOTP(user_key[0], interval=int(self.GO_OTP_NUMLEN))
            print("Current OTP:", totp.now())

            token_resp = str(request.POST.get('token_input'))
            otp = totp.verify(token_resp)
            if otp == True:
                print('bingo')
                request.session['otp_resualt'] = True

                return redirect('resetaction')
            else:
                print('try again')
                request.session['otp_resualt'] = False
                return redirect('googlechalenge')


            context['token_resp' ]= token_resp

        return render(request, self.template_name, context)

class ResetActionView(View):
    model = PassEvents()
    template_name = 'password_reset.html'
    BASEDN= config('BASEDN')
    AUTH_SRV = config('AUTH_SRV')
    SVCUSER = config('SVCUSER')
    SVCPASS = config('SVCPASS')

    def get(self, request):
        context = {}

        user_email = request.session.get('email')        
        context['email'] = user_email
        otp_resualt = request.session.get('otp_resualt')
        if otp_resualt==True and user_email != None:
            pass
            
        else:
            return redirect('/')


        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
             user_email = request.session.get('email')
             pass_new = request.POST.get('up')
             #Reset password Routine
             try:
                 tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
                 s = Server(self.AUTH_SRV, get_info=ALL, use_ssl=True, tls=tls_configuration)
                 c = Connection(s, user=self.SVCUSER, password=self.SVCPASS)
                 c.open()
                 c.bind()
                 SEARCHFILTER='(&(|(userPrincipalName='+user_email+')(samaccountname='+user_email+')(mail='+user_email+'))(objectClass=person))'

                 USER_DN=""
                 c.search(search_base = self.BASEDN,
                    search_filter = SEARCHFILTER,
                    search_scope = SUBTREE,
                    attributes = ['cn', 'givenName'],
                    paged_size = 5)
                 
                 for entry in c.response:
                     if entry.get("dn") and entry.get("attributes"):
                         if entry.get("attributes").get("cn"):
                             USER_DN=entry.get("dn")

                 print (USER_DN)
                 c.extend.microsoft.modify_password(USER_DN, pass_new)
                 print(c.result)
                 c.unbind()
                 request.session['stat_msg'] = "Password Reset completed Successfully."
                 request.session['email'] = user_email
                 request.session['ops_type'] = 'reset'
                 ip = request.META.get('REMOTE_ADDR')   
                 #event writing 
                 self.model.user_related_event = user_email
                 self.model.ip_source = ip
                 self.model.pass_event_type = 'reset password'
                 #agent details
                 self.model.user_browser = request.user_agent.browser.family
                 self.model.user_os = request.user_agent.os.family
                 self.model.user_agent = request.user_agent.device.family
            
                 self.model.save()

                 return redirect('opsreset')
             except Exception as e:
                print(e)
          
        return render(request, self.template_name)


class GoogleResetActionView(View):
    model = PassEvents()
    template_name = 'password_reset.html'
    BASEDN= config('BASEDN')
    AUTH_SRV = config('AUTH_SRV')
    SVCUSER = config('SVCUSER')
    SVCPASS = config('SVCPASS')

    def get(self, request):
        context = {}

        user_email = request.session.get('email')        
        context['email'] = user_email
        otp_resualt = request.session.get('otp_resualt')
        if otp_resualt==True and user_email != None:
            pass
            
        else:
            return redirect('/')


        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
             user_email = request.session.get('email')
             pass_new = request.POST.get('up')
             #Reset password Routine
             try:
                 tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
                 s = Server(self.AUTH_SRV, get_info=ALL, use_ssl=True, tls=tls_configuration)
                 c = Connection(s, user=self.SVCUSER, password=self.SVCPASS)
                 c.open()
                 c.bind()
                 SEARCHFILTER='(&(|(userPrincipalName='+user_email+')(samaccountname='+user_email+')(mail='+user_email+'))(objectClass=person))'

                 USER_DN=""
                 c.search(search_base = self.BASEDN,
                    search_filter = SEARCHFILTER,
                    search_scope = SUBTREE,
                    attributes = ['cn', 'givenName'],
                    paged_size = 5)
                 
                 for entry in c.response:
                     if entry.get("dn") and entry.get("attributes"):
                         if entry.get("attributes").get("cn"):
                             USER_DN=entry.get("dn")

                 print (USER_DN)
                 c.extend.microsoft.modify_password(USER_DN, pass_new)
                 print(c.result)
                 c.unbind()
                 request.session['stat_msg'] = "Password Reset completed Successfully."
                 request.session['email'] = user_email
                 request.session['ops_type'] = 'reset'
                 ip = request.META.get('REMOTE_ADDR')   
                 #event writing 
                 self.model.user_related_event = user_email
                 self.model.ip_source = ip
                 self.model.pass_event_type = 'reset password'
                 #agent details
                 self.model.user_browser = request.user_agent.browser.family
                 self.model.user_os = request.user_agent.os.family
                 self.model.user_agent = request.user_agent.device.family
            
                 self.model.save()

                 return redirect('opsreset')
             except Exception as e:
                print(e)
          
        return render(request, self.template_name)

class OperationStatusView(View):
    template_name = 'ops_reset.html'
    
    def get(self, request):

        context = {}
        user_email = request.session.get('email')
        status_msg = request.session.get('stat_msg')
        ops_type = request.session.get('ops_type')
        context['user_email'] = user_email
        context['stat_msg'] = status_msg
        
        
        if request.session.get('email') == None:
            redirect('/')

        return render(request, self.template_name, context)



    def post(self, request):
        pass


class OpsChangeView(View):
    template_name = 'ops_change.html'
    
    def get(self, request):

        context = {}
        user_email = request.session.get('email')
        status_msg = request.session.get('stat_msg')
        #ops_type = request.session.get('ops_type')
        context['user_email'] = user_email
        context['stat_msg'] = status_msg
        
        
        if request.session.get('email') == None:
            redirect('/')

        return render(request, self.template_name, context)



    def post(self, request):
        pass


            