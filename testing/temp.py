def get_initial(self):
        # Get form data from customer
        initial = super().get_initial()
        initial['name'] = self.request.POST.get('name')
        initial['mail'] = self.request.POST.get('mail')
        initial['tel_num'] = self.request.POST.get('tel_num')
        initial['message_contact'] = self.request.POST.get('message_contact')
        initial['contact_date'] = self.request.POST.get('contact_date')
        # Send Mail Rutine
        messege_subject = 'You got New Messege contact from {0}'.format(initial['name'])
        message_contact = ' שלום מ {0} \n {1} \n {2} \n טלפון ליצירת קשר: {3}'.format(initial['name'], initial['mail'], initial['message_contact'], initial['tel_num'])
        mail_from = initial['mail']
        send_mail(
            messege_subject,
            message_contact,
            mail_from,
            ['carnepremiumgrill@gmail.com', 'tbaror@gmail.com', 'shahar130313@gmail.com']

        )

        return initial
AUTH_SERVER= config('AUTH_SERVER')
BASEDN= config('BASEDN')
USER="pwmtest@dalet.com"
CURREENTPWD="Esprit@1234"
NEWPWD="Gfn@12345"

SEARCHFILTER='(&(|(userPrincipalName='+USER+')(samaccountname='+USER+')(mail='+USER+'))(objectClass=person))'

USER_DN=""

ldap_server = ldap3.Server(AUTH_SERVER, get_info=ldap3.ALL)
conn = ldap3.Connection(ldap_server, USER, CURREENTPWD, auto_bind=True)
conn.start_tls()

print(conn)

conn.search(search_base = BASEDN,
         search_filter = SEARCHFILTER,
         search_scope = ldap3.SUBTREE,
         attributes = ['cn', 'givenName'],
         paged_size = 5)

for entry in conn.response:
    if entry.get("dn") and entry.get("attributes"):
        if entry.get("attributes").get("cn"):
            USER_DN=entry.get("dn")

print (USER_DN)
print(ldap3.extend.microsoft.modifyPassword.ad_modify_password(conn, USER_DN, NEWPWD, CURREENTPWD,  controls=None))
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
 