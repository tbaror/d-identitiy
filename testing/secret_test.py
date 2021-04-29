import base64
from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings

my_secret = settings.PYADSELFSERVICE_CRYPTKEY #'HgFSg$$PhyhG!JHgjh33mn3jk5nb3m5b'

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def encrypt_val( clear_text ):
    clear_text = pad(clear_text)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( my_secret, AES.MODE_CBC, iv )
    return base64.urlsafe_b64encode( iv + cipher.encrypt(clear_text) ) 
