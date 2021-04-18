from django.db import models
import datetime
from django.contrib.auth.models import User
import pyotp
import qrcode
from io import BytesIO
from django.core.files import File 
from PIL import Image, ImageDraw

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
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

	#qr_creation = otp_google_auth(secret, user)
	otp_code = models.CharField(max_length=200)
	user_qr =  models.ImageField(upload_to='qrcodeimg/', blank=True)
	

	def __str__(self):
		return str(self.user)


	def save(self, *args, **kwargs):
		secret = pyotp.random_base32()
		self.otp_code = secret
		googleauth = pyotp.totp.TOTP(secret).provisioning_uri(name=str(self.user) + '@google.com', issuer_name='Secure Dalet')
		
		qrcode_img = qrcode.make(googleauth)
		canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
		
		canvas.paste(qrcode_img)
		fname = f'qr_code-{self.user}.png'
		buffer = BytesIO()
		canvas.save(buffer, 'PNG')
		self.user_qr.save(fname, File(buffer), save=False)
		canvas.close()
		super().save(*args, **kwargs) 