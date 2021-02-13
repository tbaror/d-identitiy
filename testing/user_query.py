import ldap3


SERVER='212.143.237.33'
BASEDN="DC=dalet,DC=local"
USER="tbaror@dalet.com"
CURREENTPWD="einfs@TA12!@"
NEWPWD="Gfn@12345"



baseDn = 'DC=dalet,DClocal'
search_filter = "(uid=tbaror)"

server = Servldap3.Serverer(SERVER, get_info=ldap3.ALL)
conn = Connection(server,USER, CURREENTPWD,auto_bind=True,check_names=True)
inetorgperson = ObjectDef(['person','user'], conn)
reader = Reader(conn,inetorgperson,baseDn,search_filter)

reader.search()