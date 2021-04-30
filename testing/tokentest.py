import pyotp
import time

""" base32secret = 'S3K3TPI5MYA2M67V'
print('Secret:', base32secret)
pyotp.TOTP(base32secret, )
totp = pyotp.TOTP(base32secret, interval=300) """

#print('OTP code:', totp.now())
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret, interval=60)
now = time.time()
totp.at(now)
otp = totp.now()

print('OTP code:', totp.now())
time.sleep(25)
print('OTP code:', totp.now())
time.sleep(30)