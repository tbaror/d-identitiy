from django.db import models
import datetime
from django.contrib.auth.models import User
import pyotp
#import qrcode
#from io import BytesIO
from django.core.files import File 
#from PIL import Image, ImageDraw
from decouple import config

# Create your models here.


class PassEvents(models.Model):

    pass_event_type = models.CharField(max_length=200)
    event_stamp = models.DateTimeField(auto_now_add=True)
    user_related_event = models.CharField(max_length=200)
    ip_source = models.CharField(max_length=16)
    user_browser = models.CharField(max_length=200)
    user_os = models.CharField(max_length=200)
    user_agent = models.CharField(max_length=200)
    user_reset_reason = models.TextField(max_length=500,default=None, null=True, blank=True)

    def __str__(self):
        return self.user_related_event


class OtpProfile(models.Model):

	DOMAIN_NAME = config('DOMAIN_NAME')
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	OTP_METHOD_CHOICES = [
    ('C', 'GOOGLE AUTH'),
    ('EM', 'EMAIL OTP'),
    ]
	
	otp_method = models.CharField(max_length=2,choices=OTP_METHOD_CHOICES, default='GOOGLE AUTH')
	
	otp_code = models.CharField(max_length=200)
	
	user_auth_url = models.CharField(max_length=300)
	

	def __str__(self):
		return str(self.user)
	

	def save(self, *args, **kwargs):
		secret = pyotp.random_base32()
		self.otp_code = secret
		googleauth = pyotp.totp.TOTP(secret).provisioning_uri(name=str(self.user) + self.DOMAIN_NAME, issuer_name='Secure Dalet')
		self.user_auth_url = googleauth
		
		super().save(*args, **kwargs) 