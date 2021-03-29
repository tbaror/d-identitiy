


class LdapOpertions():

    def __init__(self, SvcUser, SvcPassword, RequestUser, RequestUserPass=None, LdapServer, BaseDn):

        self.SvcUser = SvcUser
        self.SvcPassword = SvcPassword
        self.RequestUser = RequestUser
        self.RequestUserPass = RequestUserPass
        self.LdapServer = LdapServer
        self.BaseDn = BaseDn
        
    
    def query_user_attrib(self):
        try:
            user_info = {}
            #Try to connect
            USER_DN = ""
            user_attrib = []
            tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
            s = Server(self.LdapServer, get_info=ALL, use_ssl=True, tls=tls_configuration)
            c = Connection(s, user=self.SvcUser, password=self.SvcPassword)
            c.open()
            c.bind()
            #defien search filter for user account
            SEARCHFILTER='(&(|(userPrincipalName='+self.RequestUser+')(samaccountname='+self.RequestUser+')(mail='+self.RequestUser+'))(objectClass=person))'
            #Get user DN
            c.search(search_base = self.BaseDn,
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

                        user_info['user_email'] = c.entries[0].mail.values
                        user_info['user_givenname'] = c.entries[0].givenName.values
                        user_info['user_sn'] = c.entries[0].sn.values
                        user_info['country']= c.entries[0].co.values
                        user_info['address'] = c.entries[0].streetAddress.values
                        user_info['telephoneNumber'] = c.entries[0].telephoneNumber.values
                        user_info['department'] = c.entries[0].department.values
                        user_info['title'] = c.entries[0].title.values
                
                        c.unbind()
                        
                        
            return user_info       

        except Exception as e:
            pass            

        




        
        