from fernet import *
import pyotp
from fernet import *
from decouple import config
import random as r


#OTP_NUMLEN=config('OTP_NUMLEN')
#SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = '+4x3v5f2_=%ltehp^x1y_+(%fx-+v5^ak#n8kg)&9d-*ns-7rb'
 
OTP_NUMLEN = 6
# function for otp generation
def otpgen():
    otp=""
    for i in range(OTP_NUMLEN):
        otp+=str(r.randint(1,9))
    
    return otp


def crypt_token():
    encoded_message = otpgen().encode
    key = SECRET_KEY.encode
    print(key)
    encryption_type = Fernet(key)

    encrypted_message = encryption_type.encrypt(encoded_message)
    return encoded_message

print(crypt_token())