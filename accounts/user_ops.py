
from ldap3 import *
import ssl

class LdapOpertions():

    def __init__(self,LdapServer, BaseDn, SvcUser, SvcPassword, RequestUser,RequestUserPass=None):

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
                        user_info['status'] = True
                        
                        try:
                            temp = c.entries[0].mail.values
                            user_info['user_email'] = temp[0]
                        except Exception as e:
                            user_info['user_email'] ='No Mail Field'

                        try:

                            user_info['user_givenname'] = c.entries[0].givenName.values
                        except Exception as e:
                            user_info['user_givenname'] = 'No Given Name Field'

                        try:
                            user_info['user_sn'] = c.entries[0].sn.values
                        except Exception as e:

                            user_info['user_sn'] = 'No User Sure Name Field'

                        
                        try:
                            user_info['country']= c.entries[0].co.values
                            
                        except Exception as e:
                            user_info['country']='No Country Field'
                        
                        try:

                            user_info['address'] = c.entries[0].streetAddress.values
                        except Exception as e:
                            user_info['address'] = 'No Address Field'

                        try:

                            user_info['telephoneNumber'] = c.entries[0].telephoneNumber.values
                        except Exception as e:
                            user_info['telephoneNumber'] = 'No Telephone Field'

                        try:
                            temp = c.entries[0].department.values
                            user_info['department'] = temp[0]
                        except Exception as e:
                            user_info['department'] = 'No Depatment Field'

                        try:
                            user_info['title'] = c.entries[0].title.values
                        except Exception as e:
                            user_info['title'] = 'No Title Field'
                
                        c.unbind()
                        
                        
            return user_info       

        except Exception as e:
            user_info['status'] = False
            user_info['error'] = e
            print(e)
            return user_info            

        




        
        