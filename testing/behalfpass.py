#!/usr/bin/python

import ldap3

SERVER='212.143.237.33'
BASEDN="DC=dalet,DC=local"
USER="tbaror@dalet.com"
CHUSER="pwmtest@dalet.com"
CURREENTPWD="einfs@TA12!@"
NEWPWD="Esprit@1234"
try:
    
    SEARCHFILTER='(&(|(userPrincipalName='+CHUSER+')(samaccountname='+CHUSER+')(mail='+CHUSER+'))(objectClass=person))'

    USER_DN=""

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

    print (USER_DN)
    print (ldap3.extend.microsoft.modifyPassword.ad_modify_password(conn, USER_DN, NEWPWD, controls=None))
    #c.extend.microsoft.modify_password(user, new_password)
except Exception as e:
            print(e)
            
