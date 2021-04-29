import pyotp
import time
import base64
#from Crypto.Cipher import AES
#from Crypto import Random
from fernet import *
# OTP verified for current time

import random as r
# function for otp generation
def otpgen():
    otp=""
    for i in range(6):
        otp+=str(r.randint(1,9))
    print ("Your One Time Password is ")
    print (otp)
    return otp
otpgen()
encoded_message = otpgen().encode()
print('encoded messae',encoded_message)

#key = Fernet.generate_key()
key = 'eaAoKMlRgBM7ARnZ_n33a9uSCjYtTJbLGx2gFGiYbgU='
print('key: ',key.encode())

encryption_type = Fernet(key.encode())

encrypted_message = encryption_type.encrypt(encoded_message)
print(encrypted_message)



sec= pyotp
secret = pyotp.random_base32()
print (encrypted_message)
totp = pyotp.TOTP(encrypted_message, interval=60)
print(totp.secret)

decrypted_message = encryption_type.decrypt(encrypted_message)

print(decrypted_message.decode())