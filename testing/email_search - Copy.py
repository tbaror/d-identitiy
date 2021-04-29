import ssl
import json
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
MAILDN=""



c.search(search_base = BASEDN,
    search_filter = SEARCHFILTER,
    search_scope = SUBTREE,
    attributes = ['cn', 'givenName'],
    paged_size = 5)

for entry in c.response:
    if entry.get("dn") and entry.get("attributes"):
        #print(entry)
        if entry.get("attributes").get("cn"):
            USER_DN=entry.get("dn")
            
           


c.search(
    search_base=USER_DN,
    search_filter= '(objectClass=person)', # required
    search_scope=BASE,
    attributes=['mail']
)

user_obj = c.response()
print(user_obj)
c.unbind()