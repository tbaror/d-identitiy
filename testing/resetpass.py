import ssl
from ldap3 import *
BASEDN="DC=dalet,DC=local"
tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
s = Server('DLT-BSH-AD01.dalet.local', get_info=ALL, use_ssl=True, tls=tls_configuration)
password = 'einfs@TA12!@'
CHUSER="pwmtest@dalet.com"
NEWPWD="Zardos_12"
c = Connection(s, user="DALET\TBAROR", password=password)
c.open()
c.bind()
SEARCHFILTER='(&(|(userPrincipalName='+CHUSER+')(samaccountname='+CHUSER+')(mail='+CHUSER+'))(objectClass=person))'

USER_DN=""



c.search(search_base = BASEDN,
    search_filter = SEARCHFILTER,
    search_scope = SUBTREE,
    attributes = ['cn', 'givenName'],
    paged_size = 5)

for entry in c.response:
    if entry.get("dn") and entry.get("attributes"):
        if entry.get("attributes").get("cn"):
            USER_DN=entry.get("dn")

print (USER_DN)

user = "CN=Dummy Dumass,OU=Automatically Generated,OU=Staff,OU=RU,DC=DOMAIN,DC=LOCAL"
c.extend.microsoft.modify_password(USER_DN, NEWPWD)

""" c.modify(user, {
    'unicodePwd': [(MODIFY_REPLACE, ['New12345'])]
}) """

print(c.result)
c.unbind()