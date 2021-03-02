from fernet import *
import pyotp
from fernet import *
from decouple import config


# function for otp generation
def otpgen():
    otp=""
    for i in range(OTP_NUMLEN=config('OTP_NUMLEN')):
        otp+=str(r.randint(1,9))
    
    return otp


def crypt_token():
    encoded_message = otpgen().encode
    key = config('SECRET_KEY').encode
    encryption_type = Fernet(key)

    encrypted_message = encryption_type.encrypt(encoded_message)
    return encoded_message

print(crypt_token())