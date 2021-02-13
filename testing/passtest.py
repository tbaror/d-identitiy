import ldap3

SERVER='212.143.237.33'
BASEDN="DC=dalet,DC=local"
USER="pwmtest@dalet.com"
CURREENTPWD="Gfn@12345"
NEWPWD="Gfn@12345"

SEARCHFILTER='(&(|(userPrincipalName='+USER+')(samaccountname='+USER+')(mail='+USER+'))(objectClass=person))'

USER_DN=""
USER_EMAIL=""

ldap_server = ldap3.Server(SERVER, get_info=ldap3.ALL)
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
            print(entry)

print (USER_DN,USER_EMAIL)
print(ldap3.extend.microsoft.modifyPassword.ad_modify_password(conn, USER_DN, NEWPWD, CURREENTPWD,  controls=None))